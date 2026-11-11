import { Logo } from "@/components/logo";

export function SiteFooter() {
  return (
    <footer className="border-t border-rule bg-paper">
      <div className="mx-auto grid max-w-6xl gap-6 px-4 py-10 text-sm text-ink-muted sm:px-6 md:grid-cols-[1fr_2fr]">
        <div className="no-print">
          <Logo />
        </div>
        <div className="max-w-prose space-y-2">
          <p>
            Rulewise gives legal information to help you spot issues. It is not legal advice and
            does not make your product compliant. Ask a Sri Lankan lawyer before you decide.
          </p>
          <p>
            Covers Sri Lankan law only. Rules marked draft are not yet reviewed by a lawyer. We
            store nothing you enter.
          </p>
        </div>
      </div>
    </footer>
  );
}
