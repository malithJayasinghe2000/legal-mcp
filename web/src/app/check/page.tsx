import type { Metadata } from "next";
import { Checker } from "@/components/checker/checker";

export const metadata: Metadata = { title: "Check your product" };

export default function CheckPage() {
  return (
    <div className="mx-auto max-w-6xl px-4 py-12 sm:px-6 md:py-16">
      <Checker />
    </div>
  );
}
