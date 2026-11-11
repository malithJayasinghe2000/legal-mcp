import { z } from "zod";

/* Types for the Python API (src/legal_check/web_api.py). Responses are validated with
   zod: a response we don't understand is shown as an error, never as "no issues". */

const Option = z.object({ fact: z.string(), label: z.string() });

export const Question = z.object({
  id: z.string(),
  kind: z.enum(["yesno", "choose", "country"]),
  label: z.string(),
  help: z.string().optional(),
  fact: z.string().optional(),
  multiple: z.boolean().optional(),
  default: z.union([z.string(), z.array(z.string())]).optional(),
  show_if: z.string().optional(),
  show_if_any: z.array(z.string()).optional(),
  options: z.array(Option).optional(),
});
export type Question = z.infer<typeof Question>;

export const Section = z.object({
  id: z.string(),
  title: z.string(),
  intro: z.string().optional(),
  questions: z.array(Question),
});
export type Section = z.infer<typeof Section>;

export const QuestionsResponse = z.object({
  questionnaire: z.object({ sections: z.array(Section) }),
  areas: z.object({
    covered: z.record(z.string(), z.object({ label: z.string(), gaps: z.string() })),
    not_covered: z.array(z.string()),
  }),
});
export type QuestionsResponse = z.infer<typeof QuestionsResponse>;

export const Severity = z.enum(["Must", "Should", "Check with a lawyer"]);
export type Severity = z.infer<typeof Severity>;

export const Warning = z.object({
  severity: Severity,
  title: z.string(),
  rule_id: z.string(),
  area: z.string(),
  triggered_by: z.array(z.string()),
  why: z.string(),
  what_to_do: z.array(z.string()),
  lawyer_questions: z.array(z.string()),
  law: z.object({ name: z.string(), section: z.string(), source_url: z.string() }),
  status: z.string(),
  review: z.string(),
  last_checked: z.string(),
});
export type Warning = z.infer<typeof Warning>;

const DoneItem = z.object({
  rule_id: z.string(),
  title: z.string(),
  severity: Severity,
  check: z.string(),
});

export const CheckResult = z.object({
  summary: z.string(),
  warnings: z.array(Warning),
  done: z.array(DoneItem),
  client_duties: z
    .object({
      note: z.string(),
      items: z.array(
        z.object({ rule_id: z.string(), title: z.string(), severity: Severity, law: z.string() })
      ),
    })
    .nullable(),
  areas_covered: z.array(z.string()),
  areas_not_covered: z.array(z.string()),
  countries_not_covered: z.array(z.string()),
  disclaimer: z.string(),
});
export type CheckResult = z.infer<typeof CheckResult>;

export const RuleDetail = z.object({
  id: z.string(),
  law: z.object({
    name: z.string(),
    section: z.string(),
    source_url: z.string(),
    quote: z.string(),
  }),
  notes: z.string().optional().nullable(),
});
export type RuleDetail = z.infer<typeof RuleDetail>;

export type CheckRequest = {
  users_in: string[];
  company_in: string | null;
  processing_in: string[];
  facts: string[];
  done: string[];
};

async function getJson<T>(res: Response, schema: z.ZodType<T>): Promise<T> {
  const body = await res.json().catch(() => null);
  if (!res.ok) {
    const message =
      body && typeof body === "object" && "error" in body ? String(body.error) : `HTTP ${res.status}`;
    throw new Error(message);
  }
  const parsed = schema.safeParse(body);
  if (!parsed.success) throw new Error("The server sent an answer this page doesn't understand.");
  return parsed.data;
}

export async function fetchQuestions(): Promise<QuestionsResponse> {
  return getJson(await fetch("/api/questions", { cache: "no-store" }), QuestionsResponse);
}

export async function runCheck(body: CheckRequest): Promise<CheckResult> {
  const res = await fetch("/api/check", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    cache: "no-store",
  });
  return getJson(res, CheckResult);
}

export async function fetchRule(id: string): Promise<RuleDetail> {
  return getJson(await fetch(`/api/rules/${encodeURIComponent(id)}`, { cache: "no-store" }), RuleDetail);
}
