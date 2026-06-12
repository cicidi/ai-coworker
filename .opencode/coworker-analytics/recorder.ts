import { appendFileSync, mkdirSync, existsSync, writeFileSync } from "fs";
import { join } from "path";
import { homedir } from "os";

const BASE_DIR = join(homedir(), ".coworker", "analytics", "sessions");

export class Recorder {
  private seq: number = 0;
  private sessionDir: string;

  constructor(sessionId: string) {
    this.sessionDir = join(BASE_DIR, sessionId);
    if (!existsSync(this.sessionDir)) {
      mkdirSync(this.sessionDir, { recursive: true });
    }
  }

  nextSeq(): number {
    return ++this.seq;
  }

  writeJSONL(file: string, data: Record<string, unknown>): void {
    try {
      const line = JSON.stringify(data) + "\n";
      appendFileSync(join(this.sessionDir, file), line);
    } catch {
      // silent fail — never block AI
    }
  }

  writeSessionYaml(data: Record<string, string>): void {
    try {
      let content = "";
      for (const [k, v] of Object.entries(data)) {
        if (v) content += `${k}: "${v}"\n`;
      }
      writeFileSync(join(this.sessionDir, "session.yaml"), content);
    } catch {
      // silent fail
    }
  }
}
