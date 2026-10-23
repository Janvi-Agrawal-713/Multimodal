"""
Tests for Indian currency and number formatting utilities.
"""

from utils.formatting import format_inr, format_inr_compact, format_number_inr


def test_format_inr_standard():
    assert format_inr(1000) == "₹ 1,000"
    assert format_inr(100000) == "₹ 1,00,000"
    assert format_inr(12345678) == "₹ 1,23,45,678"
    assert format_inr(500) == "₹ 500"


def test_format_inr_decimals():
    assert format_inr(125000.50) == "₹ 1,25,000.50"
    assert format_inr(99.99) == "₹ 99.99"


def test_format_inr_compact():
    assert format_inr_compact(15000000) == "₹ 1.50 Cr"
    assert format_inr_compact(4500000) == "₹ 45.00 Lakhs"
    assert format_inr_compact(75000) == "₹ 75.0 K"
    assert format_inr_compact(850) == "₹ 850"


def test_format_number_inr_without_symbol():
    assert format_number_inr(12345678) == "1,23,45,678"
