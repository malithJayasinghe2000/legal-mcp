import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Privacy and terms",
  description:
    "What Rulewise sees, what it keeps (nothing), and what it is not.",
};

const ISSUES = "https://github.com/malithJayasinghe2000/legal-mcp/issues";

function Section({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <section className="mt-12">
      <h2 className="text-xl font-semibold tracking-tight">{title}</h2>
      <div className="mt-4 space-y-4">{children}</div>
    </section>
  );
}

export default function PrivacyPage() {
  return (
    <article className="mx-auto max-w-2xl px-4 py-16 text-[1.0625rem] leading-relaxed sm:px-6 md:py-24">
      <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">
        Privacy and terms
      </h1>
      <p className="mt-3 text-sm text-ink-muted">
        Last updated 16 November 2026
      </p>

      <p className="mt-8">
        I built Rulewise because I kept finding out about laws after I had
        already built something. When you&apos;re working on an idea, you
        shouldn&apos;t have to wonder who is reading it. So I set this up to
        know as little about you as possible. Here&apos;s exactly what that
        means.
      </p>

      <Section title="Your idea never reaches me">
        <p>
          Rulewise works inside your AI tool, like Claude Code or Codex. Your AI
          reads what you&apos;re building on your side. It then sends Rulewise
          only a short list of facts, for example &ldquo;collects phone
          numbers&rdquo; or &ldquo;takes card payments&rdquo;, and the countries
          involved, like &ldquo;LK&rdquo;.
        </p>
        <p>
          That&apos;s all Rulewise gets. No description of your idea, no code,
          no names, no files.
        </p>
        <p>
          Your AI tool itself does see your idea, of course. What happens there
          is covered by that tool&apos;s own privacy policy, not this one.
        </p>
      </Section>

      <Section title="What I keep: nothing">
        <p>
          Rulewise doesn&apos;t save the facts it receives or the warnings it
          sends back. There are no accounts, no sign-ups and no history.
        </p>
        <p>
          The server log only holds counts, like &ldquo;9 facts, 20
          warnings&rdquo;, and error messages when something breaks. I turned
          off the usual web logs on purpose, because they would record your IP
          address.
        </p>
        <p>
          To stop one person from overloading the server, it counts how many
          requests come from each address in the last minute. That count is kept
          only in memory, cleared within a few minutes, and never written down.
        </p>
      </Section>

      <Section title="This website">
        <p>
          No cookies, no analytics, no tracking pixels, no ads. The fonts are
          served from this site, so your browser doesn&apos;t contact Google or
          anyone else when you visit.
        </p>
      </Section>

      <Section title="Where it runs">
        <p>
          The Rulewise server runs on Microsoft Azure in India. This website
          runs on Vercel. Like any hosting company, they handle the network
          traffic, and they may keep basic technical records for security and to
          keep things running. I don&apos;t use those records to track anyone.
        </p>
      </Section>

      <Section title="This is not legal advice">
        <p>
          Rulewise points out laws you may need to think about. It is not a
          lawyer, and it can&apos;t tell you that your product is legal. A short
          list of warnings doesn&apos;t mean you&apos;re in the clear, only that
          nothing came up in the areas Rulewise covers today.
        </p>
        <p>
          It covers Sri Lankan law only, and only some areas of it. Each result
          lists what isn&apos;t covered. Most rules are still drafts that a
          lawyer hasn&apos;t reviewed yet, and laws change. I check the sources
          and quote them word for word, but I can still get things wrong.
        </p>
        <p>
          So please use Rulewise as a starting point, and talk to a Sri Lankan
          lawyer before you make a real decision. Each warning comes with
          questions you can take to them.
        </p>
      </Section>

      <Section title="Using it">
        <p>
          Rulewise is free to use while it&apos;s in beta. Please don&apos;t try
          to overload it or use it to get around a law. It explains the law and
          the risk instead of helping anyone avoid it.
        </p>
        <p>
          I may change how it works, or stop running it. If this page changes,
          the date at the top will change too.
        </p>
      </Section>

      <Section title="Questions or a mistake?">
        <p>
          If you spot a wrong rule, a broken link or anything on this page that
          worries you, please{" "}
          <a
            href={ISSUES}
            className="text-orange-deep underline underline-offset-2"
          >
            open an issue on GitHub
          </a>
          . I read every one.
        </p>
      </Section>
    </article>
  );
}
