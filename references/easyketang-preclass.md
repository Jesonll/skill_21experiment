# Easy云课堂 preclass workflow

Use this only after identifying the user's task. If unclear, ask whether they want pre-class work or report writing/answering. Check the series/experiment against [`easyketang-library.md`](easyketang-library.md) and the bundled library manifest; do not choose solely by newest timestamp. When reporting answers, state their provenance and distinguish local material from current server state.

## Relay and session

Probe the authenticated browser relay first; read current `xd://eval/browser` docs. A listener, connected extension, discovered tab, and authenticated website are separate states. Do not assume an example port, install directory, Python environment, or extension. If relay is unavailable, ask exactly: **(1) configure the browser relay/full functions, or (2) provide manual inputs for report-only/local work?** Assist with setup for option 1. Other agents should use their own equivalent authenticated browser-control API, preserving the same discovery, privacy, and safeguards. Never print credentials, tokens, user data, or complete request logs. Use actual visible DOM to verify current course, experiment, question and options; observed component APIs are version-dependent.

## Match answers by meaning

Quiz question and option order may change between attempts; this is a reported property of the bundled source, not a universal promise. Match current complete question wording, formulas, image meaning and type to a unique library item. Normalize harmless whitespace/width only: never erase negation, signs, inequalities, units, indices, or formula meaning. Then match correct answer content against the current option contents. Never use saved question IDs, array positions, or A/B/C/D as stable keys. For image/formula options, inspect semantics. For multi-select, match the full content set. Stop if no unique match, changed content, ambiguity, or conflict; investigate rather than guess.

For text-only choices, match contents rather than positions:

```js
function matchTextOptions(currentTexts, correctTexts) {
  const norm = s => s.normalize('NFKC').replace(/\s+/g, '');
  const actual = currentTexts.map(norm);
  const indexes = correctTexts.map(answer => {
    const hits = actual.flatMap((s, i) => s === norm(answer) ? [i] : []);
    if (hits.length !== 1) throw new Error('Answer option absent or ambiguous');
    return hits[0];
  });
  if (new Set(indexes).size !== indexes.length) throw new Error('Duplicate option match');
  return indexes;
}
```

Never normalize away negation, signs, units, subscripts, or formula/image semantics. For multi-select, derive the wanted set from correct contents and compare it to currently selected contents; toggle only the symmetric difference. Since a click can deselect, never click every correct option unconditionally. Re-read selected contents after each observed save and stop on any mismatch.

The library answer source may be a site-visible key parsed alongside the options; it is not independent correctness evidence. In this bundled snapshot, 30 answers for experiments 6–8 have historical independent derivations and a historical score of 100; the other 50 were not independently score-verified. Do not claim new scoring or alter local/site score fields.

After permitted answer saving, verify the server-persisted answer contents and any image state. For an authorized pre-class submission, continue through the review, submission, and actual-score checks below. Without that authorization, stop before final submit and ask the user to review and submit personally. Report only the state actually verified, then ask whether other requirements remain.

## Scope and server boundary

Lookup, demonstration, and library acquisition remain read-only: do not start, create, save, or submit a quiz merely to obtain or validate reference material. In an actual pre-class answering task, the user may explicitly authorize the agent to final-submit and check the score, including through an applicable standing instruction. A save-only request overrides that permission for its scope. This permission applies only to pre-class quizzes; experiment-report final submission and resubmission remain prohibited. Do not redo a completed/full-score quiz or automatically restart, retry, resubmit, or overwrite an existing grade. A further attempt requires separate user authorization and must comply with the site's attempt, timing, and permission restrictions. Quiz navigation itself may initialize server state; GET requests may also have side effects, so do not promise strict read-only based on HTTP method or an unverified guard.

For permitted non-final answer entry, first read current quiz state and actual options. Use only the site's observed answer-selection mechanism, never fabricate direct API writes. After each action, wait for an observable response, reread the visible selected answer/content, and verify the saved server state before continuing. Multi-choice toggles can deselect an answer when clicked twice; change only differences. Re-read the next question rather than reusing stale component state. If server saving is not authorized, do not perform it.

Observed current-quiz discovery, subject to current DOM/API inspection:

```js
const state = await tab.evaluate(`(() => {
  let vm = document.querySelector('.latex-container')?.__vue__;
  while (vm && !Array.isArray(vm.questions)) vm = vm.$parent;
  if (!vm?.current_question) throw new Error('Current quiz component not found');
  const q = vm.current_question;
  return { questionId: q.id, type: q.type, questionHtml: q.question,
    options: q.options || q.question_detail, selected: q.student_answer1,
    saving: vm.subing, submitted: vm.has_sub };
})()`);
```

Use `tab.evaluate` for observed Vue properties; a raw `page.evaluate` context may not expose them. Verify this state against the visible question. A previously observed `vm.submit(currentIndex)` was the per-option selection/save handler, **not** final submission. Only use it after inspecting the current page's actual handler and outcome; prefer the observed visible choice control when API meaning is uncertain. For true/false, inspect the current 对/错 encoding instead of assuming 1/0. Await observable save completion and re-read server selection contents, not just `subing=false` or a preexisting answer ID. Then navigate and re-read the next question; never reuse the stale option mapping.

## Authorized final submission and actual-score checking

1. Confirm the active course, experiment, quiz attempt, editable/unsubmitted state, and applicable user authorization for final submission. Do not confuse a report submit button or a per-option save handler with quiz final submission. A request to edit this skill alone is not an instruction to operate the website.
2. Re-read every current stem, type, complete option set, formula, and image. Resolve all uncertain answers from the manual or credible evidence; do not submit with unresolved items. Compare intended selected contents with server-fetched selections for every question, including the complete multiple-choice set. Historical full-score evidence or a site-provided key is not proof of a future score.
3. Inspect the currently displayed final 提交/交卷 control, its confirmation, and any attempt/timing consequences. If applicable user authorization already covers them, use the normal page controls to submit this reviewed attempt; do not require a redundant confirmation from the user. Ask before proceeding if newly disclosed consequences fall outside the authorization. Never fabricate or guess a final-submission API call or bypass a lock.
4. After the observed submission response, re-read the same attempt's server-confirmed submitted state and grade. Check whether the actual result is 100/100 or the site's equivalent full mark; report the exact score and maximum when available. An answered count, green indicator, `process=100`, matching answer key, or local correctness calculation is not a verified grade. If grading is pending or unavailable, report that explicitly rather than claiming 100.
5. If the result is below full marks, report it and analyze only the feedback available for this authorized quiz. Do not automatically start another attempt, resubmit, change grade fields, or overwrite the result to chase 100. A further attempt requires separate authorization and course permission. Preserve already completed/full-score quizzes.
6. Record current question contents, selected contents, server-save checks, submission status, actual grade/max grade or pending/unavailable state, and verification time locally without credentials. Distinguish `saved_unsubmitted`, `submitted_grade_pending`, and `submitted_graded`; use only the status actually observed. Finish by asking whether other requirements remain. Use “已提交，得分 X/Y” only after server verification; otherwise state “已保存，未提交” or the exact pending/failure state.

A report PDF or report-page photo is not required for ordinary pre-class choice questions. The four report outputs and text/photo delivery map apply to the report-writing branch, whose final submission remains prohibited.
