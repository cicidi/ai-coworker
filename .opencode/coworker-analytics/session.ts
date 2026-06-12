import { Recorder } from "./recorder";

function generateSessionId(): string {
  const now = new Date();
  const date = now.toISOString().slice(0, 10);
  const time = now.toTimeString().slice(0, 8).replace(/:/g, "");
  const hex = Math.random().toString(36).slice(2, 8);
  return `${date}-T${time}-${hex}`;
}

export function createSession(cwd: string, ide: string): { id: string; recorder: Recorder } {
  const id = generateSessionId();
  const recorder = new Recorder(id);
  recorder.writeSessionYaml({
    session_id: id,
    created: new Date().toISOString(),
    ide,
    cwd: cwd || "",
    project: "",
    initiative: "",
    branch: "",
  });
  return { id, recorder };
}
