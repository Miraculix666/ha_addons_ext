# Task for Jules: Deep System Healing, ZHA Zigbee Mesh Optimization & Addon Health

## Target Domains: `ha_config`, `ha_addons_ext`, `llm_stack_core`
**Auto-Acceptance Mandate:** In accordance with `AGENTS.md` §1, all PRs, blueprints, and enhancements produced by Jules under this task are auto-accepted and fast-tracked into production.

---

## 1. Objectives & Required Actions

### A. Zigbee & ZHA Mesh Health (`ha_config`)
1. **OSRAM / Ledvance Smart+ Plugs OTA Modernization:**
   - Detect all 19 OSRAM `Plug 01` (model `AB3257001DG`) repeaters in the mesh.
   - Enforce sequential OTA firmware update triggers for nodes on legacy firmware `0x01020412` and `0x01020490` (especially `Poolpumpe`, `Schneeflocke`, `Basteln`, `Gartenhütte`, `Kompressor`, `TV-Licht - Whz`) using the configured Koenkk / Ledvance OTA repository index.
   - For end-devices (e.g. LUMI Aqara sensors, IKEA remotes) that stick to dead routes, ensure keep-alive re-interview routines run sequentially through `zha_smart_maintenance.yaml`.

2. **ZHA Maintenance Automations & Cache Clear:**
   - Maintain `shell_command.zha_fix_clear_cache` and ensure `zha_smart_maintenance.yaml` automations recover failed router nodes without network flooding.

### B. Addon & Integration Health (`ha_addons_ext`, `ha_config`)
1. **Wyoming Voice Pipeline Recovery:**
   - Audit Wyoming protocol listeners (`Whisper`, `Piper`, `openWakeWord`) and ensure systemd/docker services on the local stack are reachable and auto-restart on socket timeouts.
2. **Offline Hardware Graceful Degradation:**
   - Ensure Moonraker, Yeelight, and Bluetooth integrations gracefully degrade when devices are powered down, preventing log pollution and state stalling.

### C. LLM Stack & Local AI Delegation (`llm_stack_core`)
1. **Reasonix & Local Model Health:**
   - Ensure native `llama.cpp` instances in CT 600 maintain warm inference routes for Home Assistant Assist (`Extended OpenAI Conversation` / `LLM Vision`).
   - Monitor memory usage and enforce the Primary Engine Principle (model swapping) on low-VRAM states.

---

## 2. Verification Criteria
* Validate all YAML configurations with `ha core check`.
* Verify ZHA OTA index parses without JSONDecodeErrors.
* Confirm no breaking changes or unhandled service calls exist.
