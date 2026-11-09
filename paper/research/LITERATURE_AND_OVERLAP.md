# Related Work and Overlap Check

Status key: **VERIFIED** = I located the source during P1 and read at least its abstract/landing page; **FROM MEMORY** = I believe the citation is right but did not re-open it in P1 — *check authors, year and venue before citing*; **UNREAD** = known to exist, content unavailable.
Search coverage was limited (web search, one session). Absence of a paper in this list is **not** evidence that none exists.

## Closest overlap — must be cited and distinguished

* **Toeda, "Scaffolding Helps the Smallest Gemma 4 Agent, Not the Larger Ones"**, Zenodo, DOI 10.5281/zenodo.23813680. Status: VERIFIED to exist (landing page). Reported (secondary reading of the abstract): E4B resolve rate 10.0 % → 15.4 % with code-graph tools plus an analyzer sub-agent; benefit not seen for larger Gemma 4 models. **Not verified:** whether their scaffolds include test execution/feedback, their task set, and their evaluation harness (the repository page was not readable; a fetch was refused and not retried).
  *Consequence:* the idea "scaffolding helps small Gemma 4 agents" is **not novel**. Any contribution must be narrower, e.g. isolating *deterministic harness-enforced test feedback* (vs. agent-chosen testing) on a small local model, with paired statistics and explicit negative-result reporting. Whether even that is new depends on the unread scaffold details. Do not write "first" or "novel" about this until that is checked.

## Test/execution feedback in code agents

* Chen et al., **Teaching Large Language Models to Self-Debug** (2023, arXiv 2304.05128). FROM MEMORY. Execution feedback and self-explanation improve code generation.
* Shinn et al., **Reflexion** (NeurIPS 2023). FROM MEMORY. Verbal reinforcement using feedback signals including unit tests.
* Olausson et al., **Is Self-Repair a Silver Bullet for Code Generation?** (ICLR 2024). FROM MEMORY. Finds that, once the extra sampling cost is counted, self-repair gains are modest and bounded by feedback quality — directly relevant to H1/H4 and to why cost-per-resolve is reported.
* Yang et al., **SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering** (2024). FROM MEMORY. Interface design matters; the tool set is a variable.
* Xia et al., **Agentless** (2024). FROM MEMORY. Simple localise-repair-validate pipelines compete with complex agents; tests are used for validation.

## Graph / structure-aware code tools (arm 3)

* **LocAgent** (graph-guided issue localisation), **RepoGraph**, **CodexGraph** — FROM MEMORY (titles believed right; authors/years not checked). Motivate the graph arm; none were evaluated here.

## Benchmarks

* Lin et al., **QuixBugs: A Multi-Lingual Program Repair Benchmark Set Based on the Quixey Challenge** (SPLASH Companion 2017). Repository https://github.com/jkoppel/QuixBugs — VERIFIED (repo cloned, commit pinned, license file read). Programs are small and public → contamination risk.
* **BugsInPy** (Widyasari et al., 2020). FROM MEMORY. Real-world Python bugs with tests; considered as an alternative. Its paper is CC BY-NC-ND, and environment setup per project is heavy for a CPU-only five-day project — not used.
* **HumanEvalPack / OctoPack** (Muennighoff et al., 2023, MIT). FROM MEMORY. Alternative function-level repair set; not used.

## Gemma 4 and the competition

* Gemma 4 model family (E2B, E4B, 12B, 26B-A4B, 31B; Apache 2.0; native function calling; configurable thinking) — from secondary sources/model pages seen in P1; **re-read the official model card before citing specifics**.
* Kaggle Gemma 4 Developer Agent competition and its Paper Track — the official rule pages returned only metadata through the fetch tool. Rule details in these docs (≤3,000 words, five equal criteria, deadline 2026-11-12 23:59 UTC, must click Submit, private attachments become public) come from secondary descriptions and **must be re-checked on the Kaggle page after joining**.

## What the study can honestly claim (if it runs)

1. A small, fully pre-specified, reproducible comparison of no-test vs harness-triggered-test agents for one small Gemma 4 model on a local CPU stack, with raw traces released.
2. Paired task-level estimates with wide CIs, stated as such.
3. A negative or null result is publishable under the same design.

It cannot claim: general results for small models, results for the competition harness or its tasks, any Kaggle ranking, or novelty over Toeda without the check above.

## Before submission — checklist

* [ ] Open and read Toeda's record/repo; state exactly what overlaps.
* [ ] Re-verify every FROM MEMORY citation (authors, year, venue, arXiv id).
* [ ] Targeted search for: "test-driven feedback small language model repair agent", "execution feedback QuixBugs LLM", "Gemma 4 agent" and anything newer than the knowledge cutoff.
