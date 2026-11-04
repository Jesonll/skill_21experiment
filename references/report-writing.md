# Report construction: library-backed or manual fallback

Read `student-writing.md`, `graph-review.md`, and `report-outputs.md` alongside this guide. The relay/manual/task/library choices in `../SKILL.md` happen before this workflow. Generating local files is not evidence that website answers were saved.

## Inputs by mode

**Relay report mode:** selected compatible library/current website provides question statements, instructions, manuals, and source figures. User provides their actual completed data page and required experimental photos. Inspect files first and ask for precise missing measurements/images only when necessary. A blank library record sheet is not this user's experimental record.

**Manual fallback (report only):** only four user input categories: `Qs/` complete question screenshots/PDF/text, matching instruction book, actual data page (PDF/images), and necessary waveform/circuit/instrument photos. Photos may be at root or a subdirectory; names are flexible. No user-authored CSV, JSON, style sheet, `.tex`, manifest, question inventory, or `AGENTS.md` is required. Generate your own work artifacts. Do not fetch or fill website resources in this mode.

Keep raw input photos separate from output `photos/`. If the input directory is already named `photos/`, generate report deliverables in a separate output directory rather than overwriting inputs.

## 1. Inventory and scope

- Read every question, explanatory section, graph requirement, and submission condition. Record question number/section/current ID (when available), required answer elements, evidence, and out-of-scope material. Do not count informational sections as questions or skip zero-score required items.
- Derive experiment title, header, equipment and formulas from the matching manual/questions, not the CE starter. Classify transistor/op-amp/other before selecting domain formulas.
- Read handwritten PDFs as images: text extraction may show a blank table despite handwriting. Render at 300 dpi and crop ambiguous cells at 300–400 dpi. Do not invent an unreadable digit.
- Keep measurements and computation notes outside the report prose. If evidence conflicts, preserve both sources rather than silently overwriting one. Use an explicit calculation baseline for theoretical errors.
- Ask for missing prompts or necessary measurements only after inspecting supplied files. Continue answerable work. Never invent names, IDs, signatures, stamps, or experimental readings; flag submission-form deficiencies separately.

## 2. Calculate and author

Every sentence, table, equation, and figure must answer a prompt element or be its necessary premise. Objectives contain learning goals only. Short answers may leave a page mostly blank.

Use student-style technical reasoning, relevant data and equations, without file-processing narration. Essential uncertainty stays clear and concise; detail belongs in `measurements.md` or `execution-notes.md`. Do not claim observed spikes or phases from an idealized model alone.

Check relevant physics, for example:

- Unit conversion when `|A_u|=U_o/U_i` mixes V and mV.
- For CE circuits only: `I_C=(V_CC-V_C)/R_C`, `I_E=V_E/R_E`, measured `V_C-V_E` versus `U_CE`, fully unbypassed `|A_u|<R_C/R_E`, and `A_u/A_u0≈R_L/(R_C+R_L)`.
- For ideal op-amps only when linear negative feedback holds: virtual short/open, resistor-ratio gains, integration/differentiation signs and frequency dependence. Check saturation/supply limitations before applying linear equations.
- Peak, peak-to-peak, RMS, and DC offset are different quantities. Only a zero-mean sine gives `peak=sqrt(2)*RMS`. A displayed position offset does not establish physical DC bias; distorted-waveform RMS alone does not identify clipping thresholds.

## 3. Four synchronized outputs from the same answers

Author a structured source for `scripts/build_answers.py` as documented in `report-outputs.md`; it is an agent-produced intermediate artifact. It generates `report.md`, exact number-to-string `answers.json`, and `qa/question-map.json`.

Create the LaTeX source from the same approved content. The builder does not render the PDF. `report.md` is the full readable report with figure references; `answers.json` is independently authored plain website prose with `$...$` formulas, not an automatic Markdown stripping result. Complex questions still have meaningful answer strings and a photo delivery mapping.

Expected final layout:

```text
output/
  report.md
  report.pdf
  answers.json
  photos/page-001.jpg ...
  qa/question-map.json
  qa/graph-review.md
```

Update all versions after changes. A Markdown/JSON edit is not applied to the PDF automatically. Recompile, rerender JPGs, update mappings, and recheck any affected website answer before claiming synchronization.

## 4. LaTeX construction

Use a working XeLaTeX/tectonic installation; inspect tools before installing. The former Linux example used tectonic 0.17.0; this is not a requirement to overwrite an existing engine. Bundled templates are `assets/preamble.tex` and `assets/skeleton.tex` relative to the skill root. Copy them into the output workspace, then replace all example title, numbering, circuit and measurement text.

```bash
/tmp/tectonic -X compile report.tex
pdfinfo report.pdf
```

`ctexart`/ctex supplies Chinese fonts in the tectonic bundle; first compilation may download dependencies. Use `amsmath` for actual math, `booktabs` for tables, `pgfplots` for graphs, and `circuitikz` for circuits. Equivalent drawing tools are acceptable if the question permits them and final readability is verified.

One answer per page is the default requirement. Use `\newpage` between answers, `[H]` floats with `float`, or deliberately fixed figure placement so figures do not migrate to another question. Do not duplicate question statements unnecessarily. Page number and question number are separate identifiers: `第\thepage 题` is safe only for sequential one-page questions without extra cover/appendix pages. For nonsequential numbers set the header from the actual question number and use the explicit page map.

If an answer spills: shrink figures only while they remain legible; merge short headings, inline short equations, tighten display skips, and remove irrelevant sentences. Do not delete necessary derivations or compress to unreadable text solely to fit. If requirements cannot fit at readable size, explain the conflict and ask about the pagination tradeoff rather than silently narrowing the answer.

## 5. Graphs and second review

Follow both passes in `graph-review.md` for every plot/panel/schematic. Caption physical meaning and necessary conditions concisely; put production history outside the report. Include original photos in the PDF only if permitted by the prompt; originals can remain local evidence when the report requires drawn graphs only.

- Axes show quantity, unit, ticks, and appropriate ranges. Discrete conditions are not a fictitious continuous dataset. Do not fabricate error bars without measurement uncertainty.
- CSV imports use explicit `col sep=comma` and LF line endings. Put time-axis labels only on the bottom row of multi-row panels to avoid collisions with lower titles.
- Reserve an external legend strip. Nearly coincident signals need distinguishable thin/dashed/marked styles without artificial offsets. Verify actual visibility, not just the number of plotting commands.
- For groupplots, a named shared legend belongs to the panel that actually owns its entries; another empty panel can overwrite a group-wide named legend.
- Circuits require tracing each required wire from endpoint to endpoint and inspecting junctions, crossings, feedback, polarities and units. Layout/source correctness must be checked in the rendered PDF at 250–300 dpi.

`scripts/scope_waveforms.py` has fixed illustrative CE sine-clipping parameters. It is neither an instrument-data extractor nor an op-amp integration/differentiation model. Never reuse those values as new experimental observations.

## 6. Final PDF and JPG verification

1. Confirm question coverage, order, and the exact question-to-page map; page count equality alone cannot prove this.
2. Check fonts embedded, A4 if required, original record image readable, and all critical Ω/μ/±/subscripts present. A successful compile or an absent black box is not grounds to ignore missing-character warnings.
3. Inspect every final page's prose and each graph at normal reading size plus a 250–300 dpi crop. A contact sheet alone is insufficient. Record reviewed PDF version, defects and post-fix result in `qa/graph-review.md`.
4. Export the delivered PDF with `scripts/export_pages.py report.pdf`. Default output is `photos/`, one 300-dpi quality-95 `page-NNN.jpg` per PDF page. Regenerate after any PDF edit; `--overwrite` refreshes an export-only folder and refuses unrelated files.
5. Decode all JPGs, check count/order against the PDF and map, and inspect readable output. Never upload a stale page or raw waveform photo in place of a required full report-page image.
6. The legacy `scripts/check_pages.sh` is only a structural preflight and assumes sequential questions for its printed mapping. Independently check fonts and actual question IDs; it does not prove visual completeness.

Only after local review succeeds may relay mode proceed to editor/image upload and save verification. Manual mode ends with local file delivery and instructions for the user to review/upload/submit themselves. Both modes ask whether further adjustments are needed; neither mode final-submits anything.
