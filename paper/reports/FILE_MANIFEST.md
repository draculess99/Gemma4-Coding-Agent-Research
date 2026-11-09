# FILE_MANIFEST — Paper Track P1 research package

Created 2026-11-07 in the Claude sandbox. **Direct write to D: was NOT available; nothing has been saved to your D: drive.** This manifest describes the ZIP `Gemma4_Paper_Research_Organized.zip`. Extract it into `D:\KAGGLE_Projects\Gemma4_Developer_Agent` (creates `paper\`).

## Research documents included
| Item | Location |
|---|---|
| Research feasibility report | `reports\FEASIBILITY_REPORT.md` |
| Literature review and citations (with VERIFIED / FROM MEMORY status) | `research\LITERATURE_AND_OVERLAP.md` |
| Experimental protocol | `methodology\EXPERIMENTAL_PROTOCOL.md` (copy) and `experiments\p1_harness\docs\EXPERIMENTAL_PROTOCOL.md` (canonical, hashed by freeze.py) |
| Paper outline | `drafts\PAPER_OUTLINE.md` |
| Next-step instructions | `reports\NEXT_STEPS_LIMITED_INFERENCE.md` |
| Original P1 archive, untouched | `research\source_archive\Gemma4_Developer_Agent_P1.zip` (SHA-256 `9a66da72f4e6f33b44c56123f2fc2e3c45fe08c9a8a551d5f2c8f96bfb63c1e5`) |

## Experimental files included (all under `experiments\p1_harness\`, original layout)
* QuixBugs task manifest (12 tasks + full 31-program scan log): `manifest\task_manifest.json`, builder `scripts\build_manifest.py`
* Harness: `harness\agent.py, grade.py, graph.py, llm.py, run_experiment.py, summarize.py, workspace.py, __init__.py`
* Agent configurations: `configs\common.json`, `arm1_basic.json` (baseline), `arm2_test_guided.json` (test-guided), `arm2b_agent_initiated_tests.json`, `arm3_graph_test_validated.json`, `arm3b_test_validated_nograph.json`; `prompts\system_base.md`
* Results row schema: `schema\results_schema.json`
* Scripts: `scripts\selftest.py`, `freeze.py`, `profile_machine.py`, `build_manifest.py`

## Existing test evidence
* `results\selftest_mock_log_2026-11-07.txt` — 23 PASS / 0 FAIL, scripted MOCK policies only, **no Gemma model involved**. **This log was regenerated during this transfer, on the relocated layout; no log file was saved at the time of the original P1 run** (that run was only shown in the session, with the same 23-check result). It was executed in a throwaway copy, not in the package.
* `manifest\task_manifest.json` `scan` array — measured eligibility of 31 QuixBugs programs (28 eligible; `bitcount`, `find_first_in_sorted`, `sqrt` timed out on the buggy version).
* There are NO real-model results, traces, timing measurements or machine profile.

## Altered paths / dependencies
| Original (sandbox) | In this package | Reason |
|---|---|---|
| `Gemma4_Developer_Agent\{harness,configs,prompts,manifest,schema,scripts}` | `paper\experiments\p1_harness\...` | Kept as one unit; code resolves paths relative to its root. File contents unchanged (byte-compared for harness, configs, manifest). |
| `README.md` | `experiments\p1_harness\README.md` | Project root readme. Package-level readme is `paper\README.md`. |
| `docs\EXPERIMENTAL_PROTOCOL.md` | both `methodology\` and `experiments\p1_harness\docs\` | freeze.py hashes the second path. If you edit the protocol, edit the harness copy and re-copy, or the two will drift. |
| `docs\FEASIBILITY_REPORT.md`, `NEXT_STEPS_LIMITED_INFERENCE.md` | `reports\` | Not referenced by code. |
| `docs\LITERATURE_AND_OVERLAP.md` | `research\` | Not referenced by code. |
| `docs\PAPER_OUTLINE.md` | `drafts\` | Not referenced by code. |
| `results\` (empty) | `paper\results\` | README + mock log only. |

Text inside the moved documents still uses the old root (`python scripts/...`, `docs/...`, `_scratch/QuixBugs`). I did not edit those documents; run commands from `paper\experiments\p1_harness\` and substitute backslashes on Windows.

## Missing or unavailable (not fabricated)
* QuixBugs clone (`_scratch/QuixBugs`): deliberately not packaged — third-party repo, pinned commit `4257f44b0ff1181dedaedee6a447e133219fcebf`; clone it yourself (NEXT_STEPS §2).
* `FREEZE.sha256`: not created on purpose — freeze only after sampling defaults are verified.
* Real results, traces, machine profile, model/GGUF files, llama.cpp: none exist.
* Official Kaggle rules / HARNESS_README text: never readable in P1.
* A paper draft: only the outline exists.
* No `agent\`, `submission\` or `experiments\developer_agent\` content was available to, or touched by, this session.

## Files requiring manual verification
1. Kaggle Paper Track rules, word limit and deadline. P1 docs cite 2026-11-12 23:59 UTC from secondary sources; if your notes show another date (e.g. Dec 2, 2026), confirm on the Kaggle page which applies to the Paper Track.
2. Citations flagged FROM MEMORY in `research\LITERATURE_AND_OVERLAP.md`.
3. Toeda Zenodo record (10.5281/zenodo.23813680): read it for test-feedback overlap.
4. Windows behaviour of the harness (tested only on Linux).
5. Sampling defaults in `configs\common.json`, llama-server flags, GGUF repo ID (all marked unverified).

## Verify after extracting (PowerShell, from `D:\KAGGLE_Projects\Gemma4_Developer_Agent`)
`Get-ChildItem paper -Recurse -File | Get-FileHash -Algorithm SHA256 | Select Hash,Path` and compare with the table below (this manifest file itself is not listed; its own hash cannot be self-included).

## SHA-256 checksums (33 files)
| File (relative to `paper\`) | Bytes | SHA-256 |
|---|---:|---|
| `README.md` | 1335 | `062ea66328ba826e0fff81c5bbf6563cf9c6f2173fbf97e5612b5029645949be` |
| `drafts\PAPER_OUTLINE.md` | 3125 | `564e3e24809de9073765e0efc4eb97cec24fd17b593451f3b667949a7f5cfca7` |
| `experiments\p1_harness\README.md` | 912 | `9bf49065e5a23e56c3d715d7dd8ea42697cab299ad255038a2f5d03543792dd4` |
| `experiments\p1_harness\configs\arm1_basic.json` | 274 | `66f0a4a256ca3ca16c8b08e44b6f1543d469080018761ba17c0df2358d1ab9fb` |
| `experiments\p1_harness\configs\arm2_test_guided.json` | 390 | `23b800ec199bc1f161a841337883ae17d1cea9a907d12bf9b5ae7e6f02d3549a` |
| `experiments\p1_harness\configs\arm2b_agent_initiated_tests.json` | 465 | `b3ae0ae57acbf763a6f41231f0b7845e87f1012beb606c2ddca3e24413b6bfa7` |
| `experiments\p1_harness\configs\arm3_graph_test_validated.json` | 440 | `ac990f001af390958a1b28c93ba135c9db7540bb0a53a3567bdb8c83bdca707c` |
| `experiments\p1_harness\configs\arm3b_test_validated_nograph.json` | 340 | `573b4ff8769f110c3f15d6a8e81d50a5325edaa46531c2d5bd0768606cbf886e` |
| `experiments\p1_harness\configs\common.json` | 556 | `89570d7c9835d5f3349b36745bc5c28b5520f846605154de19447610963a43b8` |
| `experiments\p1_harness\docs\EXPERIMENTAL_PROTOCOL.md` | 8062 | `97d2573ab32fe110266b3ab3931105a9bb1efa940eccfc167afec4c6dcb556f4` |
| `experiments\p1_harness\harness\__init__.py` | 29 | `f7b048c9e7325f4252a6a59c2625bf2f180cf5bea0baadbe0d7e01a0ebcccc08` |
| `experiments\p1_harness\harness\agent.py` | 10865 | `22506a379b94485ab6276815efbc1e87a941d69044fef8ae789bbddf0d6234d4` |
| `experiments\p1_harness\harness\grade.py` | 1942 | `b6b36da9dd5b789a5f06a15923f14f843692b8bad9e8d90b0d8de84a295b307a` |
| `experiments\p1_harness\harness\graph.py` | 4249 | `d1fee1c4f584eddae90ff96885a5ef20bc93f9638e84e35743cf82762ef9e9b1` |
| `experiments\p1_harness\harness\llm.py` | 2111 | `27d500c2667745f9b8fb43fa0a99caeb128769804800dfdef118e9474fefa623` |
| `experiments\p1_harness\harness\run_experiment.py` | 5140 | `889a7edef8974ff0214b598c522ef66f9d7b0a2204e687a13fda0ecab1da7b2c` |
| `experiments\p1_harness\harness\summarize.py` | 2840 | `bd9eed3dde06e5cc314dd98129eb52674d921ca329a0ddb5a44f7c99675f22a9` |
| `experiments\p1_harness\harness\workspace.py` | 3056 | `dd0adc77bf56c570287d55df84938999df833c5e735464e84019462a6708c20b` |
| `experiments\p1_harness\manifest\task_manifest.json` | 19884 | `cf248eb41d9f69e14c8e65be499a76a0463c1a9b9beb3cb27eabe9cce1adf8ad` |
| `experiments\p1_harness\prompts\system_base.md` | 335 | `6a2cf3b26c88852fa69f366e401fa472b282962dabdee81fd9d8cd5e20e731ee` |
| `experiments\p1_harness\schema\results_schema.json` | 3071 | `59befe5c7ff6c1613d21d0bdac30cb9b7d543d106163f35a4d51b758bc182375` |
| `experiments\p1_harness\scripts\build_manifest.py` | 5694 | `3a8877e921c916613bc0e76f6ce37325859bf00ca6345f08a0d9b02f01dca1af` |
| `experiments\p1_harness\scripts\freeze.py` | 1229 | `3ec6024abc63703d6a94bb1e08dee253ceb65b42a93410667f8e81a8644a0785` |
| `experiments\p1_harness\scripts\profile_machine.py` | 1194 | `f2e95fafabc425148052159c1bed35d88ddbb8a3f073678bd6344119c5e8bc0e` |
| `experiments\p1_harness\scripts\selftest.py` | 6628 | `f81664008119d62675db45faa12fd50edf7078655de7447647b939b492f435ef` |
| `methodology\EXPERIMENTAL_PROTOCOL.md` | 8062 | `97d2573ab32fe110266b3ab3931105a9bb1efa940eccfc167afec4c6dcb556f4` |
| `reports\FEASIBILITY_REPORT.md` | 4725 | `440ecac0084b43f71ea2edd0126412903f60d862f9665b63e414b9e441fd44a1` |
| `reports\NEXT_STEPS_LIMITED_INFERENCE.md` | 4348 | `a219e4ffa3fac1508632e9b52ff21990809c7f81082eeee512ebd99770167c25` |
| `research\LITERATURE_AND_OVERLAP.md` | 4851 | `167f7b72cc41c8392c87fa354015ae9d77cce47c91bd65c6afb81e2856f109c2` |
| `research\source_archive\Gemma4_Developer_Agent_P1.zip` | 45517 | `9a66da72f4e6f33b44c56123f2fc2e3c45fe08c9a8a551d5f2c8f96bfb63c1e5` |
| `results\README.md` | 289 | `1abf79f262570a85ee138e5b18761dff65af6a12d6665d310f28dfbdd5918a71` |
| `results\selftest_mock_log_2026-11-07.txt` | 1584 | `270e1b0040fdfd6d1a49b8a4e92c1431d37a18f1943565f65d8525b81a6f6680` |
| `scripts\README.md` | 505 | `5a763c64242dbeb5f3e67c2b592b6ca6949d313656e4d02e5a524f963a1192f4` |
