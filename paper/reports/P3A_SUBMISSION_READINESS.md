# P3A — Paper Draft and Submission Readiness

Date: 2026-11-08. Deadline per secondary sources: 2026-11-12 (**unconfirmed on the official page**; see §5). Work done in `paper\` only. No inference, GPU, downloads of software/models/data, paid API, Git, or Kaggle submission. Web reads were limited to citation/rule verification (searches plus two page fetches). P2A/P2B/P2C evidence untouched (hashes re-checked, §1).

**Deliverables:** `drafts\GEMMA4_PAPER_DRAFT_V1.md` (this phase), this report. Analysis scratch scripts were written to the session scratchpad outside the project; nothing else was created or modified.

## 1. Evidence completeness

| Check | Result |
|---|---|
| Freeze intact | `freeze.py --check FREEZE.sha256` → **UNCHANGED since freeze** (19 files; `FREEZE.sha256` SHA-256 `5f3095c1…fbe35`). Freeze time 2026-11-07T23:03:43Z precedes first main-run row (23:04:13Z) and last (23:22:02Z). Self-attested only. |
| Result files | `main_seed1\results.jsonl` 24 rows, SHA-256 `56a7f4ab…48eb`; `pilot_p2b\results.jsonl` 4 rows, `c4b63098…d25e`. Both match P2B/P2C. 24 and 4 traces present. All rows `is_mock=false`, 0 errors. |
| Totals recomputed independently from rows | Arm 1 **0/12**, arm 2 **1/12** (`find_in_sorted`, AST-equal). Submitted 5/2; end reasons 5 submitted + 6 max_turns + 1 format_abort / 2 submitted + 10 max_turns; format errors 5/0; edits 24/43, rejected 15/31; tokens 145,249/6,544 vs 187,721/6,884; wall 519 s/576 s. **All match P2C.** `harness.summarize` (read-only) gives +8.3 pp, bootstrap 95% CI [0.0, +25.0]. |
| Pilot vs main | 3/4 identical (patch, turns, prompt tokens); `flatten`/arm 2 differs (pilot resolved, 6 turns; main unresolved, 10 turns). |
| Protocol copies | `methodology\EXPERIMENTAL_PROTOCOL.md` is byte-identical to the frozen `docs\` copy; both still say T=0.7 (actual: 1.0). |

**Completeness verdict:** complete for a descriptive single-seed pilot paper. Not complete for any comparative claim (§4).

### New findings from this phase (all from saved traces; not previously in P2C)

1. **Source of the one non-reproduced run.** The first prompt of `flatten`/arm 2 differs between pilot and main only in process-specific memory addresses (`0x000001C4…` vs `0x000001D4…`) inside the harness-injected failure message (a generator `repr`). Only this run among the 24 contains such addresses. So "same seed" did not mean "same prompt". This is a harness-level source of nondeterminism and supersedes P2C's "cause not investigated". It is a *demonstrated prompt difference*, not a proven cause of the divergent trajectory.
2. **Edit failures are mostly whitespace.** Of 41 "matched 0 times" calls, 39 match the file once whitespace is collapsed; 2 contain text absent from the file. 35 of the 41 are repeats of a string the model had already sent in the same run. (Whitespace-collapsed matching is permissive; it shows the content was *present*, not that a corrected edit would have been right.)
3. **Arithmetic slip in P2C.** P2C says "41 of 47 error messages"; the rows give 46 rejected edits (15 + 31): 41 no-match + 4 syntax + 1 malformed. The draft uses 46. P2C is preserved unedited.
4. **Statistics added** (arithmetic on saved data): Clopper–Pearson 95% for 0/12 = 0–26.5%, for 1/12 = 0.2–38.5%; exact two-sided sign/McNemar test with 1 discordant pair p = 1.0. These were not run by the harness; labelled as such in the draft.
5. **Regression counts verified:** final state worse than the buggy baseline in 3 arm-1 runs and 2 arm-2 runs; better in 1 (arm 2). Both arms made the identical `quicksort` edit taking failures 1/13 → 13/13.
6. **Pilot tasks overlap the main set** (first two manifest tasks), and the `--reasoning off` and T=1.0 decisions followed the pilot. Disclosed in the draft's limitations.

## 2. Draft word count

Counted on `GEMMA4_PAPER_DRAFT_V1.md` with the draft-status HTML comment removed (it holds only status notes):

| Convention | Words |
|---|---:|
| Everything, whitespace tokens (table pipes counted) | 2,519 |
| Everything, table pipes/separators removed | 2,401 |
| Body incl. tables, excluding references | 2,222 |
| References | 179 |
| Abstract | 210 |

The draft is under 3,000 words under every convention, so it is safe if the (unverified) 3,000-word figure applies and the count includes tables and references. The abstract is 210 words (outline budgeted 200); trim if a separate abstract limit exists.

## 3. Citations

| # | Reference | Status | Evidence |
|---|---|---|---|
| 1 | Chen, Lin, Schärli, Zhou — Self-Debug, arXiv:2304.05128 | **VERIFIED** | arXiv/HF listing: authors, ID, dates (v1 11 Apr 2023, v2 5 Oct 2023). Author order is as on arXiv (an aggregator BibTeX with Zhou first is wrong). Venue: arXiv only; I did not find/claim a conference venue. |
| 2 | Shinn et al. — Reflexion, NeurIPS 2023, arXiv:2303.11366 | **VERIFIED** | arXiv and NeurIPS listings; six authors confirmed. |
| 3 | Olausson et al. — Self-Repair, ICLR 2024, arXiv:2306.09896 | **VERIFIED** | ICLR proceedings page, arXiv. Five authors confirmed. |
| 4 | Yang et al. — SWE-agent, NeurIPS 2024, arXiv:2405.15793 | **VERIFIED** | NeurIPS proceedings page, arXiv. Seven authors confirmed. |
| 5 | Xia et al. — Agentless, arXiv:2407.01489 | **VERIFIED** | arXiv listing; authors Xia, Deng, Dunn, Zhang. Preprint only (v2 29 Oct 2024); I did not claim a venue. |
| 6 | Toeda — Scaffolding Helps the Smallest Gemma 4 Agent…, Zenodo 10.5281/zenodo.23813680 | **VERIFIED (record read; partly)** | Fetched the record: author Taiko Toeda, Dataset, v1.0.2, 31 Oct 2026, Apache-2.0; E4B/12B/26B-A4B × 2 scaffold levels × 5 seeds on 104 public competition tasks; E4B 10.0 → 15.4% with paired-bootstrap CI +2.3 to +8.8. The abstract was read through a fetch agent's **paraphrase**, not verbatim. **Not verified:** exact scaffold components (whether test feedback is part of it), the "newer version" the page advertises, and the associated Kaggle writeup. Draft cites only what was read. **Read the record yourself before submission.** |
| 7 | Lin, Koppel, Chen, Solar-Lezama — QuixBugs, SPLASH Companion 2017, pp. 55–56, doi:10.1145/3135932.3135941 | **VERIFIED** | DBLP/researchr and the paper PDF. Repository and pinned commit verified in P1/P2A. |
| 8 | Gemma 4 E2B QAT Q4_0 GGUF model card (HF, revision 675cff42…) | **VERIFIED in P2B** | Primary source read in P2B (hash matches LFS metadata; T=1.0/top-p 0.95/top-k 64 from the card). Not re-fetched in P3A. No Gemma 4 technical report is cited; none was confirmed. |
| 9 | llama.cpp release b12192 | **VERIFIED in P2B** | Release asset digest matched the GitHub API. |

**Dropped from V1 (still unconfirmed, not cited):** LocAgent, RepoGraph, CodexGraph, BugsInPy, HumanEvalPack/OctoPack — the graph arm and alternative benchmarks were not run, so they are not needed. Do not add them without checking authors/years/venues. Not independently confirmed that the Toeda scaffolds contain *no* test feedback: the draft therefore avoids any novelty claim.

## 4. Additional seeds: necessary or optional?

- **Necessary if the paper is to make any comparative claim.** With one discordant task (p = 1.0), nothing can be claimed either way; the pre-specified design called for 3 seeds; and the one pilot discrepancy shows outcomes vary across processes.
- **Optional if the paper is framed as in V1** (descriptive pilot + failure analysis + reproducibility lessons). V1 is internally consistent without them, but its contribution is weaker and the reviewer-visible "1/12 vs 0/12" stays inconclusive.
- **Cost/feasibility (from P2C):** seeds 2–3, same two arms ≈ 36 min on this CPU. Time to deadline is ~4 days. Needs your approval (new inference).
- **Caveat for any rerun:** the memory-address defect (finding 1) is inside the frozen `harness/` code path. Editing it breaks the freeze. Either run unchanged (and state the defect, as V1 does) or normalise addresses as a clearly labelled post-freeze deviation. Do not mix the two without saying so.
- A hand audit of resolved runs is trivially satisfied so far (the one resolved run is AST-equal to the reference).

## 5. Remaining paper requirements

**Kaggle Paper Track rules: NOT CONFIRMED.** The official `kaggle.com/competitions/gemma-4-developer-agent` (and `/rules`, `/overview`) returns only a title shell to automated fetch; the guessed `…-paper-track` URLs return 404. Third-party aggregators give no word limit for the Paper Track (the only cap seen, 1,500 words, belongs to a *different* hackathon). Aggregator claims (unverified, conflicting on details): deadline 12–13 Nov 2026 depending on time zone; up to 5 paper submissions; teams ≤5. **Nothing here is treated as a rule.** The outline's "≤3,000 words / five equal criteria / must click Submit / attachments become public" is still secondary-source only.

You must read the rules page in a logged-in browser and confirm: word limit and what it counts (tables? references? abstract?), required format (Kaggle Writeup vs PDF), required fields (title/subtitle, track, cover image, attachments), whether code/notebooks must be attached and made public, the exact deadline and time zone, submission count limit, and the AI-assistance disclosure rule. (Toeda's record notes it discloses AI-assisted drafting; check if disclosure is required or expected.)

Other open items:
- [ ] Author name/affiliation and **AI-assistance disclosure** (placeholders in the draft).
- [ ] Decide where the evidence is released (traces, harness, `FREEZE.sha256`, QuixBugs pinned commit). QuixBugs is not vendored (license note in P1); the draft says "available for inspection" — make that true or reword.
- [ ] Figure(s): outline planned a paired-difference plot and an annotated trace; neither exists. With 1 discordant task, a table (already in V1) is more honest than a forest plot; optional trace excerpt (e.g. the `lis` repeated-edit loop) would help clarity.
- [ ] Author read-through: V1 was drafted by the assistant; the protocol requires the author to write and check the final text.
- [ ] Re-read Toeda's record and its associated writeup; revise Related Work if their scaffold includes test feedback.
- [ ] Optionally re-open the Gemma 4 model card to confirm the quoted sampling settings and revision.
- [ ] Mention in the text, if space permits, the unverified llama.cpp warning about two "not control-type" tokens (P2B) and that peak RAM was not measured (the latter is in Limitations).

## 6. Submission blockers

1. **Unconfirmed Kaggle Paper Track rules** (word limit, format, deadline, attachments). Hard blocker for formatting; the text itself is not blocked.
2. **Author review/ownership and AI-disclosure** not done.
3. **Deadline pressure:** ~4 days from 2026-11-08 to the unconfirmed 2026-11-12 deadline; time zone unknown.
4. **Scientific blocker only if a claim is wanted:** no comparative claim is supportable with the current data (§4). V1 makes none.
5. Release location for traces/harness not decided.

Not blockers: references (all cited ones verified or P2B-verified), word count, evidence integrity.

## 7. Exact next action

Open the Kaggle competition's Paper Track rules in a logged-in browser, copy the word limit, counting rule, format, attachment requirements, deadline and time zone into a note, and tell me; I will then conform V1 (trim/format, fill the disclosure and release statements). In parallel, decide whether to authorise the optional seeds 2–3 run (~36 min, same server command and `main_seed23` output path from P2C's NEXT_ACTION). If you approve it, I'd recommend running it unchanged and reporting the address defect as a known limitation, rather than editing frozen code with four days left.
