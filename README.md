# cn-lab-report — Easy课堂实验助手

Default: connect to the user's **Easy雨课堂 / Easy云课堂** through a browser relay, then either save pre-class answers or write and save experiment-report answers. **Never final-submit.** Manual file/photo input remains the second, report-only choice.

## Example directories — start here

### Website mode (default)

The skill contains a course library; the user normally supplies only their actual experiment measurements/photos and identifies the desired course/experiment/task if it is not clear from the page.

```text
my-experiment/
├── 原始数据记录页.jpg             # actual filled experimental record; not a blank library sheet
├── raw_photos/                  # only necessary measured waveform/circuit photos
│   ├── 积分.jpg
│   └── 微分.jpg
└── output/                      # created by the agent, not supplied by the user
    ├── report.md
    ├── report.pdf
    ├── answers.json             # {"question number": "plain prose with $formula$"}
    ├── photos/
    │   ├── page-001.jpg         # full PDF page, 300 dpi, in PDF order
    │   └── ...
    └── qa/
        ├── question-map.json    # actual question -> PDF page -> text/photo delivery
        ├── graph-review.md
        └── web-save-checks.json # generated save-verification record, when website filling occurs
```

Pre-class-only work does not need an experimental data page or a fabricated report. It uses the current website questions and matched library answers, saves editable selections, and stops before final submission.

### Manual mode (second choice, report writing only)

```text
my-experiment/
├── Qs/                          # complete question screenshots, PDFs, or text
│   ├── 01.jpg
│   └── ...
├── 实验指导书.pdf                 # matching instruction book/chapter
├── 原始数据记录页.pdf             # filled data page; PDF/images accepted
├── raw_photos/                  # necessary photos only; may also be at root
│   └── 波形.jpg
└── output/                      # agent generates the same four report deliverables
    ├── report.md
    ├── report.pdf
    ├── answers.json
    ├── photos/page-001.jpg ...
    └── qa/question-map.json
```

Names are examples, not mandatory filenames except the conventional `Qs/`. A photo folder is optional when no question needs photos. Keep raw photos separate from exported `photos/`; if inputs already live in `photos/`, use a separate output directory. No user-authored template, LaTeX source, CSV/JSON transcription, manifest, metadata form, or `AGENTS.md` is required.

## 1. Interaction order

### Step 1 — test real relay access

The agent reads the host's current browser-control documentation and checks service, extension, target discovery, logged-in state, and actual course access. A listening port is insufficient.

- **OMP:** `xd://eval/browser`, `browser.targets({app:{relay:true}})`, and the `omp browser-relay` CLI/extension.
- **Other agents:** their available authenticated-browser relay/extension with equivalent discovery and session safeguards; do not assume OMP API names exist.

If unavailable, the agent asks:

1. **配置 relay，使用完整功能** — assist with setup and login, then verify access again.
2. **手动提供材料，仅写报告** — use the manual input tree above; no pre-class web answering, resource fetching, or website filling.

An explicit manual-only request already selects option 2. Otherwise do not skip the probe and silently fall back.

### Step 2 — help with setup if selected

Check installed tools and `omp browser-relay --help`. The observed CLI supports:

```bash
omp browser-relay install   # installs extension files and prints browser loading instructions
omp browser-relay           # starts the relay service
```

Use actual installation output, not a historical hardcoded port/path. Guide the user through loading the extension and logging in in their browser; do not request credentials in chat. Other hosts use their extension's supported setup. Settings changes need the user's approval. Re-probe the actual site before claiming success. See [relay guide](references/easyketang-relay.md).

### Step 3 — choose task if not already specified

After readiness, ask only if the task is unknown:

1. **课前预习题作答**.
2. **实验报告编写与题目作答**.

Do not ask again when the user has already chosen. If course/experiment is ambiguous, resolve that before any answer write. Manual mode supports only local task 2.

### Step 4 — disclose and select the library

Before report drafting, inspect `assets/lib_*/manifest.json`, disclose the library's course/version, time, coverage, verification and missing-resource conditions, then ask:

1. **使用当前资料库**.
2. **重新获取资料库**.

Do not assume newest means compatible. If no usable library exists, explain that the current-library option cannot supply the target resources. A fresh fetch uses the current logged-in session and discovered resource IDs; it does not start/submit a quiz to obtain a score. Store a new timestamped library instead of overwriting the snapshot.

The included snapshot is `lib_20261024T143310Z_电路与电子技术实验I`: 8 experiments, 80 pre-class questions/answers, 78 report entries and 8 manuals. Thirty answers have historical independent/100-point evidence; 50 were not independently score-verified; nine theory images were unavailable. Read the real manifest at use time and compare to the current course. The library does not contain this user's filled report or measurements.

See [library acquisition](references/easyketang-library.md).

## 2. Pre-class questions: match, select, save, stop

Read [pre-class workflow](references/easyketang-preclass.md). Question and option order may change. Match the complete current stem, formulas, image semantics, type, and option **contents**, then obtain current indices. Never reuse A/B/C/D, stored question numbers, source IDs or array positions as answers.

Use the site's observed option/save handlers, account for multiple-choice toggles, and verify the persisted answer contents. A historical handler named `submit(index)` may save one option; inspect actual behavior and do not confuse it with final submission. Do not restart completed attempts or begin a new timed/limited attempt without applicable authorization.

Stop before final 交卷/提交/再次提交, grade overwrite, or submission confirmation. Leave the saved answers for the user to inspect and submit personally. Do not claim a new score.

## 3. Report mode: prepare all versions before filling

Use selected library/manual/current prompts plus actual user measurements. Ask only for precise missing personal data or necessary photos after inspecting available files. Then:

1. Inventory questions and requirements; derive the experiment header from the correct materials.
2. Transcribe measurements, calculate results, and author concise student-style answers.
3. Generate **`report.md`, `report.pdf`, `photos/`, `answers.json`**, with `qa/question-map.json` linking numbers, pages and delivery routes.
4. Check every question's scope, formulas and figures. Perform scientific and rendered second review of each graph; inspect nearly overlapping lines, wires, labels and legends.
5. Reconcile all versions and only then fill the current website.

Details: [report construction](references/report-writing.md), [student writing](references/student-writing.md), [graph review](references/graph-review.md), and [output schema](references/report-outputs.md).

### Website JSON grammar

```json
{
  "1": "掌握集成运放的基本运算功能与正确使用方法。",
  "3": "由虚短、虚断可得 $u_o=2(u_{i2}-u_{i1})$。",
  "5": "积分电路中，方波输入对应近似三角波输出。"
}
```

- Keys are question-number strings; values are independently authored website-answer strings, including for photo-routed questions.
- Normal prose is literal text, formulas alone use single `$...$` delimiters. No Markdown headings/bold/tables/images, HTML, `$$`, document LaTeX, `\(...\)` or `\[...\]`.
- Formula contents may use supported TeX, e.g. `$A_u=\frac{U_o}{U_i}$` (escape backslashes correctly in JSON files).
- Do not assume pasted dollar strings automatically render on the site. Inspect the current editor's supported formula insertion and verify the displayed formula/model after writing.
- Nonsequential question numbers need an explicit page map. Repeated numbers across sections need disambiguation rather than silently overwriting JSON keys.

### Local helpers

`SKILL_DIR` is the installed skill's absolute path. The agent creates the structured source; the user is not asked to provide it.

```bash
python3 "$SKILL_DIR/scripts/build_answers.py" answers-source.json --out-dir output
# Compile report.tex from the same approved content using a working XeLaTeX/tectonic engine.
python3 "$SKILL_DIR/scripts/export_pages.py" output/report.pdf
# After PDF changes:
python3 "$SKILL_DIR/scripts/export_pages.py" output/report.pdf --overwrite
```

`build_answers.py` creates Markdown, website JSON and page/route mapping; it does not create PDF/JPGs. The exporter defaults to `photos/` beside the PDF, quality 95 and 300 dpi, with ordered `page-NNN.jpg` names. It refuses to overwrite raw or unrelated files. The old `report_pages/` convention is superseded for newly generated outputs; existing old report folders are left untouched.

## 4. Website answer delivery: text or PHOTO, never attachment

Read [website writing guide](references/easyketang-writing.md) before editing.

- **Simple answer:** enter the authored text/formulas via the current supported editor behavior/API. Use safe escaping, not direct contenteditable HTML mutations or blind Markdown pasting.
- **Complex answer / graph / circuit / long table / image requirement:** upload the question's matching `photos/page-NNN.jpg` using the active question's **photo/image upload channel**. **Do not use the attachment upload channel**, even if it accepts JPG or PDF. Required original record photos may also be uploaded through the image channel when the question asks for them.
- Re-read current question/section/ID and editor status, preserve existing user answers, and reconcile differences before replacement. Do not bypass locked/disabled editors or append duplicate text on reruns.
- Verify uploaded image identity/count and server-saved content for each question after saving. `process=100`, “已完成”, an existing answer ID or editor DOM alone may be stale.
- Be aware blur/navigation can autosave. Permission to edit a demonstration does not imply saving; this normal answering workflow saves only the task-authorized content. Permission to save never permits final submission.

If the image channel is absent or saved state cannot be verified, report the exact blocker; never silently use attachments or claim success. Record actual per-question save results without credentials.

## 5. End state and handoff

Both website tasks stop before final submission. Do not click final submission, confirm it, resubmit, or overwrite scores. Historical source guides may mention authorized score verification; that is not an action this skill performs.

Finish with output paths (report tasks), verified save counts, uncompleted items and a truthful handoff:

> 已保存，未提交。请逐题检查并自行提交；还有其他需要调整的吗？

Use “已保存” only for verified saves; name any partial failures. In manual mode say files were generated locally, not saved on the website, and ask the user to review/upload/submit themselves.

## 6. Installation and tools

Install the package at `<project>/.omp/skills/cn-lab-report/` or `~/.omp/skills/cn-lab-report/`. Skills are discovered at session start; restart/reload the host as needed. Invoke `/skill:cn-lab-report`, request it by name, or read `skill://cn-lab-report` if available. Other hosts follow their skill-discovery convention.

Runtime needs: a supported authenticated relay/browser extension for website mode; a Chinese-capable LaTeX engine, Poppler utilities (`pdfinfo`, `pdftoppm`, etc.) and Python 3 for local output helpers. Reuse installed tools; setup is agent-side work, not extra experimental input. No special historical Python environment, browser profile, port or machine-specific path is mandatory.

## 7. Package tree

```text
cn-lab-report/
├── SKILL.md
├── README.md
├── references/
│   ├── easyketang-relay.md
│   ├── easyketang-library.md
│   ├── easyketang-preclass.md
│   ├── easyketang-writing.md
│   ├── report-writing.md
│   ├── report-outputs.md
│   ├── student-writing.md
│   └── graph-review.md
├── scripts/
│   ├── build_answers.py
│   ├── export_pages.py
│   ├── check_pages.sh
│   └── scope_waveforms.py
└── assets/
    ├── preamble.tex
    ├── skeleton.tex
    └── lib_20261024T143310Z_电路与电子技术实验I/
        ├── manifest.json
        ├── preclass_answers.json
        ├── checksums.sha256
        ├── experiments/
        └── verified_answers/
```

Core requirements are directly in `SKILL.md`; supporting references are loaded explicitly. No root or copied workspace `AGENTS.md` is needed. Templates and CE examples are agent resources, not measured defaults for new experiments. Bundled library IDs are historical provenance only, never current-account locators.
