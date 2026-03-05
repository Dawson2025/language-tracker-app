// resource_id: 21d41d3d-89ac-4723-a986-2a1983d3d2c4
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { spawn } from "node:child_process";

const server = new Server(
  { name: "notify", version: "0.1.0" },
  { capabilities: { tools: {} } }
);

server.tool(
  {
    name: "sound_notify",
    description: "Play a short notification sound on the Windows host. Args: title, message, sound.",
    inputSchema: {
      type: "object",
      properties: {
        title: { type: "string" },
        message: { type: "string" },
        sound: { type: "string" }
      },
      additionalProperties: false
    }
  },
  async (input) => {
    const title = input?.title ?? "Warp AI";
    const message = input?.message ?? "Turn complete";
    const sound = input?.sound ?? "Windows Notify System Generic.wav";

    await new Promise((resolve) => {
      const ps = spawn("powershell.exe", [
        "-NoProfile","-ExecutionPolicy","Bypass","-File",
        "C:\\Users\\Dawson\\bin\\warp-notify.ps1",
        "-Title", title, "-Message", message, "-Sound", sound
      ], { windowsHide: true });
      ps.on("close", resolve);
    });

    return { content: [{ type: "text", text: "sound played" }] };
  }
);

await server.connect(new StdioServerTransport());