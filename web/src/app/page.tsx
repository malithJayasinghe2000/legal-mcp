import Link from "next/link";
import { Button } from "@/components/ui/button";

const STEPS = [
  {
    title: "Answer a few questions",
    text: "Where your users are, what data you collect, whether you take payments or use AI. No account, and no need to describe your idea.",
  },
  {
    title: "Get your report",
    text: "Each issue shows how serious it is, the law and section behind it, and what to do. Must items come first.",
  },
  {
    title: "Take it to a lawyer",
    text: "Print the report with its questions for a lawyer. A short, focused meeting costs less than fixing a product after launch.",
  },
];

const AREAS = [
  ["Personal data", "Personal Data Protection Act No. 9 of 2022, as amended in 2025"],
  ["Payments", "Payment and Settlement Systems Act and Central Bank regulations"],
  ["AI features", "AI acting as a doctor, training on user data, bots"],
  ["Online content", "Online Safety Act No. 9 of 2024"],
  ["Doctors and lawyers", "Medical Ordinance, SLMC rules, Supreme Court rules for Attorneys-at-Law"],
];

export default function Home() {
  return (
    <>
      <section className="mx-auto grid max-w-6xl items-center gap-14 px-4 pt-16 pb-20 sm:px-6 md:pt-24 lg:grid-cols-[1.05fr_1fr]">
        <div>
          <h1 className="text-4xl leading-[1.08] font-semibold tracking-tight sm:text-[3.4rem]">
            Know the law before you build.
          </h1>
          <p className="mt-6 max-w-xl text-lg text-ink-muted">
            Answer a few questions about your product. Rulewise shows which Sri Lankan laws
            apply, how serious each one is, and what to ask a lawyer.
          </p>
          <div className="mt-9 flex flex-wrap gap-3">
            <Button asChild size="lg" className="h-12 px-6 text-base font-semibold">
              <Link href="/check">Check my product</Link>
            </Button>
            <Button asChild size="lg" variant="outline" className="h-12 px-6 text-base">
              <Link href="#claude-code">Use it in Claude Code</Link>
            </Button>
          </div>
          <p className="mt-6 text-sm text-ink-muted">Free. No sign-up. We store nothing you enter.</p>
        </div>

        <figure className="rounded-xl border border-rule bg-surface p-6 shadow-[0_1px_0_var(--rule)] sm:p-8">
          <figcaption className="text-sm text-ink-muted">
            A lawyer-finding site planned to charge lawyers Rs. 200 for each client enquiry.
          </figcaption>
          <div className="mt-6 grid gap-x-6 gap-y-2 border-t border-rule pt-6 sm:grid-cols-[8.5rem_1fr]">
            <p className="font-serif text-sm leading-snug text-ink-muted sm:border-r sm:border-rule sm:pr-4">
              Attorneys-at-Law Rules 1988
              <span className="mt-1 block font-semibold text-ink">Rule 39(1)</span>
            </p>
            <div>
              <p className="flex items-center gap-2 text-sm font-medium text-must">
                <span aria-hidden className="size-3 rounded-[2px] bg-must" /> Must
              </p>
              <p className="mt-1.5 text-lg leading-snug font-semibold">
                Don&apos;t charge lawyers per client, enquiry or message
              </p>
              <p className="mt-2 text-sm">
                Paying anyone for bringing clients counts as touting. Charge a flat software fee instead.
              </p>
            </div>
          </div>
          <div className="mt-6 grid gap-x-6 gap-y-2 border-t border-rule pt-6 sm:grid-cols-[8.5rem_1fr]">
            <p className="font-serif text-sm leading-snug text-ink-muted sm:border-r sm:border-rule sm:pr-4">
              Intermeddlers with Suitors Ordinance
              <span className="mt-1 block font-semibold text-ink">s.2(a)</span>
            </p>
            <div>
              <p className="flex items-center gap-2 text-sm font-medium text-must">
                <span aria-hidden className="size-3 rounded-[2px] bg-must" /> Must
              </p>
              <p className="mt-1.5 text-lg leading-snug font-semibold">
                Taking that payment is a criminal offence for the site itself
              </p>
            </div>
          </div>
          <p className="mt-6 border-t border-rule pt-4 text-sm text-ink-muted">
            The team found this from lawyers, after building. Rulewise flags it before.
          </p>
        </figure>
      </section>

      <section id="how" className="border-t border-rule bg-surface">
        <div className="mx-auto max-w-6xl px-4 py-20 sm:px-6">
          <h2 className="text-2xl font-semibold tracking-tight">How it works</h2>
          <ol className="mt-10 grid gap-10 md:grid-cols-3">
            {STEPS.map((s, i) => (
              <li key={s.title} className="border-t-2 border-ink pt-5">
                <span className="font-serif text-2xl text-orange-deep tabular-nums">{i + 1}</span>
                <h3 className="mt-2 text-lg font-semibold">{s.title}</h3>
                <p className="mt-2 text-ink-muted">{s.text}</p>
              </li>
            ))}
          </ol>
        </div>
      </section>

      <section id="coverage" className="border-t border-rule">
        <div className="mx-auto grid max-w-6xl gap-12 px-4 py-20 sm:px-6 md:grid-cols-[1fr_1.4fr]">
          <div>
            <h2 className="text-2xl font-semibold tracking-tight">What it covers</h2>
            <p className="mt-4 max-w-md text-ink-muted">
              Sri Lankan law, for the areas software most often runs into. Every report also
              lists what it does not cover, so a short report is never mistaken for an all-clear.
            </p>
            <p className="mt-4 max-w-md text-ink-muted">
              Each rule quotes the official text, links to it, and shows when it was last checked.
            </p>
          </div>
          <dl className="divide-y divide-rule border-y border-rule">
            {AREAS.map(([area, laws]) => (
              <div key={area} className="grid gap-1 py-4 sm:grid-cols-[11rem_1fr] sm:gap-6">
                <dt className="font-medium">{area}</dt>
                <dd className="font-serif text-ink-muted">{laws}</dd>
              </div>
            ))}
          </dl>
        </div>
      </section>

      <section className="border-t border-rule bg-ink text-paper">
        <div className="mx-auto grid max-w-6xl gap-10 px-4 py-20 sm:px-6 md:grid-cols-2">
          <h2 className="text-2xl font-semibold tracking-tight">Your idea stays yours.</h2>
          <div className="space-y-4 text-paper/80">
            <p>
              You never describe your idea. You answer yes or no questions, and only those
              answers are checked.
            </p>
            <p>
              Nothing is saved: no account, no cookies, no analytics. Answers live in your browser
              tab and are gone when you close it.
            </p>
          </div>
        </div>
      </section>

      <section id="claude-code" className="border-t border-rule">
        <div className="mx-auto grid max-w-6xl gap-10 px-4 py-20 sm:px-6 md:grid-cols-[1fr_1.4fr]">
          <div>
            <h2 className="text-2xl font-semibold tracking-tight">Use it while you code</h2>
            <p className="mt-4 max-w-md text-ink-muted">
              Rulewise also runs inside Claude Code as an MCP server. When you plan or build a
              feature, Claude checks it and explains the result, without you asking.
            </p>
          </div>
          <div>
            <pre className="overflow-x-auto rounded-lg bg-ink p-5 text-sm leading-relaxed text-paper">
              <code>claude mcp add rulewise -- uv run --directory /path/to/rulewise rulewise</code>
            </pre>
            <p className="mt-3 text-sm text-ink-muted">
              It runs on your own computer. Claude sends it only short facts, such as
              &ldquo;collects health data&rdquo;, never your code.
            </p>
          </div>
        </div>
      </section>
    </>
  );
}
