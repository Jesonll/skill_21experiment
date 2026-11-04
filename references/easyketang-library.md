# Easy云课堂 library: discovery and local inventory

This is a portable reference for Easy云课堂 at easyketang.com. It describes observed page structures, not permanent APIs. Never reuse another person's course/class/plan/task/item IDs, tokens, cookies, signed URLs, or account data. Confirm all resources in the current authenticated session; do not use unauthenticated HTTP as a substitute.

## Browser access and privacy

Use the authenticated browser relay first. Read the current `xd://eval/browser` documentation before use; API names and launch setup can change. A typical relay client discovers targets, then opens only the target actually found:

```js
const targets = await browser.targets({ app: { relay: true }, timeout: 20 });
const target = targets.find(t => t.url.includes('easyketang.com'));
if (!target) throw new Error('No authenticated Easy云课堂 tab found');
const tab = await browser.open({ name: 'course-read', app: { relay: true, target: target.target } });
```

If relay is unavailable, ask exactly: **(1) configure the browser relay/full functions, or (2) provide manual inputs for report-only/local work?** Assist with setup if option 1 is chosen. Distinguish relay listener availability, extension connection, and authenticated website access: an active listener alone does not mean a target exists or the user is signed in. Current guides observed Edge extension setup at `edge://extensions`; use current setup instructions and actual installation output, never assume a port, Python environment, extension path, or executable. For other agents, use the host's equivalent authenticated browser-control capability; preserve the same target discovery, session, privacy, and verification rules rather than assuming omp API names.

Do not print request headers, cookies, tokens, full component data, user profiles, or complete network logs. Keep credentials and signed URLs in memory only. Avoid private Vue `$data` exports; inspect only fields needed. Use real DOM state to establish active course, experiment, section, question, and visible status before acting. Private Vue/CSS names and endpoints below are observed implementation details only.

## Discovering a complete resource set

A library is a course-series snapshot, not necessarily a complete question bank. Inventory all experiments and stages, mapping report questions and explanations, preclass questions/options, original instruction books, data-record pages, related courseware, images, source, and verification status. Preserve original course Unicode. Layout convention: `lib_<UTC generation time>_<exact website series name>/` with `README.md`, `manifest.json`, `checksums.sha256`, `preclass_answers.json`, per-experiment resources under `experiments/labNN/`, and optional `verified_answers/` evidence.

Observed page hierarchy: course map → experiment → stages/resources. Stage names and order vary. A report may not be titled “实验报告”; inspect every stage and associate by current title, category, and experiment. Report content includes explanatory sections as well as questions; preserve explanations but do not count them as questions. Do not start/create/restart a quiz just to get data. If permitted data are unavailable, record that gap.

Observed category IDs (report 11, document 13, preclass 4, video 6), routes, endpoints, and Vue component structure are not contracts. Inspect live DOM and current requests; derive IDs and URLs from this session, never guess. In observed versions, read-only GETs included `/admin/task_lite/new_query` (course map), `/admin/task_item/get_nnew_list_item` (experiment stages/resources), `/admin/resource_lite/get_resource` (resource), and `/admin/new_interact_page/get_list_item` (report sections/questions). Confirm method, URL, parameters, and current page relationship before reading. Report sections may have no `resource` yet contain instructions. Do not dump whole responses: they may include student answers, identity, or credentials.
### Observed response shapes and guarded access

These schemas are historical observations; inspect current responses and the visible page before relying on them. `/admin/task_lite/new_query` returns the course-map experiments. `/admin/task_item/get_nnew_list_item` returns `data.task_item`, historically either an array or grouped `{experiment: [...], no_experiment: [...]}`; flatten groups, then inspect each stage's `resource`. `/admin/resource_lite/get_resource` reads one resource. `/admin/new_interact_page/get_list_item?item_id=...` returns section array at `data.data`; only traverse question resources when present, while retaining resource-less explanatory sections. Resource rows historically expose `id`, `filename`, `category_id`, and document `content`; report rows commonly expose `question`, `question_detail`, `content`, `options`, `score`, `type`. Do not assume fields or IDs without current evidence.

Confirm request URL/method in the current page's traffic, filter in memory, and never print full request objects. For a protected read, keep navigation and read inside the same run; this observed Puppeteer pattern aborts non-read verbs but is not a guarantee against side effects:

```js
const result = await tab.run(async ({ page, tab }, observedUrl) => {
  const blocked = [];
  await page.setRequestInterception(true);
  page.on('request', req => {
    if (!['GET', 'HEAD', 'OPTIONS'].includes(req.method())) {
      blocked.push({ method: req.method(), path: new URL(req.url()).pathname });
      return req.abort();
    }
    return req.continue();
  });
  // URL must be derived from the actual current page request, not a copied ID.
  const data = await tab.evaluate(`(async () => {
    const response = await fetch(${JSON.stringify(observedUrl)});
    if (!response.ok) throw new Error('HTTP ' + response.status);
    const json = await response.json();
    if (json.status !== 1) throw new Error('Site read failed');
    // Example only for the observed stage/resource-list schema. Project only
    // needed fields before crossing the page boundary; never export all json.data.
    const groups = json.data.task_item;
    if (!groups) throw new Error('Expected stage/resource list; inspect the current schema');
    const stages = Array.isArray(groups) ? groups : Object.values(groups).flat();
    return stages.flatMap(stage => (stage.resource || []).map(r => ({
      stage: stage.name, id: r.id, title: r.filename, category: r.category_id
    })));
  })()`);
  return { data, blocked };
}, { args: [observedUrl] });
```

This example deliberately omits resource URLs and personal/student-answer fields. Inspect document URLs only in session memory for immediate authenticated download. For report/quiz extraction, use a separate schema-specific projection of question stems, options, formulas, images and permitted answer-key content rather than reusing an unrestricted response dump.

The raw request listener is scoped to this `tab.run`; do not assume protection survives a later call. A GET may still mutate state. Do not navigate into a quiz to obtain a paper; observed exam-page opening sent a paper-initialization POST. Record blocked writes and stop if the guard breaks the page rather than allowing writes.

For an observed PDF URL, fetch bytes in the authenticated page and validate status and `%PDF-` before saving locally; do not use page filesystem access or expose a signed URL. Example small-file transfer:

```js
const encoded = await tab.evaluate(`(async () => {
  const r = await fetch(${JSON.stringify(documentUrl)});
  if (!r.ok) throw new Error('PDF HTTP ' + r.status);
  const bytes = new Uint8Array(await r.arrayBuffer());
  if (new TextDecoder().decode(bytes.subarray(0, 5)) !== '%PDF-')
    throw new Error('Not a PDF');
  let binary = '';
  for (let i = 0; i < bytes.length; i += 32768)
    binary += String.fromCharCode(...bytes.subarray(i, i + 32768));
  return btoa(binary);
})()`);
await Bun.write(outputPath, Buffer.from(encoded, 'base64'));
```

Then parse the local PDF and verify readability. This is not a streaming downloader. Retain each document's actual kind/title; never substitute a PPT or record page for an instruction book.

Preserve original rich HTML and extracted text. Decode empty formula elements such as `data-w-e-type="formula"` using their `data-value` into `$...$`; retain tables, paragraphs, and superscripts/subscripts. Inventory images in question, option, and explanation content; download through authenticated browser when available, validate, and rewrite local links. `file:///C:/...` indicates an author-local inaccessible file, not a resource URL; report it missing. Distinguish instruction books, record sheets, and slides; validate document type/content. Never strip signatures from signed resource URLs. Keep source provenance and distinguish `site_provided_key`, `derived`, and `score_verified`; a site answer key is not independent proof of correctness.

GET does not guarantee zero side effects: reports may record time, document viewing may record progress, and quiz pages may initialize a paper. Avoid quiz navigation when strict read-only access matters. A request interception guard may be useful, but observed relay route abort rules did not reliably block POST; only use a currently documented, verified guard and do not claim it guarantees no side effects. No saving, upload, quiz start/create/submit, report submit/resubmit, grade overwrite, station selection, or equipment control as part of discovery. Leave the user's tabs open and return borrowed tabs to the course map when safe.


For report mode, inspect this bundled library first and disclose its limits (including missing images and answer-verification coverage); then ask whether to use the current library or fetch a new one. A new fetch is not implied by report help and must use current authenticated-page evidence, never copied source IDs.
## Bundled inventory and evidence limits

The portable copy is [`../assets/lib_20261024T143310Z_电路与电子技术实验I/README.md`](../assets/lib_20261024T143310Z_电路与电子技术实验I/README.md); consult its manifest for exact paths and coverage. Its recorded inventory is 8 experiments, 80 current preclass questions with 80 content-based answers, 78 report questions/steps, 8 instruction books, 8 data sheets, and 3 related courseware files. Thirty answers across experiments 6–8 have historical independent derivation and 100-point score evidence; the other 50 answers were not independently score-verified. Preserve these as historical evidence only; they do not verify a current user's answers or grades. Nine theory images inaccessible from author-local Windows temporary paths remain explicitly missing (2 in experiment 1, 7 in experiment 7); do not fabricate replacements. No fresh website fetch or new verification is claimed by this reference.