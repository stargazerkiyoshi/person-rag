import type { FastifyInstance } from "fastify";
import { getCurrentUser } from "../../auth";

export async function registerProtectedRoutes(app: FastifyInstance): Promise<void> {
  app.get("/protected/me", async (request, reply) => {
    try {
      const user = getCurrentUser(request, app.settings);
      return reply.send({ user });
    } catch (error) {
      const message = (error as Error).message || "Invalid token";
      return reply.code(401).send({ detail: message });
    }
  });
}
