import { defineConfig, devices } from "@playwright/test";

// Needs both servers running (see README): the Python API and `npm run dev`.
export default defineConfig({
  testDir: "e2e",
  outputDir: "test-results",
  use: { baseURL: process.env.BASE_URL ?? "http://127.0.0.1:3100" },
  projects: [
    { name: "desktop", use: { ...devices["Desktop Chrome"], viewport: { width: 1360, height: 900 } } },
    { name: "mobile", use: { ...devices["Pixel 7"] } },
  ],
});
