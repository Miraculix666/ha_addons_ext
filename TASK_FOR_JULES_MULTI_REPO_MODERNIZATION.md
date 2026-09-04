# MASTER TASK FOR JULES: Autonomous Multi-Repository Audit, Modernization & Sync

**Assigned Agent:** Jules (`jules.google.com`)  
**Scope:** ALL GitHub Repositories (both locally cloned and remote on GitHub: `ha_config`, `ha_addons_ext`, `homelab_infra`, `llm_stack_core`, `llm_stack_config`, `agents_and_prompts`, `ha_core`, `homelab_config`, `NetworkAnalyseStack`, `proxmox_host_backup`, `ha_backup`, etc.)  
**Execution Standard:** Zero Deprecation Tolerance, Universal Portability, Ponytail Decision Ladder, Git Single-Source-of-Truth  
**Authorization Mode:** Fast-Track Global Auto-Acceptance (Rule 1: All Jules branches/PRs are automatically approved and merged).

---

## 1. Objectives & Mandate for Jules

Jules must independently inspect, audit, modernize, and synchronize every repository under the account according to the following strict guidelines:

### A. Strict Syntax & Zero Deprecation (Modernization)
1. **Home Assistant Configurations & Automations:**
   - Migrate any remaining `service:` calls to `action:`.
   - Ensure all automations have unique numeric/alphanumeric `id`s and use UI-compliant native blocks (`choose`, `if-then`, `numeric_state`, `time`) without raw YAML anchors (`&`/`*`).
   - Replace deprecated target schemas (no `entity_id: all`).
2. **Python & Script Toolchains:**
   - Ensure compatibility with Python 3.12 / 3.13.
   - Replace flaking subprocess shell blocks with robust `check=True` standard library executions (`subprocess`, `json`, `pathlib`).
3. **Supervisor Addons & Docker Containers:**
   - Update `config.json` schema to modern `schema`, `ingress`, `ingress_port` conventions.
   - Verify multi-arch support (`amd64`, `aarch64`).

### B. Universal Portability & Environment Isolation (Rule 4 & Rule 17)
1. **Zero Hardcoded Private IPs/Secrets:**
   - Isolate all credentials, tokens, and static private IPs into `.env` / `environment.yaml` using `!ENV` syntax.
   - Use dynamic path resolution (e.g. `Path(__file__).resolve().parent`, `PROJECT_ROOT`, `HA_CONFIG_DIR`) rather than rigid absolute paths.
2. **Git Provider Agnostic Remotes:**
   - Parametrize all backup and sync scripts to support any Git remote origin (`GIT_REMOTE_URL`).

### C. Ponytail Anti-Overengineering Standard (Rule 18)
- Apply the 6-rung decision ladder: *YAGNI -> Reuse -> Standard Library -> Native Platform -> Existing Dependencies -> Minimal Code*.

### D. Graphify Knowledge Graph Maintenance
- Update and cross-reference architecture nodes in the Obsidian knowledge graph (`/root/.hermes/skills/note-taking/obsidian/Architecture/`).

---

## 2. Target Repositories Matrix

```
+---------------------------------------------------------------------------------------------------+
| REPOSITORY            | PRIMARY FOCUS AREA FOR JULES                                              |
+---------------------------------------------------------------------------------------------------+
| ha_config             | Action syntax migration, UI automations, ZHA quirks & scene matrix       |
| ha_addons_ext         | Trillion voice agent, diyHue sync, Ingress schemas & multi-arch builds     |
| homelab_infra         | Justfile recipes, Pyinfra state scripts, safe non-interactive apt runners |
| llm_stack_core        | Reasonix router, setup_wizard.py, 1-click installers, model benchmark     |
| llm_stack_config      | Host endpoint templates, .env.example blueprints                         |
| agents_and_prompts    | Prompts catalog, models.json tier definitions, subagent specs            |
| NetworkAnalyseStack   | Wireshark, Zeek, Suricata capture & telemetry scripts                     |
| proxmox_host_backup   | ZFS snapshot retention, automated pruning, link_down NIC toggling        |
| homelab_config        | Core service definitions, secrets isolation templates                     |
| ha_core / ha_backup   | Backup consolidation, clean restore recipes                               |
+---------------------------------------------------------------------------------------------------+
```

---

## 3. Pull Request & Delivery Instructions
- Create clean, descriptive feature branches (e.g. `jules/modernize-<repo-name>`).
- Submit PRs with clear conventional commit messages.
- All PRs are governed by **Global Auto-Acceptance** and will be immediately integrated into `main`.
