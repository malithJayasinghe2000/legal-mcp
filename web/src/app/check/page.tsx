import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { Checker } from "@/components/checker/checker";
import { SHOW_SITE_CHECK } from "@/lib/features";

export const metadata: Metadata = { title: "Check your product" };

export default function CheckPage() {
  if (!SHOW_SITE_CHECK) notFound(); // hidden for now (D21), not deleted
  return (
    <div className="mx-auto max-w-6xl px-4 py-12 sm:px-6 md:py-16">
      <Checker />
    </div>
  );
}
