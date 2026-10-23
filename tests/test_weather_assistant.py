"""
Tests for Module D: Weather-Aware Site Assistant.
"""

from modules.weather_assistant import (
    WEATHER_CONDITIONS,
    get_weather_details,
    query_offline_assistant
)


def test_weather_details_retrieval():
    for cond_name in WEATHER_CONDITIONS:
        details = get_weather_details(cond_name)
        assert details["selected_condition"] == cond_name
        assert "risk_level" in details
        assert "key_precautions" in details
        assert len(details["key_precautions"]) >= 3
        assert "category_rules" in details
        assert details["is_simulated_selection"] is True
        assert "No live IoT/API feed" in details["data_source_notice"]


def test_offline_assistant_knowledge_match():
    # Curing query
    resp = query_offline_assistant("What is the curing time for concrete?", "Normal / Clear Weather")
    assert "IS 456" in resp
    assert "7 days" in resp or "14 days" in resp
    
    # Wind query
    resp_wind = query_offline_assistant("What is the crane wind limit?", "High Wind (>40 km/h) / Storm")
    assert "38 km/h" in resp_wind or "tower crane" in resp_wind


def test_offline_assistant_fallback():
    resp_gen = query_offline_assistant("Tell me about green building certification in India", "Normal / Clear Weather")
    assert "Knowledge Engine Response" in resp_gen
    assert "IS 456" in resp_gen
