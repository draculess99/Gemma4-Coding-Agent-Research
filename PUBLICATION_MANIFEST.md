# Publication manifest and exclusion list

Prepared in phase G1 (publication audit) and reconciled with the final file bytes in phase G2 (see `paper/ERRATA.md` for the one added file).
The file table below is generated from `git diff --cached --name-only` (the exact staged paths, which equal what the scoped `.gitignore` allows), with the SHA-256 of each file's current bytes. This manifest is not listed in its own table.

**97 files, 2.2 MB in total** (excluding this manifest). Largest file: 572.4 KB.

## 1. Published files

| Group | Files | Bytes |
|---|---:|---:|
| Repository root | 6 | 26,215 |
| Harness, frozen configuration, protocol, manifest, freeze list | 23 | 80,624 |
| Raw results and traces (genuine Gemma inference) | 32 | 257,844 |
| Mock self-test log | 1 | 1,584 |
| Runtime provenance (small logs only) | 12 | 259,431 |
| Phase reports | 7 | 55,007 |
| Draft paper | 2 | 18,780 |
| Methodology and related-work notes | 2 | 12,913 |
| Verification script | 1 | 8,061 |
| Figures, rendering scripts, media verification | 11 | 1,553,721 |

### Repository root

| File | Bytes | SHA-256 |
|---|---:|---|
| `.gitattributes` | 541 | `a752080453467b152a46203f95e706a5796e631ca6eaec25ceeffa864a000f20` |
| `.gitignore` | 1,501 | `c1d797455c20107a1ad5bbb595445650319956de3ce0ddfa0314dec4f3db10e7` |
| `README.md` | 7,689 | `cbbce5cda2ecfeddea8eef40ff358bd38ee5a7ef33205211f7a4e2cb7722588b` |
| `THIRD_PARTY_NOTICES.md` | 3,315 | `2c7eab47899d91cce10d3deffceb96a8b82c423914736125427cbe07f4119daf` |
| `paper/ERRATA.md` | 3,078 | `acaf78221265f315bfa572bbf36a410b9c06ff3b2e31429906b9dc737c512c73` |
| `paper/REPRODUCING.md` | 10,091 | `812014a4e6c422f2c5ac18cca89793e040f0f5f565443beb3c723a8cfb230572` |

### Harness, frozen configuration, protocol, manifest, freeze list

| File | Bytes | SHA-256 |
|---|---:|---|
| `paper/experiments/p1_harness/FREEZE.sha256` | 1,757 | `5f3095c183c6a3e06829a0825378b52472eed5daf27fe1cccaf5ab9b2e3fbe35` |
| `paper/experiments/p1_harness/configs/arm1_basic.json` | 274 | `66f0a4a256ca3ca16c8b08e44b6f1543d469080018761ba17c0df2358d1ab9fb` |
| `paper/experiments/p1_harness/configs/arm2_test_guided.json` | 390 | `23b800ec199bc1f161a841337883ae17d1cea9a907d12bf9b5ae7e6f02d3549a` |
| `paper/experiments/p1_harness/configs/arm2b_agent_initiated_tests.json` | 465 | `b3ae0ae57acbf763a6f41231f0b7845e87f1012beb606c2ddca3e24413b6bfa7` |
| `paper/experiments/p1_harness/configs/arm3_graph_test_validated.json` | 440 | `ac990f001af390958a1b28c93ba135c9db7540bb0a53a3567bdb8c83bdca707c` |
| `paper/experiments/p1_harness/configs/arm3b_test_validated_nograph.json` | 340 | `573b4ff8769f110c3f15d6a8e81d50a5325edaa46531c2d5bd0768606cbf886e` |
| `paper/experiments/p1_harness/configs/common.json` | 629 | `7e3755ad603cb56999c4c7bfa071898573509f054fc957f3093f82e830564f06` |
| `paper/experiments/p1_harness/docs/EXPERIMENTAL_PROTOCOL.md` | 8,062 | `97d2573ab32fe110266b3ab3931105a9bb1efa940eccfc167afec4c6dcb556f4` |
| `paper/experiments/p1_harness/harness/__init__.py` | 29 | `f7b048c9e7325f4252a6a59c2625bf2f180cf5bea0baadbe0d7e01a0ebcccc08` |
| `paper/experiments/p1_harness/harness/agent.py` | 10,865 | `22506a379b94485ab6276815efbc1e87a941d69044fef8ae789bbddf0d6234d4` |
| `paper/experiments/p1_harness/harness/grade.py` | 1,942 | `b6b36da9dd5b789a5f06a15923f14f843692b8bad9e8d90b0d8de84a295b307a` |
| `paper/experiments/p1_harness/harness/graph.py` | 4,249 | `d1fee1c4f584eddae90ff96885a5ef20bc93f9638e84e35743cf82762ef9e9b1` |
| `paper/experiments/p1_harness/harness/llm.py` | 2,111 | `27d500c2667745f9b8fb43fa0a99caeb128769804800dfdef118e9474fefa623` |
| `paper/experiments/p1_harness/harness/run_experiment.py` | 5,140 | `889a7edef8974ff0214b598c522ef66f9d7b0a2204e687a13fda0ecab1da7b2c` |
| `paper/experiments/p1_harness/harness/summarize.py` | 2,840 | `bd9eed3dde06e5cc314dd98129eb52674d921ca329a0ddb5a44f7c99675f22a9` |
| `paper/experiments/p1_harness/harness/workspace.py` | 3,056 | `dd0adc77bf56c570287d55df84938999df833c5e735464e84019462a6708c20b` |
| `paper/experiments/p1_harness/manifest/task_manifest.json` | 19,884 | `cf248eb41d9f69e14c8e65be499a76a0463c1a9b9beb3cb27eabe9cce1adf8ad` |
| `paper/experiments/p1_harness/prompts/system_base.md` | 335 | `6a2cf3b26c88852fa69f366e401fa472b282962dabdee81fd9d8cd5e20e731ee` |
| `paper/experiments/p1_harness/schema/results_schema.json` | 3,071 | `59befe5c7ff6c1613d21d0bdac30cb9b7d543d106163f35a4d51b758bc182375` |
| `paper/experiments/p1_harness/scripts/build_manifest.py` | 5,694 | `3a8877e921c916613bc0e76f6ce37325859bf00ca6345f08a0d9b02f01dca1af` |
| `paper/experiments/p1_harness/scripts/freeze.py` | 1,229 | `3ec6024abc63703d6a94bb1e08dee253ceb65b42a93410667f8e81a8644a0785` |
| `paper/experiments/p1_harness/scripts/profile_machine.py` | 1,194 | `f2e95fafabc425148052159c1bed35d88ddbb8a3f073678bd6344119c5e8bc0e` |
| `paper/experiments/p1_harness/scripts/selftest.py` | 6,628 | `f81664008119d62675db45faa12fd50edf7078655de7447647b939b492f435ef` |

### Raw results and traces (genuine Gemma inference)

| File | Bytes | SHA-256 |
|---|---:|---|
| `paper/experiments/p1_harness/results/main_seed1/results.jsonl` | 37,992 | `56a7f4ab64a65b7ea3ea9aea6f8cd3c21d8bbd69ef5c0b4ad8a5df244e1648eb` |
| `paper/experiments/p1_harness/results/main_seed1/run_meta.json` | 644 | `c07dc25a2a8f6268a8673065b04cdfc2f443c7f53731c03222a741695bfe6def` |
| `paper/experiments/p1_harness/results/main_seed1/traces/13bea2c07ef7f2b4.jsonl` | 8,476 | `9039212e270959811599d526f6670d50bf837398f72bba2d0ab55cc21043205c` |
| `paper/experiments/p1_harness/results/main_seed1/traces/2030df85b3181e64.jsonl` | 10,582 | `5c9b93749e6afe91d18df15f37a37350f1b9f747c382200a3b0d1526c561fae7` |
| `paper/experiments/p1_harness/results/main_seed1/traces/3dadb99ed6c9c968.jsonl` | 7,312 | `504d8a964c6bdd9467c9b9f058c350a9d70035ed3ec17048eaecb44eaa598fc2` |
| `paper/experiments/p1_harness/results/main_seed1/traces/44fdb2bc797a690a.jsonl` | 8,140 | `06e6ae2082d232df0c3d22fffedb7b96d41472a31126950c2532fb479acc7973` |
| `paper/experiments/p1_harness/results/main_seed1/traces/4a47316f7ac015a9.jsonl` | 7,755 | `68e87ee762f0f0ef5f8da7072c6d55a50c702a9c94ec11e4c1f3ef03548feb05` |
| `paper/experiments/p1_harness/results/main_seed1/traces/4b189cd92c03602e.jsonl` | 7,782 | `06e11c95a0d17ef64d68dd84bc4c1e58eb3c1aa01450ee3d274bf4897f7f1b6d` |
| `paper/experiments/p1_harness/results/main_seed1/traces/4e7619c07de83ec3.jsonl` | 9,034 | `0f68dc342bb6405007313000a96e7cdc8208838673342ce076454be336c620c0` |
| `paper/experiments/p1_harness/results/main_seed1/traces/4f294fe8e72c2740.jsonl` | 9,243 | `12395ed6f0e5361930c487d98959e780716a379d38b2f2fde22c7787d54c12b1` |
| `paper/experiments/p1_harness/results/main_seed1/traces/6415728c1c08eaf0.jsonl` | 8,240 | `f988e0ec636bf6a45c82c4fe44be36667740c6b3f114fe9b07db490b14b202f8` |
| `paper/experiments/p1_harness/results/main_seed1/traces/6b0c8da2c7a2883e.jsonl` | 5,728 | `9ca3ea2dc138483d99f739906c4d1d58962b813bd8478fa029e08f25829febf3` |
| `paper/experiments/p1_harness/results/main_seed1/traces/7a21a5423c138640.jsonl` | 7,418 | `79cd2b1981be45e33a54420b2906b9ea97cd2b173659ed749fced30ff8c29330` |
| `paper/experiments/p1_harness/results/main_seed1/traces/852e51c747a2e9b4.jsonl` | 9,655 | `42f6bfd33f0358749e1e4a5f7ec3c41299b39e648fedb9994a9967490eee6834` |
| `paper/experiments/p1_harness/results/main_seed1/traces/876b0bb95810137a.jsonl` | 7,738 | `1391474211998618fcc89679322b3bca1bf0fcf6f7dad006e2cfa92c1bae774f` |
| `paper/experiments/p1_harness/results/main_seed1/traces/9677e14722a81479.jsonl` | 5,351 | `a2e242a0a7b678116fd4643aaf1ce11316b290955ae2871fbc56379fa4589dfe` |
| `paper/experiments/p1_harness/results/main_seed1/traces/97d622a8e494a959.jsonl` | 8,683 | `aba28b91d5dd7393796dd5a594bfe94db9c54926dbb432825cf8963557c9a1d9` |
| `paper/experiments/p1_harness/results/main_seed1/traces/a1399b1cc2832906.jsonl` | 5,683 | `452ce12cc9241a9d7b54a420d76fe984bd4bd492c2913c4389f8187af20a24cd` |
| `paper/experiments/p1_harness/results/main_seed1/traces/a8d30b1d91e4e505.jsonl` | 6,870 | `b190f152e2b11811d9a74e70c4137bd3cce42bc1315b4d4dbea114395334ca07` |
| `paper/experiments/p1_harness/results/main_seed1/traces/aae71324e7a0de39.jsonl` | 4,831 | `31294af9ae62c1d90790f1c42b9e0539edde5a646198ffd28f957620f77d7df4` |
| `paper/experiments/p1_harness/results/main_seed1/traces/bb6826d56e696810.jsonl` | 7,948 | `8cad518aa833a65d320bf815269a381fe21adb5d22f792ed0feacb4a4df93ad0` |
| `paper/experiments/p1_harness/results/main_seed1/traces/da273619c463bbec.jsonl` | 5,483 | `024e3f63a45d777360b5338fcd93c770139d804ecf6130e79b58f188d0d37a37` |
| `paper/experiments/p1_harness/results/main_seed1/traces/db7a5ed99c16f019.jsonl` | 8,638 | `85329c5e11f8514f30ccc3ec4fa161d01fe53139fe6b7913b9fa37d2a6d82350` |
| `paper/experiments/p1_harness/results/main_seed1/traces/eb8990f97a8196e1.jsonl` | 8,713 | `0abe02b6aed81acf57ab9927cc34597ac9cda7f0014b4e9b1084dbd74da40931` |
| `paper/experiments/p1_harness/results/main_seed1/traces/ed68f4a53b24fc30.jsonl` | 8,796 | `4a74f972a71c003fb79ce61dd44adbca081d7a47e07839cc6e90301f663f33cb` |
| `paper/experiments/p1_harness/results/main_seed1/traces/fb26c56e0cc79bbc.jsonl` | 9,724 | `8d21d4e4d1a6d71417268c122b78dd906bcece7207117f512e92b0fa19bcc69e` |
| `paper/experiments/p1_harness/results/pilot_p2b/results.jsonl` | 6,616 | `c4b630984b5a40eb88e5a4bf4386d9632945a6a6683a7631fa54665a5d87d25e` |
| `paper/experiments/p1_harness/results/pilot_p2b/run_meta.json` | 644 | `c07dc25a2a8f6268a8673065b04cdfc2f443c7f53731c03222a741695bfe6def` |
| `paper/experiments/p1_harness/results/pilot_p2b/traces/4e7619c07de83ec3.jsonl` | 5,147 | `6f1fe3dd603bd439012beaf58c5f758646d3b93d986058a5cdc706d54eb165f9` |
| `paper/experiments/p1_harness/results/pilot_p2b/traces/9677e14722a81479.jsonl` | 5,351 | `a2e242a0a7b678116fd4643aaf1ce11316b290955ae2871fbc56379fa4589dfe` |
| `paper/experiments/p1_harness/results/pilot_p2b/traces/aae71324e7a0de39.jsonl` | 4,831 | `31294af9ae62c1d90790f1c42b9e0539edde5a646198ffd28f957620f77d7df4` |
| `paper/experiments/p1_harness/results/pilot_p2b/traces/ed68f4a53b24fc30.jsonl` | 8,796 | `4a74f972a71c003fb79ce61dd44adbca081d7a47e07839cc6e90301f663f33cb` |

### Mock self-test log

| File | Bytes | SHA-256 |
|---|---:|---|
| `paper/results/selftest_mock_log_2026-11-07.txt` | 1,584 | `270e1b0040fdfd6d1a49b8a4e92c1431d37a18f1943565f65d8525b81a6f6680` |

### Runtime provenance (small logs only)

| File | Bytes | SHA-256 |
|---|---:|---|
| `paper/runtime/.gitignore` | 563 | `e70b4ad1ecb700b59082e2ecaad262dc42c6c585cb9c884e26c9d33ae96c592b` |
| `paper/runtime/analyze_p2c.py` | 2,398 | `cf786363cfeb0b45ed97207615eca1fb63613a93a2e6bbe45148ed7460406657` |
| `paper/runtime/logs/first_inference.json` | 980 | `32f72ff88be0d00e642361a3d5acfe6e398603dee82aa6ff7d2ab29dbbcb60f0` |
| `paper/runtime/logs/first_inference_reasoning_auto.json` | 1,139 | `a2c5d3f14b14b25f292b7d884c07b6c83a7f086ea3d42c3dfe04bcafc3496c88` |
| `paper/runtime/logs/first_inference_reasoning_off.json` | 980 | `32f72ff88be0d00e642361a3d5acfe6e398603dee82aa6ff7d2ab29dbbcb60f0` |
| `paper/runtime/logs/freeze_time_utc.txt` | 21 | `c3116290045fec8c79632e24ab66296128be4f3c7697a8fa97f7718f90967e07` |
| `paper/runtime/logs/main_seed1_stdout.log` | 3,445 | `0a296e36fd64dbaf4260e7d176cc6813138b6719a0b27d75d6f61330ddf62d69` |
| `paper/runtime/logs/pilot_stdout.log` | 597 | `9a1e2b90f29a361c15c29bcd8385efb6e3c8c8a2df76fc561090f03f83fab39e` |
| `paper/runtime/logs/server.err.log` | 29,621 | `595a5e8bc698f9711f07d7bdda2f4b94ea5258c8f9f9cf7c95c1de6239030f91` |
| `paper/runtime/logs/server_p2c.err.log` | 217,010 | `99f5ac1eda5d30db618a9c2554468020c9e397007f0f88b6d6e1e930de138970` |
| `paper/runtime/logs/server_reasoning_auto.log` | 2,121 | `95249d4d588aa29954531d830109d7fafda3dde6a4a5e9089e37cb65f5d77e43` |
| `paper/runtime/p1_originals/common.json.P1_original` | 556 | `89570d7c9835d5f3349b36745bc5c28b5520f846605154de19447610963a43b8` |

### Phase reports

| File | Bytes | SHA-256 |
|---|---:|---|
| `paper/reports/FEASIBILITY_REPORT.md` | 4,725 | `440ecac0084b43f71ea2edd0126412903f60d862f9665b63e414b9e441fd44a1` |
| `paper/reports/FILE_MANIFEST.md` | 9,366 | `62e06a51d4def37ef7ea58eacbfb75fbb6cc4a286dec84e5301619d2dd5c2e65` |
| `paper/reports/NEXT_STEPS_LIMITED_INFERENCE.md` | 4,348 | `a219e4ffa3fac1508632e9b52ff21990809c7f81082eeee512ebd99770167c25` |
| `paper/reports/P2A_LOCAL_VERIFICATION.md` | 7,112 | `2dd8863a7e5b80c4bc8464fbbc8337791b0ad37ea623b6ff9344f6bffd4b115d` |
| `paper/reports/P2B_INITIAL_INFERENCE.md` | 7,824 | `f0b0292b894542edf89cf6eaeba60e80785a9957ac66b8b35e250ee47e2997e2` |
| `paper/reports/P2C_MAIN_EXPERIMENT.md` | 9,893 | `1686c6387908a8fd541e4f88500cce235157a8a69686942c59764d3abccbad5d` |
| `paper/reports/P3A_SUBMISSION_READINESS.md` | 11,739 | `abcc49a5bffd4ff4b1bc410f1bb2d4d96133a754417acd16b298d66ede2cd895` |

### Draft paper

| File | Bytes | SHA-256 |
|---|---:|---|
| `paper/drafts/GEMMA4_PAPER_DRAFT_V1.md` | 15,655 | `874e6c53a62bc38eeb9a0ee4059d08b5de3a3b8b297900ec710bb4dd566e6bab` |
| `paper/drafts/PAPER_OUTLINE.md` | 3,125 | `564e3e24809de9073765e0efc4eb97cec24fd17b593451f3b667949a7f5cfca7` |

### Methodology and related-work notes

| File | Bytes | SHA-256 |
|---|---:|---|
| `paper/methodology/EXPERIMENTAL_PROTOCOL.md` | 8,062 | `97d2573ab32fe110266b3ab3931105a9bb1efa940eccfc167afec4c6dcb556f4` |
| `paper/research/LITERATURE_AND_OVERLAP.md` | 4,851 | `167f7b72cc41c8392c87fa354015ae9d77cce47c91bd65c6afb81e2856f109c2` |

### Verification script

| File | Bytes | SHA-256 |
|---|---:|---|
| `paper/scripts/verify_published_metrics.py` | 8,061 | `980a370c0f8221ae25b40c0626cc2bff66f35f4ef60273a319d2d24791beb1cf` |

### Figures, rendering scripts, media verification

| File | Bytes | SHA-256 |
|---|---:|---|
| `paper/media/01_research_methodology.png` | 586,149 | `62ff0ef4375ff60b74d700beec963fa533d502d37bb25e14a86a0f703dddfe83` |
| `paper/media/02_results_comparison.png` | 412,083 | `573203c8ee53eca57afa6a35ac7589c5defb9c3257125534c6d2850d5bdd105a` |
| `paper/media/03_reproducibility.png` | 499,911 | `f75370e443187d904893c37dea9405c3c8322926a3b269a06add29a0f9671a84` |
| `paper/media/MEDIA_VERIFICATION.md` | 11,051 | `5ee8b3c1a680bb095c4c510e9d01e5cbb1d39f1d3c51f1cad137d624d54db52c` |
| `paper/media/scripts/README.md` | 2,203 | `010607a6f028cc434b1b36065cf60425b360c911c27caf684b1fc3757061a301` |
| `paper/media/scripts/_common.py` | 9,221 | `ee90aabbb6b04436c8733d9d40399e9d7b2d0aa30b3a06ea96638329f1312d4a` |
| `paper/media/scripts/fig01_methodology.py` | 8,785 | `408f0560f7306392bb01f366ea76c05e153aa09b69e7dbfc036fd5bd7029bd7c` |
| `paper/media/scripts/fig02_results.py` | 8,208 | `2a2a96c9abeaea2f6dce55754f04cc445a59edde5580c582084f548d3019e620` |
| `paper/media/scripts/fig03_reproducibility.py` | 11,807 | `be9f2554285ebc0dd780d8e85273beabc41725bd9c087ca7a9468a41ba1337ce` |
| `paper/media/scripts/render_all.py` | 482 | `70b01a7b42cbc6580369c269e3e5dc7703eb741e83ddad09d8fa1750db53de0a` |
| `paper/media/scripts/verify_against_reports.py` | 3,821 | `b9c4ad466deef9e84bcae6e9724a3c54aad8809493b146a358c79ff1544f5bd5` |

Notes on this list:

- The 19 files named in `paper/experiments/p1_harness/FREEZE.sha256` are published byte-for-byte (`.gitattributes` disables line-ending conversion for that tree). Their hashes in the table above equal the freeze list.
- Four media scripts have CRLF line endings on disk; Git will normalise them to LF on commit (`core.autocrlf=true`). They are source code, not hashed evidence.
- P1 documents (`FEASIBILITY_REPORT.md`, `NEXT_STEPS_LIMITED_INFERENCE.md`, `FILE_MANIFEST.md`, `PAPER_OUTLINE.md`) are historical, written before any result existed, and contain statements such as "no real-model results exist". They are published as dated records; the root `README.md` says so.
- `paper/drafts/GEMMA4_PAPER_DRAFT_V1.md` is a working draft with `[AUTHOR]` placeholders.

## 2. Deliberately excluded (present on disk, not published)

| Path | Size | Reason |
|---|---|---|
| `agent/` | 2 file(s), 3.5 KB | Developer Agent competition implementation. Out of scope for this phase (Paper Track only). |
| `submission/` | 2 file(s), 4.0 KB | Developer Agent competition submission ZIPs. Must not be published or modified. |
| `experiments/developer_agent/` | 3 file(s), 23.4 KB | Developer Agent build and validation tooling (its test fixture contains a deliberately fake `api_key` string). Out of scope. |
| `reference/` | 1 file(s), 54.6 KB | `HARNESS_README.md`: Kaggle competition documentation; redistribution permission not established. |
| `reports/` | 6 file(s), 37.6 KB | Developer Agent phase reports (D1, D2) and the G1 audit report; contain local user paths and internal workflow notes. |
| `paper/runtime/models/` | 1 file(s), 3194.3 MB | 3.35 GB Gemma 4 GGUF weights. Never published; hash recorded instead. |
| `paper/runtime/llama.cpp/` | 52 file(s), 60.8 MB | llama.cpp b12192 binaries and DLLs (third-party binaries). Version and asset hash recorded instead. |
| `paper/runtime/dl/` | 1 file(s), 23.6 MB | llama.cpp download archive. |
| `paper/runtime/logs/server.log, server_p2c.log` | 2 file(s), 0.0 KB | Empty (0 byte) files. |
| `paper/experiments/p1_harness/_scratch/` | 438 file(s), 2.1 MB | Third-party QuixBugs clone with its own nested `.git`; users clone it at the pinned commit. |
| `paper/research/source_archive/` | 1 file(s), 44.5 KB | Redundant binary ZIP of the P1 files (already published in extracted form). |
| `paper/media/cover/gemma4_paper_cover.png` | 1 file(s), 1.7 MB | HELD BACK: contains the Google DeepMind and Gemma logos and a green check / red cross presentation of 1/12 vs 0/12 without the significance caveat; not covered by `MEDIA_VERIFICATION.md`; provenance undocumented. See the review report. |
| `paper/README.md, paper/experiments/p1_harness/README.md, paper/results/README.md, paper/scripts/README.md` | 4 file(s), 3.0 KB | Stale P1 navigation files that state "no real-model results exist"; superseded by the root `README.md` and `paper/REPRODUCING.md`. |

Also never published (blocked by `.gitignore` patterns): `*.gguf`, `*.safetensors`, `*.zip`, `*.dll`, `*.exe`, `.env*`, `*.pem`, `*.key`, `kaggle.json`, virtual environments, `__pycache__/`, `.pytest_cache/`, editor and OS files.

## 3. Safety review summary

- Credential scan of all published files (regex for AWS/GitHub/Hugging Face/OpenAI/Google/Slack/Kaggle keys, private keys, JWTs, bearer tokens, URL credentials, `key=`/`password=` assignments, plus an entropy scan): **no credential found.**
- Personal data: no e-mail address, no Windows user-profile path and no account name in any published file. Informational: two published reports mention the project path `D:\KAGGLE_Projects\Gemma4_Developer_Agent` and the hardware model (Dell Inspiron 15 3535, Ryzen 5 7530U), which are research metadata.
- Traces contain only QuixBugs program text, harness prompts and model replies. No competition dataset is included.
- Licensing: see `THIRD_PARTY_NOTICES.md`. The repository's own license is **not yet chosen**.

## 4. Verification commands

```
python -B paper/scripts/verify_published_metrics.py
python -B paper/experiments/p1_harness/scripts/freeze.py --check paper/experiments/p1_harness/FREEZE.sha256
```
