# ⚙️ TASK FOR JULES: Anzeigen- & Verkaufssystem Update (Auto-Seller Stack)

## 🎯 Objective
Upgrade the existing automated ads and sales system ("Automatisches Anzeigen- und Verkaufssystem"). The system requires two major new architectural features:

1. **Multi-User Capability (Mandantenfähigkeit):** 
   The system must be upgraded to support multiple independent users/accounts. Each user must be able to manage their own ads, inventory, messages, and sales without cross-contamination.
   
2. **Automatic Label Printing (Automatischer Labeldruck):** 
   Integrate a pipeline for automated shipping label generation and direct printing. As soon as a sale is finalized and paid, the system should automatically generate the shipping label and send it directly to a local/network printer.

3. **Dynamic Pricing Strategies (Preisfestsetzung):**
   Implement a pricing engine with selectable default strategies per category/item:
   - "Billig / Hauptsache weg" (Cheap / Just get rid of it)
   - "Normaler Marktpreis" (Normal market price)
   - "Leicht oberhalb" (Slightly above market for negotiation room)
   - "Eher teuer" (Premium / Expensive)
   
4. **Deployment Options (Aragog Target):**
   After successful implementation and testing, package the system so it can run as a standalone LXC, Docker container, or Home Assistant Add-on. Deploy/install the updated system directly on the host node **aragog**.

## 📋 Requirements & Architecture
- **Multi-User Architecture:** Implement tenant IDs or separate database schemas. Upgrade the authentication system for secure multi-account login.
- **Label Printing Pipeline:** Integrate with shipping APIs (e.g. DHL, Hermes) or parse incoming sales data. Generate PDF labels automatically. Connect to a local printer spooler (e.g., via CUPS) to print without manual interaction.
- **Code Standards (Rule 14 & 18):** Follow the Ponytail Decision Ladder (YAGNI, Reuse, Standard-Lib). No unnecessary heavy frameworks.
- **Deployment:** Provide a Dockerfile and Home Assistant Add-on config (`config.json`, `build.yaml`).

## 🚀 Execution Directive
@jules: Please analyze the codebase of the auto-seller stack, draft the multi-user schema changes, and implement the label printing and pricing logic. Once tested, merge the changes automatically according to the Global Auto-Acceptance Rule (Rule 1).
