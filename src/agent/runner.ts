import { ChatPromptTemplate } from "@langchain/core/prompts";
import type { Settings } from "../config";
import type { LlmProvider } from "./providers";
import type { Chunk } from "./retriever";
import { ActionExecutor, type ActionResult } from "./actions";
import { formatHistory, SessionStore } from "./sessions";
import { PgVectorRetriever } from "./retriever";
import { buildProvider } from "./providers";
import { ensureSchema, getPool } from "../db";

export interface TraceEntry {
  step: string;
  status: string;
  detail: string;
  at: string;
}

export interface AgentResult {
  result: string;
  sources: string[];
  trace: TraceEntry[];
  actions: ActionResult[];
  sessionId: string;
}

interface RetrievalDecision {
  needRetrieval: boolean;
  reason: string;
}

export class AgentRunner {
  constructor(
    private readonly provider: LlmProvider,
    private readonly retriever: PgVectorRetriever,
    private readonly actions: ActionExecutor,
    private readonly sessions: SessionStore,
    private readonly topK: number
  ) {}

  async run(task: string, sessionId?: string | null): Promise<AgentResult> {
    const trace: TraceEntry[] = [];
    const llm = this.provider.getChatModel();
    const finalSessionId = await this.sessions.getOrCreate(sessionId ?? undefined);
    const history = await this.loadHistory(finalSessionId);

    const decision = await this.decideRetrieval(llm, task, history);
    trace.push(this.trace("decide_retrieval", "success", decision.reason || "已完成检索判定"));

    if (!decision.needRetrieval) {
      const answer = await this.answerWithoutRetrieval(llm, task, history);
      trace.push(this.trace("answer", "success", "已返回纯对话结果"));
      await this.storeTurn(finalSessionId, task, answer);
      return { result: answer, sources: [], trace, actions: [], sessionId: finalSessionId };
    }

    const chunks = await this.retriever.retrieve(task, this.topK);
    trace.push(this.trace("retrieve", "success", `命中 ${chunks.length} 条片段`));

    if (chunks.length === 0) {
      return {
        result: "未找到相关资料，无法完成任务。",
        sources: [],
        trace,
        actions: [],
        sessionId: finalSessionId
      };
    }

    const prompt = ChatPromptTemplate.fromMessages([
      [
        "system",
        "你是一个智能体，请基于给定资料完成任务。只输出 JSON，不要包含任何解释或代码块。" +
          "JSON fields: summary, analysis_steps, actions, result, sources_used。"
      ],
      [
        "human",
        "历史对话:\n{history}\n\n任务:\n{task}\n\n资料:\n{context}\n\n" +
          "actions 为数组，可为空。sources_used 为来源列表。"
      ]
    ]);

    const context = this.renderContext(chunks);
    const messages = await prompt.formatMessages({ task, history, context });
    const response = await llm.invoke(messages);
    trace.push(this.trace("analyze", "success", "模型已返回结果"));

    const payload = this.parsePayload(asContent(response.content));
    const actions = this.actions.execute((payload.actions as Array<Record<string, unknown>>) ?? []);
    if (actions.length > 0) {
      trace.push(this.trace("actions", "success", `执行动作 ${actions.length} 项`));
    }

    const sources = this.normalizeSources(payload.sources_used as string[] | undefined, chunks);
    const resultText = String(payload.result ?? "").trim() || "模型未返回有效结果。";
    await this.storeTurn(finalSessionId, task, resultText);

    return {
      result: resultText,
      sources,
      trace,
      actions,
      sessionId: finalSessionId
    };
  }

  private async decideRetrieval(llm: ReturnType<LlmProvider["getChatModel"]>, task: string, history: string): Promise<RetrievalDecision> {
    const prompt = ChatPromptTemplate.fromMessages([
      [
        "system",
        "你负责判断是否需要检索资料才能回答。只输出 JSON，不要包含任何解释或代码块。" +
          "JSON fields: need_retrieval (true/false), reason。"
      ],
      ["human", "历史对话:\n{history}\n\n问题:\n{task}"]
    ]);
    const messages = await prompt.formatMessages({ task, history });
    const response = await llm.invoke(messages);
    const payload = this.parsePayload(asContent(response.content));
    return {
      needRetrieval: Boolean(payload.need_retrieval),
      reason: String(payload.reason ?? "")
    };
  }

  private async answerWithoutRetrieval(
    llm: ReturnType<LlmProvider["getChatModel"]>,
    task: string,
    history: string
  ): Promise<string> {
    const prompt = ChatPromptTemplate.fromMessages([
      [
        "system",
        "你是一个对话助手，请直接回答用户问题。不要编造来源或引用资料。"
      ],
      ["human", "历史对话:\n{history}\n\n问题:\n{task}"]
    ]);
    const messages = await prompt.formatMessages({ task, history });
    const response = await llm.invoke(messages);
    return asContent(response.content).trim() || "模型未返回有效结果。";
  }

  private renderContext(chunks: Chunk[]): string {
    return chunks
      .map((chunk, idx) => `[${idx + 1}] ${chunk.text}\n来源: ${chunk.source}`)
      .join("\n\n");
  }

  private parsePayload(content: string): Record<string, unknown> {
    try {
      return JSON.parse(content);
    } catch (error) {
      const trimmed = this.extractJson(content);
      if (trimmed) {
        try {
          return JSON.parse(trimmed);
        } catch (inner) {
          throw new Error("模型返回非 JSON 内容");
        }
      }
      throw new Error("模型返回非 JSON 内容");
    }
  }

  private extractJson(content: string): string | null {
    const start = content.indexOf("{");
    const end = content.lastIndexOf("}");
    if (start === -1 || end === -1 || end <= start) {
      return null;
    }
    return content.slice(start, end + 1);
  }

  private normalizeSources(sources: string[] | undefined, chunks: Chunk[]): string[] {
    if (sources && sources.length > 0) {
      return sources.map((source) => String(source));
    }
    return chunks.map((chunk) => chunk.source);
  }

  private trace(step: string, status: string, detail: string): TraceEntry {
    return {
      step,
      status,
      detail,
      at: new Date().toISOString()
    };
  }

  private async loadHistory(sessionId: string): Promise<string> {
    const messages = await this.sessions.recentMessages(sessionId);
    return formatHistory(messages);
  }

  private async storeTurn(sessionId: string, userText: string, assistantText: string): Promise<void> {
    await this.sessions.addMessage(sessionId, "user", userText);
    await this.sessions.addMessage(sessionId, "assistant", assistantText);
  }
}

export async function buildAgentRunner(settings: Settings): Promise<AgentRunner> {
  const provider = buildProvider(settings);
  await ensureSchema(settings);
  const pool = getPool(settings);
  const sessions = new SessionStore(pool, settings.sessionMaxRounds);
  const retriever = new PgVectorRetriever(pool, () => provider.getEmbeddings(), settings.pgVectorTable);
  const actions = new ActionExecutor(settings.dataDir);
  return new AgentRunner(provider, retriever, actions, sessions, settings.retrieverTopK);
}

function asContent(content: unknown): string {
  if (typeof content === "string") {
    return content;
  }
  return JSON.stringify(content ?? "");
}
