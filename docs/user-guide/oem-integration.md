# Codeme OEM SDK & Embedded Integration Guide

The Codeme OEM SDK (`codeme-oem-sdk`) enables third-party platforms, autonomous AI coding agents, and CI/CD vendors to embed Codeme verification engines directly into their runtime without shell subprocess overhead or text-formatting scrapers.

---

## SDK Features
- **Direct Programmatic API**: Call `SyntaxEngine`, `QualityEngine`, `VerifyEngine`, and `InvariantEngine` directly from Python or TypeScript.
- **Strict JSON Contracts**: Input and output conform to versioned JSON schemas:
  - `invocation-contract.v1.json`
  - `diagnostic-contract.v1.json`
- **Zero CLI Formatting Overhead**: Eliminates text parsing, terminal ANSI escape stripping, and subshell performance penalties.
- **Token Metrics & Savings Accounting**: Computes precise token usage metrics and estimated token savings achieved by avoiding noisy LLM repair loops.

---

## Quickstart (Python)

### 1. Installation
Install the standalone OEM SDK package:
```bash
pip install codeme-oem-sdk
```

### 2. Programmatic Execution Example
```python
from codeme_oem_sdk import CodemeClient, EngineType, InvocationRequest

client = CodemeClient()

# Execute verification request
request = InvocationRequest(
    engine=EngineType.QUALITY,
    target_path="src/service.py",
    options={"max_complexity": 8, "enforce_ddd": True}
)

response = client.execute(request)

if response.success:
    print("Code verified clean.")
else:
    print(f"Detected {len(response.diagnostics)} violations:")
    for diag in response.diagnostics:
        print(f" - [{diag.rule_id}] Line {diag.line}: {diag.message}")
```

### 3. Token Accounting Example
```python
savings = client.get_token_metrics()
print(f"Total tokens saved by autonomous repair: {savings.estimated_tokens_saved}")
print(f"Direct LLM calls avoided: {savings.prevented_llm_roundtrips}")
```
