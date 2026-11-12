import type { Metadata } from "next";
import { Source_Serif_4, Space_Grotesk } from "next/font/google";
import { SiteFooter } from "@/components/site-footer";
import { SiteHeader } from "@/components/site-header";
import "./globals.css";

// next/font self-hosts these: visitors never send a request to Google.
const grotesk = Space_Grotesk({ variable: "--font-grotesk", subsets: ["latin"] });
const serif = Source_Serif_4({
  variable: "--font-serif-law",
  subsets: ["latin"],
  style: ["normal", "italic"],
});

export const metadata: Metadata = {
  title: { default: "Rulewise - know the law before you build", template: "%s - Rulewise" },
  description:
    "Rulewise works inside your AI coding tool. While you plan a product, it shows which Sri Lankan laws apply, how serious each one is, and what to ask a lawyer.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={`${grotesk.variable} ${serif.variable} h-full`}>
      <body className="flex min-h-full flex-col">
        <a
          href="#main"
          className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:rounded-md focus:bg-surface focus:px-4 focus:py-2"
        >
          Skip to content
        </a>
        <SiteHeader />
        <main id="main" className="flex-1">
          {children}
        </main>
        <SiteFooter />
      </body>
    </html>
  );
}
