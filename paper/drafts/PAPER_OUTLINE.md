# Paper Outline (≤ 3,000 words, Kaggle Paper Track)

Working title: **Does Deterministic Test Feedback Improve Small Coding Agents? A Pre-Specified Local Study with Gemma 4 E2B**
Rule of use: every `[RESULT PENDING]` stays until a non-mock run of the frozen harness exists. The author writes the final text; this is a skeleton and word budget only.

| § | Section | Words | Content |
|---|---------|------:|---------|
| 1 | Abstract + contribution statement | 200 | Question, setup, headline paired difference with CI `[RESULT PENDING]`, one-sentence limitation. |
| 2 | Introduction and hypotheses | 300 | Why small local agents; why test feedback is a cheap, deterministic signal; H1 confirmatory, H2–H5 exploratory. |
| 3 | Related work | 350 | Self-Debug, Reflexion, Olausson et al., SWE-agent, Agentless; graph tools (LocAgent/RepoGraph/CodexGraph); **Toeda (Zenodo) overlap stated plainly**. |
| 4 | Method | 700 | Arms table; harness (JSON protocol, edit guards, budgets); model/runtime (GGUF Q4_0, llama.cpp); tasks and selection rule (28 eligible, 12 sampled, seed recorded); metrics; statistics; pre-registration by hash. |
| 5 | Results | 500 | Per-arm table (resolve %, turns, tokens, wall time); paired differences with bootstrap CIs; end-reason distribution; cost per resolved task; hand-audit of test-adequate-but-wrong patches. All `[RESULT PENDING]`. |
| 6 | Analysis | 300 | Where feedback helped/hurt (trace examples); format-error and edit-error rates; whether arm 3's graph was used at all (graph_calls). |
| 7 | Limitations / threats to validity | 350 | Contamination; 12 tasks; one model; GGUF vs competition w4a16-ct; JSON protocol vs native tool calls; thinking-mode handling; graph arm vacuous on QuixBugs; CPU only; sampling defaults. |
| 8 | Reproducibility | 150 | Repo contents, pinned commit, hashes, `FREEZE.sha256`, deviations list, how to rerun. |
| 9 | Conclusion | 100 | What the data support; what it does not; next step. |
|   | Total | 2,950 | Tables/figures and references count toward the limit as Kaggle specifies — **check the counting rule on the Kaggle page.** |

## Mapping to the five equal criteria (self-check, not a prediction)

* Novelty — narrow and hedged; see LITERATURE_AND_OVERLAP.md. Weakest criterion given the Toeda overlap.
* Quality/generality — limited by one model and 12 tasks; compensated by explicit threats section.
* Relevance — direct (small Gemma 4 agent, test feedback, local deployment).
* Verifiability — strongest: pinned commit, hashes, traces, seeded selection, mock-guarded summaries.
* Clarity — keep to one table, one figure (paired differences with CIs).

## Figures/tables planned

1. Arms table (from protocol §2).
2. Results table (from `harness.summarize`).
3. Forest-style plot of paired differences with CIs `[RESULT PENDING]`.
4. One annotated trace of a feedback-driven fix and one failure trace.

## If H1 is null or negative

Say so in the abstract. Report cost per run and error-mode analysis; that is the contribution. Do not reframe the hypothesis after seeing the data; list any post-hoc analysis as exploratory.
