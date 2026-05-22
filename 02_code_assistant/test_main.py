"""
02_code_assistant/test_main.py

Pytest tests for calculate_complexity_score() in main.py

Run with:  pytest test_main.py -v

AI Assistance Log:
- AI generated initial test structure (ACCEPTED with modifications)
- AI used assert score == 0 for empty input (CHANGED — score key existence is safer)
- AI used parametrize for loop tests (ACCEPTED)
- AI added a test for comment-only code (ACCEPTED — good edge case)
- Renamed all tests to follow test_<function>_<scenario> convention (MANUAL CHANGE)
"""

import pytest
from main import calculate_complexity_score


# ---------------------------------------------------------------------------
# Test 1: Empty string input
# ---------------------------------------------------------------------------

def test_calculate_complexity_score_empty_string():
    """
    Empty string should return all zeros and a helpful feedback message.
    The function should not crash or raise an error on empty input.
    """
    result = calculate_complexity_score("")

    assert result["lines"] == 0
    assert result["functions"] == 0
    assert result["loops"] == 0
    assert result["nested_loops"] == 0
    assert result["score"] == 0
    assert "No code" in result["feedback"]


# ---------------------------------------------------------------------------
# Test 2: Simple function with no loops
# ---------------------------------------------------------------------------

def test_calculate_complexity_score_simple_function():
    """
    A basic function with no loops should have low complexity score,
    1 function counted, and 0 loops/nested loops.
    """
    code = """
def greet(name):
    message = f"Hello, {name}!"
    return message
"""
    result = calculate_complexity_score(code)

    assert result["functions"] == 1
    assert result["loops"] == 0
    assert result["nested_loops"] == 0
    assert result["score"] <= 10  # Should be very simple


# ---------------------------------------------------------------------------
# Test 3: Function with exactly one loop
# ---------------------------------------------------------------------------

def test_calculate_complexity_score_single_loop():
    """
    A function containing a single for loop should have:
    - loops == 1
    - nested_loops == 0
    - Score higher than a no-loop function
    """
    code = """
def sum_list(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
"""
    result = calculate_complexity_score(code)

    assert result["loops"] == 1
    assert result["nested_loops"] == 0
    assert result["score"] > 0


# ---------------------------------------------------------------------------
# Test 4: Function with nested loops
# ---------------------------------------------------------------------------

def test_calculate_complexity_score_nested_loops():
    """
    A function with a loop inside a loop should correctly report:
    - loops >= 2 (outer + inner)
    - nested_loops >= 1
    - Higher complexity score than single-loop code
    - Feedback should mention nested loops
    """
    code = """
def find_pairs(nums, target):
    result = []
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                result.append((nums[i], nums[j]))
    return result
"""
    result = calculate_complexity_score(code)

    assert result["loops"] >= 2
    assert result["nested_loops"] >= 1
    assert result["score"] > 10
    assert "nested" in result["feedback"].lower()


# ---------------------------------------------------------------------------
# Test 5: Edge case — code with only comments
# ---------------------------------------------------------------------------

def test_calculate_complexity_score_comments_only():
    """
    Code that consists entirely of comments should be treated as
    effectively empty: lines == 0 (comments excluded), score == 0.
    The function should not raise any errors.
    """
    code = """
# This is just a comment
# Another comment
# No actual code here
"""
    result = calculate_complexity_score(code)

    assert result["lines"] == 0
    assert result["functions"] == 0
    assert result["loops"] == 0
    assert result["score"] == 0


# ---------------------------------------------------------------------------
# Bonus Test 6: SyntaxError raises ValueError
# ---------------------------------------------------------------------------

def test_calculate_complexity_score_syntax_error():
    """
    Invalid Python code should raise a ValueError with a descriptive message.
    This ensures the platform surfaces errors cleanly to the interview UI.
    """
    bad_code = "def broken(:\n    pass"

    with pytest.raises(ValueError, match="Syntax error in code"):
        calculate_complexity_score(bad_code)
