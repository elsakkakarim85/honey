# ApisLM Developer SDK & Plugin Guide

Welcome to the **ApisLM Open SDK**. This guide empowers hardware vendors, drone operators, and Agritech developers to build community plugins that seamlessly integrate with the ApisLM Zero-Cost Swarm Platform.

## 1. What is an ApisLM Plugin?

An ApisLM Plugin is a standalone Python module that is dynamically loaded by the local FastAPI server. Plugins can:
- Mount custom API endpoints.
- Intercept Core Events (e.g., `onHiveWeightDrop`, `onVarroaThresholdReached`).
- Access the offline **LLaMA-3 GGUF Model** without managing inference code.
- Query the local **Qdrant Vector Database**.
- Send Audio alerts via the Edge Mobile App's **Piper TTS**.

## 2. Writing Your First Plugin

Create a file in `ApisLM_Local_Backend/plugins/`, e.g., `smart_drone_feeder.py`.

```python
from fastapi import APIRouter
from pydantic import BaseModel
import requests

# 1. Define the required setup() function
def setup(router: APIRouter):
    print("Initializing DJI Agras Smart Feeder Plugin...")
    
    # 2. Register your custom endpoints on the shared router
    @router.post("/dji_feeder/deploy")
    async def deploy_drone(apiary_id: str):
        # 3. Hook into core ApisLM AI (Example using local SDK)
        # response = await apislm_sdk.llm.query(f"Generate drone flight path for {apiary_id}")
        
        return {"status": "success", "message": f"Drone deployed to {apiary_id} with emergency fondant."}
```

## 3. Core SDK Event Hooks

The `ApisLM_SDK` exposes a Python/TypeScript event bus.

### TypeScript / React Native (Edge UI)
```typescript
import { ApisLMEvents } from 'apislm-sdk';

ApisLMEvents.on('onHiveWeightDrop', (data) => {
    console.log(`Hive ${data.hive_id} lost ${data.weight_lost}kg!`);
});
```

### Python (Backend)
```python
from apislm_sdk import event_bus

@event_bus.subscribe("onVarroaThresholdReached")
def handle_varroa_spike(hive_id, mite_count):
    # e.g., Trigger robotic organic acid dispenser
    pass
```

## 4. Submitting to the Marketplace
To feature your plugin in the ApisLM Next.js Extension Marketplace, submit a Pull Request with your signed Ed25519 hash. Our zero-gas DPP module will verify the signature upon installation, ensuring 100% security for beekeepers.
