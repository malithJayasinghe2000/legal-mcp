import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Logo } from "@/components/logo";

const NAV = [
  { href: "/#how", label: "How it works" },
  { href: "/#coverage", label: "What it covers" },
  { href: "/#claude-code", label: "Use in Claude Code" },
];

export function SiteHeader() {
  return (
    <header className="no-print border-b border-rule bg-paper">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between gap-6 px-4 sm:px-6">
        <Logo />
        <nav aria-label="Main" className="hidden items-center gap-7 text-sm md:flex">
          {NAV.map((item) => (
            <Link key={item.href} href={item.href} className="text-ink-muted no-underline hover:text-ink">
              {item.label}
            </Link>
          ))}
        </nav>
        <Button asChild size="lg" className="h-10 px-4 text-sm font-semibold">
          <Link href="/check">Check my product</Link>
        </Button>
      </div>
    </header>
  );
}
