import Link from "next/link";

/** Wordmark with an orange margin rule: the "marginal note" device from the report. */
export function Logo() {
  return (
    <Link href="/" className="group inline-flex items-center gap-2.5 text-ink no-underline">
      <span aria-hidden className="h-6 w-1.5 rounded-sm bg-orange" />
      <span className="text-lg font-semibold tracking-tight">Rulewise</span>
    </Link>
  );
}
