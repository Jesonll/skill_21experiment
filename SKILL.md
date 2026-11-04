---
name: cn-lab-report
description: Use Easy雨课堂/Easy云课堂 through an authenticated browser relay to answer, save, and—with user authorization—submit pre-class quizzes and check actual scores; write and save experiment reports without final submission. Supports course libraries, report.md, report.pdf, photos/ page JPGs, answers.json, and a manual report-only fallback.
---

# Easy课堂实验助手

## Non-negotiable contract

- Default to the user's authenticated browser relay, not manual screenshots or an unrelated managed browser. This is a real account; inspect only the requested course and task.
- **Pre-class quizzes: save, verify, then submit and check the actual score when authorized.** The agent may click the current quiz's final 提交/交卷 and its confirmation after the user explicitly authorizes pre-class submission, including an applicable standing instruction. Match and review every current answer and verify server saves first; unresolved answers block submission. A save-only request takes precedence. Read the resulting server-confirmed score and determine whether it is 100/100 (or the displayed equivalent full mark); do not guarantee 100 before grading or infer it from a library key, completion percentage, or historical score. Below-full, pending, or unavailable grades must be reported accurately. Do not automatically retry, restart, resubmit, or overwrite an existing grade to chase 100; a further attempt requires separate authorization and must respect course rules.
- **Experiment reports: save, verify, never final-submit.** Do not click a report's final 提交/再次提交, confirm report submission, or call report final-submission APIs, even when pre-class submission is authorized. Leave report review and final submission to the user. Library acquisition remains read-only: never submit a quiz merely to obtain or validate a library. Finish by reporting actual saved/submitted/graded state and asking whether other requirements remain.
- Report prose answers only the prompt, in Chinese student-style technical language. No equipment/safety/provenance filler in objectives, and no file-processing narration in answers/captions. Do not fabricate measurements or hide essential uncertainty.
- Every graph requires scientific completeness review and final rendered visual review. Hidden/missing curves/wires or colliding legends block delivery.
- For graphs, circuits, tables, long derivations, or image-required questions, upload the corresponding report-page JPG through the **photo/image channel, never the attachment channel**. Simple answers use the text editor unless the question requires images.
- Do not expose credentials, cookies, tokens, signed URLs, or unrelated user answers. Do not bypass disabled editors, locks, permissions, or course restrictions.
- Read bundled references explicitly; their paths are relative to this skill root. Do not require workspace `AGENTS.md` installation.

## 1. Probe relay first

Read [relay setup and access](references/easyketang-relay.md). In OMP, first read `xd://eval/browser`, then use `browser.targets({app:{relay:true}})` (the OMP browser-relay integration, sometimes called omp_browser relay). Other agents may use their supported relay/browser extension with equivalent authenticated-session access. Do not assume a tool exists because its name appears here.

A listening port alone is not success. Confirm extension connection, access to the actual Easy课堂 site (observed `easyketang.com`), logged-in state, and visibility of the intended course. Discover targets/URLs; never reuse historical resource IDs. Preserve user tabs and avoid auto-writing exam/report navigation during this capability probe.

If relay/site access is unavailable, use the host's interactive ask tool with exactly these two choices:

1. **配置 relay，使用完整功能** — help configure the browser relay/extension and login; then re-probe until actual course access works.
2. **手动提供材料，仅写报告** — use local inputs and generate the report deliverables; no pre-class web answering or website filling in this mode.

Do not silently select the fallback. If option 1 is chosen, inspect current CLI/extension instructions, perform safe local setup, and guide the user through browser extension loading and login steps that require human interaction. Never request a password/token in chat, change settings without approval, or claim setup succeeded before the access probe passes. If it remains blocked, state the exact missing prerequisite and offer the same fallback; finish reachable work.

An explicit user request for manual-only operation already selects option 2; respect it rather than touching a live account.

## 2. Select the task when unknown

After connection/setup is ready, if the user has not already specified the task, ask:

1. **课前预习题作答** — match current questions/options by content, fill and save; with applicable user authorization, final-submit the reviewed quiz and check whether its actual grade is 100/full marks. Otherwise leave it unsubmitted.
2. **实验报告编写与题目作答** — select a library, combine it with personal measurements, generate all report formats, fill/upload and save, do not submit.

Do not repeat a choice already given. Determine the course and experiment from the visible course/resources and user request; ask only if genuinely ambiguous. Manual mode supports task 2 locally only: explain that pre-class web operation requires relay instead of pretending to provide it offline.

## 3. Select or obtain the course library

Read [library discovery and acquisition](references/easyketang-library.md). **For report tasks, this choice is required before drafting.** For pre-class tasks, use the same library checks before matching answers.

1. Inspect `assets/lib_*/manifest.json` and any user-designated library. Report course name, generation time, experiment/manual/question coverage, answer verification status, missing assets, and current-course/version compatibility. Do not just say “library exists”.
2. The initial bundled snapshot is `assets/lib_20261024T143310Z_电路与电子技术实验I/manifest.json`: 8 experiments, 80 pre-class questions/answers, 78 report entries, 8 manuals; 30 answers have historical independent/score evidence, 50 do not; 9 theory images were unavailable. Re-read the actual manifest on every run: these are historical facts, not a guarantee for the current course/account.
3. After disclosure, ask exactly:
   - **使用当前资料库** — identify the offered compatible library; retain its declared limitations.
   - **重新获取资料库** — obtain a fresh current-session course snapshot.
4. If no current library is usable, say so; do not present a nonexistent or incompatible library as valid. Keep the current-library option explicit about its limitation, and require missing target resources before relying on it. If the user explicitly already chose refresh/current library, do not ask again.
5. Fetch a new library only after selection, using authenticated browser reads and current discovered resources. Name it `lib_<UTC YYYYMMDDTHHMMSSZ>_<exact course name>`, save under skill `assets/` when writable (otherwise an explicitly reported workspace path), retain provenance/coverage/limitations, and verify files/checksums. Do not overwrite the old snapshot or save credentials.
6. Read-only acquisition must not start/restart an exam, create a paper, submit for verification, or invoke saves/uploads. Website page loading itself may write progress; use the reference's scoped request guard and document unavoidable limitations without claiming zero writes.

The library supplies questions, manuals, blank record sheets, and reusable knowledge, **not this user's measurements**. Inspect user files before requesting the actual filled data page, necessary waveforms, or a precise missing item. Do not demand a user-authored CSV, manifest, style file, template, or LaTeX source.

## 4A. Pre-class answering (relay only)

Read [pre-class matching, saving, authorized submission, and score checking](references/easyketang-preclass.md).

- Inspect whether a paper already exists, is editable, or is already submitted. Do not redo a completed/full-score attempt or start a new attempt merely to inspect a library. Starting a new paper may consume an attempt; use it only when the user clearly requests starting/completing that assessment and any displayed attempt/timing consequence is authorized.
- Read each current stem, type, complete options, formulas, and images. Match course/experiment + semantic content to a unique library answer; resolve the answer to **current option content**, never stored question numbers, letters, indices, or another account's IDs.
- On unmatched/ambiguous/changed content, derive from the manual/credible evidence or ask for the exact missing information; do not guess. Preserve negations, signs, units, and image semantics.
- Select options through observed page controls/save handlers and verify persisted selected contents. Multiple-choice toggles require difference-based updates, not blind repeated clicks.
- Distinguish a site's per-option handler (historically called `submit(index)`) from final submission by inspecting its actual behavior. A method name alone neither permits nor prohibits it. Use the current verified final-submit control only for the authorized pre-class quiz, never a report or library-acquisition flow.
- Review all saved answers before final submission. When the user authorizes pre-class submission and every answer is resolved and verified saved, submit that attempt through the observed final control and confirmation; then re-read its submitted status and actual server-confirmed score. Check whether it is 100/full marks and report the result without inventing a score. If submission is not authorized, leave it unsubmitted and ask the user to review and submit personally. Record actual save/submission/grade status and unresolved items locally. No automatic reattempts or grade overwrites; ask whether other requirements remain.

## 4B. Report writing and answering

Read these references before the relevant stage:

- [Report writing and graph construction](references/report-writing.md).
- [Student voice and scope](references/student-writing.md), before drafting.
- [Graph second review](references/graph-review.md), before drawing and after final rendering.
- [Output schema and web-answer grammar](references/report-outputs.md).
- [Website editor and image saving](references/easyketang-writing.md), before any web edit/upload.

### Prepare and write locally first

Use the selected library's target questions, instructions, manual, and figures, plus the user's actual filled data page and required photos. Reconcile them with current website prompts and ordering. Ask for missing personal experimental evidence only when necessary; never substitute the library's blank record sheet or the CE example's measurements.

Transcribe and calculate measurements; preserve source discrepancies in working notes. Match every answer to required elements, and use LaTeX formulas and academic drawing tools. Keep theory, approximations, and measurements distinct. Do not narrate reconstruction software in report prose. Generate the complete report and pass content/graph review **before** website filling.

### At least four synchronized report deliverables

```text
report.md                  # complete student-facing Markdown report
report.pdf                 # one answer per page, tidy LaTeX formulas
photos/
  page-001.jpg             # full PDF page, 300 dpi / JPEG quality 95
  page-002.jpg
  ...
answers.json               # question-number keys -> website answer strings
qa/question-map.json       # agent-generated mapping: number, page, text/photo route
```

`answers.json` is a plain object, e.g. `{"1":"掌握运放的基本运算功能。","3":"由虚短、虚断可得 $u_o=2(u_{i2}-u_{i1})$。"}`. Ordinary prose is literal text; only formulas use single `$...$` delimiters. No Markdown headings/bold/tables/images, HTML, display `$$`, document-level LaTeX, `\(...\)` or `\[...\]`. Mathematical expressions inside `$...$` may use supported TeX syntax. This format is not a claim that the site automatically converts pasted dollar text: inspect the current formula/editor mechanism and verify rendered formulas, as described in the website reference.

Author the Markdown answer and website answer explicitly from the same reasoning; do not blindly strip arbitrary Markdown/LaTeX into website prose. `scripts/build_answers.py` validates agent-authored structured input and generates the Markdown, website JSON, and page/route map. This intermediate input is created by the agent, not required from the user. Build the PDF with the LaTeX workflow, then run:

```bash
python3 "$SKILL_DIR/scripts/export_pages.py" report.pdf
# Following a PDF revision: same command with --overwrite
```

The exporter defaults to `photos/` beside the PDF. Verify exactly one readable JPG for each PDF page, synchronized with the delivered PDF. Existing old `report_pages/` folders are not used as current uploads; leave unrelated user files alone. Never overwrite raw input photos in a populated `photos/` folder: use a separate report output directory or an explicitly designated clean export directory and update the mapping.

Question numbers are identifiers, not necessarily page positions or stable site IDs. Use `qa/question-map.json` plus current question content to resolve the exact JPG for each complex question. If numbers repeat across sections, obtain a clear disambiguated numbering scheme before producing an ambiguous flat JSON; do not silently overwrite keys. Include zero-score required questions, but do not turn informational chapters into questions.

### Fill, upload, save — never submit

- Re-read each current question/section/ID and editable state. Preserve user edits; do not overwrite differing saved answers without reconciling the intended replacement. Do not append duplicate copies on repeated runs.
- Simple text/formula answers: use `answers.json` values and the observed supported editor API/input behavior. Escape prose when creating HTML; use the current verified formula-node mechanism if required. Never directly mutate contenteditable `innerHTML`, blindly use `execCommand`, or upload the whole PDF as an attachment.
- Complex/image-required answers: upload that question's `photos/page-NNN.jpg` through the active question's **photo/image upload** control. Verify selector/accept/mime/context; a generic file picker or attachment button is not sufficient. Required original signed data/waveform images may also be uploaded through the photo channel when requested. If the photo channel is missing, stop that upload and report it—do not switch to attachments.
- Save every authorized answer and image; verify the server-fetched content/image list for the same question, not merely the DOM, a green “已完成”, `process=100`, or an existing answer ID. Reopen/reload only after handling blur autosave deliberately. Keep a per-question save/check result in `qa/` without credentials.
- Retain unsubmitted state. A lock, already-submitted attempt, missing write permission, or an interface that offers only final submit is not a reason to bypass the limit.
- Finish with local deliverable paths, actual saved/not-saved counts and blockers, and: **“已保存，未提交。请逐题检查并自行提交；还有其他需要调整的吗？”** Use “已保存” only for verified saves; accurately name any incomplete items.

## 5. Manual photo-input fallback — report writing only

This is the second choice, not the default workflow. No browser filling, library fetching, or pre-class web answering is performed after this choice.

The user provides only four categories: `Qs/` (complete screenshots/PDF/text questions), the matching instruction book/chapter, the actual data page (PDF/photos), and only necessary experimental photos. File names are flexible; photos may be at root or an input directory. The agent supplies templates/tools, transcribes data, derives the title, and creates all intermediate files. No user-authored JSON/CSV, template, metadata form, or `AGENTS.md` is required.

Use [report-writing.md](references/report-writing.md) and the same student/graph reviews. Ask only for specific missing evidence within those four categories. Generate the same four local deliverables (`report.md`, `report.pdf`, `photos/`, `answers.json`) plus a page map; do not claim anything was filled or saved on the website. Finish by asking the user to review the files, submit/upload themselves, and state any further requirements.

## Resources

- `references/easyketang-relay.md`: access probe, setup help, and mode questions.
- `references/easyketang-library.md`: library inventory, user choice, fresh authenticated acquisition.
- `references/easyketang-preclass.md`: semantic matching, saving, authorized pre-class submission, and actual-score verification.
- `references/easyketang-writing.md`: current editor/formula/image handling and verified saving.
- `references/report-writing.md`, `references/student-writing.md`, `references/graph-review.md`: report construction and quality gates.
- `references/report-outputs.md`: structured input and four-output contract.
- `scripts/build_answers.py`, `scripts/export_pages.py`, `scripts/check_pages.sh`, `scripts/scope_waveforms.py`: local helpers; the CE waveform generator contains illustrative parameters, not new measurements.
- `assets/preamble.tex`, `assets/skeleton.tex`: starter templates; replace example title/parameters.
- `assets/lib_*/manifest.json`: packaged course snapshots; inspect before offering to use one.
