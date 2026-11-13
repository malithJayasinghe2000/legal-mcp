# Legal Landscape

Research notes from 2026-11-11. **These are starting points, not rules.** Several
dates come from news sites and trackers that disagree with each other. Confirm
every item against the official text before it becomes a rule.

## Sri Lanka - verified for the first 5 areas (2026-11-11)

Checked by downloading the official copy and reading the title page.
Links and details: [sources/sources.yaml](../sources/sources.yaml).

| Area | Law (verified name and number) | What we found |
|---|---|---|
| Personal data | Personal Data Protection Act, No. 9 of 2022 | Certified 19 March 2022. **s.2(1)** applies when processing is in Sri Lanka, or the company is incorporated / domiciled / resident in Sri Lanka, or it targets or monitors people in Sri Lanka. Key sections for rules: s.18-19 automated decisions, s.20 Data Protection Officer, s.23 data breach, s.24 impact assessment (incl. profiling), s.26 cross-border transfer, s.27 direct marketing. |
| Personal data | Personal Data Protection (Amendment) Act, No. 22 of 2025 | Certified 30 October 2025. Start dates are now set by **the Minister** by Gazette order (not fixed dates). Check whether it changed the sections above. |
| Personal data | Commencement order, Gazette Extraordinary No. 2498/16 (22 July 2026) | **Verified** (dpa.gov.lk copy): s.2, s.3, Part I and Part III start **1 January 2027**. Order by the President as Minister of Digital Economy, 13 July 2026. Part II (rights), Part IV (marketing), Part VII (penalties) still have no date. |
| Payments | Payment and Settlement Systems Act, No. 28 of 2005 | Certified 20 September 2005 (CBSL copy). **No amendments** (Parliament's acts listing, checked by script). Parliament lists it as "Payments and Settlement Systems". |
| Payments | Payment Cards and Mobile Payment Systems Regulations No. 1 of 2013 | Gazette Extraordinary No. 1813/25 of 7 June 2013, under the Act above. |
| Payments | Money or Value Transfer Service Providers Regulations No. 1 of 2024 | Gazette Extraordinary No. 2382/11 of 30 April 2024. Reg 4: Central Bank registration needed. |
| Payments | Money or Value Transfer Service Providers Regulations No. 01 of 2025 | Gazette Extraordinary No. 2468/06 of 23 December 2025. **Amends the 2024 Regulations** from 31 December 2025 (definition, eligibility: Rs. 15m capital). |
| Payments | Central Bank Direction No. 01/2018 (e-commerce card acquiring through service providers) | Scanned PDF; typed copy in `sources/transcripts/`. Gateways must not access card number, CVV, expiry (para 2.4). |
| AI | (no AI law) | Covered through the PDPA (s.18 automated decisions, s.24 profiling), professional rules and the Online Safety Act. |
| Online content | Online Safety Act, No. 9 of 2024 | Certified 1 February 2024. Still in force. The Online Safety (Repeal) Bill is "pending for 2nd reading" (Parliament page). The 2024 amendment bill also not passed. |
| Lawyers | Supreme Court (Conduct of and Etiquette for Attorneys-at-Law) Rules, 1988, Gazette Extraordinary No. 535/7 of 07.12.1988 | Official copy on supremecourt.lk (blocks scripts; downloaded by hand). Rule 39 touting (incl. paying for clients, advertising to unfairly attract clients), Rules 40/45 directories, Rule 49 practice particulars. **No separate fee-sharing rule.** |
| Lawyers | Intermeddlers with Suitors Ordinance, **Cap. 40, Ordinances Nos. 11 of 1894 and 35 of 1917** | Both earlier names were right ("No. 11 of 1894" and "Cap. 40"). **s.2(c)**: a person not authorised to practise who takes payment for procuring a lawyer's employment commits an offence. Official CommonLII copy (1980 Revised Edition, downloaded by hand) confirms. **s.2(a)**: receiving payment from a lawyer for procuring clients is an offence; fine up to Rs. 500 in the 1980 text. |
| Lawyers | BASL cautionary note (June 2021) | **No official copy found.** Only a news report (counterpoint.lk, 15 Sep 2021) quoting it: legal advice through non-lawyer online platforms "constitutes the act and conduct of touting, which is unlawful". |
| Doctors | Medical Ordinance (Chapter 105) | SLMC consolidated copy, includes amendments up to No. 28 of 2018 (checked). Parliament lists 18 amending Acts 1949-2024. |
| Doctors | Medical (Amendment) Act, No. 46 of 2024 | **New, wasn't in our list.** Certified 15 August 2024. |
| Doctors | SLMC Guidelines on Ethical Conduct (July 2009); SLMC Instructions on Serious Professional Misconduct (July 2009) | Advertising and canvassing are misconduct. SLMC also has newer Social Media Guidelines (web page only). |

Note: documents.gov.lk (Government Printer) was rebuilt and its old PDF links
return 404, so we use Parliament and regulator copies instead.

## Sri Lanka - laws to collect (later areas)

Candidate list for the rule library. Act numbers and years are from memory unless
marked; **verify each one** on the official source before use.

| Area | Law / source | Notes |
|---|---|---|
| Personal data | Personal Data Protection Act No. 9 of 2022 (+ amendments) | Core parts brought into force by commencement order, Gazette 2498/16. Sources disagree on the date (July 2026 vs January 2027). Check the Gazette. No AI-specific clauses, but covers profiling of people in Sri Lanka. |
| Online content | Online Safety Act No. 9 of 2024 | Platforms, user-generated content, takedowns |
| Electronic contracts | Electronic Transactions Act No. 19 of 2006 (amended by No. 25 of 2017) | E-signatures, online contracts, AI agents. **Rules written 2026-11-12** (`rules/e-commerce/`) |
| Cybercrime | Computer Crime Act No. 24 of 2007 | Scraping, leaked data, interception. **Rules written 2026-11-13** (`rules/cybercrime/`) |
| Cyber security | Cyber Security Bill | **Pending**. Track as "coming law" |
| Payments | Payment and Settlement Systems Act No. 28 of 2005; Central Bank directions on payment cards / mobile payments | Wallets, payment apps |
| Payment fraud | Payment Devices Frauds Act No. 30 of 2006 | |
| Lending / finance | Banking Act, Finance Business Act; Central Bank directions | Lending apps, holding money |
| Foreign exchange | Foreign Exchange Act No. 12 of 2017 | Foreign payments, crypto |
| Crypto | Central Bank public warnings on virtual currencies; proposed Virtual Asset Service Providers Bill | |
| Consumer | Consumer Affairs Authority Act No. 9 of 2003 (amended by No. 20 of 2021, penalties only) | Misleading claims, pricing. **Rules written 2026-11-12** (`rules/consumer/`) |
| Copyright / IP | Intellectual Property Act No. 36 of 2003 | Training data, content ownership |
| Telecom | Sri Lanka Telecommunications Act No. 25 of 1991 | SMS, calls, telecom services |
| Lawyers | Supreme Court (Conduct of and Etiquette for Attorneys-at-Law) Rules 1988 (Gazette 535/7): Rules 39, 40, 45, 49; Intermeddlers with Suitors Ordinance (Cap. 40) s.2; BASL note June 2021 | Already researched in law-finder (`law-finder/lawyer-finder-web/docs/`) |
| Doctors / health | Medical Ordinance; Sri Lanka Medical Council rules | Advertising, telemedicine |
| Education / universities | UGC National AI Policy Framework for State Universities (2026) | Policy, not law. Four AI risk tiers. |
| Employment | Shop and Office Employees Act; others | Later |
| Children | Children and Young Persons Ordinance; others | Later |
| Gambling | Casino Business (Regulation) Act; betting laws | Later |
| Tax | Inland Revenue Act; VAT on digital services | Later |

**Sri Lanka has no AI-specific law (as of 2026-11-11).** AI is covered indirectly
by the data protection, consumer, online safety and professional rules.

Sources: theleveragedyears.com (PDPA commencement, Gazette 2498/16),
govinfo.lk (UGC AI framework 2026), sundaytimes.lk (AI in Sri Lanka, Feb 2026),
lankanewspapers.com and cpalanka.org (AI-assisted law drafting, VASP Bill).

## AI laws around the world

### European Union - EU AI Act (strictest)
Risk-based:
- **Banned**: social scoring, manipulative AI, some face recognition.
- **High risk** (jobs, loans, education, health, justice): testing,
  documentation, human oversight. The **Digital Omnibus** (Regulation (EU)
  2026/1744, in force 27 July 2026) moved this to **2 December 2027**, and to
  **2 August 2028** for AI built into regulated products. It delays these rules; it
  doesn't remove them.
- **Already applying**: bans, AI literacy duty, general-purpose model rules, and
  transparency (Article 50: chatbots must say they are AI, AI content labelled).

**Applies outside Europe** when the system is offered to EU users or its output
is used in the EU. GDPR works the same way.
Sources: gibsondunn.com, orrick.com, freshfields.com, artificialintelligenceact.eu (Digital Omnibus).

### South Korea - AI Basic Act
In force since 22 January 2026. Users must be told when AI is involved, and
generated content must be marked. Fines reportedly deferred for at least a year.
Sources: archibal.ai, casrai.org.

### China
AI-generated content labelling (visible labels + machine-readable marks) since September 2025.
Sources: ai-label.app, numonic.ai.

### Japan
AI Promotion Act (2025): mostly guidance, no fines. *(From memory, not this search.)*

### United States - no national law, state by state
- **California**: SB 53 (frontier model transparency), SB 942 AI Transparency Act
  (labelling, reportedly delayed to 2 August 2026, possibly changed by SB 1000).
- **Texas**: TRAIGA (HB 149), in force 1 January 2026. Bans certain harmful uses.
- **Colorado**: AI / automated decision law. **Sources disagree on the date** (June
  30, 2026 for SB 24-205 vs 1 January 2027 for SB 26-189). Check before use.
Sources: casrai.org, steg.ai, thebriefscript.com, numonic.ai.

### Worldwide (no single world AI law)
- **Council of Europe Framework Convention on AI (2024)**: the only binding treaty.
  Binds governments that ratify it, not companies directly. Sri Lanka has not
  signed, as far as known. *(From memory, so ratification status may have changed.)*
- **UNESCO Recommendation on the Ethics of AI (2021)**: all members, Sri Lanka included. Not binding.
- **OECD AI Principles**: around 50 countries. Not binding.
- **UN General Assembly AI resolutions (2024)**: not binding.
- **G7 Hiroshima Code of Conduct**: voluntary, for advanced AI developers.
- **Standards clients ask for**: ISO/IEC 42001 (AI management system,
  certifiable), NIST AI Risk Management Framework.

### Laws that aren't "AI laws" but apply to AI
Data protection (GDPR, Sri Lanka PDPA), copyright (training data, output
ownership), consumer protection (misleading AI claims), professional rules (AI
giving legal or medical advice; this is what hit law-finder).
