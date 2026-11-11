"use client";

import { ExternalLink, Printer } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { type CheckResult, fetchRule, type RuleDetail, type Severity, type Warning } from "@/lib/api";
import { countryName } from "@/lib/countries";
import { cn } from "@/lib/utils";

const SEVERITY: Record<Severity, { color: string; marker: string; meaning: string }> = {
  Must: { color: "text-must", marker: "bg-must", meaning: "Required by law" },
  Should: { color: "text-should", marker: "bg-[linear-gradient(90deg,var(--should)_50%,transparent_50%)] ring-1 ring-should ring-inset", meaning: "A real risk" },
  "Check with a lawyer": { color: "text-lawyer", marker: "ring-2 ring-lawyer ring-inset", meaning: "The law is unclear here" },
};
const ORDER: Severity[] = ["Must", "Should", "Check with a lawyer"];

function SeverityMark({ severity }: { severity: Severity }) {
  return <span aria-hidden className={cn("inline-block size-3 shrink-0 rounded-[2px]", SEVERITY[severity].marker)} />;
}

type Props = {
  result: CheckResult;
  busy: boolean;
  onToggleDone: (ruleId: string) => void;
  onEdit: () => void;
};

export function Report({ result, busy, onToggleDone, onEdit }: Props) {
  const counts = ORDER.map((s) => [s, result.warnings.filter((w) => w.severity === s).length] as const);

  return (
    <article aria-labelledby="report-title" className="mx-auto max-w-5xl">
      <header className="flex flex-wrap items-end justify-between gap-6 border-b border-rule pb-8">
        <div className="max-w-2xl">
          <h1 id="report-title" className="text-3xl font-semibold tracking-tight">
            Your report
          </h1>
          <p className="mt-3 text-ink-muted" aria-live="polite">
            {result.summary}
          </p>
        </div>
        <div className="no-print flex gap-3">
          <Button variant="outline" size="lg" className="h-10 px-4" onClick={onEdit}>
            Change answers
          </Button>
          <Button variant="outline" size="lg" className="h-10 px-4" onClick={() => window.print()}>
            <Printer aria-hidden /> Print or save as PDF
          </Button>
        </div>
      </header>

      <dl className="grid grid-cols-3 border-b border-rule">
        {counts.map(([severity, n]) => (
          <div key={severity} className="border-r border-rule py-6 pr-4 pl-0 last:border-r-0 sm:pl-6 sm:first:pl-0">
            <dt className={cn("flex items-start gap-2 text-sm font-medium leading-tight", SEVERITY[severity].color)}>
              <SeverityMark severity={severity} />
              {severity}
            </dt>
            <dd className="mt-1 animate-in fade-in slide-in-from-bottom-1 text-3xl font-semibold text-ink tabular-nums duration-500 sm:text-4xl">
              {n}
            </dd>
            <dd className="text-xs leading-snug text-ink-muted sm:text-sm">{SEVERITY[severity].meaning}</dd>
          </div>
        ))}
      </dl>

      {result.warnings.length === 0 && (
        <p className="mt-10 max-w-2xl rounded-lg bg-surface p-6">
          No issues found in the areas we cover. That does not mean your product is compliant:
          check the areas and countries we don&apos;t cover, below.
        </p>
      )}

      {result.warnings.length > 1 && (
        <nav aria-labelledby="glance-title" className="no-print mt-10">
          <h2 id="glance-title" className="text-sm font-semibold">At a glance</h2>
          <ol className="mt-3 grid gap-x-10 gap-y-2 text-sm md:grid-cols-2">
            {result.warnings.map((w, i) => (
              <li key={w.rule_id} className="flex items-baseline gap-3">
                <span className="w-5 shrink-0 text-right font-serif text-ink-muted tabular-nums">{i + 1}</span>
                <SeverityMark severity={w.severity} />
                <a href={`#${w.rule_id}`} className="text-ink underline decoration-rule hover:decoration-ink">
                  {w.title}
                  <span className="sr-only"> ({w.severity})</span>
                </a>
              </li>
            ))}
          </ol>
        </nav>
      )}

      <div className={cn("mt-6 transition-opacity", busy && "opacity-60")}>
        {result.warnings.map((w, i) => (
          <WarningSection key={w.rule_id} warning={w} number={i + 1} busy={busy} onDone={() => onToggleDone(w.rule_id)} />
        ))}
      </div>

      {result.done.length > 0 && (
        <section aria-labelledby="done-title" className="mt-14">
          <h2 id="done-title" className="text-xl font-semibold">Marked done by you</h2>
          <p className="mt-1 text-sm text-ink-muted">Rulewise can&apos;t check your work. Each line says what to double-check.</p>
          <ul className="mt-4 divide-y divide-rule border-y border-rule">
            {result.done.map((d) => (
              <li key={d.rule_id} className="flex flex-wrap items-start justify-between gap-4 py-4">
                <div className="max-w-2xl">
                  <p className="font-medium">{d.title}</p>
                  <p className="mt-1 text-sm text-ink-muted">{d.check}</p>
                </div>
                <Button variant="ghost" size="sm" className="no-print" disabled={busy} onClick={() => onToggleDone(d.rule_id)}>
                  Not done yet
                </Button>
              </li>
            ))}
          </ul>
        </section>
      )}

      {result.client_duties && (
        <section aria-labelledby="client-title" className="mt-14">
          <h2 id="client-title" className="text-xl font-semibold">Your client&apos;s duties</h2>
          <p className="mt-1 max-w-2xl text-sm text-ink-muted">{result.client_duties.note}</p>
          <ul className="mt-4 divide-y divide-rule border-y border-rule">
            {result.client_duties.items.map((c) => (
              <li key={c.rule_id} className="grid gap-1 py-3 sm:grid-cols-[13rem_1fr] sm:gap-8">
                <span className="font-serif text-sm text-ink-muted">{c.law}</span>
                <span className="flex items-center gap-2">
                  <SeverityMark severity={c.severity} />
                  {c.title}
                </span>
              </li>
            ))}
          </ul>
        </section>
      )}

      <section aria-labelledby="scope-title" className="mt-14 grid gap-10 border-t border-rule pt-10 md:grid-cols-2">
        <div>
          <h2 id="scope-title" className="text-xl font-semibold">What this report covers</h2>
          <ul className="mt-3 space-y-2 text-sm">
            {result.areas_covered.map((a) => <li key={a}>{a}</li>)}
          </ul>
        </div>
        <div>
          <h2 className="text-xl font-semibold">Not covered</h2>
          <p className="mt-3 text-sm">{result.areas_not_covered.join(", ")}.</p>
          {result.countries_not_covered.length > 0 && (
            <p className="mt-3 text-sm">
              Laws of {result.countries_not_covered.map(countryName).join(", ")} are not covered. Rulewise covers Sri Lankan law only.
            </p>
          )}
        </div>
      </section>

      <p className="mt-10 max-w-2xl border-t border-rule pt-6 text-sm text-ink-muted">{result.disclaimer}</p>
    </article>
  );
}

function WarningSection({ warning: w, number, busy, onDone }: { warning: Warning; number: number; busy: boolean; onDone: () => void }) {
  const [law, setLaw] = useState<{ state: "closed" } | { state: "loading" } | { state: "open"; rule: RuleDetail } | { state: "error"; message: string }>({ state: "closed" });
  const lawId = `law-${w.rule_id}`;

  async function toggleLaw() {
    if (law.state === "open" || law.state === "error") return setLaw({ state: "closed" });
    setLaw({ state: "loading" });
    try {
      setLaw({ state: "open", rule: await fetchRule(w.rule_id) });
    } catch (e) {
      setLaw({ state: "error", message: (e as Error).message });
    }
  }

  return (
    <section id={w.rule_id} aria-labelledby={`${w.rule_id}-title`} className="scroll-mt-6 grid gap-x-10 gap-y-3 border-b border-rule py-9 md:grid-cols-[13rem_1fr] print:break-inside-avoid">
      {/* The marginal note: the law, beside the duty, like a printed Act. */}
      <aside className="font-serif text-sm leading-snug text-ink-muted md:border-r md:border-rule md:pr-6">
        <span className="tabular-nums">{number}.</span> {w.law.name}
        <span className="mt-1 block font-semibold text-ink">{w.law.section}</span>
      </aside>

      <div className="max-w-2xl">
        <p className={cn("flex items-center gap-2 text-sm font-medium", SEVERITY[w.severity].color)}>
          <SeverityMark severity={w.severity} />
          {w.severity}
          <span className="font-normal text-ink-muted">{w.status}</span>
        </p>
        <h2 id={`${w.rule_id}-title`} className="mt-2 text-xl font-semibold leading-snug tracking-tight">
          {w.title}
        </h2>
        <p className="mt-3">{w.why}</p>

        <h3 className="mt-5 text-sm font-semibold">What to do</h3>
        <ul className="mt-2 list-disc space-y-1.5 pl-5 marker:text-orange-deep">
          {w.what_to_do.map((t) => <li key={t}>{t}</li>)}
        </ul>

        {w.lawyer_questions.length > 0 && (
          <>
            <h3 className="mt-5 text-sm font-semibold">Ask a lawyer</h3>
            <ul className="mt-2 list-disc space-y-1.5 pl-5 marker:text-ink-muted">
              {w.lawyer_questions.map((t) => <li key={t}>{t}</li>)}
            </ul>
          </>
        )}

        {law.state === "open" && (
          <blockquote id={lawId} className="mt-6 border-l-2 border-orange bg-surface py-4 pr-5 pl-5">
            <p className="font-serif text-base leading-relaxed italic">&ldquo;{law.rule.law.quote}&rdquo;</p>
            <footer className="mt-3 text-sm text-ink-muted">
              {law.rule.law.name}, {law.rule.law.section}.{" "}
              <a href={law.rule.law.source_url} target="_blank" rel="noreferrer noopener" className="inline-flex items-center gap-1 text-orange-deep underline">
                Official text <ExternalLink className="size-3.5" aria-hidden />
                <span className="sr-only">(opens in a new tab)</span>
              </a>
            </footer>
          </blockquote>
        )}
        {law.state === "error" && (
          <p id={lawId} role="alert" className="mt-4 text-sm text-must">The law text could not be loaded: {law.message}</p>
        )}

        <div className="no-print mt-6 flex flex-wrap items-center gap-3">
          <Button variant="outline" size="sm" className="h-9 px-3" aria-expanded={law.state === "open"} aria-controls={lawId} onClick={toggleLaw}>
            {law.state === "open" ? "Hide the law" : law.state === "loading" ? "Loading…" : "Read the law"}
          </Button>
          <Button variant="ghost" size="sm" className="h-9 px-3" disabled={busy} onClick={onDone}>
            Mark as done
          </Button>
          <span className="text-xs text-ink-muted">{w.review}. Checked {w.last_checked}.</span>
        </div>
      </div>
    </section>
  );
}
