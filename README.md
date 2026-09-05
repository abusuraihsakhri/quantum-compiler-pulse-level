# Quantum Compiler Pulse Level

> **Domain:** Post-Quantum Cryptography & Quantum Pulse-Level Microwave Control  
> **Reference Guidelines & Standards:** `NIST FIPS 203/204/205, Qiskit Pulse / OpenPulse Standard`

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

Quantum Compiler Pulse Level is a dual-domain analytical platform combining:

1. **Enterprise Post-Quantum Cryptography Suite** (`agents/`): Multi-worker consensus evaluation engine with HMAC-SHA256 tamper-evident audit trail and zero-PHI outbound data protection.
2. **Pulse-Level Microwave Control & Qiskit Pulse Calibration Agent** (`pulse_compiler/`): Specialized sub-agent system for DRAG pulse optimization, Rabi oscillation analysis, and state leakage auditing.

---

## ⚙️ Key Capabilities & Algorithmic Modules

### Enterprise Suite (agents/)
- **Multi-Worker Consensus Engine**: Three specialized workers (InvariantQC, SafetyEscalation, ProtocolConformance) evaluate task payloads with automated urgency classification.
- **Zero-PHI Outbound Interceptor**: Active regex inspection blocking SSNs, MRNs, phone numbers, emails, and patient identifiers.
- **Tamper-Evident HMAC-SHA256 Audit Trail**: Chained, cryptographically signed logs for every evaluation and state transition.
- **FastAPI REST API**: Exposes OpenAPI 3.1 REST endpoints (`/api/audit`, `/api/chat`, `/api/audit/logs`, `/health`, `/metrics`).

### Pulse Calibration Agent (pulse_compiler/)
- **DRAG Pulse Shaper Agent**: Primary parameter boundary auditor with Bayesian optimization tuning.
- **Rabi Oscillation Analyzer Agent**: Critical kinetics and security safeguard interlock.
- **State Leakage Auditor Agent**: Protocol conformance and anomaly triage with crosstalk-aware pulse scheduling.
- **Pulse Control Coordinator**: Executive coordinator managing execution ledger and air-gapped supervisory intelligence.

### Enrichment Modules
- **DRAG Pulse Optimization via Bayesian Tuning**: Dynamic threshold-based scoring with historical tracking.
- **Cross-Talk Aware Pulse Scheduling**: Correlation analysis for pulse scheduling optimization.
- **Active Learning Bayesian Calibration Engine**: Dynamic worker reliability weight tracking with Brier calibration drift monitoring.

---

## 💻 Installation

```bash
# Clone the repository
git clone https://github.com/abusuraihsakhri/quantum-compiler-pulse-level.git
cd quantum-compiler-pulse-level

# Install dependencies
pip install fastapi uvicorn pydantic pytest
```

### Environment Variables

| Variable | Description | Default |
|:---------|:------------|:--------|
| `AUDIT_SECRET_KEY` | Secret key for HMAC-SHA256 audit trail signing | Ephemeral (generated per session) |
| `MODEL_PROVIDER` | LLM provider for chat (mock, ollama, claude, openai) | mock |

---

## 💻 CLI Quickstart & Usage

### 1. Single Task Evaluation
```bash
python cli.py audit --task-id TASK-001 --target TARGET-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
```

### 2. Supervisory Chat
```bash
python cli.py chat "What is the system status?"
```

### 3. Batch CSV Processing
```bash
python cli.py batch -i sample.csv -o results.csv
```

### 4. Verify Audit Trail Integrity
```bash
python cli.py verify-audit
```

### 5. Launch REST API Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### 6. Pulse Calibration Agent CLI
```bash
python pulse_compiler/cli.py audit --task-id TASK-001 --target TARGET-01 --primary 29.4 --secondary 15.1 --critical --status DISCORDANT
python pulse_compiler/cli.py batch -i sample.csv -o pulse_results.csv
```

### Parameter Reference
- `--task-id`: Unique task identifier (string)
- `--target`: Target entity identifier (string)
- `--primary`: Primary measurement value (float)
- `--secondary`: Secondary metric value (float)
- `--critical`: Flag for critical/emergency status (boolean)
- `--status`: Status descriptor (e.g., NOMINAL, DISCORDANT_ANOMALY, MUTANT_VARIANT)

---

## 🛡️ Security & Enterprise Architecture

* **Zero-PHI Outbound Interceptor:** Active regex inspection blocking SSNs, MRNs, phone numbers, emails, and patient identifiers before any audit logging or outbound transmission.
* **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs with linked hash chain for integrity verification.
* **Path Traversal Protection:** Batch CSV processing validates input/output paths to prevent directory traversal attacks.
* **Input Validation:** Robust error handling for malformed CSV data with per-row error reporting.
* **Air-Gapped LLM Reasoning Adapter:** Agnostic integration for local Ollama instances, Claude 3.5 Sonnet, GPT-4o, and deterministic test mocks.
* **FastAPI & Prometheus Telemetry:** Exposes OpenAPI 3.1 REST endpoints and operational Prometheus metrics (`/metrics`).

---

## 🧪 Testing & Verification

Run the full automated test suite:

```bash
pytest -v
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py 1000
```

Run specific test modules:

```bash
pytest tests/test_security_and_validation.py -v
pytest tests/test_enrichment.py -v
pytest tests/test_pulse_compiler.py -v
```

---

## 🐳 Container Deployment

```bash
docker build -t quantum-compiler-pulse-level .
docker run -p 8000:8000 -e AUDIT_SECRET_KEY=your-secret-key quantum-compiler-pulse-level
```

Or using Docker Compose:

```bash
docker-compose up -d
```

---

## 📁 Project Structure

```
quantum-compiler-pulse-level/
├── agents/                    # Enterprise Post-Quantum Cryptography Suite
│   ├── __init__.py
│   ├── api.py                 # FastAPI REST endpoints
│   ├── base.py                # Security, PHI Guard, HMAC Audit Trail
│   ├── learning.py            # Active Learning Bayesian Calibration
│   ├── llm_factory.py         # LLM provider abstraction
│   ├── metrics.py             # Prometheus metrics exporter
│   ├── models.py              # Pydantic v2 schemas
│   ├── streamer.py            # WebSocket telemetry broadcaster
│   ├── supervisor.py          # Multi-worker orchestrator
│   └── workers.py             # Specialized evaluation workers
├── pulse_compiler/            # Qiskit Pulse Calibration Agent
│   ├── __init__.py
│   ├── agents.py              # DRAG, Rabi, Leakage sub-agents
│   ├── cli.py                 # Pulse calibration CLI
│   ├── engine.py              # Core algorithmic engine
│   ├── models.py              # Data models and telemetry
│   └── server.py              # FastAPI server factory
├── tests/                     # Pytest test suite
│   ├── test_enrichment.py     # Enrichment module tests
│   ├── test_pulse_compiler.py # Pulse calibration tests
│   ├── test_quantum_compiler_pulse_level.py  # Enterprise suite tests
│   └── test_security_and_validation.py       # Security & validation tests
├── web/index.html             # Operations console UI
├── cli.py                     # Main CLI entry point
├── pulse_compiler_app.py      # CLI wrapper
├── simulator.py               # High-throughput simulation
├── enrichment.py              # Enrichment feature modules
├── sample.csv                 # Sample batch input data
├── sample_payload.json        # Sample API payload
├── benchmark_dataset.json     # Golden benchmark test suite
├── openapi_spec.json          # OpenAPI 3.1 specification
├── Dockerfile                 # Container build
├── docker-compose.yml         # Container orchestration
└── pyproject.toml             # Package metadata
```

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.
