import fs from "fs";
import path from "path";

export interface ActionResult {
  name: string;
  status: string;
  detail: string;
}

export class ActionExecutor {
  constructor(private readonly dataDir: string = "data") {}

  execute(actions: Array<Record<string, unknown>>): ActionResult[] {
    return actions.map((action) => this.executeOne(action));
  }

  private executeOne(action: Record<string, unknown>): ActionResult {
    const name = String(action.name ?? action.type ?? "").trim();
    if (!name) {
      return { name: "unknown", status: "skipped", detail: "缺少动作名称" };
    }
    if (name === "save_note") {
      return this.saveNote(action);
    }
    return { name, status: "failed", detail: "不支持的动作" };
  }

  private saveNote(action: Record<string, unknown>): ActionResult {
    const content = String(action.content ?? action.input ?? "").trim();
    if (!content) {
      return { name: "save_note", status: "failed", detail: "缺少内容" };
    }
    const target = String(action.path ?? "agent_notes.txt");
    const baseDir = path.resolve(this.dataDir);
    const targetPath = path.resolve(this.dataDir, target);
    if (!targetPath.startsWith(baseDir)) {
      return { name: "save_note", status: "failed", detail: "非法路径" };
    }
    fs.mkdirSync(path.dirname(targetPath), { recursive: true });
    fs.appendFileSync(targetPath, `${content}\n`, "utf8");
    return { name: "save_note", status: "success", detail: targetPath };
  }
}
