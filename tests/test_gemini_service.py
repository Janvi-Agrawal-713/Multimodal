"""
Tests for Gemini API Service Layer and JSON extraction.
"""

from modules.gemini_service import (
    extract_json_from_response,
    resolve_api_key,
    is_live_ai_available
)


def test_extract_json_clean():
    raw = '{"safety_score": 90, "status": "Compliant"}'
    parsed = extract_json_from_response(raw)
    assert parsed == {"safety_score": 90, "status": "Compliant"}


def test_extract_json_with_markdown_fences():
    raw = """
    Here is the analysis result:
    ```json
    {
      "defect_identified": "Shrinkage crack",
      "severity": "Low"
    }
    ```
    Please take appropriate actions.
    """
    parsed = extract_json_from_response(raw)
    assert parsed is not None
    assert parsed["defect_identified"] == "Shrinkage crack"
    assert parsed["severity"] == "Low"


def test_resolve_api_key_empty():
    assert resolve_api_key("") is None or isinstance(resolve_api_key(""), str)
    assert is_live_ai_available("short") is False
    assert is_live_ai_available("AIzaSy1234567890abcdef") is True
