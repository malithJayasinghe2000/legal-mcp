"use client";

import { Tabs } from "radix-ui";

const DIR = "/path/to/rulewise";

const TOOLS = [
  {
    id: "claude-code",
    name: "Claude Code",
    where: "Run in your terminal:",
    code: `claude mcp add rulewise -- uv run --directory ${DIR} rulewise`,
  },
  {
    id: "cursor",
    name: "Cursor",
    where: "Add to ~/.cursor/mcp.json:",
    code: `{
  "mcpServers": {
    "rulewise": {
      "command": "uv",
      "args": ["run", "--directory", "${DIR}", "rulewise"]
    }
  }
}`,
  },
  {
    id: "codex",
    name: "Codex",
    where: "Add to ~/.codex/config.toml:",
    code: `[mcp_servers.rulewise]
command = "uv"
args = ["run", "--directory", "${DIR}", "rulewise"]`,
  },
  {
    id: "vscode",
    name: "VS Code",
    where: "Add to .vscode/mcp.json in your project:",
    code: `{
  "servers": {
    "rulewise": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "--directory", "${DIR}", "rulewise"]
    }
  }
}`,
  },
];

export function SetupTabs() {
  return (
    <Tabs.Root defaultValue={TOOLS[0].id} className="min-w-0">
      <Tabs.List aria-label="AI tool" className="flex flex-wrap gap-2">
        {TOOLS.map((t) => (
          <Tabs.Trigger
            key={t.id}
            value={t.id}
            className="h-9 rounded-md border border-rule bg-surface px-3 text-sm text-ink-muted hover:text-ink focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-orange data-[state=active]:border-ink data-[state=active]:bg-ink data-[state=active]:text-paper"
          >
            {t.name}
          </Tabs.Trigger>
        ))}
      </Tabs.List>
      {TOOLS.map((t) => (
        <Tabs.Content
          key={t.id}
          value={t.id}
          className="mt-4 focus-visible:outline-none"
        >
          <p className="text-sm text-ink-muted">{t.where}</p>
          <pre
            tabIndex={0}
            aria-label={`${t.name} setup`}
            className="mt-2 overflow-x-auto rounded-lg bg-ink p-5 text-sm leading-relaxed text-paper focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-orange"
          >
            <code>{t.code}</code>
          </pre>
        </Tabs.Content>
      ))}
    </Tabs.Root>
  );
}
