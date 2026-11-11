"use client";

import { useEffect, useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { type CheckResult, fetchQuestions, type QuestionsResponse, runCheck } from "@/lib/api";
import {
  type Answers,
  collectFacts,
  initialAnswers,
  isVisible,
  missingAnswers,
  toRequest,
} from "@/lib/answers";
import { cn } from "@/lib/utils";
import { QuestionField } from "./question-field";
import { Report } from "./report";

type State =
  | { phase: "loading" }
  | { phase: "load-error"; message: string }
  | { phase: "ready"; data: QuestionsResponse };

export function Checker() {
  const [state, setState] = useState<State>({ phase: "loading" });

  useEffect(() => {
    fetchQuestions()
      .then((data) => setState({ phase: "ready", data }))
      .catch((e: Error) => setState({ phase: "load-error", message: e.message }));
  }, []);

  if (state.phase === "loading") {
    return <p className="py-24 text-ink-muted" role="status">Loading the questions…</p>;
  }
  if (state.phase === "load-error") {
    return (
      <ErrorBox
        title="The questions could not be loaded"
        message={state.message}
        action={<Button onClick={() => location.reload()}>Try again</Button>}
      />
    );
  }
  return <Wizard data={state.data} />;
}

function Wizard({ data }: { data: QuestionsResponse }) {
  const sections = data.questionnaire.sections;
  const [answers, setAnswers] = useState<Answers>(() => initialAnswers(sections));
  const [step, setStep] = useState(0);
  const [showErrors, setShowErrors] = useState(false);
  const [done, setDone] = useState<string[]>([]);
  const [result, setResult] = useState<CheckResult | null>(null);
  const [checkError, setCheckError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const headingRef = useRef<HTMLHeadingElement>(null);

  const facts = collectFacts(sections, answers);
  const section = sections[step];
  const missing = missingAnswers(section, answers, facts);
  const isLast = step === sections.length - 1;

  function go(to: number) {
    setStep(to);
    setShowErrors(false);
    requestAnimationFrame(() => headingRef.current?.focus());
  }

  async function submit(nextDone = done) {
    setBusy(true);
    setCheckError(null);
    try {
      setResult(await runCheck(toRequest(sections, answers, nextDone)));
      setDone(nextDone);
      window.scrollTo({ top: 0 });
    } catch (e) {
      setResult(null);
      setCheckError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }

  function next() {
    if (missing.length) {
      setShowErrors(true);
      return;
    }
    if (isLast) void submit();
    else go(step + 1);
  }

  if (result) {
    return (
      <Report
        result={result}
        busy={busy}
        onToggleDone={(id) => void submit(done.includes(id) ? done.filter((d) => d !== id) : [...done, id])}
        onEdit={() => {
          setResult(null);
          go(0);
        }}
      />
    );
  }

  return (
    <div className="grid gap-10 md:grid-cols-[14rem_1fr] md:gap-16">
      <nav aria-label="Steps" className="no-print">
        <p className="mb-3 text-sm text-ink-muted md:hidden">
          Step {step + 1} of {sections.length}
        </p>
        <ol className="hidden space-y-1 md:block">
          {sections.map((s, i) => (
            <li key={s.id}>
              <button
                type="button"
                onClick={() => i < step && go(i)}
                disabled={i > step}
                aria-current={i === step ? "step" : undefined}
                className={cn(
                  "flex w-full items-baseline gap-3 rounded-md px-3 py-2 text-left text-sm",
                  i === step && "bg-surface font-medium text-ink shadow-[inset_3px_0_0_var(--orange)]",
                  i < step && "text-ink hover:bg-surface",
                  i > step && "cursor-default text-ink-muted"
                )}
              >
                <span className="font-serif tabular-nums">{i + 1}</span>
                {s.title}
              </button>
            </li>
          ))}
        </ol>
      </nav>

      <form
        className="max-w-2xl pb-28 md:pb-0"
        onSubmit={(e) => {
          e.preventDefault();
          next();
        }}
      >
        <h1 ref={headingRef} tabIndex={-1} className="text-2xl font-semibold tracking-tight outline-none">
          {section.title}
        </h1>
        {section.intro && <p className="mt-2 max-w-prose text-ink-muted">{section.intro}</p>}

        <div className="mt-10 space-y-10">
          {section.questions
            .filter((q) => isVisible(q, facts))
            .map((q) => (
              <QuestionField
                key={q.id}
                question={q}
                answers={answers}
                invalid={showErrors && missing.includes(q)}
                onChange={setAnswers}
              />
            ))}
        </div>

        {checkError && (
          <div className="mt-10">
            <ErrorBox title="The check did not run" message={checkError} />
          </div>
        )}

        <div className="no-print fixed inset-x-0 bottom-0 flex gap-3 border-t border-rule bg-paper px-4 py-3 md:static md:mt-12 md:border-0 md:p-0">
          {step > 0 && (
            <Button type="button" variant="outline" size="lg" className="h-11 px-5" onClick={() => go(step - 1)}>
              Back
            </Button>
          )}
          <Button type="submit" size="lg" className="h-11 flex-1 px-6 font-semibold md:flex-none" disabled={busy}>
            {isLast ? (busy ? "Checking…" : "Show my report") : "Next"}
          </Button>
        </div>
      </form>
    </div>
  );
}

export function ErrorBox({
  title,
  message,
  action,
}: {
  title: string;
  message: string;
  action?: React.ReactNode;
}) {
  return (
    <div role="alert" className="max-w-2xl rounded-lg border border-must/30 bg-surface p-5">
      <p className="font-medium text-must">{title}</p>
      <p className="mt-1 text-sm text-ink">{message}</p>
      <p className="mt-1 text-sm text-ink-muted">
        This is an error, not a result. Nothing was checked, so don&apos;t read it as &ldquo;no issues&rdquo;.
      </p>
      {action && <div className="mt-4">{action}</div>}
    </div>
  );
}
