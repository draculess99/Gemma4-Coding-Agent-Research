# Third-party notices

This repository contains original research code, documents and figures, plus small amounts of third-party material, listed here. It does not contain model weights or third-party binaries.

## QuixBugs (included in part)

- Source: https://github.com/jkoppel/QuixBugs, commit `4257f44b0ff1181dedaedee6a447e133219fcebf`. Lin et al., "QuixBugs: A Multi-Lingual Program Repair Benchmark Set Based on the Quixey Challenge", SPLASH Companion 2017.
- The repository is **not** vendored. However, the experiment traces under `paper/experiments/p1_harness/results/*/traces/` reproduce excerpts of its buggy Python programs, docstrings and test files exactly as they were shown to the model, and `task_manifest.json` records its program names and test counts. The reference (correct) programs are not included.
- License: MIT. Required notice:

  > Copyright 2017-2019 James Koppel
  >
  > Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
  >
  > The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
  >
  > THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

- Note: QuixBugs' own `legal_notes.txt` explains that the intellectual-property history of the original Quixey Challenge programs is unusual (the company dissolved; its creator gave informal permission) and is "not legal advice". The upstream project distributes the data under the MIT license above.

## Gemma 4 (referenced, weights not included)

- Model: Google `gemma-4-E2B-it-qat-q4_0-gguf`, Hugging Face revision `675cff42a74c774d6cb76f76d8eacb49b48c9b93`. The model card read during the study states the Apache 2.0 license; this was not independently verified in the repository.
- Raw model replies (outputs of the model on the benchmark tasks) are published in the traces as research data. "Gemma" is a Google trademark; this repository is independent and unaffiliated.

## llama.cpp (referenced, binaries not included)

- https://github.com/ggml-org/llama.cpp, release b12192 (MIT license upstream). Only server logs produced by that build are included.

## Python packages (dependencies, not included)

- pytest (MIT) is required to grade runs. matplotlib (matplotlib license, BSD-compatible) and numpy (BSD-3-Clause) are required only to re-render the figures.

## Papers cited in the draft

References are cited, not reproduced. Their verification status is recorded in `paper/reports/P3A_SUBMISSION_READINESS.md` and `paper/research/LITERATURE_AND_OVERLAP.md`.
