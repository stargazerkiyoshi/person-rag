import { loadSettings } from "./config";
import { buildProvider } from "./agent/providers";
import { getPool, ensureSchema, clearDocuments } from "./db";
import { ingestDocuments, PgVectorRetriever } from "./agent/retriever";

async function main() {
  const [command, ...rest] = process.argv.slice(2);
  if (!command || command === "--help" || command === "-h") {
    printUsage();
    return;
  }

  const settings = loadSettings();
  const provider = buildProvider(settings);
  const pool = getPool(settings);
  await ensureSchema(settings);

  if (command === "ingest") {
    const inserted = await ingestDocuments(pool, provider.getEmbeddings(), settings.pgVectorTable, {
      dataDir: settings.dataDir
    });
    console.log(`ingest: inserted ${inserted} chunks`);
    return;
  }

  if (command === "index") {
    await clearDocuments(settings);
    const inserted = await ingestDocuments(pool, provider.getEmbeddings(), settings.pgVectorTable, {
      dataDir: settings.dataDir
    });
    console.log(`index: rebuilt ${inserted} chunks`);
    return;
  }

  if (command === "query") {
    const queryText = rest.join(" ").trim();
    if (!queryText) {
      console.error("query: missing query text");
      process.exitCode = 1;
      return;
    }
    const retriever = new PgVectorRetriever(pool, () => provider.getEmbeddings(), settings.pgVectorTable);
    const chunks = await retriever.retrieve(queryText, settings.retrieverTopK);
    if (chunks.length === 0) {
      console.log("query: no results");
      return;
    }
    for (const chunk of chunks) {
      console.log(`- ${chunk.source}`);
      console.log(chunk.text);
      console.log("---");
    }
    return;
  }

  console.error(`Unknown command: ${command}`);
  printUsage();
  process.exitCode = 1;
}

function printUsage() {
  console.log("Personal RAG CLI");
  console.log("Usage:");
  console.log("  node dist/cli.js ingest");
  console.log("  node dist/cli.js index");
  console.log("  node dist/cli.js query <text>");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
