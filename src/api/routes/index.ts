import type { FastifyInstance } from "fastify";
import { registerHealthRoutes } from "./health";
import { registerAuthRoutes } from "./auth";
import { registerProtectedRoutes } from "./protected";
import { registerAgentRoutes } from "./agent";

export async function registerRoutes(app: FastifyInstance): Promise<void> {
  await registerHealthRoutes(app);
  await registerAuthRoutes(app);
  await registerProtectedRoutes(app);
  await registerAgentRoutes(app);
}
