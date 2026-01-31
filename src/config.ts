import fs from "fs";
import path from "path";

export interface Settings {
  appUsername: string;
  appPassword: string;
  jwtSecret: string;
  jwtAlgorithm: string;
  jwtExpireMinutes: number;
  logLevel: string;
  llmProvider: string;
  llmApiKey: string;
  llmModel: string;
  llmBaseUrl: string;
  llmTimeoutSeconds: number;
  embeddingModel: string;
  embeddingDimensions: number;
  dataDir: string;
  sessionMaxRounds: number;
  databaseUrl: string;
  pgVectorTable: string;
  retrieverTopK: number;
}

const DEFAULT_CONFIG_PATH = "config/config.json";

function loadConfigFile(filePath: string): Record<string, unknown> {
  if (!filePath) {
    return {};
  }
  const absolute = path.isAbsolute(filePath) ? filePath : path.join(process.cwd(), filePath);
  if (!fs.existsSync(absolute)) {
    return {};
  }
  const raw = fs.readFileSync(absolute, "utf8");
  return JSON.parse(raw);
}

function getString(envKey: string, config: Record<string, unknown>, fallback: string): string {
  const envValue = process.env[envKey];
  if (envValue !== undefined && envValue !== "") {
    return envValue;
  }
  const configValue = config[envKey.toLowerCase()];
  if (typeof configValue === "string" && configValue.trim() !== "") {
    return configValue;
  }
  return fallback;
}

function getNumber(envKey: string, config: Record<string, unknown>, fallback: number): number {
  const envValue = process.env[envKey];
  if (envValue !== undefined && envValue !== "") {
    const parsed = Number(envValue);
    if (!Number.isNaN(parsed)) {
      return parsed;
    }
  }
  const configValue = config[envKey.toLowerCase()];
  if (typeof configValue === "number") {
    return configValue;
  }
  if (typeof configValue === "string") {
    const parsed = Number(configValue);
    if (!Number.isNaN(parsed)) {
      return parsed;
    }
  }
  return fallback;
}

export function loadSettings(): Settings {
  const configPath = process.env.CONFIG_FILE || DEFAULT_CONFIG_PATH;
  const config = loadConfigFile(configPath);

  return {
    appUsername: getString("APP_USERNAME", config, "admin"),
    appPassword: getString("APP_PASSWORD", config, "admin"),
    jwtSecret: getString("JWT_SECRET", config, "change-me"),
    jwtAlgorithm: getString("JWT_ALGORITHM", config, "HS256"),
    jwtExpireMinutes: getNumber("JWT_EXPIRE_MINUTES", config, 60),
    logLevel: getString("LOG_LEVEL", config, "info").toLowerCase(),
    llmProvider: getString("LLM_PROVIDER", config, "openai"),
    llmApiKey: getString("LLM_API_KEY", config, ""),
    llmModel: getString("LLM_MODEL", config, "gpt-4o-mini"),
    llmBaseUrl: getString("LLM_BASE_URL", config, ""),
    llmTimeoutSeconds: getNumber("LLM_TIMEOUT_SECONDS", config, 60),
    embeddingModel: getString("EMBEDDING_MODEL", config, "text-embedding-3-small"),
    embeddingDimensions: getNumber("EMBEDDING_DIMENSIONS", config, 1536),
    dataDir: getString("DATA_DIR", config, "data"),
    sessionMaxRounds: getNumber("SESSION_MAX_ROUNDS", config, 6),
    databaseUrl: getString("DATABASE_URL", config, "postgres://postgres:postgres@127.0.0.1:5432/person_rag"),
    pgVectorTable: getString("PGVECTOR_TABLE", config, "documents"),
    retrieverTopK: getNumber("RETRIEVER_TOP_K", config, 5)
  };
}
