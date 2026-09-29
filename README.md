# genpark-cloud-sandbox-task-delegation-coordinator-skill

> Cloud Sandbox Long-Running Task Delegation Coordinator with Heartbeats. 100% Python Standard Library.

Distilled from **Muse** (Meta) and **Instinct**, where personal agents manage long-horizon web tasks in isolated cloud virtual sandboxes while broadcasting periodic progress heartbeats back to messaging channels.

## Architecture

```mermaid
flowchart TD
    UserMsg["User via WhatsApp / iMessage ('Find best flight deals')"] --> Dispatch["Delegate Task to Cloud Sandbox Coordinator"]
    Dispatch --> VMSpawn["Spawn Cloud Sandbox Task Worker"]
    VMSpawn --> Step1["Step 1: Scrape airline booking sites"]
    Step1 --> CP1["Record Checkpoint (30%) & Push Heartbeat"]
    Step1 --> Step2["Step 2: Compare layovers & bag fees"]
    Step2 --> CP2["Record Checkpoint (80%) & Push Heartbeat"]
    Step2 --> Completion["Finalize Task & Summarize"]
    Completion --> Delivery["Deliver Actionable Summary to Messaging Thread"]
```

## Features
- **Asynchronous State Checkpointing**: Retains execution milestones for graceful resume after disconnections.
- **Heartbeat Emitters**: Emits real-time progress percentages to keep users informed without message spam.
- **Clean Completion Hooks**: Bundles final insights into concise messages suitable for SMS/iMessage delivery.
