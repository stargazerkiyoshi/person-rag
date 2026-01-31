import { Pool } from "pg";
import type { Settings } from "../config";

let pool: Pool | null = null;

export function getPool(settings: Settings): Pool {
  if (!pool) {
    pool = new Pool({
      connectionString: settings.databaseUrl
    });
  }
  return pool;
}

export async function ensureSchema(settings: Settings): Promise<void> {
  const client = await getPool(settings).connect();
  try {
    await client.query("CREATE EXTENSION IF NOT EXISTS vector");
    const tableName = safeIdentifier(settings.pgVectorTable);
    const dimensions = settings.embeddingDimensions;
    if (!Number.isFinite(dimensions) || dimensions <= 0) {
      throw new Error("Invalid embedding dimensions.");
    }
    await client.query(
      `CREATE TABLE IF NOT EXISTS ${tableName} (
        id SERIAL PRIMARY KEY,
        content TEXT NOT NULL,
        source TEXT NOT NULL,
        embedding vector(${dimensions}) NOT NULL
      )`
    );
    await client.query(
      "CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, created_at TIMESTAMPTZ DEFAULT now())"
    );
    await client.query(
      "CREATE TABLE IF NOT EXISTS messages (id SERIAL PRIMARY KEY, session_id TEXT NOT NULL REFERENCES sessions(id), role TEXT NOT NULL, content TEXT NOT NULL, created_at TIMESTAMPTZ DEFAULT now())"
    );
  } finally {
    client.release();
  }
}

export async function clearDocuments(settings: Settings): Promise<void> {
  const client = await getPool(settings).connect();
  try {
    const tableName = safeIdentifier(settings.pgVectorTable);
    await client.query(`TRUNCATE TABLE ${tableName}`);
  } finally {
    client.release();
  }
}

function safeIdentifier(value: string): string {
  if (!/^[A-Za-z_][A-Za-z0-9_]*$/.test(value)) {
    throw new Error(`Invalid identifier: ${value}`);
  }
  return value;
}
