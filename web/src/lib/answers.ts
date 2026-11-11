import type { CheckRequest, Question, Section } from "@/lib/api";

/* Answers live only in this tab (brief D6): never saved, never sent anywhere but /api/check. */
export type Answers = {
  countries: Record<string, string[]>; // users_in, company_in, processing_in
  yesno: Record<string, boolean>; // question id -> answer
  chosen: Record<string, string[]>; // question id -> ticked facts
};

export function initialAnswers(sections: Section[]): Answers {
  const answers: Answers = { countries: {}, yesno: {}, chosen: {} };
  for (const q of sections.flatMap((s) => s.questions)) {
    if (q.kind === "country") {
      const d = q.default;
      answers.countries[q.id] = d === undefined ? [] : Array.isArray(d) ? d : [d];
    }
  }
  return answers;
}

const yesnoFact = (q: Question) => q.fact ?? q.id;

/** Facts set by the visible questions. A hidden question never contributes. */
export function collectFacts(sections: Section[], answers: Answers): Set<string> {
  const facts = new Set<string>();
  // Questions are ordered so a condition is always answered before it is used.
  for (const q of sections.flatMap((s) => s.questions)) {
    if (!isVisible(q, facts)) continue;
    if (q.kind === "yesno" && answers.yesno[q.id]) facts.add(yesnoFact(q));
    if (q.kind === "choose") for (const f of answers.chosen[q.id] ?? []) facts.add(f);
  }
  return facts;
}

export function isVisible(q: Question, facts: Set<string>): boolean {
  if (q.show_if && !facts.has(q.show_if)) return false;
  if (q.show_if_any && !q.show_if_any.some((f) => facts.has(f))) return false;
  return true;
}

/** The questions in a section that are still unanswered and need an answer. */
export function missingAnswers(section: Section, answers: Answers, facts: Set<string>): Question[] {
  return section.questions.filter((q) => {
    if (!isVisible(q, facts)) return false;
    if (q.kind === "yesno") return answers.yesno[q.id] === undefined;
    if (q.kind === "country") return q.id === "users_in" && (answers.countries[q.id] ?? []).length === 0;
    return false; // "choose": ticking nothing is a valid answer
  });
}

export function toRequest(sections: Section[], answers: Answers, done: string[]): CheckRequest {
  const facts = collectFacts(sections, answers);
  return {
    users_in: answers.countries.users_in ?? [],
    company_in: answers.countries.company_in?.[0] ?? null,
    processing_in: answers.countries.processing_in ?? [],
    facts: [...facts].sort(),
    done,
  };
}
