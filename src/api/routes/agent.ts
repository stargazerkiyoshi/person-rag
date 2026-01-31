import type { FastifyInstance } from "fastify";
import { ProviderConfigError } from "../../agent/providers";

interface AgentRequest {
  task: string;
  session_id?: string | null;
}

export async function registerAgentRoutes(app: FastifyInstance): Promise<void> {
  app.post("/agent", async (request, reply) => {
    const body = request.body as AgentRequest;
    if (!body?.task) {
      return reply.code(400).send({ detail: "Missing task" });
    }
    try {
      const result = await app.agentRunner.run(body.task, body.session_id ?? undefined);
      return reply.send({
        result: result.result,
        sources: result.sources,
        trace: result.trace,
        actions: result.actions,
        session_id: result.sessionId
      });
    } catch (error) {
      if (error instanceof ProviderConfigError) {
        return reply.code(400).send({ detail: error.message });
      }
      if ((error as Error).message === "模型返回非 JSON 内容") {
        return reply.code(502).send({ detail: "模型响应解析失败" });
      }
      request.log.error(error);
      return reply.code(500).send({ detail: "Internal Server Error" });
    }
  });
}
