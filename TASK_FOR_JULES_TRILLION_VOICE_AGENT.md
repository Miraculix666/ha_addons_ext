# TASK FOR JULES: Autonomous Trillion Voice-First AI Agent & Jarvis Engine

**Assigned Agent:** Jules (`jules.google.com`)  
**Architecture Source:** Adapted from `hellotrillion.ai` (Trillion Voice-First AI Architecture)  
**Target Repositories:** `/GitHub/ha_addons_ext/trillion_voice_agent/`, `/GitHub/llm_stack_core/`, `/GitHub/ha_config/`  
**Execution Mode:** Autonomous Full Build, Fast-Track Auto-Accepted (Rule 1 SSOT)

---

## 1. Executive Summary & Objective
Implement a production-grade, low-latency (<1.0s turn-around), **Voice-First AI Agent ("Jarvis Homelab Co-Founder")** based on the architectural principles of `hellotrillion.ai`, adapted natively to our hybrid Proxmox, Home Assistant, and Local LLM (Reasonix / CT 600) stack.

---

## 2. Layer-by-Layer Architectural Specification (Trillion Adaptation)

```
+---------------------------------------------------------------------------------------------------+
|                        TRILLION VOICE-FIRST HYBRID AGENT ARCHITECTURE                             |
+---------------------------------------------------------------------------------------------------+
|  1. THE BRAIN (Multi-Tier Intelligence):                                                          |
|     • Tier 1 (Ultra-Fast Local): CT 600 Reasonix / Llama.cpp Qwen2.5-Coder (192.168.80.60:8080)   |
|     • Tier 2 (Domain Reasoning): devstral / Hermes-3 / Qwen-HA Quantized GGUF Models              |
|     • Tier 3 (Cloud Fallback & Coding): Claude Code / Gemini API / Jules Engine                   |
|                                                                                                   |
|  2. LOW-LATENCY AUDIO PIPELINE (<1s Streaming Loop):                                              |
|     • Speech-In (STT): Wyoming / Local Whisper + Fast Deepgram WebSocket streaming API           |
|     • Speech-Out (TTS): Local Piper (Fast) + ElevenLabs High-Fidelity Voice Synthesis             |
|     • Audio Stream Pipelining: Begin TTS token generation on the first emitted LLM sentence chunk |
|                                                                                                   |
|  3. PERSISTENT 3-TIER MEMORY & KNOWLEDGE SYSTEM:                                                  |
|     • Tier A (Core Identity): Two-block immutable persona prompt (German, precise, sarcastic/pro) |
|     • Tier B (Working Memory): Session context tracking stored in `/data/memory/working_state.json`|
|     • Tier C (Semantic Long-Term Memory): Markdown Obsidian Vault bridge in `/root/.hermes/...`   |
|                                                                                                   |
|  4. HOME ASSISTANT TOOL REGISTRY & SAFETY GUARDRAILS:                                             |
|     • Declarative MCP Tool Registry (`tools/ha_tools.py`): Query & toggle lights, climate, alarm  |
|     • Human-in-the-Loop Safety Gate: Destructive actions require explicit spoken confirmation     |
|                                                                                                   |
|  5. FRONTEND & MOBILE ORB UI:                                                                     |
|     • PWA Web-Audio Visualizer Orb (React/Vanilla JS) embedded as HA Lovelace Panel Card          |
+---------------------------------------------------------------------------------------------------+
```

---

## 3. Jules Deliverables & File Structure

Jules must generate and verify the following components in `/GitHub/ha_addons_ext/trillion_voice_agent/`:

```
trillion_voice_agent/
├── Dockerfile                      # Python 3.12 / FastAPI / Uvicorn / PyAudio / WebSockets
├── config.json                     # Supervisor Addon Metadata (Ingress, Audio, Port 8890)
├── manifest.json                   # Custom Component / Addon registration
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI WebSocket Server (Audio Streaming + Event Bus)
│   ├── brain.py                    # Multi-Tier LLM Router (CT 600 Reasonix <-> Cloud fallback)
│   ├── memory.py                   # 3-Tier Persistent Memory (Working JSON + Obsidian Vault sync)
│   ├── audio/
│   │   ├── stt_deepgram.py         # Deepgram Streaming WebSocket Client
│   │   ├── stt_whisper.py          # Wyoming Local Whisper Client
│   │   ├── tts_elevenlabs.py       # ElevenLabs Chunked Streamer
│   │   └── tts_piper.py            # Local Piper TTS Streamer
│   ├── tools/
│   │   ├── registry.py             # Tool Discovery & Function Calling Dispatcher
│   │   ├── ha_client.py            # Home Assistant REST & WebSocket API Adapter
│   │   └── safety_guard.py         # Human-in-the-Loop Confirmation Gate
│   └── frontend/
│       ├── index.html              # Mobile-first Voice Orb UI
│       ├── style.css               # Glowing Siri/Jarvis Neon Orb Styling
│       └── app.js                  # Web Audio API Streamer & Visualizer
└── tests/
    ├── test_latency.py             # Verify <1.0s Time-to-First-Audio-Byte (TTFAB)
    └── test_ha_tools.py            # Verify HA switch/light tool execution
```

---

## 4. Jules Verification & Auto-Acceptance Criteria
1. **Latency Verification:** Ensure streaming pipeline starts playing audio chunks before the entire response is completed.
2. **Offline-Resilience:** If internet is down, fallback automatically to local Whisper + Reasonix + Piper.
3. **Home Assistant Integration:** Register as custom panel in HA and expose service `trillion_voice.speak` and `trillion_voice.listen`.
4. **Git Sync:** Commit all files to `main` branch with clean conventional commit message.
