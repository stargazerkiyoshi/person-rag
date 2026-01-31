import fs from "fs";
import path from "path";
import type { Pool } from "pg";
import type { OpenAIEmbeddings } from "@langchain/openai";

export interface Chunk {
  text: string;
  source: string;
}

export class PgVectorRetriever {
  private embeddingsInstance: OpenAIEmbeddings | null = null;

  constructor(
    private readonly pool: Pool,
    private readonly embeddingsProvider: () => OpenAIEmbeddings,
    private readonly tableName: string
  ) {
    this.tableName = safeIdentifier(tableName);
  }

  async retrieve(query: string, topK: number): Promise<Chunk[]> {
    const trimmed = query.trim();
    if (!trimmed) {
      return [];
    }
    const embeddings = this.getEmbeddings();
    const embedding = await embeddings.embedQuery(trimmed);
    const vectorLiteral = vectorToSql(embedding);
    const { rows } = await this.pool.query(
      `SELECT content, source FROM ${this.tableName} ORDER BY embedding <-> $1::vector LIMIT $2`,
      [vectorLiteral, topK]
    );
    return rows.map((row) => ({ text: row.content, source: row.source }));
  }

  private getEmbeddings(): OpenAIEmbeddings {
    if (!this.embeddingsInstance) {
      this.embeddingsInstance = this.embeddingsProvider();
    }
    return this.embeddingsInstance;
  }
}

export interface IngestOptions {
  dataDir: string;
  extensions?: string[];
  batchSize?: number;
}

export async function ingestDocuments(
  pool: Pool,
  embeddings: OpenAIEmbeddings,
  tableName: string,
  options: IngestOptions
): Promise<number> {
  const safeTable = safeIdentifier(tableName);
  const chunks = loadChunks(options.dataDir, options.extensions ?? [".txt", ".md"]);
  if (chunks.length === 0) {
    return 0;
  }
  const batchSize = options.batchSize ?? 32;
  let inserted = 0;
  for (let i = 0; i < chunks.length; i += batchSize) {
    const batch = chunks.slice(i, i + batchSize);
    const vectors = await embeddings.embedDocuments(batch.map((chunk) => chunk.text));
    for (let j = 0; j < batch.length; j += 1) {
      const chunk = batch[j];
      const vectorLiteral = vectorToSql(vectors[j]);
      await pool.query(
        `INSERT INTO ${safeTable} (content, source, embedding) VALUES ($1, $2, $3::vector)`,
        [chunk.text, chunk.source, vectorLiteral]
      );
      inserted += 1;
    }
  }
  return inserted;
}

function loadChunks(dataDir: string, extensions: string[]): Chunk[] {
  const absolute = path.resolve(dataDir);
  if (!fs.existsSync(absolute)) {
    return [];
  }
  const files = listFiles(absolute, extensions);
  const chunks: Chunk[] = [];
  for (const filePath of files) {
    let text = "";
    try {
      text = fs.readFileSync(filePath, "utf8");
    } catch {
      continue;
    }
    for (const block of splitBlocks(text)) {
      chunks.push({ text: block, source: filePath });
    }
  }
  return chunks;
}

function listFiles(root: string, extensions: string[]): string[] {
  const entries = fs.readdirSync(root, { withFileTypes: true });
  const files: string[] = [];
  for (const entry of entries) {
    const fullPath = path.join(root, entry.name);
    if (entry.isDirectory()) {
      files.push(...listFiles(fullPath, extensions));
      continue;
    }
    const ext = path.extname(entry.name).toLowerCase();
    if (extensions.includes(ext)) {
      files.push(fullPath);
    }
  }
  return files;
}

function splitBlocks(text: string): string[] {
  return text
    .split(/\n\s*\n/g)
    .map((block) => block.trim())
    .filter(Boolean);
}

function vectorToSql(vector: number[]): string {
  const safe = vector.map((value) => Number(value).toFixed(8));
  return `[${safe.join(",")}]`;
}

function safeIdentifier(value: string): string {
  if (!/^[A-Za-z_][A-Za-z0-9_]*$/.test(value)) {
    throw new Error(`Invalid identifier: ${value}`);
  }
  return value;
}
