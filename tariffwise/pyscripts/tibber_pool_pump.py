# [AI-EDIT] Agent: DevOps | Model: Gemini 3.7 Flash | Date: 2026-08-27 15:47 | Reason: Added strict never-to-exceed hard maximum price cutoff (hard_max_price_threshold) overriding all schedules and operations.
import datetime

@service
def tibber_evaluate_pool(
    target_entity=None,
    price_sensor=None,
    price_mode="brutto",
    negative_price_threshold=0.0,
    max_price_threshold=35.0,
    hard_max_price_enabled=True,
    hard_max_price_threshold=45.0,
    negative_prices_always_on=True,
    duration_summer_hours=4.0,
    duration_spring_autumn_hours=2.5,
    duration_winter_hours=1.5,
    summer_temp_threshold=22.0,
    winter_temp_threshold=12.0,
    season_sensor=None,
    temperature_sensor=None,
    quiet_hours_enabled=True,
    quiet_hours_start="22:00:00",
    quiet_hours_end="06:00:00",
    fallback_mode="fixed_time",
    fallback_time_start="12:00:00",
    fallback_duration_hours=1.5,
    optimization_engine="tariffwise",
    eos_entity=None,
    emhass_entity=None,
    pv_surplus_sensor=None,
    pv_surplus_threshold=1500.0
):
    if not target_entity:
        log.error("Pool Optimizer: Kein target_entity (Schalter für Poolpumpe) angegeben!")
        return

    now = datetime.datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    current_hour_str = now.strftime("%H")
    current_minute = (now.minute // 15) * 15
    current_slot = f"{current_hour_str}:{current_minute:02d}"
    now_time = now.time()

    # Track daily runtime in minutes
    if now.hour == 0 and now.minute < 15:
        state.set("sensor.pool_pump_runtime_today", value=0.0, new_attributes={"unit_of_measurement": "min", "icon": "mdi:clock"})
    else:
        current_switch_state = state.get(target_entity)
        if current_switch_state == "on":
            current_runtime = float(state.get("sensor.pool_pump_runtime_today") or 0.0)
            state.set("sensor.pool_pump_runtime_today", value=current_runtime + 15.0, new_attributes={"unit_of_measurement": "min", "icon": "mdi:clock"})
            try:
                service.call("input_datetime", "set_datetime", entity_id="input_datetime.pool_pump_last_run", timestamp=now.timestamp())
            except Exception:
                pass

    # -------------------------------------------------------------
    # 1. TEMPERATUR & SAISON-TAGESAUFTEILUNG (8 / 6 / 4 Intervalle)
    # -------------------------------------------------------------
    temp = 20.0
    if temperature_sensor:
        try:
            val = state.get(temperature_sensor)
            if val not in ["unknown", "unavailable", None]:
                temp = float(val)
        except Exception:
            pass

    season = "spring_autumn"
    if season_sensor:
        try:
            s_val = str(state.get(season_sensor)).lower()
            if "summer" in s_val or "sommer" in s_val:
                season = "summer"
            elif "winter" in s_val:
                season = "winter"
            else:
                season = "spring_autumn"
        except Exception:
            pass
    else:
        # Auto-detection based on temperature thresholds
        if temp >= float(summer_temp_threshold):
            season = "summer"
        elif temp <= float(winter_temp_threshold):
            season = "winter"
        else:
            season = "spring_autumn"

    if season == "summer":
        intervals_count = 8      # 8x 3-Stunden-Fenster (Tagesteilung durch 8)
        base_hours = float(duration_summer_hours)
    elif season == "winter":
        intervals_count = 4      # 4x 6-Stunden-Fenster (Tagesteilung durch 4)
        base_hours = float(duration_winter_hours)
    else:
        intervals_count = 6      # 6x 4-Stunden-Fenster (Tagesteilung durch 6)
        base_hours = float(duration_spring_autumn_hours)

    window_size_hours = 24 // intervals_count
    required_slots = max(intervals_count, round(base_hours * 4))

    # -------------------------------------------------------------
    # 2. SPERRZEITEN (QUIET HOURS / LÄRMSCHUTZ)
    # -------------------------------------------------------------
    is_quiet_time = False
    if quiet_hours_enabled:
        try:
            q_start = datetime.time.fromisoformat(quiet_hours_start[:5])
            q_end = datetime.time.fromisoformat(quiet_hours_end[:5])
            if q_start > q_end:
                is_quiet_time = (now_time >= q_start or now_time < q_end)
            else:
                is_quiet_time = (q_start <= now_time < q_end)
        except Exception as ex:
            log.warning(f"Pool Optimizer: Fehler beim Parsen der Sperrzeiten: {ex}")

    # -------------------------------------------------------------
    # 3. PREIS-ERMITTLUNG & FALLBACK-LOGIK
    # -------------------------------------------------------------
    price_blocks = []
    price_source = "unknown"

    # Try custom price sensor first if provided
    if price_sensor:
        try:
            p_attrs = state.getattr(price_sensor) or {}
            for day in ["today", "tomorrow", "raw_today", "raw_tomorrow", "prices"]:
                if day in p_attrs and isinstance(p_attrs[day], list):
                    for b in p_attrs[day]:
                        st = b.get("startsAt") or b.get("start_time") or b.get("start")
                        # Gross vs Netto Spot Price selection
                        if price_mode == "netto_spot" and "marketprice" in b:
                            pr = b.get("marketprice")
                        elif price_mode == "netto_spot" and "energy" in b:
                            pr = b.get("energy")
                        else:
                            pr = b.get("total") if "total" in b else b.get("price") or b.get("value")
                        if st and pr is not None:
                            price_blocks.append({"start_time": str(st), "price": float(pr)})
            if price_blocks:
                price_source = price_sensor
        except Exception:
            pass

    # Automatic fallback price discovery if no custom sensor worked
    if not price_blocks:
        try:
            from tariffwise_prices import get_all_blocks
            price_blocks = get_all_blocks()
            if price_blocks:
                price_source = "tariffwise_auto_discovery"
        except Exception:
            pass

    # Build today's 15-minute slot grid
    today_blocks = [b for b in price_blocks if str(b.get("start_time", "")).startswith(today_str)]
    slots = []

    if today_blocks:
        for b in today_blocks:
            st_str = str(b["start_time"])
            # Format: 2026-08-27T10:00:00...
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

    # Find current price
    current_price = None
    if slots:
        for s in slots:
            if s["time"] == current_slot:
                current_price = s["price"]
                break

    # Check Hard Maximum Price violation (Niemals zu überschreitender Maximalpreis)
    hard_max_limit_hit = False
    if hard_max_price_enabled and current_price is not None:
        # Scale check: if user entered e.g. 45 (ct) and price is 0.45 (EUR), handle scaling
        limit_val = float(hard_max_price_threshold)
        if current_price > 1.0 and limit_val < 1.0:
            limit_val = limit_val * 100.0
        elif current_price < 1.0 and limit_val > 1.0:
            limit_val = limit_val / 100.0

        if current_price > limit_val:
            hard_max_limit_hit = True

    # -------------------------------------------------------------
    # 4. ENTSCHEIDUNG: DYNAMIC PRICE VS. FALLBACK VS. EOS/EMHASS
    # -------------------------------------------------------------
    scheduled_slots = set()
    system_mode_status = "Dynamic Price Active"

    # Check for direct EOS or EMHASS override if enabled
    eos_active = False
    if optimization_engine in ["eos", "hybrid"] and eos_entity:
        try:
            if state.get(eos_entity) == "on":
                eos_active = True
                system_mode_status = "Akkudoktor EOS Override Active"
        except Exception:
            pass

    emhass_active = False
    if optimization_engine in ["emhass", "hybrid"] and emhass_entity:
        try:
            if state.get(emhass_entity) == "on":
                emhass_active = True
                system_mode_status = "EMHASS MPC Override Active"
        except Exception:
            pass

    # PV Surplus boost if sensor exists
    pv_boost = False
    if pv_surplus_sensor:
        try:
            pv_val = float(state.get(pv_surplus_sensor) or 0.0)
            if pv_val >= float(pv_surplus_threshold):
                pv_boost = True
                system_mode_status = f"PV Surplus Boost Active ({pv_val:.0f} W)"
        except Exception:
            pass

    if slots and len(slots) >= 24:
        # Filter slots by hard max price if enabled
        valid_slots = slots
        if hard_max_price_enabled:
            limit_val = float(hard_max_price_threshold)
            if slots[0]["price"] < 1.0 and limit_val > 1.0:
                limit_val = limit_val / 100.0
            valid_slots = [s for s in slots if s["price"] <= limit_val]

        if not valid_slots:
            valid_slots = slots  # fallback to slots if all exceed limit

        # Dynamic Price calculation across intervals
        for i in range(intervals_count):
            start_h = i * window_size_hours
            end_h = start_h + window_size_hours
            interval_slots = [s for s in valid_slots if start_h <= s["hour"] < end_h]
            if interval_slots:
                cheapest = min(interval_slots, key=lambda x: x["price"])
                scheduled_slots.add(cheapest["time"])

        # Fill remaining required hours
        remaining_needed = required_slots - len(scheduled_slots)
        if remaining_needed > 0:
            remaining_slots = [s for s in valid_slots if s["time"] not in scheduled_slots]
            # Filter out slots above max_price_threshold if possible
            soft_limit = float(max_price_threshold)
            if slots[0]["price"] < 1.0 and soft_limit > 1.0:
                soft_limit = soft_limit / 100.0

            affordable_remaining = [s for s in remaining_slots if s["price"] <= soft_limit]
            if len(affordable_remaining) >= remaining_needed:
                affordable_remaining.sort(key=lambda x: x["price"])
                for s in affordable_remaining[:remaining_needed]:
                    scheduled_slots.add(s["time"])
            else:
                remaining_slots.sort(key=lambda x: x["price"])
                for s in remaining_slots[:remaining_needed]:
                    scheduled_slots.add(s["time"])

        # Negative price super-charge (always on if price <= negative_price_threshold)
        if negative_prices_always_on:
            neg_limit = float(negative_price_threshold)
            if slots[0]["price"] < 1.0 and neg_limit > 1.0:
                neg_limit = neg_limit / 100.0
            for s in slots:
                if s["price"] <= neg_limit:
                    scheduled_slots.add(s["time"])

    else:
        # -------------------------------------------------------------
        # FALLBACK VARIANTE (WENN KEIN PREIS VERFÜGBAR / API DROPPED)
        # -------------------------------------------------------------
        system_mode_status = f"Fallback Mode Active ({fallback_mode})"
        log.warning(f"Pool Optimizer: Keine Preise verfügbar. Aktiviere Fallback: {fallback_mode}")

        if fallback_mode == "fixed_time":
            try:
                fb_start_dt = datetime.datetime.strptime(fallback_time_start[:5], "%H:%M")
                fb_duration_min = int(float(fallback_duration_hours) * 60)
                for m_offset in range(0, fb_duration_min, 15):
                    slot_dt = fb_start_dt + datetime.timedelta(minutes=m_offset)
                    scheduled_slots.add(slot_dt.strftime("%H:%M"))
            except Exception as e:
                scheduled_slots.update(["12:00", "12:15", "12:30", "12:45", "13:00", "13:15"])
        else:
            for i in range(intervals_count):
                start_h = i * window_size_hours
                scheduled_slots.add(f"{start_h:02d}:00")

    # Filter out quiet hours from schedule unless negative price super-charge occurs
    if quiet_hours_enabled and not (negative_prices_always_on and slots and any(s["price"] <= float(negative_price_threshold) and s["time"] == current_slot for s in slots)):
        try:
            q_start_h = int(quiet_hours_start[:2])
            q_end_h = int(quiet_hours_end[:2])
            filtered_slots = set()
            for s_time in scheduled_slots:
                s_h = int(s_time[:2])
                if q_start_h > q_end_h:
                    if not (s_h >= q_start_h or s_h < q_end_h):
                        filtered_slots.add(s_time)
                else:
                    if not (q_start_h <= s_h < q_end_h):
                        filtered_slots.add(s_time)
            scheduled_slots = filtered_slots
        except Exception:
            pass

    # -------------------------------------------------------------
    # 5. SCHALT-ENTSCHEIDUNG & HARD MAX PREIS-SPERRE
    # -------------------------------------------------------------
    should_run = False

    if hard_max_limit_hit:
        should_run = False
        system_mode_status = f"⛔ Preissperre aktiv (Strompreis {current_price} übersteigt absoluten Maximalpreis {hard_max_price_threshold})"
        log.warning(f"Pool Optimizer: {system_mode_status}")
    elif is_quiet_time and not (negative_prices_always_on and slots and any(s["price"] <= float(negative_price_threshold) and s["time"] == current_slot for s in slots)):
        should_run = False
        system_mode_status = "Sperrzeit aktiv (Lärmschutz)"
    elif eos_active or emhass_active or pv_boost:
        should_run = True
    elif current_slot in scheduled_slots:
        should_run = True

    # Update sensors for Lovelace UI
    today_schedule_str = ", ".join(sorted(list(scheduled_slots))) if scheduled_slots else "Keine Läufe (Sperrzeit/Inaktiv)"
    state.set(
        "sensor.pool_pump_schedule_today",
        value=today_schedule_str,
        new_attributes={
            "icon": "mdi:pool",
            "season": season,
            "intervals": intervals_count,
            "window_size_hours": window_size_hours,
            "target_hours": base_hours,
            "system_mode": system_mode_status,
            "price_source": price_source,
            "price_mode": price_mode,
            "quiet_hours_active": is_quiet_time,
            "hard_max_price_hit": hard_max_limit_hit
        }
    )

    # Execute physical switch state
    current_state = state.get(target_entity)
    if should_run:
        if current_state != "on":
            log.info(f"Pool Optimizer: Schalte {target_entity} EIN (Grund: {system_mode_status}, Slot: {current_slot})")
            service.call("switch", "turn_on", entity_id=target_entity)
    else:
        if current_state != "off":
            log.info(f"Pool Optimizer: Schalte {target_entity} AUS (Grund: {system_mode_status})")
            service.call("switch", "turn_off", entity_id=target_entity)
