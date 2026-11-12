import Link from "next/link";
import { SetupTabs } from "@/components/setup-tabs";
import { Button } from "@/components/ui/button";
import { SHOW_SITE_CHECK } from "@/lib/features";

// Steps for the website's own check (hidden for now, D21).
const SITE_STEPS = [
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

const MCP_STEPS = [
  {
    title: "Add Rulewise to your AI tool",
    text: "Claude Code, Cursor, Codex, VS Code or any tool that supports MCP. It takes one line of setup.",
  },
  {
    title: "Plan or build as usual",
    text: "When you describe a feature, your AI asks a few short questions and checks them against the Sri Lankan laws in Rulewise.",
  },
  {
    title: "Get warnings with the law",
    text: "Each warning shows how serious it is, the law and section behind it, what to do, and what to ask a lawyer.",
  },
];

const AREAS = [
  [
    "Personal data",
    "Personal Data Protection Act No. 9 of 2022, as amended in 2025",
  ],
  [
    "Payments",
    "Payment and Settlement Systems Act and Central Bank regulations",
  ],
  ["AI features", "Training on user data, bots, AI giving medical advice"],
  ["Online content", "Online Safety Act No. 9 of 2024"],
  ["Consumer rights", "Consumer Affairs Authority Act No. 9 of 2003"],
  ["Online contracts", "Electronic Transactions Act No. 19 of 2006, as amended in 2017"],
  ["Professions", "Rules that limit platforms for doctors and lawyers"],
];

function Example() {
  const items = [
    {
      law: "Personal Data Protection Act",
      section: "s.27(1)",
      title: "Promotional messages need consent and an easy opt-out",
      text: "Ask for a separate yes before sending offers, and put a free opt-out in every SMS.",
    },
    {
      law: "Personal Data Protection Act",
      section: "s.11; Schedule V",
      title: "Tell users what you collect and why",
      text: "Show a privacy notice when people sign up: what you collect, why, and who gets it.",
    },
  ];
  return (
    <figure className="rounded-xl border border-rule bg-surface p-6 shadow-[0_1px_0_var(--rule)] sm:p-8">
      <figcaption className="text-sm text-ink-muted">
        An online shop app saves customers&apos; phone numbers and sends them
        offers by SMS.
      </figcaption>
      {items.map((item) => (
        <div
          key={item.section}
          className="mt-6 grid gap-x-6 gap-y-2 border-t border-rule pt-6 sm:grid-cols-[8.5rem_1fr]"
        >
          <p className="font-serif text-sm leading-snug text-ink-muted sm:border-r sm:border-rule sm:pr-4">
            {item.law}
            <span className="mt-1 block font-semibold text-ink">
              {item.section}
            </span>
          </p>
          <div>
            <p className="flex items-center gap-2 text-sm font-medium text-must">
              <span aria-hidden className="size-3 rounded-[2px] bg-must" /> Must
            </p>
            <p className="mt-1.5 text-lg leading-snug font-semibold">
              {item.title}
            </p>
            <p className="mt-2 text-sm">{item.text}</p>
          </div>
        </div>
      ))}
      <p className="mt-6 border-t border-rule pt-4 text-sm text-ink-muted">
        Easy to miss when you only think about the code. Rulewise flags it
        before you build.
      </p>
    </figure>
  );
}

export default function Home() {
  const steps = SHOW_SITE_CHECK ? SITE_STEPS : MCP_STEPS;
  return (
    <>
      <section className="mx-auto grid max-w-6xl items-center gap-14 px-4 pt-16 pb-20 sm:px-6 md:pt-24 lg:grid-cols-[1.05fr_1fr]">
        <div>
          <h1 className="text-4xl leading-[1.08] font-semibold tracking-tight sm:text-[3.4rem]">
            Know the law before you build.
          </h1>
          <p className="mt-6 max-w-xl text-lg text-ink-muted">
            {SHOW_SITE_CHECK
              ? "Answer a few questions about your product. Rulewise shows which Sri Lankan laws apply, how serious each one is, and what to ask a lawyer."
              : "Rulewise works inside your AI coding tool. While you plan a product, it shows which Sri Lankan laws apply, how serious each one is, and what to ask a lawyer."}
          </p>
          <div className="mt-9 flex flex-wrap gap-3">
            {SHOW_SITE_CHECK && (
              <Button
                asChild
                size="lg"
                className="h-12 px-6 text-base font-semibold"
              >
                <Link href="/check">Check my product</Link>
              </Button>
            )}
            <Button
              asChild
              size="lg"
              variant={SHOW_SITE_CHECK ? "outline" : "default"}
              className="h-12 px-6 text-base font-semibold"
            >
              <Link href="#setup">Add to your AI tool</Link>
            </Button>
          </div>
          <p className="mt-6 text-sm text-ink-muted">
            Free. No sign-up. We store nothing you send.
          </p>
        </div>

        <Example />
      </section>

      <section id="how" className="border-t border-rule bg-surface">
        <div className="mx-auto max-w-6xl px-4 py-20 sm:px-6">
          <h2 className="text-2xl font-semibold tracking-tight">
            How it works
          </h2>
          <ol className="mt-10 grid gap-10 md:grid-cols-3">
            {steps.map((s, i) => (
              <li key={s.title} className="border-t-2 border-ink pt-5">
                <span className="font-serif text-2xl text-orange-deep tabular-nums">
                  {i + 1}
                </span>
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
            <h2 className="text-2xl font-semibold tracking-tight">
              What it covers
            </h2>
            <p className="mt-4 max-w-md text-ink-muted">
              Sri Lankan law, for the areas software most often runs into. Every
              result also lists what it does not cover, so a short result is
              never mistaken for an all-clear.
            </p>
            <p className="mt-4 max-w-md text-ink-muted">
              Each rule quotes the official text, links to it, and shows when it
              was last checked.
            </p>
          </div>
          <dl className="divide-y divide-rule border-y border-rule">
            {AREAS.map(([area, laws]) => (
              <div
                key={area}
                className="grid gap-1 py-4 sm:grid-cols-[11rem_1fr] sm:gap-6"
              >
                <dt className="font-medium">{area}</dt>
                <dd className="font-serif text-ink-muted">{laws}</dd>
              </div>
            ))}
          </dl>
        </div>
      </section>

      <section className="border-t border-rule bg-ink text-paper">
        <div className="mx-auto grid max-w-6xl gap-10 px-4 py-20 sm:px-6 md:grid-cols-2">
          <h2 className="text-2xl font-semibold tracking-tight">
            Your idea stays yours.
          </h2>
          <div className="space-y-4 text-paper/80">
            {SHOW_SITE_CHECK ? (
              <>
                <p>
                  You never describe your idea. You answer yes or no questions,
                  and only those answers are checked.
                </p>
                <p>
                  Nothing is saved: no account, no cookies, no analytics.
                  Answers live in your browser tab and are gone when you close
                  it.
                </p>
              </>
            ) : (
              <>
                <p>
                  Your AI tool reads your idea on your side. Rulewise only gets
                  short facts, such as &ldquo;collects phone numbers&rdquo;,
                  never your idea or your code.
                </p>
                <p>
                  It runs on your own computer, and nothing is saved: no
                  account, no cookies, no analytics.
                </p>
              </>
            )}
          </div>
        </div>
      </section>

      <section id="setup" className="border-t border-rule">
        <div className="mx-auto grid max-w-6xl gap-10 px-4 py-20 sm:px-6 md:grid-cols-[1fr_1.4fr]">
          <div>
            <h2 className="text-2xl font-semibold tracking-tight">
              Add it to your AI tool
            </h2>
            <p className="mt-4 max-w-md text-ink-muted">
              Rulewise is an MCP server, so it works with any AI tool that
              supports MCP. When you plan or build a feature, your AI checks it
              and explains the result.
            </p>
            <p className="mt-4 max-w-md text-ink-muted">
              You need{" "}
              <a href="https://docs.astral.sh/uv/" className="text-orange-deep underline underline-offset-2">
                uv
              </a>{" "}
              and a copy of the Rulewise code. Change the path to where you
              saved it.
            </p>
          </div>
          <SetupTabs />
        </div>
      </section>
    </>
  );
}
