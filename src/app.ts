import Fastify from "fastify";
import { loadSettings, type Settings } from "./config";
import { buildAgentRunner, type AgentRunner } from "./agent/runner";
import { registerRoutes } from "./api/routes";

declare module "fastify" {
  interface FastifyInstance {
    settings: Settings;
    agentRunner: AgentRunner;
  }
}

export async function createApp() {
  const settings = loadSettings();
  const app = Fastify({
    logger: { level: settings.logLevel }
  });
  const agentRunner = await buildAgentRunner(settings);
  app.decorate("settings", settings);
  app.decorate("agentRunner", agentRunner);
  await registerRoutes(app);
  return app;
}
