# genpark-agent-hallucinated-tool-call-and-fuzzy-intent-resolver-skill

Resolves hallucinated agent tool calls, fuzzy parameter misspellings, and schema mismatches using Levenshtein distance and token similarity.

100% Python Standard Library implementation with zero external dependencies.

## Key Capabilities
- **Hallucinated Tool Resolution**: Compares model-invoked tool names against registered tool catalogs to find close syntactic or semantic matches.
- **Fuzzy Argument Alignment**: Maps misspelled or alternate argument names (e.g., `file_path` vs `AbsolutePath`) to formal tool schemas.
- **Confidence Scoring**: Returns probabilistic match confidence scores (0.0 - 1.0) with configurable fallback cutoffs.
- **Zero Dependencies**: Pure standard library execution with sub-millisecond match resolution.

## Architecture

```
[Hallucinated / Misspelled Tool Call]
                  │
                  ▼
┌──────────────────────────────────────────────┐
│  FuzzyToolResolver                           │
│  ├─ Levenshtein Edit Distance Matrix         │
│  ├─ Snake-case & Delimiter Normalization     │
│  ├─ Manifest Candidate Matcher               │
│  └─ Schema Property Align Engine             │
└──────────────────────────────────────────────┘
                  │
                  ▼
[Auto-Corrected Tool Invocations with Confidence]
```

## MCP Server Integration

Run standard MCP stdio server:
```bash
python mcp_server.py
```

Exposed Tools:
- `resolve_tool_name`: Maps an unrecognized tool name to the closest authorized manifest tool.
- `resolve_arguments`: Remaps misspelled argument names to valid schema properties.

## Quickstart

```python
from client import FuzzyToolResolver

valid_tools = ["view_file", "run_command", "write_to_file"]
res = FuzzyToolResolver.resolve_tool_name("view_file_contents", valid_tools)

print(res["tool_name"])   # "view_file"
print(res["confidence"])  # 0.818
```

---

## GenPark Ecosystem

- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)
