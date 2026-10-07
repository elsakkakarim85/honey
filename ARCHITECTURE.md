# ApisLM: Global Swarm Architecture

The ApisLM ecosystem is a radically decentralized, Zero-Cost apiculture platform. It unifies IoT telemetry, edge AI inference, and federated learning into a seamless local-first architecture.

## System Diagram

```mermaid
graph TD
    subgraph Edge IoT [Zero-Cost Solar Hardware]
        ESP32[ESP32 Node] -->|Weight & Temp| Si7021[Sensors]
        ESP32 -->|Acoustic Frequency| Mic[Analog Mic]
    end

    subgraph Mobile UI [React Native Edge App]
        AR[AR Field Guide & Skia]
        UI[AI Advisor Chat]
        Acad[Omnimodal Academy]
        Twin[Virtual Apiary Simulator]
        Brand[Marketing & Brand Studio]
    end

    subgraph Local Server [FastAPI / Python Backend]
        API[API Gateway]
        Qdrant[(Qdrant Vector DB)]
        LLM[LLaMA-3 GGUF Model]
        TTS[Piper TTS Audio]
        DPP[Zero-Gas Ed25519 DPP]
        SDR[Automated B2B CRM]
        FedAvg[P2P Swarm Sync]
    end

    %% Data Flow
    ESP32 ==>|Wi-Fi / Mesh| API
    UI <==> API
    AR --> LLM
    Acad <==> Qdrant
    Twin <==> API
    Brand ==> API
    API <==> LLM
    API ==> DPP
    API ==> SDR
    LLM <==> FedAvg
    
    %% External Nodes
    FedAvg <..>|WebRTC Deltas| GlobalSwarm((Global Swarm Network))
    SDR ==>|SMTP| Buyers(B2B Honey Buyers)
```

## Core Modules Overview

1. **Hardware & Telemetry:** `ApisLM_IoT_Edge` gathers acoustics and climate data via C++ ESP32 firmware, posting to the local backend.
2. **Local Intelligence:** `ApisLM_Local_Backend` hosts the FastAPI server, the offline CRAG (Corrective Retrieval-Augmented Generation) pipeline, and the mathematical logic for the Digital Twin.
3. **Decentralization:** `federated_swarm_sync.py` executes mathematical federated averaging (FedAvg) on DPO weight deltas, broadcasting them globally with differential privacy.
4. **Edge Interface:** `ApisLM_Mobile_Edge` executes 60fps TFLite object detection, SuperMemo-2 spaced repetition, and interactive marketing tools.
5. **Traceability:** Local Python logic uses Ed25519 keys to generate cryptographic QR codes for Honey Jars and Academy Certificates, guaranteeing authenticity without paying gas fees.
