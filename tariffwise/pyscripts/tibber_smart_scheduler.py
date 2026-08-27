# [AI-EDIT] Agent: DevOps | Model: Gemini 3.7 Flash | Date: 2026-08-27 15:50 | Reason: Universal smart scheduler for arbitrary devices (washing machine, dishwasher, EV, boiler) supporting deadline windows, continuous vs split blocks, price caps, and push notifications.
import datetime

@service
def tibber_evaluate_device(
    target_entity=None,
    hours=2.0,
    start_time="00:00:00",
    end_time="23:59:00",
    continuous=False,
    price_sensor=None,
    price_mode="brutto",
    hard_max_price_enabled=False,
    hard_max_price_threshold=45.0,
    negative_prices_always_on=False,
    notify_device=None
):
    if not target_entity:
        log.error("Universal Scheduler: Kein target_entity angegeben!")
        return

    try:
        hours = float(hours)
    except Exception:
        hours = 2.0

    now = datetime.datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    tomorrow_str = (now + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    current_hour_str = now.strftime("%H")
    current_minute = (now.minute // 15) * 15
    current_slot = f"{current_hour_str}:{current_minute:02d}"
    current_time_str = now.strftime("%H:%M:%S")

    # Format window times
    s_time = start_time[:5] if len(start_time) >= 5 else "00:00"
    e_time = end_time[:5] if len(end_time) >= 5 else "23:59"

    # -------------------------------------------------------------
    # 1. PREISDATEN BESCHAFFEN
    # -------------------------------------------------------------
    price_blocks = []
    
    if price_sensor:
        try:
            p_attrs = state.getattr(price_sensor) or {}
            for day in ["today", "tomorrow", "raw_today", "raw_tomorrow", "prices"]:
                if day in p_attrs and isinstance(p_attrs[day], list):
                    for b in p_attrs[day]:
                        st = b.get("startsAt") or b.get("start_time") or b.get("start")
                        if price_mode == "netto_spot" and "marketprice" in b:
                            pr = b.get("marketprice")
                        elif price_mode == "netto_spot" and "energy" in b:
                            pr = b.get("energy")
                        else:
                            pr = b.get("total") if "total" in b else b.get("price") or b.get("value")
                        if st and pr is not None:
                            price_blocks.append({"start_time": str(st), "price": float(pr)})
        except Exception:
            pass

    if not price_blocks:
        try:
            from tariffwise_prices import get_all_blocks
            price_blocks = get_all_blocks()
        except Exception:
            pass

    # Build 15-minute slots for today
    today_blocks = [b for b in price_blocks if str(b.get("start_time", "")).startswith(today_str)]
    slots = []

    if today_blocks:
        for b in today_blocks:
            st_str = str(b["start_time"])
            hour_part = st_str[11:13] if len(st_str) >= 13 else "00"
            try:
                h_int = int(hour_part)
            except:
                h_int = 0
            for m in [0, 15, 30, 45]:
                slots.append({
                    "time": f"{h_int:02d}:{m:02d}",
                    "hour": h_int,
                    "price": float(b["price"])
                })

    # -------------------------------------------------------------
    # 2. FILTERUNG NACH ZEITFENSTER (START BIS DEADLINE)
    # -------------------------------------------------------------
    window_slots = []
    for s in slots:
        t = s["time"]
        if s_time <= e_time:
            if s_time <= t <= e_time:
                window_slots.append(s)
        else:
            # Over midnight window
            if t >= s_time or t <= e_time:
                window_slots.append(s)

    if not window_slots:
        window_slots = slots  # fallback

    # Check Hard Max Price
    if hard_max_price_enabled and window_slots:
        limit_val = float(hard_max_price_threshold)
        if window_slots[0]["price"] < 1.0 and limit_val > 1.0:
            limit_val = limit_val / 100.0
        window_slots = [s for s in window_slots if s["price"] <= limit_val]

    slots_needed = max(1, int(round(hours * 4)))
    scheduled_slots = set()

    # -------------------------------------------------------------
    # 3. KONTINUIERLICHER BLOCK VS. GESTÜCKELTE SLOTS
    # -------------------------------------------------------------
    is_continuous = str(continuous).lower() in ["true", "1", "yes"]

    if is_continuous and len(window_slots) >= slots_needed:
        # Find continuous sequence of N 15-minute slots with minimum total price
        min_total_price = float("inf")
        best_sequence = []
        for i in range(len(window_slots) - slots_needed + 1):
            seq = window_slots[i : i + slots_needed]
            total_p = sum(s["price"] for s in seq)
            if total_p < min_total_price:
                min_total_price = total_p
                best_sequence = seq
        for s in best_sequence:
            scheduled_slots.add(s["time"])
    else:
        # Pick the N cheapest slots inside the window
        sorted_slots = sorted(window_slots, key=lambda x: x["price"])
        for s in sorted_slots[:slots_needed]:
            scheduled_slots.add(s["time"])

    # Negative price super-charge
    if negative_prices_always_on:
        for s in slots:
            if s["price"] <= 0.0:
                scheduled_slots.add(s["time"])

    # -------------------------------------------------------------
    # 4. SCHALTUNG & NOTIFICATION
    # -------------------------------------------------------------
    should_run = current_slot in scheduled_slots
    current_state = state.get(target_entity)
    attrs = state.getattr(target_entity) or {}
    friendly_name = attrs.get("friendly_name") or target_entity

    # Friendly schedule string
    sched_list = sorted(list(scheduled_slots))
    schedule_str = ", ".join(sched_list) if sched_list else "Keine Läufe im Zeitfenster"

    # Status Sensor
    safe_slug = target_entity.replace(".", "_")
    state.set(
        f"sensor.smart_schedule_{safe_slug}",
        value=schedule_str,
        new_attributes={
            "icon": "mdi:calendar-clock",
            "target_entity": target_entity,
            "friendly_name": f"Zeitplan: {friendly_name}",
            "requested_hours": hours,
            "window": f"{s_time} - {e_time}",
            "continuous_mode": is_continuous,
            "should_run_now": should_run
        }
    )

    if should_run:
        if current_state != "on":
            log.info(f"Universal Scheduler: Schalte {target_entity} EIN ({friendly_name}, Slot: {current_slot})")
            service.call("homeassistant", "turn_on", entity_id=target_entity)
            if notify_device and notify_device != "":
                try:
                    service.call(
                        notify_device.split(".")[0],
                        notify_device.split(".")[1] if "." in notify_device else "notify",
                        title="⚡ Günstigster Strompreis aktiv",
                        message=f"{friendly_name} wurde gestartet (Günstigster Preisslot: {current_slot} Uhr)."
                    )
                except Exception:
                    pass
    else:
        if current_state != "off":
            log.info(f"Universal Scheduler: Schalte {target_entity} AUS ({friendly_name}, Slot {current_slot} beendet)")
            service.call("homeassistant", "turn_off", entity_id=target_entity)
