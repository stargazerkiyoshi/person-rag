import { ChatOpenAI, OpenAIEmbeddings } from "@langchain/openai";
import type { Settings } from "../config";

export class ProviderConfigError extends Error {}

export interface LlmProvider {
  getChatModel(): ChatOpenAI;
  getEmbeddings(): OpenAIEmbeddings;
}

export class OpenAIProvider implements LlmProvider {
  constructor(private readonly settings: Settings) {}

  getChatModel(): ChatOpenAI {
    if (!this.settings.llmApiKey) {
      throw new ProviderConfigError("未配置 LLM_API_KEY");
    }
    return new ChatOpenAI({
      apiKey: this.settings.llmApiKey,
      model: this.settings.llmModel,
      temperature: 0,
      timeout: this.settings.llmTimeoutSeconds * 1000,
      configuration: this.settings.llmBaseUrl
        ? {
            baseURL: this.settings.llmBaseUrl
          }
        : undefined
    });
  }

  getEmbeddings(): OpenAIEmbeddings {
    if (!this.settings.llmApiKey) {
      throw new ProviderConfigError("未配置 LLM_API_KEY");
    }
    return new OpenAIEmbeddings({
      apiKey: this.settings.llmApiKey,
      model: this.settings.embeddingModel,
      configuration: this.settings.llmBaseUrl
        ? {
            baseURL: this.settings.llmBaseUrl
          }
        : undefined
    });
  }
}

export function buildProvider(settings: Settings): LlmProvider {
  const provider = settings.llmProvider.toLowerCase();
  if (provider === "openai" || provider === "chatgpt") {
    return new OpenAIProvider(settings);
  }
  throw new ProviderConfigError(`不支持的提供方: ${settings.llmProvider}`);
}
