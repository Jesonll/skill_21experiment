# Generated report and answer outputs

`scripts/build_answers.py` converts an agent-authored UTF-8 JSON working artifact into `report.md`, `answers.json`, and `qa/question-map.json`. The JSON source is an internal agent artifact, not an additional user input category. It has no browser access and performs no uploads or submission.

Run from the report workspace (or specify `--out-dir`):

```sh
python3 "$SKILL_DIR/scripts/build_answers.py" answers-source.json
```

The source object has a non-empty `title` and a non-empty `questions` array. Each question has a unique `number` (integer or string), non-empty `title`, non-empty report `answer` in Markdown, explicitly authored non-empty `web_answer`, positive integer `page`, and `delivery` equal to `text` or `photo`.

```json
{
  "title": "实验报告",
  "questions": [
    {
      "number": 2,
      "title": "实验结果",
      "answer": "由测量可得，增益为 $A_u=U_o/U_i$。",
      "web_answer": "测得增益为 $A_u=U_o/U_i$，结果与理论值接近。",
      "page": 1,
      "delivery": "text"
    },
    {
      "number": "5(b)",
      "title": "分析波形",
      "answer": "输出近似为三角波。",
      "web_answer": "输出近似为三角波，换向处变化较快。",
      "page": 2,
      "delivery": "photo"
    }
  ]
}
```

Question numbers need not be sequential; surrounding whitespace is trimmed. Duplicate normalized/stringified numbers and duplicate JSON fields are rejected. Pages must be 1, 2, … in question-array order to enforce one answer per report page. `answers.json` is exactly a JSON object mapping question-number strings to `web_answer` strings: no metadata wrapper. `qa/question-map.json` records each number, page, delivery and a `photo` path (`photos/page-NNN.jpg`) for photo delivery; text delivery uses `null`. Both simple and complex answers appear in this map. All files are UTF-8. The builder validates the complete input before touching output files; malformed input does not create or partially update outputs.

`web_answer` must be authored separately as plain prose plus optional single-line `$...$` formulas. It is not derived by stripping report Markdown. Outside formulas, Markdown headings, tables, images, links, emphasis, inline code, list/quote markers, fences, HTML, `\(...\)`, `\[...\]`, and document/display math environments are rejected. Numbered prose such as “1. …” is allowed. Formula contents are preserved literally, including TeX commands such as `\frac`, Unicode, and HTML-significant characters. Dollar signs are reserved as formula delimiters; write literal currency-dollar text in words or another unambiguous form. Unmatched, doubled (`$$`), multiline or empty formulas are rejected. This validation does not parse TeX or prove the website supports every formula; inspect rendering in the actual editor. Never use the absence of a validator error as evidence of website save success.

## Safe editor bridge

For simple (`text`) answers, enter the authored prose in the website's answer editor and insert formulas only through the site's verified formula-element API/editor controls. Do not dump `report.md` or unescaped source into HTML. Treat prose as text and escape it for the specific editor/API boundary; formula insertion must use the editor's actual formula-element mechanism, not HTML interpolation. Confirm in the live editor that prose characters remain literal and inspect each rendered formula. `$...$` is this JSON interchange convention only: never claim it automatically renders on the website without inspecting the result. Complex answers use the corresponding `photos/page-NNN.jpg` through the PHOTO upload channel, not an attachment.

Save report changes and verify the server's persisted state. Never final-submit or resubmit an experiment report or overwrite its grade; leave report review and final submission to the user. Pre-class quizzes use the separate authorized-submission and actual-score workflow in `easyketang-preclass.md`; report outputs do not confer submission permission.

## Scope of generated files

This utility generates only `report.md`, `answers.json`, and `qa/question-map.json`. The complete task deliverables remain `report.md`, `report.pdf`, `photos/page-NNN.jpg`, and `answers.json`. PDF rendering remains the existing LaTeX workflow; this tool does not produce a PDF or photo pages. Generate and inspect those separately, then follow the relay-first website workflow for server persistence and verification.
