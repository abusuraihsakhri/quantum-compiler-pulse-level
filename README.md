# Quantum Compiler Pulse Level

A Python collection of **deterministic threshold evaluators** with CLI, optional FastAPI, CSV batch processing, and a standalone browser demonstration.

The project name is historical: the current implementation does **not** compile quantum gates to pulse waveforms, generate DRAG waveforms, model Rabi oscillations, interact with Qiskit hardware, or verify conformance to Qiskit/OpenPulse or NIST standards.

## Browser demonstration

The standalone [browser evaluator](web/index.html) implements the repository's example decision rules in JavaScript and can be used without a Python server. It evaluates a single task locally, displays its alerts, and supports JSON export. The root `index.html` links to this application for branch-based static hosting.

The GitHub repository advertises a Pages URL, but live availability has not been independently verified. The browser evaluator and Python server are separate implementations.

## Available Python interfaces

- `agents/`: primary metric > 25, secondary metric > 12, an optional critical flag, and a fixed set of descriptor substrings; results are summarized with a three-worker classification and an in-memory HMAC-SHA256 audit chain.
- `pulse_compiler/`: primary metric > 25, secondary metric > 10, a critical flag, and descriptor checks; produces alert dossiers.
- `enrichment.py`: additional threshold-based demonstration engines.
- `cli.py`: enterprise evaluation, chat mock, CSV processing, audit-chain verification, and FastAPI server.
- `pulse_compiler/cli.py`: independent pulse-labelled numeric evaluator CLI.
- `agents/api.py`: optional REST endpoints `/health`, `/api/audit`, `/api/chat`, `/api/audit/logs` and `/metrics`.

Thresholds are example software rules without calibrated scientific units. They are not validated safety limits.

## Install and run

Requires Python 3.9 or later.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[api,test]"

python cli.py audit --task-id T1 --target Q1 --primary 28.5 --secondary 14.2
python cli.py batch -i sample.csv -o results.csv
python -m pulse_compiler.cli audit --primary 29.4 --secondary 15.1
python cli.py serve --host 127.0.0.1 --port 8000
```

The API serves on port 8000 by default. For a static frontend, open `web/index.html` in a browser or use a static file server. GitHub Pages cannot host the Python API.

## Security and privacy

- The browser demonstration does not send task data to a server. JSON exports include the supplied identifiers, so avoid submitting sensitive data.
- Python includes **pattern-based** detection for selected identifiers, not comprehensive de-identification or HIPAA certification. Do not use real patient data.
- Audit entries are retained **in memory** and are HMAC-signed with `AUDIT_SECRET_KEY`. Without a configured key, an ephemeral per-process key is used; audit entries do not survive restarts.
- `GET /api/audit/logs` returns 403 unless `AUDIT_LOGS_TOKEN` is configured and sent as an `Authorization: Bearer <token>` header. Protect the API behind authentication and TLS before network exposure; other endpoints do not implement authentication.
- `MODEL_PROVIDER` currently uses deterministic mock responses. No external model integration is implemented.

To run Docker Compose, provide a unique secret without committing it:

```bash
export AUDIT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
docker compose up --build
```

Optionally configure `AUDIT_LOGS_TOKEN` separately for authorized audit-log reads.

## Tests

```bash
python -m pytest -v
node --test tests/browser.test.cjs
```

The GitHub Actions workflow runs the Python suite on Python 3.10–3.12 and checks the browser decision rules with Node.js. Container smoke testing and external Pages availability require separate verification.

## Project layout

`agents/` contains the enterprise API, evaluator, mock chat adapter, and audit tooling. `pulse_compiler/` contains the separate numeric pulse-labelled evaluator. `web/` contains the static JavaScript application. `tests/` contains Python and browser regression tests.

## Browser compatibility and license

The static application uses standard browser JavaScript, DOM APIs, and Blob downloads; use a current desktop or mobile browser. It has no external JavaScript dependencies. The repository is licensed under [MIT](LICENSE).
