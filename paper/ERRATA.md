# Errata and clarifications

Corrections and precise definitions for statements in the published reports and the draft. The original files are preserved unedited (they are the dated record); this file qualifies them. Every figure below can be recomputed with `python -B paper/scripts/verify_published_metrics.py` (standard library only) from the saved traces.

## E1. Number of rejected edits: 46, not 47

`reports/P2C_MAIN_EXPERIMENT.md` says "41 of 47 error messages". The correct total is **46** rejected edits = 15 (arm 1) + 31 (arm 2) = 41 "`old` matched 0 times" + 4 rejected for creating a syntax error + 1 malformed (`new` missing). The draft and the root README use 46. (`reports/P3A_SUBMISSION_READINESS.md` already records this slip.)

## E2. "35 of the 41 no-match calls repeat a string" — exact definition

Two different wordings exist in the published files; they count different things.

| Wording | Where | Definition | Count (of 41) |
|---|---|---|---|
| "the failing `old` string was one the model sent **at least twice within the same run**" | draft, "Edit application dominates" | the exact `old` string occurs in two or more `replace_in_file` calls of that run (the failing call itself counts as one occurrence) | **35** (36 if whitespace is ignored) |
| "repeats of a string the model **had already sent**" | `P3A_SUBMISSION_READINESS.md` | the exact `old` string was sent in an *earlier* call of that run | 27 (29 counting earlier `old` and `new` strings, whitespace-collapsed) |

The **draft's wording and its figure of 35 are supported** (verifier check "35 of the 41 …"). The looser P3A phrasing should be read as the draft's definition, not as "earlier repeats" (27). Example in the draft: on `lis`, one `old` string was sent five times; the largest repeat count of a single string in a `lis` run is 5.

## E3. "two contain text absent from the file" — qualification

The draft says that after collapsing whitespace, 39 of the 41 no-match calls differ from the file only in whitespace and two "contain text absent from the file". Precisely: **39 of 41** match the *original buggy file* once whitespace is removed from both; the other two do not match the original, but they do match the file as it stood after the model's own earlier *applied* edits. (Tracking edits forward gives 36 whitespace-collapsed matches, and every one of the 41 matches one of the two file states.) So no failed `old` string was unrelated to the file's content. Whitespace-collapsed matching is permissive: it shows the intended text was present, not that a corrected edit would have been right.

## E4. Draft status

`drafts/GEMMA4_PAPER_DRAFT_V1.md` is the working draft written from the saved results before the Kaggle writeup was submitted (2026-11-09, per the author). It contains `[AUTHOR]` placeholders and may differ from the submitted writeup. Nothing in this repository claims an official Kaggle score or ranking, or a statistically significant improvement: the measured outcome is arm 1 0/12 vs arm 2 1/12 with one discordant task (exact sign test p = 1.0).
