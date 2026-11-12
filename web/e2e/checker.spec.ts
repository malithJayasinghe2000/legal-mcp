import AxeBuilder from "@axe-core/playwright";
import { expect, type Page, test } from "@playwright/test";
import { SHOW_SITE_CHECK } from "../src/lib/features";

const shot = (page: Page, name: string) =>
  page.screenshot({
    path: `test-results/screens/${test.info().project.name}-${name}.png`,
    fullPage: true,
  });

async function noA11yViolations(page: Page) {
  const results = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
    .analyze();
  expect(results.violations.map((v) => `${v.id}: ${v.help}`)).toEqual([]);
}

test("home page", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(
    "Know the law before you build.",
  );
  await expect(page.getByText(/online shop app/)).toBeVisible();
  await expect(page.getByText(/lawyer-finding|Attorneys-at-Law/)).toHaveCount(
    0,
  );
  await shot(page, "home");
  await noA11yViolations(page);
});

test("setup shows each AI tool", async ({ page }) => {
  await page.goto("/");
  const tabs = page.getByRole("tablist", { name: "AI tool" });
  await tabs.getByRole("tab", { name: "Cursor" }).click();
  await expect(page.getByLabel("Cursor setup")).toContainText('"mcpServers"');
  await tabs.getByRole("tab", { name: "Codex" }).click();
  await expect(page.getByLabel("Codex setup")).toContainText(
    "[mcp_servers.rulewise]",
  );
  await noA11yViolations(page);
});

test("the site check is hidden while switched off", async ({ page }) => {
  test.skip(SHOW_SITE_CHECK, "site check is on");
  const res = await page.goto("/check");
  expect(res?.status()).toBe(404);
  await page.goto("/");
  await expect(page.locator('a[href="/check"]')).toHaveCount(0);
});

// The tests below cover the site check; they run only when SHOW_SITE_CHECK is on.
test.describe(() => {
  test.skip(!SHOW_SITE_CHECK, "site check is hidden (D21)");

  async function answerYesNo(
    page: Page,
    question: string,
    answer: "Yes" | "No",
  ) {
    await page
      .getByRole("radiogroup", { name: question })
      .getByText(answer, { exact: true })
      .click();
  }

  test("doctor booking app: full flow to the report", async ({ page }) => {
    await page.goto("/check");
    await expect(
      page.getByRole("heading", { level: 1, name: "Where" }),
    ).toBeVisible();
    await shot(page, "step1");

    // Next without answering shows a clear error, not a silent skip.
    await page.getByRole("button", { name: "Next", exact: true }).click();
    await expect(page.getByText("Choose yes or no.")).toBeVisible();

    await answerYesNo(
      page,
      "Are you building or running this for a client who decides how the data is used?",
      "No",
    );
    await page.getByRole("button", { name: "Next", exact: true }).click();

    await answerYesNo(
      page,
      "Does the product collect or use information about people?",
      "Yes",
    );
    await page.getByText("Health or medical information").click();
    await page
      .getByText("Contact details (name, email, phone, address)")
      .click();
    await answerYesNo(
      page,
      "Could any users, or people whose data you hold, be under 16?",
      "No",
    );
    await shot(page, "step2");
    await noA11yViolations(page);
    await page.getByRole("button", { name: "Next", exact: true }).click();

    await page.getByText("Users pay us online").click();
    await page.getByRole("button", { name: "Next", exact: true }).click();
    await page.getByRole("button", { name: "Next", exact: true }).click(); // AI: none
    await answerYesNo(
      page,
      "Can users post things that others see (posts, comments, reviews, group chats, uploads)?",
      "No",
    );
    await page.getByRole("button", { name: "Next", exact: true }).click();

    await page.getByText("Doctors or dentists").click();
    await page
      .getByText("They pay us per client, booking, lead, enquiry or message")
      .click();
    await page.getByRole("button", { name: "Show my report" }).click();

    await expect(
      page.getByRole("heading", { level: 1, name: "Your report" }),
    ).toBeVisible();
    await expect(
      page.getByRole("heading", {
        name: "Don't charge doctors per patient or booking",
      }),
    ).toBeVisible();
    await expect(
      page.getByRole("heading", { name: /Sensitive data/ }),
    ).toBeVisible();

    // Proof: the exact law text and its official link.
    const section = page.getByRole("region", {
      name: "Don't charge doctors per patient or booking",
    });
    await section.getByRole("button", { name: "Read the law" }).click();
    await expect(section.getByText(/commission or bonus/)).toBeVisible();
    await shot(page, "report");
    await noA11yViolations(page);

    // Mark as done: the item moves to the done list with what to double-check.
    await page
      .getByRole("region", {
        name: "Tell users what you collect and why (privacy notice)",
      })
      .getByRole("button", { name: "Mark as done" })
      .click();
    await expect(
      page.getByRole("heading", { name: "Marked done by you" }),
    ).toBeVisible();
    await expect(
      page.getByText(/covers every item in Schedule V/),
    ).toBeVisible();
  });

  test("a failed check shows an error, never 'no issues'", async ({ page }) => {
    await page.route("**/api/check", (route) =>
      route.fulfill({
        status: 503,
        contentType: "application/json",
        body: JSON.stringify({
          error: "The rule library could not be loaded.",
        }),
      }),
    );
    const next = page.getByRole("button", { name: "Next", exact: true });
    await page.goto("/check");
    await answerYesNo(
      page,
      "Are you building or running this for a client who decides how the data is used?",
      "No",
    );
    await next.click();
    await answerYesNo(
      page,
      "Does the product collect or use information about people?",
      "No",
    );
    await next.click();
    await next.click(); // money: none
    await next.click(); // AI: none
    await answerYesNo(
      page,
      "Can users post things that others see (posts, comments, reviews, group chats, uploads)?",
      "No",
    );
    await next.click();
    await page.getByRole("button", { name: "Show my report" }).click();
    await expect(
      page.getByRole("alert").filter({ hasText: "The check did not run" }),
    ).toBeVisible();
    await expect(page.getByText("No issues found")).toHaveCount(0);
  });
});
