"""
02_code_assistant/main.py

AI Smart Coding Interviewer — Code Complexity Analyzer

This module analyzes Python code submissions and returns a complexity score.
Used by the interview platform to give candidates feedback on their solutions.

AI Assistance Log:
- AI suggested initial structure using `ast` module (ACCEPTED)
- AI used regex for loop counting (REJECTED — switched to ast node traversal for accuracy)
- AI didn't handle nested loops separately (CHANGED — added custom visitor logic)
"""

import ast
from dataclasses import dataclass


@dataclass
class ComplexityResult:
    """Result of code complexity analysis."""
    lines: int
    functions: int
    loops: int
    nested_loops: int
    score: int
    feedback: str


def calculate_complexity_score(code: str) -> dict:
    """
    Analyzes Python code and returns a complexity score dictionary.

    Parameters
    ----------
    code : str
        The Python source code to analyze.

    Returns
    -------
    dict with keys:
        - 'lines'        : int  — total non-empty, non-comment lines
        - 'functions'    : int  — number of function definitions
        - 'loops'        : int  — total for/while loops
        - 'nested_loops' : int  — loops that are directly inside another loop
        - 'score'        : int  — complexity score 0–100 (lower = simpler)
        - 'feedback'     : str  — human-readable summary

    Raises
    ------
    ValueError
        If the code string contains a syntax error and cannot be parsed.

    Examples
    --------
    >>> result = calculate_complexity_score("def hello():\\n    print('hi')")
    >>> result['functions']
    1
    >>> result['loops']
    0
    """
    # --- Handle empty input ---
    if not code or not code.strip():
        return {
            "lines": 0,
            "functions": 0,
            "loops": 0,
            "nested_loops": 0,
            "score": 0,
            "feedback": "No code provided.",
        }

    # --- Count non-empty, non-comment lines ---
    lines = sum(
        1
        for line in code.splitlines()
        if line.strip() and not line.strip().startswith("#")
    )

    # --- Parse AST ---
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code: {e}") from e

    # --- Count functions ---
    functions = sum(
        1 for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    )

    # --- Count all loops and nested loops using a custom visitor ---
    loop_types = (ast.For, ast.While)

    total_loops = sum(1 for node in ast.walk(tree) if isinstance(node, loop_types))

    nested_loops = _count_nested_loops(tree)

    # --- Calculate score (0–100, lower = simpler) ---
    # Weighted formula: lines are minor weight, loops are major complexity drivers
    raw_score = (lines * 0.5) + (functions * 2) + (total_loops * 5) + (nested_loops * 15)
    score = min(100, int(raw_score))

    # --- Generate feedback ---
    feedback = _generate_feedback(score, total_loops, nested_loops)

    return {
        "lines": lines,
        "functions": functions,
        "loops": total_loops,
        "nested_loops": nested_loops,
        "score": score,
        "feedback": feedback,
    }


def _count_nested_loops(tree: ast.AST) -> int:
    """
    Count loops that appear directly inside another loop body.

    AI note: AI originally suggested regex for this (REJECTED).
    This AST-based approach correctly handles indentation-independent nesting.
    """
    loop_types = (ast.For, ast.While)
    count = 0

    for node in ast.walk(tree):
        if isinstance(node, loop_types):
            # Check if any direct child in body/orelse is also a loop
            for child in ast.walk(node):
                if child is node:
                    continue
                if isinstance(child, loop_types):
                    count += 1
                    break  # Count this outer loop once even if multiple nested

    return count


def _generate_feedback(score: int, loops: int, nested_loops: int) -> str:
    """Generate human-readable feedback based on score."""
    if score == 0:
        return "No code to analyze."
    elif score <= 10:
        return "Excellent! Very clean and simple code."
    elif score <= 25:
        return "Good solution. Complexity is manageable."
    elif score <= 50:
        if nested_loops > 0:
            return (
                f"Moderate complexity. You have {nested_loops} nested loop(s) — "
                "consider if they can be flattened or replaced with a hash map."
            )
        return "Moderate complexity. Consider breaking into smaller functions."
    elif score <= 75:
        return (
            "High complexity detected. Multiple nested loops may indicate an O(n²) or worse solution. "
            "Review your algorithm choice."
        )
    else:
        return (
            "Very high complexity. This solution may struggle with large inputs. "
            "Consider a fundamentally different algorithmic approach."
        )

