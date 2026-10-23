"""
Formatting utilities for Indian currency, numbers, and UI presentation.
"""

def format_inr(number: float, include_symbol: bool = True) -> str:
    """
    Format a number according to the Indian numbering system.
    e.g., 12345678 -> ₹ 1,23,45,678.00 or 1,23,45,678
    """
    if number is None:
        return "₹ 0" if include_symbol else "0"
    
    prefix = "₹ " if include_symbol else ""
    is_negative = number < 0
    num = abs(float(number))
    
    # Split into integer and decimal parts
    parts = f"{num:.2f}".split(".")
    int_part = parts[0]
    dec_part = parts[1]
    
    if len(int_part) <= 3:
        formatted_int = int_part
    else:
        last_three = int_part[-3:]
        remaining = int_part[:-3]
        # Group in pairs of 2 from the right
        groups = []
        while len(remaining) > 2:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]
        if remaining:
            groups.insert(0, remaining)
        formatted_int = ",".join(groups) + "," + last_three
    
    # If decimal is zero, display integer; otherwise display 2 decimals
    if dec_part == "00":
        result = f"{formatted_int}"
    else:
        result = f"{formatted_int}.{dec_part}"
        
    return f"{'-' if is_negative else ''}{prefix}{result}"


def format_inr_compact(number: float) -> str:
    """
    Format an amount into compact Indian denominations (Crores / Lakhs / Thousands).
    e.g. 15000000 -> ₹ 1.50 Cr
         4500000  -> ₹ 45.00 L
         75000    -> ₹ 75.0 K
    """
    if number is None:
        return "₹ 0"
    
    num = float(number)
    is_neg = num < 0
    val = abs(num)
    sign = "-" if is_neg else ""
    
    if val >= 10_000_000: # 1 Crore = 100 Lakhs = 10 Million
        return f"{sign}₹ {val / 10_000_000:.2f} Cr"
    elif val >= 100_000: # 1 Lakh = 100 Thousand
        return f"{sign}₹ {val / 100_000:.2f} Lakhs"
    elif val >= 1_000:
        return f"{sign}₹ {val / 1_000:.1f} K"
    else:
        return f"{sign}₹ {val:.0f}"


def format_number_inr(number: float) -> str:
    """Format plain quantities without currency symbol using Indian grouping."""
    return format_inr(number, include_symbol=False)
