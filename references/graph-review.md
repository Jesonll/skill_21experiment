# Per-graph second-review worksheet

Use this for every graph and schematic. Save completed entries in the report's `qa/graph-review.md`, outside the student-facing PDF. A template checkbox is not evidence of review.

## Review identity

- Question / page / figure / panel:
- Required answer elements from the question:
- Source data, channel identity, amplitude convention, and model (if any):
- Final PDF path and version (hash or timestamp):
- Reviewer:

## Pass A — scientific completeness

- [ ] Enumerate every required series or circuit branch before checking the implementation.
- [ ] Match each series/branch to a source or an explicitly identified theory/model; no invented readings.
- [ ] Check domain, period, amplitude convention, sign, phase, units, and critical features such as corners, clipping, spikes, feedback, or polarity.
- [ ] Compare representative values or endpoints to calculations/data, not just the overall appearance.
- [ ] Count required and implemented series/branches separately.

| Required item | Source/model | Key values/endpoints or topology | Style/label | Implemented? |
|---|---|---|---|---|

A result: PASS / FAIL / unresolved evidence. Explain unresolved evidence specifically; do not mark PASS while required information is absent.

## Pass B — final rendered output

Compile first. Open the final page at normal reading size and a 250–300 dpi graph crop. Review the pixels, not only LaTeX or plotting code.

- [ ] Trace each required curve across its complete domain. Confirm required count = implemented count = visibly identifiable count, except explicitly explained exact coincidence.
- [ ] Trace each required wire to both endpoints; inspect junction dots, crossings, feedback return, terminals, and ground/power connections.
- [ ] Match each legend entry to its visible curve; check consistent styles across every panel.
- [ ] Check whether a nearly coincident curve is hidden by draw order, excessive line width, or a dashed line's gaps. Use sparse markers and contrasting line styles without falsifying numerical coordinates.
- [ ] Place the legend in a reserved area that does not collide with titles, axes, ticks, labels, or data. Inspect the entire legend box, not just its anchor.
- [ ] Check data are not clipped by axis limits, other graphics, page borders, or neighboring panels.
- [ ] Check tick labels, units, Ω/μ/±, subscripts, line weights, and marker visibility at intended print size.
- [ ] Check titles, legends, and multiline labels at both page and crop scale; a contact sheet alone is insufficient.
- [ ] Inspect all panels individually; never infer their correctness from the first panel.

| Required item | Visible across full domain / connected end-to-end? | Legend/label identifiable? | Rendered evidence path | Defect / fix |
|---|---|---|---|---|

- Rendered required/implemented/visible counts:
- Legend location and collision result:
- Layout result: PASS / FAIL.
- Series/topology result: PASS / FAIL.
- Final result: PASS only when both results pass.

## Change invalidation

A later change to styles, ranges, dimensions, labels, global fonts, or layout invalidates affected Pass B results. Recompile, render again, and record the post-fix review. Never use a superseded crop as proof of the delivered PDF.

## Regression example: Experiment 6 trial, page 3

The prompt requires the subtractor circuit and two pairs of input/output waveforms. Treat the schematic and each waveform panel as separate review units.

- The first panel implements amplitudes 1.40856 V and 1.41421 V. The difference is about 0.4%, so two plotting commands may still look like one curve. This is a rendered visibility failure if the reader cannot identify both signals.
- Keep the values unchanged. Draw a thin solid curve plus a clearly dashed/marked second curve; check full-period visibility and the legend. If curves genuinely coincide, state the coincidence briefly and use markers or a justified inset rather than adding a fake DC offset.
- The trial source anchors the legend near the same above-axis area as the title. Allocate a separate shared-legend strip and inspect its full bounding box after rendering.
- Independently trace the subtractor's required input, feedback, ground, and output wires. The user reported a missing line; do not assume it is only a hidden waveform because two curves exist in source.

### Shared-legend implementation check

For pgfplots groupplots, assign `legend to name=wave-legend` to the specific panel that owns the legend entries, not indiscriminately to every panel. A later panel without entries can overwrite a group-wide named legend and leave the external legend blank. Render and confirm the actual entries, not merely the reserved white space.

```latex
% Inside groupplot; other panels use the same signal styles.
\nextgroupplot[legend to name=wave-legend]
\addplot[blue,thin] ...;
\addlegendentry{$u_{i2}$}
\addplot[black,densely dashed,thin,mark=o,mark repeat=20] ...;
\addlegendentry{$u_o$}
% Other panels: no legend-to-name override.
% After end{tikzpicture}, in a dedicated strip:
\pgfplotslegendfromname{wave-legend}
```

In the revision smoke run, the first compile succeeded but the external legend was empty. Pass B rejected it. Moving legend ownership to the first panel and rerendering restored both entries. The near-coincident pair remained at its original values; thin solid plus dashed/open-circle styling made signal identity visible. This smoke proof covers the plotting rule, not the trial report's full circuit or any unmodified PDF.

## Boundary: what automation cannot prove

Page count, text extraction, font embedding, file existence, or counting `addplot` commands do not establish visual completeness. Automated structural checks are useful inputs, not replacements for Pass B. Retain a failed review when it demonstrates a defect rather than replacing it with an unsupported “all passed”.
