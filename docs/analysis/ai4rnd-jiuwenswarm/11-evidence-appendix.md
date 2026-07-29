# Evidence Appendix

Every tagged claim, resolved to a repository, file, and line reference at the analysed
commit.

## Repositories and commits

| Tag prefix | Repository | Commit | Branch |
|---|---|---|---|
| `E-J*` | `suraj-subrahmanyan/jiuwenswarm` (fork of `openJiuwen-ai/jiuwenswarm`) | `a98d7ad` | `develop` |
| `E-A*` | `Stellven/AI4Research` | `d35c511` | `openJiuwen-Solar` |
| `E-A2` (design) | `Stellven/AI4Research` | `d35c511` | `DESIGN.md` at repo root |
| `E-SDD*` | `Stellven/AI4Research-A` | default branch | docs-only |

Status labels: **Verified** = read in source. **Documented** = stated in in-repo docs,
not independently confirmed in source. **Inferred** = a conclusion drawn from evidence,
with the inference stated.

---

## JiuwenSwarm evidence

### E-J01 — `openjiuwen` is an external, unvendored dependency
**Verified.** `pyproject.toml:20` — `"openjiuwen==0.1.15.post3"` in `[project.dependencies]`
(also line 60, `distribute = ["openjiuwen[postgres,zmq]"]`).
No `openjiuwen` directory exists in the repository. A Python import in the analysis
environment failed with `ModuleNotFoundError`.
Imported throughout, e.g. `jiuwenswarm/agents/swarm/registry.py:22-45`
(`openjiuwen.agent_evolving.trajectory`, `openjiuwen.agent_teams.harness.manifest`,
`openjiuwen.agent_teams.rails.builtin_elements`, `…schema.build_context`) and
`jiuwenswarm/agents/harness/team/rails/team_member_skill_toolkit_rail.py:10-11`
(`openjiuwen.core.foundation.tool`, `openjiuwen.harness.rails.base`).

### E-J02 — Entry points and process topology
**Verified.** `pyproject.toml` `[project.scripts]` — `jiuwenswarm`, `jiuwenswarm-app`,
`jiuwenswarm-agentserver`, `jiuwenswarm-gateway`, `jiuwenswarm-web`, `jiuwenswarm-start`,
`jiuwenswarm-init`, `jiuwenswarm-desktop`, `jiuwenswarm-acp`, `jiuwenswarm-acp-chat`,
`jiuwenbox`, `jiuwenbox-server`.

### E-J03 — E2A protocol
**Documented.** `docs/en/E2A-protocol.md` §0–3. Implementation at
`jiuwenswarm/common/e2a/` — `models.py` (492 LOC), `adapters.py` (257),
`wire_codec.py` (444), `gateway_normalize.py` (609), `constants.py` (125).
The document states `models.py` is authoritative on conflict.

### E-J04 — AgentServer WebSocket RPC surface
**Verified.** `jiuwenswarm/server/agent_ws_server.py:1341` (`_handle_message`) and the
dispatch chain at lines 1414–1498: `_handle_session_list`, `_handle_session_rename`,
`_handle_session_switch`, `_handle_session_delete`, `_handle_session_rewind_full` (three
call sites — plain, `restore_files=True`, `compact=True`), `_handle_session_rewind_context`,
`_handle_team_delete`, `_handle_permissions_config`, `_handle_history_get[_stream]`,
`_handle_team_snapshot`, `_handle_proactive_tick`, `_handle_command_workflows`,
`_handle_team_history_get`, `_handle_team_members_get`, and slash-command handlers
`_handle_command_{add_dir,chrome,compact,compact_partial,context,recap,btw,diff,simplify,model,mcp,sandbox}`.
Stream event kinds at lines 165–169.

### E-J05 — Swarm assembly, param/context boundary, and the `config_specs` gate
**Verified (design doc) + Verified (source).**
`jiuwenswarm/agents/swarm/DESIGN.md` — §0 (one-line overview of declarative assembly),
§1 (layer diagram), §3 (`SwarmBuildContext` field table), §5 (`ConstructionInput`,
`InputSource.PARAMS` / `CONTEXT`), §6 (param-vs-context judgement table; "`ctx.config` is
an attribute source disguised as environment"), §7 (`_RAIL_PARAM_BUILDERS`,
`_TOOL_PARAM_BUILDERS`, `_COMMON_RAIL_NAMES` / `_CODE_RAIL_NAMES` / `_CODE_TOOL_NAMES`),
§8 (`enrich_team_spec_for_swarm` four steps), §12 (serialisation), §13 (how to add an
element — step 4 requires editing `config_specs.py`), **§15 (future work: "configuration
file → harness loader" listed as not implemented; also "upstream openjiuwen alignment")**.
Source: `jiuwenswarm/agents/swarm/assembly.py:66` (`enrich_team_spec_for_swarm` definition,
with the four enrichment steps in its module docstring at lines 3-17),
`jiuwenswarm/agents/swarm/config_specs.py` (781 LOC).

### E-J06 — Harness element manifest and provider registries
**Verified (registration code) + Documented (framework internals).**
`jiuwenswarm/agents/swarm/registry.py:166` — `register_swarm_providers()` calls
`ensure_harness_elements_registered()`, `register_from_catalog()` and
`register_build_context_factory(_build_swarm_context_from_seed)`, guarded by a
`_REGISTERED` idempotency flag. Name constants re-exported at lines 64-140
(`SKILL_TOOLKIT` 64, `WEB_SEARCH` 75, `RESPONSE_PROMPT` 119).
`_build_swarm_context_from_seed` at lines 149-162.
`DESIGN.md` §2.2 states the registries are plain `dict[str, Callable]`:
`_RAIL_PROVIDER_REGISTRY`, `_TOOL_PROVIDER_REGISTRY`, `_SUBAGENT_PROVIDER_REGISTRY`.
§9.1 gives the `HarnessElementDescriptor` model (`kind`, `name`, `description`,
`factory_ref`, `input_schema`, `input_model_ref`, `interface_methods`).
§10 lists all 36 elements with their param/context sources.

### E-J07 — Extension SDK surface and hook events
**Verified.**
`jiuwenswarm/extensions/sdk/base.py:15-36` — `BaseExtension` with abstract
`initialize(config)` and `shutdown()`; `_load_metadata_from_yaml` (line 54),
`_load_config_from_yaml` (line 106).
`jiuwenswarm/extensions/registry.py:54-107` — `register_agent_server_client`,
`register_crypto_utility`, `register_rpc_handler`, `get_rpc_handler` (line 68),
`list_rpc_methods` (line 71), `register`/`unregister`/`trigger` over the
`AsyncCallbackFramework`.
`jiuwenswarm/extensions/hook_event.py` — the complete event set:
`GatewayHookEvents` (`gateway_started`, `gateway_stopped`, `before_chat_request`) and
`AgentServerHookEvents` (`agent_server_started`, `agent_server_stopped`,
`before_chat_request`, `memory_before_chat`, `memory_after_chat`,
`before_system_prompt_build`).
Only two extensions ship: `jiuwenswarm/extensions/symphony/extension.yaml` and
`jiuwenswarm/extensions/agent_client/extension.yaml`.

### E-J08 — Extension RPC is closed to external callers ⭐
**Verified.**
`jiuwenswarm/server/runtime/agent_adapter/interface.py:437-445`:
```python
_SYMPHONY_METHODS: frozenset[ReqMethod] = frozenset({
    ReqMethod.SYMPHONY_BUILD_SCORE, ReqMethod.SYMPHONY_PAUSE_BUILD,
    ReqMethod.SYMPHONY_SCORE_STATUS, ReqMethod.SYMPHONY_GRAPH, ReqMethod.SYMPHONY_PLAN,
})
```
`interface.py:1398` — `async def _handle_symphony_request`, returning `None` (lines
1400-1401) for any `req_method` outside that set, then resolving the handler at line 1405.
Call sites at lines 1641 and 1784.
`jiuwenswarm/common/schema/message.py:10` (`class ReqMethod(Enum)`), lines 116-120 (the five
symphony members), line 219 (`CHAT_SYMPHONY_STATUS`).
A repository-wide grep for `_SYMPHONY_METHODS` returns exactly two hits — the definition and
the single guard. No generic extension-method passthrough exists.

### E-J09 — Rail plugin system ⭐
**Verified.** `jiuwenswarm/agents/harness/common/plugins/rail_manager.py`:
- line 52 — `class RailManager` (singleton via `__new__`)
- line 70 — `self._extensions_dir = get_agent_workspace_dir() / "extensions"`;
  line 71 — `extensions_config.json`
- line 124 — `import_extension(folder_path)`; requires `rail.py` (line 153)
- line 197 — `_validate_rail_file`: requires the text to contain `DeepAgentRail` or
  `AgentRail`, then `compile(...)`. **This is the entire security validation.**
- line 232 — `_extract_class_name` by regex `class\s+(\w+Rail)\s*\(\s*(DeepAgentRail|AgentRail)\s*\)`
- line 265 — `_extract_priority` by regex, default 50
- line 358 — `set_agent_instance`
- line 362 — `async hot_reload_rail(name, enabled)` → `agent.register_rail(...)` (line 386)
  / `agent.unregister_rail(...)` (line 400)
Driven from `jiuwenswarm/server/agent_ws_server.py:5922, 5957, 5988, 6022`
(four handlers) and `interface_deep.py:4375-4377` (sets the agent instance for hot update).

### E-J10 — A Rail can register tools on a live agent ⭐
**Verified.**
`jiuwenswarm/agents/harness/team/rails/team_member_skill_toolkit_rail.py`:
- line 22 — `class MemberSkillToolkitRail(DeepAgentRail)`, `priority = 95`
- line 40 — `def init(self, agent: "DeepAgent")`
- lines 54-55 — `for tool in tools: agent.ability_manager.add_ability(tool.card, tool)`
- line 65 — `def uninit(self, agent)`; line 71 — `agent.ability_manager.remove_ability(tool.card.name)`
The comment at lines 50-52 notes `add_ability` qualifies the tool id with the owner agent id
and registers with `refresh=True`, so a rail registration deterministically overrides a
declarative tool element of the same name.
**Combined with E-J09 this is the decisive integration seam.**

### E-J11 — Sandbox
**Verified.** `jiuwenswarm/server/sandbox/jiuwenbox_runner.py:1-50` — module docstring
describes `/sandbox enable` triggering, default `http://127.0.0.1:8321`, `internal` vs
`external` startup modes, `JIUWENBOX_POLICY_PATH` injection, and `stop()` on parent exit.
Line 42 — `_PR_SET_PDEATHSIG = 1`.
`jiuwenbox/src/jiuwenbox/`: `supervisor/bwrap.py` (503), `supervisor/cgroup.py` (528),
`supervisor/network.py` (876), `supervisor/sandbox_daemon.py` (826),
`server/sandbox_manager.py` (1,367), `server/runtime/process.py` (3,003),
`models/policy.py` (762), `proxy/inference_privacy_proxy_manager.py` (498).

### E-J12 — Tiered permission policy
**Documented.** `docs/en/ToolPermissionsSecurity.md` §1 (three-tier actions,
`permissions.enabled` master switch, `permissions.schema: tiered_policy`), §2.1
(severity→action mapping by `permission_mode`), §2.2 (parameter-rule matching by shell /
path / network category), §2.3 (the nine-step resolution order), §2.4
(`maybe_escalate_shell_operators`, `ExternalDirectoryChecker` merge), §3
(`jiuwenswarm/resources/builtin_rules.yaml`; user rules cannot override built-in denials),
§4 (external directory handling).
The engine is stated to live in `openjiuwen.harness.security` — not readable here.

### E-J13 — Skill self-evolution
**Documented + Verified (rail names).**
`docs/en/SkillSelfEvolution.md` §1.1–2.5 — automatic signal detection after tool execution
and dialogue completion; `evolutions.json` under the skill directory; `/evolve <skill>`,
`/evolve list`; `evolution_auto_scan` switch; system-managed fields listed as not
user-editable.
Rails verified at `jiuwenswarm/agents/swarm/providers/evolution_rails.py` (706 LOC),
re-exported in `registry.py:100-103` as `TEAM_SKILL_EVOLUTION`, `TEAM_SKILL_CREATE`,
`MEMBER_SKILL_EVOLUTION`, `EVOLUTION_INTERRUPT`.

### E-J14 — No evidence, claim, citation or factuality model ⭐
**Verified by exhaustive search.** Repository-wide grep across all `*.py` for
`evidence_ledger`, `citation_span`, `claim_graph`, `factuality` returns **zero files**.
A broader grep for `evidence|citation` matches 32 files, all incidental prose in comments
and prompts — no data model, no schema, no gate. No SQL schema, dataclass, or storage
module for evidence or claims exists.

### E-J15 — Agent loop, rails, stop conditions
**Documented.** `docs/en/Harness.md` §1.2 (single-round ReAct vs dual-layer task loop),
§1.3 (six design principles), §2 (three layers: core engine / extension / infrastructure),
§3.1 (`TaskLoopController`, `LoopCoordinator`, `TaskLoopEventHandler`,
`TaskLoopEventExecutor`, `LoopQueues`; `follow_up` / `steer` / `abort`; `TaskPlanningRail`,
`TaskCompletionRail`; `MaxRoundsEvaluator`, `TimeoutEvaluator`, `TokenBudgetEvaluator`,
`CompletionPromiseEvaluator`, `CustomPredicateEvaluator`, OR semantics),
§3.2 (the rail lifecycle event table reproduced in
[01-jiuwenswarm-architecture.md](01-jiuwenswarm-architecture.md) §4.2).
All classes named live in `openjiuwen`.

### E-J16 — Skill format and the built-in deep-research skill
**Verified.**
Format: `jiuwenswarm/resources/agent/workspace/skills/skvm-general/SKILL.md:1-4` — YAML
frontmatter with `name` and `description`.
Deep research: `.../skills/openJiuwen-DeepSearch/SKILL.md:1-4` — description claims
"knowledge-enhanced deep retrieval and deep research, supporting query planning, information
gathering, understanding and reflection, research report generation with multi-agent
collaboration… can generate Markdown, Doc and HTML research reports". Body (lines 8-14)
describes launching `uv run scripts/main.py --mode query`, a ~15-minute background
subprocess, a `PID.info` file, and a 20-minute polling cron to detect completion.
No evidence ledger, claim model, citation verification or gate appears anywhere in the skill.
Sources documented in `docs/en/Skills.md` — built-in, SkillNet, ClawHub, SwarmSkills, local
import.

### E-J17 — Extension loader installs dependencies
**Verified.** `jiuwenswarm/extensions/loader.py`:
- line 59 — `await self._install_dependencies(manifest, root)` before module import
- lines 77-120 — `_install_dependencies`: reads `manifest["dependencies"]`, checks
  `importlib.metadata.version`, then `subprocess.check_call([uv_path, "pip", "install", …])`
  (line 103-108) or `[sys.executable, "-m", "pip", "install", …]` (line 110-115), timeout
  120 s. `TimeoutExpired` and `CalledProcessError` are **logged, not raised** (lines 117-120).
- lines 122-140 — `_import_module` loads `extension.py` via `importlib.util.spec_from_file_location`
  and `exec_module`.
`jiuwenswarm/extensions/manager.py:47-53` — search paths from `extensions.extension_dirs`
(semicolon-separated) plus the in-package default; lines 79-92 — `load_all_extensions`
catches and logs per-extension failures.

### E-J18 — In-process RPC dispatch by string
**Verified.** `jiuwenswarm/agents/harness/common/tools/symphony_toolkits.py:33-66` —
`_call_rpc(method, params)` obtains `ExtensionRegistry.get_instance()`, calls
`registry.get_rpc_handler(method)` (line 47), awaits with a timeout, and returns the payload.
Shows that any in-process caller — including a Rail-registered tool — can reach extension
RPC handlers by name, without the enum gate of E-J08.

### E-J19 — Agent caching key
**Verified.** `jiuwenswarm/server/runtime/agent_manager.py:50` —
`_make_agent_cache_key(mode, sub_mode, project_dir)`; used at lines 158 and 304.
`class AgentManager` at line 76; `_reload_agent_topology` at line 112;
`get_client_capabilities` at line 255.

### E-J20 — Interrupt semantics
**Verified.** `jiuwenswarm/server/runtime/agent_adapter/interface.py:1434` —
`async def _process_interrupt`, whose docstring dispatches on intent: `pause` (suspend the
ReAct loop without cancelling the task), `resume`, `cancel` (cancel the session's running
task).
`agent_ws_server.py:1316-1317` — comment stating that on gateway exit the per-session
streaming producers must be cancelled and the inner DeepAgent loop aborted, because merely
awaiting `_handle_message` blocks until the task finishes naturally.

---

## AI4RnD evidence

### E-A01 — Self-described maturity ⚠️
**Verified.** `README.md:1-8` — "OpenJiuwen Solar is a Python/bash harness for running a
local multi-agent software cockpit with Codex or Claude Code as the selected pane runtime.
It opens real agent processes in tmux panes… Solar is not a finished autonomous cloud
service and not a TypeScript orchestrator product. The working product today is the local
harness plus the installer/lifecycle tooling around it."
Lines ~72-74 — "Some code in `core/` is roadmap scaffolding or compatibility glue. It is
kept in the repository, but the README and CLI surfaces should not treat it as a fully
working autonomous orchestrator."
Platform table — macOS Primary; Linux Supported; "Windows / WSL2 Experimental"; the macOS
DMG "still requires real-machine release proof".

### E-A02 — Four agents, capability-routed DAG, honest stalling ⭐
**Verified.** `DESIGN.md` (repo root) YAML frontmatter `signature` field, and the prose:
- "AI4Research is a **multi-agent orchestration surface**: four named agents
  (PM → Planner → Builder → Evaluator) hand work down a capability-routed DAG, and the run
  **stalls honestly** when no agent advertises a needed capability."
- "the orchestration is a capability-routed **DAG, not a line**, so do NOT draw a fixed
  PM → Planner → Builder → Evaluator pipeline with directional flow/arrows — that implies a
  linearity that isn't real."
- Honest state rules: "A stalled sprint **never** shows a filled percentage/progress bar or
  a synthesized 'Result is available'"; "A stall is shown by the relay's broken handoff +
  the process stream's blocked step (whose raw tokens like `no_matching_worker` live in that
  step's expandable detail)".
- "Settings controls are real but **do not persist** in P0 (no runtime write path); say so
  plainly."

### E-A03 — Frozen sprint state machine
**Verified.** `harness/config/coordinator-state-machine.json`:
`"version": "1.0.0"`, `"frozen_since": "2026-05-08"`, description "Coordinator Control
Plane v2 — canonical transition table. All routing decisions flow through this table."
`lifecycle_states`: `intake`, `prd_ready`, `planning`, `planning_complete`, `building`,
`build_complete`, `evaluating`, `done`, `blocked`, `quarantined`, `failed`, `corrupt`.
Transitions with `guard` on artifact existence, `requested_role`, `required_artifacts`,
`timeout_policy` (`ack` / `artifact`), `retry_policy` (`max_attempts`, `backoff`):
`intake_to_prd_ready`, `prd_ready_to_planning_complete`,
`planning_complete_to_build_complete`, `build_complete_to_done`,
`build_complete_to_blocked`, `blocked_to_build_complete`.

### E-A04 — Logical operator registry
**Verified.** `harness/config/logical-operators.json` — `version: 1`,
`updated_at: 2026-06-02T01:59:19Z`. Operator types with `required_capabilities` (integer
levels), `primary_role`, `cost_hint`, `concurrency.{max_parallel,singleton}`, some with
`risk_constraints.allowed_shell_scope`:
`DeepArchitect`, `RootCauseDebugger`, `ImplementationWorker`, `PatchWorker`, `TestDesigner`,
`TestRunner`, `BenchmarkRunner`, `ParallelExplorer`, `ResearchScout`.
Loader: `harness/lib/logical_operator_registry.py` — `load_logical_operator_registry`,
`logical_operator_def`, `logical_operator_binding`.

### E-A05 — Physical operators launch with permissions disabled ⚠️
**Verified.** `harness/config/physical-operators.json` — e.g. `mini-claude-opus-planner`:
```json
"surface": { "type": "claude_code_interactive", "tool": "claude",
             "launch_cmd": "claude --dangerously-skip-permissions --model opus" }
```
Also present per operator: `plane`, `owner_host`, `pane`, `profile`, `role`, `persona`,
`provider`, `vendor`, `backend`, `model`, `auth_mode`, `key_ref` (indirection, not an inline
key), `billing_surface`, `billing_pool`, `quota_cycle`, `quota_guard_state`, `enabled`,
`available`, `health_status`, `roles`, `task_classes`, `strengths`, `preferred_for`,
`avoid_for`, `cost_tier`, `latency_tier`, `context_tier`, `max_concurrency`,
`fallback_profile`, `state.{availability,runtime_state,cooldown_until}`,
`flow_control.{last_block_state,last_block_reason,…}`, `compat_alias_for: "tmux_pane"`,
`compat_maps_to.carrier_hint.tmux_pane_meta`.
Static eligibility logic: `harness/lib/physical_operator_catalog.py` —
`static_operator_rejection_reasons` (disabled / unavailable / deprecated / health_status),
`resolve_static_operator_reference` (exact-ID precedence over profile match).

### E-A06 — Capability routing algorithm ⭐
**Verified.** `harness/lib/graph_scheduler.py`:
- line 2318 — comment: "Capability match is the HONEST hard gate (never relaxed): a worker
  missing a required capability is genuinely unqualified and is skipped for BOTH the strict
  and the relaxed pass."
- lines 2305-2350 — the per-worker loop: `_role_penalty`, `_missing_skills`,
  `_missing_capabilities`, `_capabilities_match`, `_worker_quota_exhausted`,
  `_model_requires_strict_match` / `_model_match`, `_worker_unavailable_reason`,
  `used_panes`, `_worker_busy`, `_capability_score`, `_skill_match_count`
- line 2353 — comment: "Layer 3 (liveness net): no worker matched the (possibly
  drifted/free-form) skill strings, but capability-qualified role-appropriate workers ARE
  free. Dispatch to the best one rather than permanently strand the DAG."
- lines 2378-2400 — stall reason discrimination:
  `worker_runtime_unavailable` / `worker_capacity_exhausted` (line 2384) /
  `no_matching_worker` (line 2386), with `details` carrying `required_role`,
  `required_skills`, `required_capabilities`, `any_worker_seen`, `role_candidates_seen`,
  `missing_skills`, `missing_capabilities`
- line 3452 — `graph["node_results"][node_id]["blocking_reason"] = "no_matching_worker"`
- lines 2290-2294 — an `ImplementationWorker` with no declared capabilities is defaulted to
  requiring `code_impl` "so the honest hard gate bites"
Tests: `harness/tests/graph/test_worker_assignment_reasons.py:40, 52, 72, 288, 311, 314`
(explicitly asserts capacity vs `no_matching_worker` are distinguished).

### E-A07 — DAG scheduler guarantees
**Verified.** `harness/lib/graph_scheduler.py:1-14` (module docstring):
```
  - invalid DAGs fail fast (missing deps, cycles, duplicate nodes)
  - ready nodes require all dependencies to be passed
  - nodes with overlapping write_scope never share a batch
  - nodes without declared write_scope are treated as exclusive writers
  - parent sprint cannot pass until every node and required gate has passed
```
Functions: `validate_graph` (1639), `topo_order` (1705), `topo_layers` (1736),
`critical_path` (1755), `graph_parallelism_metrics` (1612).
Pass-mark guards: `_validate_contract_closeout_receipt` (1319), `_assert_pass_mark_allowed`
(1413), `_assert_human_review_status_write_allowed` (1430),
`assert_node_status_write_allowed` (1450), `_node_has_independent_eval_report` (1272),
`_node_eval_is_self_graded` (1291), `_passed_without_required_eval` (1310).
Human review: `HUMAN_REVIEW_STATUS = "needs_human_review"` (line 48),
`_human_review_record` (969), `_human_review_is_blocking` (998).
Also `harness/lib/plan_validator.py:533` — comment tying plan validation to routability:
"(no_matching_worker) — 'compiles' must imply 'dispatchable'".

### E-A08 — Dispatch protocol and failure post-mortems ⚠️
**Verified.** `harness/DISPATCH-PROTOCOL.md`, nine documented root-cause analyses:
1. **send-keys swallowed input** — `tmux send-keys "$cmd" Enter` loses `Enter`; fix is
   text, `sleep 0.8`, then `Enter`.
2. **Directory-level mtime misses content edits** — macOS APFS does not update parent
   directory mtime on file content change; fix scans all `sprint-*.status.json` for max
   mtime (~24 ms per round for 24 files).
3. **Busy panes swallow input** — busy markers `✳|✶|⏺|Cogitated|Cooked|Propagating|Worked for`;
   poll up to 12 × 10 s, then emit `DISPATCH_DEFERRED`.
4. **Zombie pidfile blocks startup** — `kill -0` liveness check with stale-PID cleanup.
5. **`last_state` swallows the first dispatch.**
6. **Scattered pidfile ownership** — unified to `coordinator.sh`.
7. **`get_latest_sprint_file` skipping terminal states** meant `handle_passed` never fired.
8. **plan-review deadlock** — evaluator appended a history event but did not change status,
   because the dispatch told it to edit JSON with an inline `python3 -c`. Fix: the atomic
   `plan-verdict` / `handoff-submit` / `eval-verdict` triad (tempfile+rename, updating
   status + history + event together).
9. **Bug #5 — 13 hours, 3,766 poll iterations, zero heal-branch executions**, because the
   running bash process had loaded the pre-fix version of `coordinator.sh` from disk at
   start. Fix: log the script md5 at startup; add permanent low-frequency PROBE logs to
   rarely-taken branches.
Also documents the Codex bridge: architecture diagram, `req → dispatch → res → forward`
sequence, three call tiers (S 4000 / A 2000 / B forbidden), and budget circuit-breaking
(`daily_call_limit: 30`, `daily_token_limit: 20000`, `hard_stop: true`), with
`codex exec -s read-only`.
Bash sizes verified by `wc -l`: `solar-harness.sh` 6,119; `coordinator.sh` 5,797;
`coordinator-watchdog.sh` 963; total shell 83,044.

### E-A09 — File-first design principles
**Verified.** `AI4Research-A/docs/architecture.md` "Design Principles":
"Follow SDD: define contracts, interfaces, and acceptance criteria before implementation";
"Keep every phase runnable end to end, even when early phases use stubs";
"Store major outputs as files so runs are easy to inspect, test, and debug";
"Treat sources, evidence, claims, reviews, and reports as separate artifacts";
"Gate later stages on validated artifacts instead of hidden model context";
"Add capability incrementally rather than building a fragile full agent at once".
Run-artifact layout given under "Run Artifacts".

### E-A10 — Gate ledger ⭐
**Verified.** `harness/lib/gate_ledger.py:1-31` (module docstring):
"Gate ledger — append-only gate/status evidence; node status as a projection."
Storage `sprints/<sid>.gate-ledger.jsonl`, one JSON object per line, schema v1.1.
`RECORD_KINDS` at line 40: `eval_verdict`, `auto_resolution`, `repair_start`,
`repair_exhausted`, `human_verdict`, `gate_check`, `status_transition`, `route_record`.
Record fields: `record_id`, `sid`, `node_id`, `kind`, `author.{type,operator_id}`,
`verdict`, `verdict_kind` (`content|mechanical|infrastructure`), `eval_generation`,
`repair_attempt`, `pm_task_id`, `evidence_snapshot_at`, `created_at`, and for route records
`route.{provider,model,operator_id,backend,exit_code,started_at,finished_at}`.
Line 21 — status transitions carry `writer`, "the code seam that performed the write — the
AC-R4.3 audit key", plus `applied: False` for neutralised doctor writes and `reopen: True`
for the legacy reopen-from-pass allowance.
Flag-gated by `SOLAR_GATE_LEDGER`; the raw append/read/projection APIs are unconditional.

### E-A11 — Writer ≠ verifier enforcement ⭐
**Verified.** `harness/lib/verification_gate.py`:
- line 1-5 (docstring): "Evidence-based verification gate for DAG completion. Requires:
  patch/artifact evidence, test or benchmark evidence, and independent verifier decision
  for critical DAG completion."
- line 19 — `check_code_task(has_patch, has_test_evidence, writer_actor_id,
  verifier_actor_id, verifier_decision)`; failure reasons `no_patch_artifact`,
  `no_test_evidence`, `writer_and_verifier_same_actor` (line 36), `no_verifier_decision`
- line 46 — `check_dag_done(..., high_risk, available_providers)`; same actor check at
  line 65

### E-A12 — Research evaluator and gate registry ⭐
**Verified.** `harness/lib/research/evaluator.py` (1,673 LOC):
`policy_doctor` (133), `explain_source_authority` (165), `audit_sources` (207),
`_grounding_checks` (443), `_citation_grounding_metrics` (482),
`_expert_analysis_lines` (525), `_expert_novelty_metrics` (541),
`_section_coverage_metrics` (579), `_source_diversity_metrics` (631),
`_source_type_is_plausible` (652), `_source_type_validation_metrics` (691),
`_source_authority_score` (728), `_source_authority_metrics` (779),
`_profile_policy` (814), `source_requirements_for_profile` (827), `_apply_profile_gate` (850),
`evaluate_artifacts` (921), `evaluate_final_closeout` (1141),
`evaluate_retrieval_closeout` (1351), `evaluate_figures_grounding` (1529).
Token-overlap grounding primitives at lines 418-422: `_tokens`, `_jaccard`.
Policy data: `harness/lib/research/policies/source_authority.json`,
`harness/lib/research/profiles/cais_agent_insight.yaml`.
Gate registry: `harness/lib/research/survey/gates/_registry.py` — `_GateRegistry`,
`GateRegistry`, `register_gate(name)` decorator, `DuplicateGateError`, `GateNotFoundError`.
Shipped gates: `argument_density.py`, `controversy_matrix.py`,
`global_consistency_pass.py`, `source_quality_distribution.py`,
`compile_gate_report.py`.

### E-A13 — Research data model ⭐
**Verified.** `harness/lib/research/schemas.py` dataclasses at the stated lines:
`SourceConnector` (98), `SourceHit` (153), `SourceDocument` (192), `EvidenceItem` (238),
`Claim` (304), `ClaimEvidenceLink` (352), `CitationSpan` (380), `Section` (436),
`Chapter` (468), `BibEntry` (485), `Bibliography` (504), `QualityReport` (509),
`ReportAST` (521), `FigureSpec` (583), `LivingReport` (635), `ResearchLab` (664),
`ResearchMemory` (688), `AIInfraPack` (715), `ArtifactDelta` (753).
Supporting modules: `ids.py` (deterministic SHA-256 ids — `make_id` joins parts with `|`,
SHA-256s UTF-8, takes the first 16 hex chars; `evidence_id`, `claim_id`, `connector_id`),
`hashing.py` (`content_hash`, `verify_content_hash`), `storage.py` (SQLite + JSONL +
feature flags), `evidence/ledger.py`, `evidence/citation_span.py` (UTF-8 span verification
at char and byte offsets), `extractors/markdown.py`, `sources/base.py` (`SourceConnector`
ABC), `sources/internal_mirage.py`, `migrations/001_init.sql` (7 tables).
Documented in `harness/README.research.md`, which also states installation requires only
`PYTHONPATH="$PWD/lib"` — no pip install.

### E-A14 — LLM placement discipline ⭐
**Verified.** `AI4Research-A/docs/pipeline_a_actual_architecture_sdd.md` §5.3:
```
LLM proposes.
Schemas constrain.
Code validates.
Gates decide.
Artifacts preserve.
```
Bad LLM uses listed: "Inventing citations. Owning run state. Secretly changing the research
contract. Bypassing gates. Introducing unsupported facts directly into final prose."
§5.2 (Optimizer): "The optimizer should not be hidden chain-of-thought. It should be
code-defined, inspectable, and persisted."
§5.4 (Codex placement): "Codex should receive bounded work packets and return artifacts. It
should not receive an unrestricted instruction to 'research the topic' or 'write the whole
report' outside the operator plan."
§5.8 lists ten quality gates; §5.9 gives the repair-DAG example; §9 gives the full run
artifact layout.

### E-A15 — Research CLI surface
**Verified.** `harness/lib/research/cli.py` (4,381 LOC) — `add_parser` calls at lines
3897–4354, enumerated in
[02-ai4rnd-architecture.md](02-ai4rnd-architecture.md) §8.2. Includes `survey-auto-repair`
(4178, "Strict-eval survey, rewrite failed sections, then re-eval"), `survey-finalize-run`
(4197), `survey-continue` (4276, "Safely continue… until done or a human/source-gap pause"),
`closeout` (4354).
Depth tiers documented in `harness/README.research.md`: `quick` 3–5 sources,
`standard` 10–20, `deep` 50+.

### E-A16 — Knowledge-base schema contracts
**Verified.** `runtime/schema/`:
- `entities.yaml` — typed fields (`str|int|float|bool|date|enum|object|link|list_*`),
  `required`, `default`, `range`, `values`, `to`, `required_when`, nested `fields`/`item`;
  `terminal: true` exempts an entity from the reverse-link rule. `papers` entity shown with
  `importance: {type: int, range: [1,5], required: true, default: 3}`.
- `edges.yaml` — `endpoints {from,to}`, `direction directed|symmetric`, owning `workflow`
  (`ingest|evidence|experiment|idea|provenance|citation`), `attributes`. Documents the
  reduction from 8 to 4 paper↔paper edges with reasoning for each removal.
- `xref.yaml` — mandatory bidirectional link rules; `reverse.action append_slug|append_record`.
- `conventions.yaml` — `slug_rule` regex, `path_pattern: "wiki/{kind}/{slug}.md"`,
  `wikilink_syntax`, `date_format`, `log_grammar`, `edge_storage` (default
  `wiki/graph/edges.jsonl`, `cites` → `wiki/graph/citations.jsonl`), and **ownership**:
  `user_owned: [raw/papers, raw/notes, raw/web]` ("skills must not overwrite"),
  `tools_only: [wiki/graph]`, `append_only: [wiki/log.md]`.

### E-A17 — Contracted intake fails closed
**Verified.** `harness/lib/workflow_intake.py:1-24` (module docstring): instantiates a
registered fixed-stages contract into `sprints/<sid>.task_graph.json` carrying
`workflow_contract_id`/`version`/`hash`; writes the drafting sprint scaffold plus planner
artifacts; and (lines 17-18) "fails CLOSED on an unknown or planner-generated workflow_id —
never a silent fall-through to the generic path (exit 3 / 4 at the CLI)".
Stated to be "pure like the rest of the Lane 1 family: stdlib + workflow_contract only, no
runtime imports, atomic writes."

### E-A18 — Status server HTTP surface
**Verified.** `harness/lib/symphony/status-server.py` (14,400 LOC) — `do_POST` (13904),
`do_GET` (13973). Endpoints include `POST /api/sprints/<sid>/plan-verdict` (13957),
`/eval-verdict` (13961), `/handoff-submit` (13965); `GET /api/sprints` (14058),
`/api/sprints/<sid>/contract` (14291), `/projection` (14299), `/api/capability` (14325),
`/api/evolution` (14329), `/api/pane-model-call` (14028).
React app at `harness/status-server/react-app/src/` — `types.ts` (441), `api.ts` (438),
`format.ts` (402), `nodeActor.ts` (126), `runPipeline.ts` (52).
Test asserting honest stall display: `harness/tests/test-status-server-p0-dashboard.py:167`
— `assert data["stall"]["state"] == "no_matching_worker"`.

---

## Measurement method

Sizes were obtained with `find … | xargs wc -l` over the working trees at the stated
commits. `.git` directories and, for AI4RnD, `vendor/` subtrees are included in totals
unless stated otherwise; treat LOC figures as order-of-magnitude indicators of relative
scale, not precise counts.

Repository-wide absence claims (E-J14 in particular) were made with `grep -ril` over all
`*.py` files in the JiuwenSwarm working tree. Absence from the tree does not prove absence
from the `openjiuwen` dependency — but the identifiers searched for are domain concepts of
a research system, and `openjiuwen` is a general agent framework, so the inference is
considered safe. It is nonetheless an inference, and is recorded as such in
[10-risks-assumptions-open-questions.md](10-risks-assumptions-open-questions.md) §L1.
