# [DONE] # Directive for Jules: Universal Addon Discovery & Store Notifier Blueprint

## Objective
Develop a high-quality, UI-compatible Home Assistant Blueprint and accompanying YAML automation package to proactively detect and notify users about new additions to the Home Assistant Addon Store and available addon updates.

## Technical Specifications & Requirements
1. **Repository Target:** `/GitHub/ha_addons_ext/updateall/blueprints/addon_store_discovery.yaml`
2. **Domain:** `automation`
3. **UI-Compatibility (Mandatory):**
   - 100% Home Assistant 2026+ Standard compliant.
   - Use `action:` exclusively (no deprecated `service:` calls).
   - No YAML anchors/aliases (`&`, `*`).
   - Use standard HA Selectors (`device`, `boolean`, `select`, `text`).
4. **Trigger Mechanism:**
   - State trigger on `update.home_assistant_supervisor_update` or catalogue refresh events.
   - Time pattern cron trigger (`hours: "/6"` or customizable).
5. **Detection Logic:**
   - Detect non-installed store items: `states.update | selectattr('attributes.installed', 'equalto', false) | list`
   - Detect pending updates: `states.update | selectattr('state', 'eq', 'on') | list`
6. **Notification Capabilities:**
   - Push notification via Companion App (`mobile_app`) with actionable buttons (`Open Addon Store`, `Install`).
   - Persistent notification creation in Home Assistant Core (`persistent_notification.create`).

Please implement this blueprint and test syntax validity.

