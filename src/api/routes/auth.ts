import type { FastifyInstance } from "fastify";
import jwt from "jsonwebtoken";

interface LoginRequest {
  username: string;
  password: string;
}

export async function registerAuthRoutes(app: FastifyInstance): Promise<void> {
  app.post("/auth/login", async (request, reply) => {
    const body = request.body as LoginRequest;
    if (!body?.username || !body?.password) {
      return reply.code(400).send({ detail: "Missing credentials" });
    }
    const settings = app.settings;
    if (body.username !== settings.appUsername || body.password !== settings.appPassword) {
      return reply.code(401).send({ detail: "Invalid credentials" });
    }
    const expiresAt = Math.floor(Date.now() / 1000) + settings.jwtExpireMinutes * 60;
    const token = jwt.sign({ sub: body.username, exp: expiresAt }, settings.jwtSecret, {
      algorithm: settings.jwtAlgorithm as jwt.Algorithm
    });
    return reply.send({
      access_token: token,
      token_type: "bearer",
      expires_at: expiresAt
    });
  });
}
