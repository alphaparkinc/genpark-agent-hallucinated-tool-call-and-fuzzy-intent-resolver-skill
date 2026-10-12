"""MCP server for Agent Hallucinated Tool Call & Fuzzy Intent Resolver."""
import sys
import json
from client import FuzzyToolResolver


def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "resolve_tool_name",
                    "description": "Resolves a hallucinated or misspelled tool name against an authorized list of valid tool names",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "invoked_name": {"type": "string", "description": "The tool name emitted by the LLM"},
                            "valid_tools": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of valid tool names",
                            },
                            "threshold": {"type": "number", "default": 0.6},
                        },
                        "required": ["invoked_name", "valid_tools"],
                    },
                },
                {
                    "name": "resolve_arguments",
                    "description": "Fuzzy-matches misspelled parameter names to authorized schema property names",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "invoked_args": {"type": "object", "description": "Arguments emitted by the LLM"},
                            "expected_schema_properties": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Valid schema property names",
                            },
                        },
                        "required": ["invoked_args", "expected_schema_properties"],
                    },
                },
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "resolve_tool_name":
            res = FuzzyToolResolver.resolve_tool_name(
                args.get("invoked_name", ""),
                args.get("valid_tools", []),
                threshold=args.get("threshold", 0.6),
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
        elif tool_name == "resolve_arguments":
            res = FuzzyToolResolver.resolve_arguments(
                args.get("invoked_args", {}),
                args.get("expected_schema_properties", []),
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}


if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
