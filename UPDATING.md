# Updating the Stoddard Lab Funding Finder

The catalog goes stale fast: deadlines move, programs pause, and pages change. This is the routine that keeps it honest.

## Principles
1. **The funder's own page is the only source of truth.** Aggregators (grant-listing sites, search snippets, university advising pages) can point you to a program but never confirm a date. If you could only reach a secondary source, set `unv` to say exactly what is unconfirmed. Remove `unv` only after reading the funder's page.
2. **Never guess a date.** If the next cycle isn't posted, set `s: "watch"`, `d: null`, and say in `dt` what the last cycle was. The build already moves any passed deadline to Watch.
3. **Record what you checked.** Set `checked` to today's date on every row you re-read, even if nothing changed.
4. **Fit before volume.** A row belongs only if someone in the lab could realistically apply. Put eligibility restrictions (membership, citizenship, career stage, host country) in `e` and the matching flags (`us`, `nom`).

## Cadence
| When | What | Who |
|---|---|---|
| Every Monday | Open the auto-created **Weekly recheck** issue (made by `.github/workflows/check.yml`, built by `engine/recheck_report.py`). Work through its four lists: deadlines in the next 60 days, passed deadlines, unconfirmed rows, rows not checked in 30 days. Tick items off as you commit. | Rotating lab member (about 30 minutes) |
| Weekly | Triage open `suggestion` issues: verify on the funder's page, add or correct the row, close the issue from the commit. | Same person |
| Monthly (first week) | **Discovery sweep**: search for new programs, using the source list below. Add anything that fits. | Same person |
| Quarterly (Jan, Apr, Jul, Oct) | **Cycle sweep**: re-read every `watch` row. Most annual programs post their next call 3 to 6 months ahead. Also re-check each Princeton page and the SAFE portal for changed amounts. | Lab manager or a postdoc |
| Each August and January | Roll the annual calendar below forward and update `notes.json` ("What's changed"). | PI or postdoc |

## How to recheck one row
1. Open the row's `u` link. If it 404s or redirects, find the program's new page and update `u`.
2. Read: status (still exists, paused, discontinued?), amount, next deadline with its year, eligibility, membership or citizenship rules.
3. Edit the row in `catalog/programs/*.json`: set `s`, `d`, `dt`, `a`, `e`, `checked`. Keep `dt` plain: say what the page says, including the year.
4. If the page says "closed" with no next date: `s: "watch"`, `d: null`.
5. If the funder's site blocks you, search for the same facts in a second place that cites the funder (a university research office page works), and keep `unv` set.
6. Run `python3 engine/build.py` and commit `index.html`, `data/programs.json` and the catalog change together. GitHub Actions fails the commit if `index.html` is out of date.

## Where to look for new programs (monthly sweep)
- **Ornithology and evolution societies:** AOS, WOS, Cooper, BOU, SSE, SSB, ABS, ESA, SICB, Linnean Society.
- **Museums:** AMNH Chapman, Smithsonian (SIFP, STRI), Field Museum, Carnegie, Burke, MCZ, Florida Museum, LSU, Natural History Museum London (SYNTHESYS).
- **Federal:** NSF BIO (PRFB, GRFP, core programs), NIH F and K awards, NEI.
- **Foundations:** HHMI, Simons, Packard, Sloan, Templeton, HFSP, EMBO, LSRF, Company of Biologists.
- **Field-work awards:** Explorers Club, National Geographic (now request-for-proposal only).
- **Princeton:** Graduate School SAFE portal, Dean for Research, High Meadows Environmental Institute, EEB department, Office of the Dean of the Faculty (postdocs).
- **Tools:** a saved search per funder name plus "grant 2027"; the Yale finder's `catalog/programs` for new general programs; the SAFE portal's fund list.

## Annual calendar (recurring cycles to expect)
Verify each against the funder's page before relying on it; these are the pattern, not the dates.
- **Jan to Feb:** AMNH Collection and Chapman rounds, Company of Biologists (Feb), EMBO (Jan), AOS awards open, HHMI Gilliam.
- **Mar to May:** Sigma Xi (Mar 15), SSE graduate grants (May), AOS decisions (May 1), NSF CAREER prep (July due).
- **Jun to Aug:** NSF PRFB prep (Sept due), HFSP calls open, LSRF opens, Simons graduate fellowship letter of intent (Jun).
- **Sep to Dec:** NSF PRFB (4th Tuesday of Sept), NSF GRFP (Oct), Smithsonian (Oct 15), BOU (Oct 30), AMNH Chapman (Nov 30), ABS (Dec 15), HHMI Hanna Gray (Dec in some years), NIH F32 (Dec 8).

## Row hygiene
- One program per row; separate rows when a program has tiers with different eligibility (for example SSE Lewontin and Rosemary Grant).
- Use stable ids (`aos-kessel-fellowships`). Never reuse an id for a different program. Princeton-only rows start `princeton-` and may carry a `pu` step (`{d, t, u}`) for internal deadlines.
- Remove a row only when the program is confirmed discontinued; say so in `notes.json` ("What's changed") so people know it wasn't just missed.

## Quality checks before pushing
- `python3 engine/build.py --check` passes with no `note:` lines you don't understand.
- No row has `s: "open"` without a future date.
- Every `u` is an `https://` link to the funder (not an aggregator).
- New `unv` text says what to confirm, not just "unverified".

## Ideas to automate further
- A scheduled Claude task each Monday that runs `engine/recheck_report.py`, reads the funder pages, drafts the edits and opens a pull request for a human to review. Keep a human in the loop for any change to a date.
- A link checker in `check.yml` for the `u` URLs (many funder sites block bots, so treat failures as prompts to look, not errors).
