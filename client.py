"""Agent Hallucinated Tool Call & Fuzzy Intent Resolver.
100% Python Standard Library.
"""

from typing import List, Dict, Any, Tuple, Optional


class FuzzyToolResolver:
    """Detects and resolves hallucinated or misspelled tool names and arguments
    against an authorized manifest of available tools using Levenshtein distance and token similarity."""

    @staticmethod
    def levenshtein_distance(s1: str, s2: str) -> int:
        """Computes Levenshtein edit distance between two strings using standard library."""
        if len(s1) < len(s2):
            return FuzzyToolResolver.levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]

    @classmethod
    def similarity_ratio(cls, s1: str, s2: str) -> float:
        """Returns similarity score between 0.0 and 1.0."""
        s1, s2 = s1.lower().replace("-", "_"), s2.lower().replace("-", "_")
        if s1 == s2:
            return 1.0
        dist = cls.levenshtein_distance(s1, s2)
        max_len = max(len(s1), len(s2))
        return 1.0 - (dist / max_len) if max_len > 0 else 1.0

    @classmethod
    def resolve_tool_name(
        cls,
        invoked_name: str,
        valid_tools: List[str],
        threshold: float = 0.6,
    ) -> Dict[str, Any]:
        """Finds the best matching valid tool for a hallucinated or misspelled tool name."""
        if invoked_name in valid_tools:
            return {
                "resolved": True,
                "exact_match": True,
                "tool_name": invoked_name,
                "confidence": 1.0,
            }

        scores = [
            (tool, cls.similarity_ratio(invoked_name, tool))
            for tool in valid_tools
        ]
        scores.sort(key=lambda x: x[1], reverse=True)

        if scores and scores[0][1] >= threshold:
            best_match, score = scores[0]
            return {
                "resolved": True,
                "exact_match": False,
                "tool_name": best_match,
                "original_name": invoked_name,
                "confidence": round(score, 3),
                "alternative_matches": [t for t, s in scores[1:3] if s >= threshold],
            }

        return {
            "resolved": False,
            "exact_match": False,
            "tool_name": None,
            "original_name": invoked_name,
            "confidence": 0.0,
            "error": f"Tool '{invoked_name}' could not be resolved to any registered tool.",
        }

    @classmethod
    def resolve_arguments(
        cls,
        invoked_args: Dict[str, Any],
        expected_schema_properties: List[str],
        threshold: float = 0.6,
    ) -> Dict[str, Any]:
        """Maps misspelled argument names to valid schema parameter names."""
        resolved_args = {}
        unmapped = {}
        corrections = {}

        for arg_key, arg_val in invoked_args.items():
            if arg_key in expected_schema_properties:
                resolved_args[arg_key] = arg_val
                continue

            scores = [
                (prop, cls.similarity_ratio(arg_key, prop))
                for prop in expected_schema_properties
            ]
            scores.sort(key=lambda x: x[1], reverse=True)

            if scores and scores[0][1] >= threshold:
                best_prop, score = scores[0]
                resolved_args[best_prop] = arg_val
                corrections[arg_key] = {
                    "mapped_to": best_prop,
                    "confidence": round(score, 3),
                }
            else:
                unmapped[arg_key] = arg_val

        return {
            "resolved_args": resolved_args,
            "corrections": corrections,
            "unmapped_args": unmapped,
        }
