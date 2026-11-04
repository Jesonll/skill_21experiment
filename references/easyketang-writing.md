# Easy云课堂 report writing

Use report resources and library under [`easyketang-library.md`](easyketang-library.md); identify the user's specific task first. If unclear, ask whether they want pre-class work or report writing/answering. This reference does not authorize final report submission or resubmission.

## Relay access and privacy

First probe the authenticated browser relay and read current `xd://eval/browser` documentation. Listener availability, extension connection, target discovery, and authenticated website access are distinct. Never hardcode a port, executable, install path, or Python environment from an example. If relay unavailable, ask exactly: **(1) configure the browser relay/full functions, or (2) provide manual inputs for report-only/local work?** Assist with setup if option 1. Other agents use their host's equivalent authenticated browser-control API while preserving these safeguards. Discover targets rather than guessing IDs; establish active report/question/editor through actual DOM and visible content. Do not expose tokens, cookies, account data, signed URLs, or entire Vue state. Never bypass disabled/locked editing or a prior submission state.

## Prepare four local deliverables

Create `report.md`, `report.pdf`, `photos/page-NNN.jpg`, and `answers.json`. JSON uses question-number string keys mapped to answer strings; prose is plain text and formulas use single-dollar `$...$` only—no Markdown or block LaTeX. Complex answers requiring an image must upload the corresponding JPG through the PHOTO channel, never as an attachment; narrow the image-only file selector to the active question before choosing its image. Simple answers use text in the editor. Do not attach an image where the requirement is text-only. The bundled library `report_questions` guides requirements but does not include student answers or authorize submission.

## Editor behavior and writing

Observed page versions use wangEditor with Slate. Update editor state through its documented/current editor API (historically `editor.setHtml(html)`), not direct `contenteditable.innerHTML` or `execCommand`. Read current API behavior before use. For plain text, construct DOM nodes and set `textContent`; do not interpolate unescaped user text into HTML. Preserve existing content by default; replacing it requires explicit user instruction. Verify current question ID, prompt, section, and enabled state immediately before editing. IDs and Vue/CSS selectors are volatile. After editing, verify runtime editor `getHtml()`/`getText()`, visible DOM, and that the active question model's answer equals editor HTML. Do not treat a delay or DOM alone as proof.

Blur and navigation can save even without clicking a save button. In observed implementation, editor change updated the model and blur called answer-save logic; therefore editing/blur, switching questions, or dismissing a tab can persist content. A relay request-interception listener was observed to exist only within its run; prior experiments did not show that a broad POST abort reliably prevents writes. Never promise a draft remains unsaved based only on no save-button click or a temporary guard. Do not deliberately blur/navigate away to test. If retaining an unsaved draft, warn that it may persist, and keep its tab state rather than triggering blur.

## Active-question image upload

The observed picker was `input[type=file][accept*="image"]`, but a page may expose several such inputs. Inspect actual file inputs and their `accept`/visibility/association in the current question UI, then narrow the selector to the active question's image-only input before using the current relay `tab.uploadFile` API. Never upload through a broad selector if it could target another question or a general attachment. The historical call shape was `await tab.uploadFile(selector, absoluteJpgPath)`; confirm current API documentation. Use only the requested corresponding JPG, through the PHOTO channel (not attachment); verify after selection that the UI associates it with the active question. After authorized save, compare server `student_wd_imgs` for that active question. Do not remove existing images unless explicitly requested.

Observed page model was `page.dataList[sectionIndex].resource[questionIndex]`; inspect the active item and its `student_wd_imgs`, along with `student_wd_answer` and `process`. The index layout and selector are implementation details: establish the active question via real DOM and prompt, and never infer association from an index alone.
## Upload, save and verify

Upload only the required corresponding JPEG, with the image picker scoped to the active question (not every image selector on the page). Confirm the selected file, question association, upload result, and resulting server-side image list. For permitted text saves, use the current page's intended save behavior only after authorization; saving a question is not report submission. Re-read the server state using a request observed in the active session, match by current question, and compare saved answer content and images to intended values. Process/completion flags alone may predate this work and are not proof. Keep secrets out of logs and artifacts. Never final-submit, resubmit, overwrite grades, or infer permission to submit from permission to edit/save.

After the permitted save, verify server-stored answer content and uploaded images, not merely editor state or old process flags. Ask the user to review and submit the report themselves; then ask whether they have other requirements. Do not claim that local PDF or local files were saved remotely.


Observed current-component discovery (selectors/private Vue links are version-dependent):

```js
const state = await tab.evaluate(`(() => {
  const page = document.querySelector('.stepBox')?.__vue__?.$parent;
  const editor = document.querySelector('.wangEditor')?.__vue__?.editor;
  if (!page || !editor) throw new Error('Report/editor not ready');
  const item = page.dataList[page.nowIndex]?.resource?.[page.nowIndex1];
  if (!item) throw new Error('No active question');
  return { questionId: item.id, questionHtml: item.question, disabled: editor.isDisabled(),
    section: page.nowIndex, question: page.nowIndex1,
    text: editor.getText(), html: editor.getHtml(), is_sub: page.is_sub,
    is_again: page.is_again };
})()`);
```

Compare returned question identity/prompt to the visible DOM before writing. Never use an example number or ID. A disabled editor or locked report means stop, not enable/bypass. Only use `tab.evaluate` for these `__vue__` properties; historical `page.evaluate` did not expose them.

For plain prose, create paragraph nodes and assign `textContent`, letting the DOM serialize escaping; never concatenate raw user text into HTML. Preserve current HTML unless replacement was explicitly requested:

```js
const result = await tab.evaluate(`(() => {
  const page = document.querySelector('.stepBox').__vue__.$parent;
  const editor = document.querySelector('.wangEditor').__vue__.editor;
  const item = page.dataList[page.nowIndex]?.resource?.[page.nowIndex1];
  if (item?.id !== ${JSON.stringify(targetQuestionId)} || editor.isDisabled())
    throw new Error('Active question mismatch or editor disabled');
  const fragment = document.createElement('div');
  for (const line of ${JSON.stringify(text)}.split(/\\r?\\n/)) {
    const p = document.createElement('p');
    if (line) p.textContent = line; else p.append(document.createElement('br'));
    fragment.append(p);
  }
  const before = editor.getHtml();
  editor.setHtml(before + fragment.innerHTML);
  return { html: editor.getHtml(), text: editor.getText(), model: item.student_wd_answer };
})()`);
```

Formula nodes observed in source HTML may be empty spans with `data-w-e-type="formula"` and LaTeX in `data-value`. Plain text conversion loses that value. Do not assume `$...$` in input automatically renders as a formula. Use a runtime editor-supported formula insertion/API verified for the current editor version; then inspect `getHtml()`, rendered DOM, and model to confirm it survived. If the editor cannot safely create the formula node, stop and retain it for user review instead of fabricating markup.

Only when the user explicitly permits saving, and only for the verified active question, the historically observed page handler was `page.saveQaAnswer(item.student_wd_answer, item, page.nowIndex, page.nowIndex1)`. It is not final submission. Never use `saveHtmlCont` for an answer. After it returns, confirm the intended current session GET (URL discovered from `tab.requests()`; never print URL/token) and verify server question content by ID:

```js
const stored = await tab.evaluate(`(async () => {
  const r = await fetch(${JSON.stringify(observedQuestionReadUrl)});
  if (!r.ok) throw new Error('Question reload HTTP ' + r.status);
  const json = await r.json();
  if (json.status !== 1) throw new Error('Question reload failed');
  const q = json.data.data.flatMap(s => s.resource || [])
    .find(q => q.id === ${JSON.stringify(targetQuestionId)});
  if (!q) throw new Error('Question absent from server response');
  return { answer: q.student_wd_answer, images: q.student_wd_imgs };
})()`);
```

Compare `stored.answer` and image list with the intended values; flags such as `process=100` can predate the current action. The URL is sensitive and must remain in memory. A browser navigation/blur may itself save, so don't force blur to validate.
After the permitted save, verify server-stored answer content and uploaded images, not merely editor state or old process flags. Ask the user to review and submit the report themselves; then ask whether they have other requirements. Do not claim that local PDF or local files were saved remotely.