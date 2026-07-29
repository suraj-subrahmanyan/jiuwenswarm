# AI4RnD on JiuwenSwarm — Architecture Package

**Recommendation: build AI4RnD as a first-class, persistent research product on JiuwenSwarm.
AI4RnD keeps all product semantics; OpenJiuwen executes; migration of low-level scheduling is
progressive, gated by compatibility tests. All 142 workbook outcomes are preserved.**

Start with the [Executive Summary](00-executive-summary.md).

## The seven documents

| # | Document | Answers |
|---|---|---|
| 00 | [Executive Summary](00-executive-summary.md) | the recommendation and why, in five minutes |
| 01 | [The Intended AI4RnD Product](01-intended-ai4rnd-product.md) | what is being built — the 142-outcome definition |
| 02 | [JiuwenSwarm & OpenJiuwen Architecture](02-jiuwenswarm-openjiuwen-architecture.md) | what the foundation reliably provides, and what it doesn't |
| 03 | [Integration Options](03-integration-options.md) | the five coherent architectures and the preservation gate |
| 04 | [Recommended Target Architecture](04-recommended-target-architecture.md) | the design: layers, end-to-end workflow, boundary rules, RSI |
| 05 | [Feature Ownership & Implementation Plan](05-feature-ownership-implementation-plan.md) | who owns what, and the dependency-driven plan |
| 06 | [Evidence, Assumptions & Open Questions](06-evidence-assumptions-open-questions.md) | verified vs judged vs assumed, and what remains open |

## Rendered editions

Fully offline — open directly in a browser, no network needed:

- [`html/index.html`](html/index.html) — navigable site
- [`ai4rnd-architecture-review.html`](ai4rnd-architecture-review.html) — single-file review edition

## Machine-readable artifacts

- [142-feature implementation ownership](traceability/142-feature-implementation-ownership.csv) — all rows, all columns
- [142-feature preservation gate](traceability/142-feature-preservation-gate.csv) — every outcome × every option
- Earlier coverage matrix: [MD](traceability/142-feature-matrix.md) · [CSV](traceability/142-feature-matrix.csv)

## Provenance

The full working history — 21 analysis documents across four revisions, probe scripts, and the
correction log of what each revision got wrong — is preserved under
[source-material/](source-material/README.md). It is superseded source material; the seven
documents above are authoritative.

Regenerate everything from source:

```
python3 tools/gen_ownership.py .   # workbook -> traceability CSVs
python3 tools/mdsite.py .          # -> html/
python3 tools/onepage.py .         # -> ai4rnd-architecture-review.html
```
