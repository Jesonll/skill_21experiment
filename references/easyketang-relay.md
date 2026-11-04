# Easy云课堂 browser relay

For Easy云课堂 at easyketang.com, the first probe is an authenticated browser relay. Read the current `xd://eval/browser` documentation before using omp's browser API: APIs and setup evolve. This is skill documentation only; it does not access a live account or authorize mutations.

## Availability is layered

Treat these as separate checks: (1) relay listener/service is running, (2) browser extension is connected, (3) relay can discover a real target, and (4) that target has authenticated Easy云课堂 access. A port responding does not prove the extension is connected; an empty target list is not proof the user is logged out. Use current setup procedures and their observed output. Historical examples such as a specific port, `py_da` environment, or extension directory are environment observations, not requirements. Do not guess target IDs, use unauthenticated curl, or operate a different user's session.

If relay is unavailable, ask exactly: **(1) configure the browser relay/full functions, or (2) provide manual inputs for report-only/local work?** For option 1, assist with setup using current documented tools; do not ask the user to do steps the agent can perform. For option 2, work only from the four supplied categories (`Qs/`, manual, data, necessary photos) and produce local outputs; no site operations. For agents without omp, use the host's equivalent authenticated browser-control interface, keeping the same target discovery and safety rules; do not assume its method names match omp.

## Discover, inspect, protect

Typical current omp shape, subject to current docs:

In the documented setup observed for this environment, `omp browser-relay --help` reports actions `serve|install`; install the extension with `omp browser-relay install`, then run `omp browser-relay` to serve. Treat these commands as observed omp CLI behavior and re-check `--help` before use. Follow the install output to load the unpacked extension in Edge via `edge://extensions`, enable it, and sign in to Easy云课堂 normally. The relay service alone is insufficient. After setup, prove it works by discovering a target and checking its URL/title and authenticated page DOM; never print credentials or assume a target from a label. If discovery is empty, distinguish stopped relay from unloaded/disconnected extension and logged-out website before retrying.

```js
const targets = await browser.targets({ app: { relay: true }, timeout: 20 });
const target = targets.find(t => t.url.includes('easyketang.com'));
if (!target) throw new Error('No authenticated Easy云课堂 target found');
const tab = await browser.open({ name: 'course-read', app: { relay: true, target: target.target } });
// Inspect locally; do not print full URLs (which may contain session parameters).
const proof = await tab.evaluate(`({ title: document.title, host: location.hostname,
  body: document.body.innerText.slice(0, 1500) })`);
if (!(proof.host === 'easyketang.com' || proof.host.endsWith('.easyketang.com')))
  throw new Error('Unexpected site');
// A nonempty login page is NOT authenticated access. Inspect the current course
// list/map and its requested course using tab.observe()/actual DOM before passing.
// Do not infer authentication from hostname, title, or nonempty body alone.
```


Use only a discovered target; alternatively create a separate tab in the authenticated session using current documented API and a URL discovered from the user's current resources. Preserve the user's original tabs and sessions; do not close their tabs or sign out. Do not print cookies, authorization headers, tokens, signed URLs, personal data, full request logs, or entire Vue component state. Inspect only necessary fields and keep secrets in memory. Verify real DOM content and visible state for course, experiment, current question, and editor; private Vue properties, selectors, endpoints, and category numbers are version-specific. Re-read after navigation or question changes.

The website may write state without an explicit save click: report views can record time, document views progress, and quiz-page entry can initialize a paper. GET does not establish zero side effects. A previously observed request abort route did not reliably block POST; guards are run-scoped and must not be represented as a durable sandbox. If a protected read is needed, use current documented controls and inspect what was blocked; on unexpected state change or guard-related breakage, stop rather than enabling writes to clear an error.

When task is unclear, ask whether the user wants pre-class work or report writing/answering. For report mode, inspect the bundled library and disclose its condition before asking: **use the current library, or fetch a new one?** Never silently fetch. A fetch must use the active authenticated session and session-local evidence; no source IDs copied from historical guides.

## Permission boundary

The relay-first workflow is not permission to mutate. Creating/starting/restarting quizzes, saving answers, uploads, equipment control, and station selection require applicable user authorization. For pre-class quizzes only, explicit user authorization (including an applicable standing instruction) permits the agent to submit a reviewed, server-save-verified attempt and read its actual score under `easyketang-preclass.md`; a save-only request overrides that permission. Do not automatically retry, resubmit, or overwrite a grade. Experiment-report final submission and resubmission are always prohibited by this skill: save and verify the report, then leave final submission to the user. Library acquisition never authorizes quiz submission. Never claim server saving, submission, or a 100/full-mark result from a local editor, model, completion flag, or historical score; report verified state and ask whether further requirements remain.

When the task is unknown, ask whether the user wants pre-class work or report writing/answering. For report mode inspect bundled assets/lib first, disclose the library's condition, and ask whether to use the current library or fetch a new one. A fresh fetch is a separate authorized activity, not implied by this reference; use current session and current page evidence, never historical source IDs. See [`easyketang-library.md`](easyketang-library.md), [`easyketang-preclass.md`](easyketang-preclass.md), and [`easyketang-writing.md`](easyketang-writing.md).