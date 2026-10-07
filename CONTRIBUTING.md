# Contributing to ApisLM 🐝

Thank you for your interest in contributing to ApisLM! By participating in this project, you are helping build a zero-cost, privacy-first Swarm Intelligence network for global food security.

## How Can I Contribute?

### 1. Code & Architecture (Developers)
- **Local LLM Optimization**: Help us further compress the GGUF models for older mobile devices.
- **P2P Federated Sync**: We are actively looking for network engineers to harden `federated_swarm_sync.py` using `libp2p`.
- **Next.js Dashboard**: Enhance the React UI in `ApisLM_Workspace/cloud-tenant-dashboard`.

### 2. Apiculture Experts (Data & RLHF)
You don't need to be a coder to contribute! By using the ApisLM Mobile App and providing "Thumbs Down" corrections (RLHF), your local DPO weight updates will be anonymously synced to the global Swarm network, making the AI smarter for everyone.

### 3. Edge Hardware (IoT)
Help us optimize the ESP32 C++ codebase for lower power consumption to maximize solar battery life in the field.

## Development Workflow

1. Fork the repository.
2. Run the One-Click Installer for your OS (`setup_windows.bat` or `setup_linux_mac.sh`).
3. Create a feature branch: `git checkout -b feature/amazing-feature`.
4. Commit your changes: `git commit -m 'feat: Add amazing feature'`.
5. Push to the branch: `git push origin feature/amazing-feature`.
6. Open a Pull Request.

## Swarm Privacy Policy
If you are contributing to the Federated Learning module, you must strictly adhere to our Zero-Data transmission policy. **Raw telemetry, audio recordings, and text MUST NOT leave the local device.** Only mathematical weight deltas (tensors) with added differential privacy noise are permitted over the P2P network.

Welcome to the Swarm!
