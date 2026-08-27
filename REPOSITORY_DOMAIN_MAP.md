# 🗺️ Master Repository Restructuring & Domain Architecture Map

**Target Systems & Agents:** Google Antigravity (IDE/CLI), Jules (`jules.google.com`), Claude Code, Gemini CLI, Hermes Agent, OpenJarvis  
**Standard Version:** 4.0.0 (Post-Restructuring SSOT)  
**Root Path:** `/GitHub/` (Linux) / `C:\GitHub\` (Windows)

---

## 🌐 1. Active Repositories (Single-Source-of-Truth Matrix)

| Repository | Domain / Layer | Scope & Purpose | Remote URL |
| :--- | :--- | :--- | :--- |
| **`ha_config`** | Home Assistant / Config | Live Home Assistant Konfiguration (`configuration.yaml`, `automations.yaml`, `packages/`, `dashboards/`, `themes/`, `scripts/`, `blueprints/`). | `https://github.com/Miraculix666/ha_config.git` |
| **`homelab_infra`** | DevOps & Host / Infra | Host-Administration, Proxmox-Automatisierung, Pyinfra Playbooks, Justfiles, Backup- & CI/CD-Pipelines (Komodo). | `https://github.com/Miraculix666/homelab_infra.git` |
| **`llm_stack_core`** | AI & Local LLM / Core | LLM-Server (`llama.cpp`), Reasonix Multi-Tier Router, AI Model Benchmarker, LXC-Template Konfigurationen. | `https://github.com/Miraculix666/llm_stack_core.git` |
| **`ha_addons_ext`** | Home Assistant / Addons | Externe Addons, Custom Integrations (HACS), TariffWise Extension, Zusatz-Tools. | `https://github.com/Miraculix666/ha_addons_ext.git` |
| **`agents_and_prompts`**| Agent Directives / Meta | System-Prompts, Agenten-Rollen, Knowledge-Base Skills, Model-Manifests (`models.json`). | `https://github.com/Miraculix666/agents_and_prompts.git` |
| **`homelab_config`** | Homelab / Config | Proxmox Host-Backups (`/etc/pve/`, Network, Storage, Cron), Traefik Proxy Configs. | `https://github.com/Miraculix666/homelab_config.git` |
| **`ha_core`** | Home Assistant / Core | Modifizierte Core-Komponenten, System-Patches, Upstream-Forks. | `https://github.com/Miraculix666/ha_core.git` |
| **`ha_backup`** | Home Assistant / Backup | Kanonisches Backup-Repository für HA-Konfigurations-Snapshots (nach Unarchive auf GitHub aktiv). | `https://github.com/Miraculix666/HA_backup.git` |

---

## 📦 2. Restrukturierte & Archivierte Repositories (Legacy -> New Mapping)

| Altes / Veraltetes Repo / Pfad | Neuer kanonischer Pfad | Status / Hinweis |
| :--- | :--- | :--- |
| `ha_git_mirror` / `ha_git_mirror_config_backup` | `/GitHub/ha_config` | **Konsolidiert & Ersetzt** (Aktiver Live-Mirror) |
| `homelab_devops` | `/GitHub/homelab_infra` | **Umbenannt & Migriert** (Pyinfra & Just SSOT) |
| `LLM_Stack` | `/GitHub/llm_stack_core` | **Umbenannt & Strukturiert** (Llama.cpp & Reasonix) |
| `HA-addons_hacs` | `/GitHub/ha_addons_ext` | **Umbenannt & Aufgeteilt** (Addons & HACS) |
| `ha_backup_slim` | `/GitHub/homelab_infra/archive/` / `ha_backup` | **Archiviert** (Zusammengeführt in `ha_backup`) |
| `ha_backup_full` | `homelab_infra/archive/` | **Archiviert** (Read-Only) |
| `/root/ha_git_mirror` / `/root/scripts` | `/GitHub/ha_config` / `/GitHub/homelab_infra/scripts` | **Symlinks/Pfade bereinigt** |

---

## 🤖 3. Verbindliche Direktiven für alle KI-Agenten

1. **Keine veralteten Pfadnamen verwenden:**
   - Niemals mehr Referenzen zu `homelab_devops`, `ha_git_mirror` oder `ha_backup_slim` neu anlegen.
2. **Dynamische Pfadauflösung (Rule 17):**
   - Skripte und Justfiles ermitteln Pfade immer über Umgebungsvariablen (`PROJECT_ROOT`, `HA_CONFIG_DIR`, `INFRA_DIR`) oder relativ zum Skriptverzeichnis (`Path(__file__).resolve().parent`).
3. **Domain Segregation & Secrets (Rule 4):**
   - Zugangsdaten und Tokens dürfen NIEMALS in Repositories committed werden. Alle sensiblen Variablen gehören in `/GitHub/homelab_infra/infra/.env` (isoliert und per `.gitignore` geschützt).
