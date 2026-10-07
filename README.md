# ApisLM: Zero-Cost Swarm Intelligence for Beekeeping 🐝

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

Welcome to **ApisLM**, a radically decentralized, Zero-Cost open-source ecosystem designed to bring enterprise-grade AI and IoT telemetry to beekeepers globally. 

## The Vision
Commercial apiculture suffers from a severe technology gap. Sensor networks are expensive, cloud AI fees are recurring, and rural apiaries lack reliable internet connectivity.

ApisLM solves this by leveraging the hardware already in the beekeeper's pocket: **The Smartphone**. 

By processing audio diagnostics locally via a quantized LLM (ApisLM-3B) and maintaining a local RAG (Retrieval-Augmented Generation) pipeline, we eliminate AWS/GCP cloud costs entirely. This allows beekeepers in rural areas to instantly diagnose colony stress, varroa mite levels, and swarming intent entirely offline.

## System Architecture

Our ecosystem comprises three highly decoupled layers:

1. **Edge IoT Network (ESP32)**: Ultra-cheap microcontrollers send weight, humidity, and acoustic frequency data.
2. **Local AI Hub (Smartphone/Laptop)**: A FastAPI server that runs local quantized models (GGUF) and a Qdrant Vector database for the CRAG (Corrective RAG) pipeline.
3. **Decentralized Swarm Intelligence**: Every node securely averages its DPO (Direct Preference Optimization) RLHF weight updates with global peers via a privacy-preserving P2P federated averaging protocol.

## Zero-Cost Philosophy

- **No API Keys**: We use local models like LLaMA-3 (quantized to 4-bit) instead of OpenAI.
- **No Cloud DBs**: Telemetry is stored via local SQLite, and memory via local Qdrant.
- **Federated Learning**: Instead of paying for central supercomputers to train on data, the models get smarter by anonymously averaging the mathematical weight deltas of local experts. Your raw data never leaves your device.

## Getting Started

We have provided One-Click Installers to instantly provision your local environment.

### Windows
```cmd
cd ApisLM_Workspace
setup_windows.bat
```

### Linux / macOS
```bash
cd ApisLM_Workspace
chmod +x setup_linux_mac.sh
./setup_linux_mac.sh
```

## Contributing
We welcome researchers, rust developers, and apiculture experts. See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to join the Swarm!
