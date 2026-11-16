"use client";

import { useState } from "react";
import { Tabs } from "radix-ui";
import { SHOW_CURSOR } from "@/lib/features";

// The hosted server (Azure Container Apps, brief D23). Nothing to install.
const URL =
  "https://rulewise.victoriousdune-a7b660c5.centralindia.azurecontainerapps.io/mcp";

// Codex doesn't act on the server's own instructions, so without this line it only uses
// Rulewise when asked. Tested 2026-11-16: with it, Codex checks new features by itself.
const AGENTS_LINE =
  "Before planning or building a product or feature, check it with the Rulewise MCP tools (get_fact_questions, then check_legal_risks).";

type Tool = {
  id: string;
  name: string;
  where: string;
  code: string;
  then?: { where: string; code: string };
};

const ALL_TOOLS: Tool[] = [
  {
    id: "claude-code",
    name: "Claude Code",
    where: "Run in your terminal:",
    code: `claude mcp add --transport http rulewise ${URL}`,
  },
  {
    id: "cursor",
    name: "Cursor",
    where: "Add to ~/.cursor/mcp.json:",
    code: `{
  "mcpServers": {
    "rulewise": {
      "url": "${URL}"
    }
  }
}`,
  },
  {
    id: "codex",
    name: "Codex",
    where: "Add to ~/.codex/config.toml:",
    code: `[mcp_servers.rulewise]
url = "${URL}"`,
    then: {
      where:
        "Then add this line to AGENTS.md (in your project, or ~/.codex/AGENTS.md for all projects), so Codex checks new features by itself:",
      code: AGENTS_LINE,
    },
  },
  {
    id: "vscode",
    name: "VS Code",
    where: "Add to .vscode/mcp.json in your project:",
    code: `{
  "servers": {
    "rulewise": {
      "type": "http",
      "url": "${URL}"
    }
  }
}`,
  },
];

const TOOLS = ALL_TOOLS.filter((t) => SHOW_CURSOR || t.id !== "cursor");

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
          <CodeBlock label={`${t.name} setup`} where={t.where} code={t.code} />
          {t.then && (
            <div className="mt-6">
              <CodeBlock
                label={`${t.name} AGENTS.md line`}
                where={t.then.where}
                code={t.then.code}
              />
            </div>
          )}
        </Tabs.Content>
      ))}
    </Tabs.Root>
  );
}

function CodeBlock({
  label,
  where,
  code,
}: {
  label: string;
  where: string;
  code: string;
}) {
  return (
    <>
      <div className="flex items-end justify-between gap-3">
        <p className="text-sm text-ink-muted">{where}</p>
        <CopyButton text={code} label={`Copy ${label}`} />
      </div>
      <pre
        tabIndex={0}
        aria-label={label}
        className="mt-2 rounded-lg bg-ink p-5 text-sm leading-relaxed whitespace-pre-wrap text-paper [overflow-wrap:anywhere] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-orange"
      >
        <code>{code}</code>
      </pre>
    </>
  );
}

function CopyButton({ text, label }: { text: string; label: string }) {
  const [status, setStatus] = useState<"idle" | "copied" | "failed">("idle");
  async function copy() {
    try {
      await navigator.clipboard.writeText(text);
      setStatus("copied");
    } catch {
      setStatus("failed"); // e.g. clipboard blocked: say so, the text is still selectable
    }
    setTimeout(() => setStatus("idle"), 2000);
  }
  return (
    <button
      type="button"
      onClick={copy}
      aria-label={label}
      className="h-8 shrink-0 rounded-md border border-rule bg-surface px-3 text-sm text-ink hover:border-ink focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-orange"
    >
      <span aria-live="polite">
        {status === "copied"
          ? "Copied"
          : status === "failed"
            ? "Select and copy"
            : "Copy"}
      </span>
    </button>
  );
}
