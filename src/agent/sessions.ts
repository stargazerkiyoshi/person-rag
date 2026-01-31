import crypto from "crypto";
import type { Pool } from "pg";

export interface SessionMessage {
  role: string;
  content: string;
}

export class SessionStore {
  constructor(private readonly pool: Pool, private readonly maxRounds: number) {}

  async getOrCreate(sessionId?: string | null): Promise<string> {
    if (sessionId) {
      const exists = await this.sessionExists(sessionId);
      if (exists) {
        return sessionId;
      }
    }
    const newId = crypto.randomUUID().replace(/-/g, "");
    await this.pool.query("INSERT INTO sessions (id) VALUES ($1)", [newId]);
    return newId;
  }

  async addMessage(sessionId: string, role: string, content: string): Promise<void> {
    await this.pool.query(
      "INSERT INTO messages (session_id, role, content) VALUES ($1, $2, $3)",
      [sessionId, role, content]
    );
  }

  async recentMessages(sessionId: string): Promise<SessionMessage[]> {
    const limit = Math.max(0, this.maxRounds * 2);
    if (limit === 0) {
      return [];
    }
    const { rows } = await this.pool.query(
      "SELECT role, content FROM messages WHERE session_id = $1 ORDER BY id DESC LIMIT $2",
      [sessionId, limit]
    );
    return rows.reverse().map((row) => ({ role: row.role, content: row.content }));
  }

  private async sessionExists(sessionId: string): Promise<boolean> {
    const { rows } = await this.pool.query("SELECT 1 FROM sessions WHERE id = $1", [sessionId]);
    return rows.length > 0;
  }
}

export function formatHistory(messages: Iterable<SessionMessage>): string {
  const lines: string[] = [];
  for (const msg of messages) {
    const role = msg.role === "user" ? "用户" : "助手";
    lines.push(`${role}: ${msg.content}`);
  }
  return lines.join("\n");
}
