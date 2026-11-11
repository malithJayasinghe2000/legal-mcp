"use client";

import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import type { Question } from "@/lib/api";
import type { Answers } from "@/lib/answers";
import { CountryPicker } from "./country-picker";

type Props = {
  question: Question;
  answers: Answers;
  invalid: boolean;
  onChange: (next: Answers) => void;
};

export function QuestionField({ question: q, answers, invalid, onChange }: Props) {
  const labelId = `${q.id}-label`;
  const errorId = `${q.id}-error`;

  return (
    <fieldset className="space-y-4" aria-describedby={invalid ? errorId : undefined}>
      <legend id={labelId} className="text-lg font-medium leading-snug text-ink">
        {q.label}
      </legend>
      {q.help && <p className="-mt-2 text-sm text-ink-muted">{q.help}</p>}

      {q.kind === "country" && (
        <CountryPicker
          id={q.id}
          labelId={labelId}
          multiple={q.multiple ?? true}
          value={answers.countries[q.id] ?? []}
          onChange={(v) => onChange({ ...answers, countries: { ...answers.countries, [q.id]: v } })}
        />
      )}

      {q.kind === "yesno" && (
        <RadioGroup
          aria-labelledby={labelId}
          value={answers.yesno[q.id] === undefined ? "" : answers.yesno[q.id] ? "yes" : "no"}
          onValueChange={(v) => onChange({ ...answers, yesno: { ...answers.yesno, [q.id]: v === "yes" } })}
          className="flex gap-3"
        >
          {(["yes", "no"] as const).map((v) => (
            <Label
              key={v}
              htmlFor={`${q.id}-${v}`}
              className="flex h-11 min-w-24 cursor-pointer items-center gap-3 rounded-md border border-input bg-surface px-4 text-base font-normal has-[[data-state=checked]]:border-ink has-[[data-state=checked]]:bg-orange-wash"
            >
              <RadioGroupItem id={`${q.id}-${v}`} value={v} />
              {v === "yes" ? "Yes" : "No"}
            </Label>
          ))}
        </RadioGroup>
      )}

      {q.kind === "choose" && (
        <div className="grid gap-2">
          {(q.options ?? []).map((o) => {
            const chosen = answers.chosen[q.id] ?? [];
            const id = `${q.id}-${o.fact}`;
            return (
              <Label
                key={o.fact}
                htmlFor={id}
                className="flex cursor-pointer items-start gap-3 rounded-md border border-input bg-surface px-4 py-3 text-base font-normal leading-snug has-[[data-state=checked]]:border-ink has-[[data-state=checked]]:bg-orange-wash"
              >
                <Checkbox
                  id={id}
                  className="mt-0.5"
                  checked={chosen.includes(o.fact)}
                  onCheckedChange={(c) =>
                    onChange({
                      ...answers,
                      chosen: {
                        ...answers.chosen,
                        [q.id]: c ? [...chosen, o.fact] : chosen.filter((f) => f !== o.fact),
                      },
                    })
                  }
                />
                {o.label}
              </Label>
            );
          })}
          <p className="text-sm text-ink-muted">Leave all unticked if none apply.</p>
        </div>
      )}

      {invalid && (
        <p id={errorId} className="text-sm font-medium text-must">
          {q.kind === "country" ? "Choose at least one country." : "Choose yes or no."}
        </p>
      )}
    </fieldset>
  );
}
