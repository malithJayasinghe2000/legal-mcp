"use client";

import { useState } from "react";
import { Tabs } from "radix-ui";

// The hosted server (Azure Container Apps, brief D23). Nothing to install.
const URL =
  "https://rulewise.victoriousdune-a7b660c5.centralindia.azurecontainerapps.io/mcp";

// The Claude Code plugin bundles the server, the skill and /rulewise:check and
// /rulewise:pdpa. Codex doesn't act on the server's own instructions, so it needs the
// skill (skills/rulewise/SKILL.md); tested 2026-11-18 and 2026-11-19. VS Code Copilot
// shows the server's prompts as /mcp.rulewise.<name>; Cursor follows plain words.
const PLUGIN_INSTALL = `claude plugin marketplace add malithJayasinghe2000/legal-mcp
claude plugin install rulewise@rulewise`;
const SKILL_INSTALL = "npx skills add malithJayasinghe2000/legal-mcp";

type Step = { label: string; where: string; code: string };
type Try = { say: string; does: string };
type Tool = {
  id: string;
  name: string;
  steps: Step[];
  tryWhere: string;
  tryIt: Try[];
  alt?: Step;
};

const PLAIN_WORDS: Try[] = [
  { say: "Run the Rulewise PDPA checklist", does: "PDPA 2027 checklist" },
  {
    say: "Check my project with Rulewise",
    does: "Report on the whole project",
  },
  {
    say: "Or just describe what you're building",
    does: "Warnings as you build",
  },
];

const TOOLS: Tool[] = [
  {
    id: "claude-code",
    name: "Claude Code",
    steps: [
      {
        label: "setup",
        where:
          "Run in your terminal. It adds Rulewise and its two commands in one go:",
        code: PLUGIN_INSTALL,
      },
    ],
    tryWhere: "Restart Claude Code, then type:",
    tryIt: [
      { say: "/rulewise:pdpa", does: "PDPA 2027 checklist" },
      { say: "/rulewise:check", does: "Report on the whole project" },
      {
        say: "Or just describe what you're building",
        does: "Warnings as you build",
      },
    ],
    alt: {
      label: "server only",
      where: "Only want the warnings, without the commands? Run this instead:",
      code: `claude mcp add --transport http rulewise ${URL}`,
    },
  },
  {
    id: "codex",
    name: "Codex",
    steps: [
      {
        label: "setup",
        where: "Add to ~/.codex/config.toml:",
        code: `[mcp_servers.rulewise]
url = "${URL}"`,
      },
      {
        label: "skill",
        where:
          "Add the Rulewise skill (needs Node.js), so Codex knows when and how to use it:",
        code: SKILL_INSTALL,
      },
    ],
    tryWhere: "Restart Codex, then say:",
    tryIt: PLAIN_WORDS,
  },
  {
    id: "cursor",
    name: "Cursor",
    steps: [
      {
        label: "setup",
        where: "Add to ~/.cursor/mcp.json:",
        code: `{
  "mcpServers": {
    "rulewise": {
      "url": "${URL}"
    }
  }
}`,
      },
    ],
    tryWhere: "Restart Cursor, then say in Agent mode:",
    tryIt: PLAIN_WORDS,
  },
  {
    id: "vscode",
    name: "VS Code",
    steps: [
      {
        label: "setup",
        where:
          'Open the Command Palette (Cmd+Shift+P), run "MCP: Open User Configuration" and add:',
        code: `{
  "servers": {
    "rulewise": {
      "type": "http",
      "url": "${URL}"
    }
  }
}`,
      },
    ],
    tryWhere: "In Copilot Chat (Agent mode), type:",
    tryIt: [
      { say: "/mcp.rulewise.pdpa_checklist", does: "PDPA 2027 checklist" },
      {
        say: "/mcp.rulewise.check_project",
        does: "Report on the whole project",
      },
      {
        say: "Or just describe what you're building",
        does: "Warnings as you build",
      },
    ],
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
          className="mt-5 focus-visible:outline-none"
        >
          <ol className="space-y-6">
            {t.steps.map((s, i) => (
              <li key={s.label} className="grid grid-cols-[1.75rem_1fr] gap-2">
                <StepNumber n={i + 1} />
                <div className="min-w-0">
                  <CodeBlock
                    label={`${t.name} ${s.label}`}
                    where={s.where}
                    code={s.code}
                  />
                </div>
              </li>
            ))}
            <li className="grid grid-cols-[1.75rem_1fr] gap-2">
              <StepNumber n={t.steps.length + 1} />
              <TryIt
                label={`${t.name} try it`}
                where={t.tryWhere}
                items={t.tryIt}
              />
            </li>
          </ol>
          {t.alt && (
            <div className="mt-8 border-t border-rule pt-6">
              <CodeBlock
                label={`${t.name} ${t.alt.label}`}
                where={t.alt.where}
                code={t.alt.code}
              />
            </div>
          )}
        </Tabs.Content>
      ))}
    </Tabs.Root>
  );
}

function StepNumber({ n }: { n: number }) {
  return (
    <span className="pt-0.5 font-serif text-lg leading-none text-orange-deep tabular-nums">
      {n}
    </span>
  );
}

function TryIt({
  label,
  where,
  items,
}: {
  label: string;
  where: string;
  items: Try[];
}) {
  return (
    <div className="min-w-0">
      <p className="text-sm text-ink-muted">{where}</p>
      <ul
        aria-label={label}
        className="mt-2 divide-y divide-rule rounded-lg border border-rule bg-surface"
      >
        {items.map((it) => (
          <li
            key={it.say}
            className="grid gap-1 px-4 py-3 sm:grid-cols-[1fr_auto] sm:items-center sm:gap-4"
          >
            {it.say.startsWith("/") ? (
              <code className="font-mono text-sm font-medium [overflow-wrap:anywhere]">
                {it.say}
              </code>
            ) : it.say.startsWith("Or ") ? (
              <span className="text-sm text-ink-muted">{it.say}</span>
            ) : (
              <span className="text-sm font-medium">
                &ldquo;{it.say}&rdquo;
              </span>
            )}
            <span className="text-sm text-ink-muted">{it.does}</span>
          </li>
        ))}
      </ul>
    </div>
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
