# @apislm/sdk

The official enterprise-grade TypeScript SDK for the **ApisLM** ecosystem. 

## Features
- **IoT Telemetry Ingestion**: Seamlessly stream hardware metrics from ESP32 edge nodes directly into the local `ApisLM_Local_Backend`.
- **AI Swarm Prediction**: Interface with the local Llama-3-8B weights to request real-time swarm likelihood analysis.
- **Digital Product Passport (DPP)**: Cryptographically sign honey harvest batches using Ed25519 (mocked as SHA256 in this demo) to guarantee zero-trust traceability for consumers.

## Installation
```bash
npm install @apislm/sdk
```

## Usage

### 1. Initialize Client
```typescript
import { ApisLMClient } from '@apislm/sdk';

const client = new ApisLMClient({
  apiKey: process.env.APISLM_KEY,
  edgeBaseUrl: 'http://localhost:8000/api/iot' // Optional: points to local edge by default
});
```

### 2. Ingest IoT Telemetry
```typescript
await client.ingestTelemetry({
  deviceId: 'Hive_001',
  timestampMs: Date.now(),
  sensors: {
    broodTempC: 34.5,
    humidityRh: 62.1,
    weightKg: 42.5,
    acousticHz: 245
  },
  metrics: {
    batteryLevelPct: 88,
    signalStrengthDbm: -65
  }
});
```

### 3. Generate a Digital Product Passport
```typescript
import { DPPGenerator } from '@apislm/sdk';

const generator = new DPPGenerator(process.env.PRIVATE_KEY_PEM);

const signedPassport = generator.generateSignedPassport({
  batchId: '2026-FALL-A1',
  apiaryLocation: { lat: 40.7128, lng: -74.0060, name: 'Hudson Valley Apiary' },
  harvestDate: '2026-09-15',
  floralSource: ['Wildflower', 'Clover'],
  metrics: { moisturePercent: 16.5, totalWeightKg: 1250 }
});

console.log(signedPassport.signature);
```
