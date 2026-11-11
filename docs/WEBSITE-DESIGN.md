# Rulewise website - design plan

Decisions behind it: brief D17 (guided questions), D18 (light base, orange), D19 (stack).
Made with the `frontend-design` skill (plan, review against the brief, then build).

## Brief
- **Subject:** a tool that shows software builders which Sri Lankan laws apply before they build.
- **Audience:** developers, students, startup founders. Many read English as a second
  language, so copy is plain and short.
- **Primary job:** answer short questions, get a clear report: Must items first, each with
  the law and section, what to do, and what to ask a lawyer.

## The one memorable thing: the marginal note
Sri Lankan Acts are printed with **marginal notes**: a short heading beside each section
("Application of the Act", "Right to erasure"). The report borrows this. Each warning is
laid out like a section of an Act: the **law citation sits in the left margin** (Act, section),
the plain-language duty in the main column. Law quotes are set in a serif, like the printed
Act. On phones the margin note moves above the text. Everything else stays quiet.

## Tokens
| Name | Value | Use |
|---|---|---|
| Paper | `#F7F7F4` | page background (cool off-white, not cream) |
| Surface | `#FFFFFF` | inputs, the report sheet |
| Ink | `#1A1F2B` | text (15.4:1 on paper) |
| Muted ink | `#5B6170` | secondary text (5.8:1) |
| Rule | `#E2E3DF` | lines and borders |
| Signature orange | `#F57E22` | primary buttons (with **ink** text, 6.2:1), focus ring, the logo mark |
| Deep orange | `#B54A00` | orange text and links (5.0:1); orange text is never `#F57E22` |
| Must | `#B42318` | severity, with label + filled square marker |
| Should | `#1F5FA6` | severity, with label + half-filled marker |
| Check with a lawyer | `#6B3FB5` | severity, with label + ring marker |

Severity never relies on colour alone: every item shows its label and a marker shape.

**Type.** Space Grotesk (the fiveneurals face) for interface and headings; Source Serif 4
for law quotes and marginal notes. Scale 1.25: 14 / 16 / 20 / 25 / 31 / 39 / 49 px. Body 16-17
px, line length under 72 characters. Sentence case everywhere; no all-caps labels.

**Layout.** Left-aligned. Wizard: step list on the left (the sections really are a sequence,
so they are numbered), one section of questions on the right; on phones the steps collapse
to "Step 2 of 6" and Back/Next stick to the bottom. Report: a white sheet with a 13rem margin
column for citations.

**Motion.** One moment only: when the report appears, the severity summary counts in.
Everything else is instant. `prefers-reduced-motion` turns it off.

## Avoided on purpose (generic tells)
Gradient hero, identical rounded feature cards with icons, all-caps eyebrow labels, arrows
appended to buttons, middle-dot meta strings, long dashes (also a project rule: use "-").

## Privacy in the interface
No analytics, no cookies, no local storage of answers. Fonts self-hosted by next/font
(no requests to Google). Answers live only in the open tab and go to `/api/check`, which
stores nothing (brief D6).
