"""Example usage for Agent Hallucinated Tool Call & Fuzzy Intent Resolver."""
from client import FuzzyToolResolver

if __name__ == "__main__":
    valid_manifest = ["view_file", "run_command", "replace_file_content", "write_to_file"]

    # 1. Resolve hallucinated tool name
    hallucinated = "view_file_contents"
    res_tool = FuzzyToolResolver.resolve_tool_name(hallucinated, valid_manifest)
    print("Resolved Tool Name:", res_tool["tool_name"])
    print("Confidence:", res_tool["confidence"])

    # 2. Resolve misspelled argument names
    invoked_args = {"file_path": "src/main.py", "start_ln": 10}
    expected_props = ["AbsolutePath", "StartLine", "EndLine"]
    # Compare with another tool schema
    expected_cmd = ["CommandLine", "Cwd", "WaitMsBeforeAsync"]
    res_args = FuzzyToolResolver.resolve_arguments(
        {"cmd": "git status", "timeout": 5000},
        ["cmd_line", "timeout_ms", "working_dir"]
    )
    print("\nResolved Args:", res_args["resolved_args"])
    print("Corrections:", res_args["corrections"])
