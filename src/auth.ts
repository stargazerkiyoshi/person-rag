import jwt from "jsonwebtoken";
import type { FastifyRequest } from "fastify";
import type { Settings } from "./config";

export function authenticateUser(username: string, password: string, settings: Settings): boolean {
  return username === settings.appUsername && password === settings.appPassword;
}

export function createAccessToken(subject: string, settings: Settings): { token: string; expiresAt: number } {
  const expiresAt = Math.floor(Date.now() / 1000) + settings.jwtExpireMinutes * 60;
  const token = jwt.sign({ sub: subject, exp: expiresAt }, settings.jwtSecret, {
    algorithm: settings.jwtAlgorithm as jwt.Algorithm
  });
  return { token, expiresAt };
}

export function getCurrentUser(request: FastifyRequest, settings: Settings): string {
  const authHeader = request.headers.authorization ?? "";
  if (!authHeader.startsWith("Bearer ")) {
    throw new Error("Missing token");
  }
  const token = authHeader.slice("Bearer ".length).trim();
  if (!token) {
    throw new Error("Missing token");
  }
  try {
    const payload = jwt.verify(token, settings.jwtSecret, {
      algorithms: [settings.jwtAlgorithm as jwt.Algorithm]
    }) as jwt.JwtPayload;
    const subject = payload.sub;
    if (!subject || typeof subject !== "string") {
      throw new Error("Invalid token");
    }
    return subject;
  } catch {
    throw new Error("Invalid token");
  }
}
