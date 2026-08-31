# ⚙️ Jules AI Agent Configuration & Execution Directives

## 🚀 Auto-Acceptance & Fast-Track Mode (Active)
- **Status:** **Auto-Accept & Direct Merge Enabled**
- **Review Requirement:** **NONE (Auto-Accept without manual review)**
- **Behavior:** All drafts, suggestions, blueprints, packages, and code changes proposed by Jules in branches or PRs are automatically merged and deployed into the main branch by the system sync daemon (`auto_jules_sync.py`).

## 📋 Guidelines for Jules:
1. Ensure all Home Assistant configurations follow modern 2026+ standards (`action:` instead of `service:`, no YAML anchors).
2. Commit directly or push feature branches named `jules/*` or `jules-*`.
3. Provide concise documentation alongside new components.
