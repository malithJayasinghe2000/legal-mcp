import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Logo } from "@/components/logo";
import { SHOW_SITE_CHECK } from "@/lib/features";

const NAV = SHOW_SITE_CHECK
  ? [
      { href: "/#how", label: "How it works" },
      { href: "/#coverage", label: "What it covers" },
      { href: "/#setup", label: "Set it up" },
    ]
  : [
      { href: "/#pdpa", label: "PDPA checklist" },
      { href: "/#how", label: "How to use it" },
      { href: "/#coverage", label: "What it covers" },
      { href: "/#setup", label: "Set it up" },
    ];

export function SiteHeader() {
  return (
    <header className="no-print border-b border-rule bg-paper">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between gap-6 px-4 sm:px-6">
        <Logo />
        <nav
          aria-label="Main"
          className="hidden items-center gap-7 text-sm md:flex"
        >
          {NAV.map((item) => (
            <a
              key={item.href}
              href={item.href}
              className="text-ink-muted no-underline hover:text-ink"
            >
              {item.label}
            </a>
          ))}
        </nav>
        <Button asChild size="lg" className="h-10 px-4 text-sm font-semibold">
          {SHOW_SITE_CHECK ? (
            <Link href="/check">Check my product</Link>
          ) : (
            // Plain <a> on purpose: next/link ignores a repeat click on the same #hash.
            // eslint-disable-next-line @next/next/no-html-link-for-pages
            <a href="/#setup">Add to your AI tool</a>
          )}
        </Button>
      </div>
    </header>
  );
}
