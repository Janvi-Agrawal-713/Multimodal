"""
Gemini API Service Layer
Handles communication with Google's Gemini Multimodal models with robust error handling,
clean JSON extraction, and API key management across env vars, secrets, and UI input.
"""

import os
import json
import re
from typing import Optional, Dict, Any, Tuple
from PIL import Image

try:
    import streamlit as st
except ImportError:
    st = None

try:
    import google.generativeai as genai
    HAS_GENAI_LIB = True
except ImportError:
    genai = None
    HAS_GENAI_LIB = False


def resolve_api_key(user_input_key: Optional[str] = None) -> Optional[str]:
    """
    Resolve API key in order of priority:
    1. Direct user input from Streamlit UI
    2. Environment variable GEMINI_API_KEY
    3. Streamlit secrets (if available)
    """
    if user_input_key and user_input_key.strip():
        return user_input_key.strip()
    
    env_key = os.environ.get("GEMINI_API_KEY")
    if env_key and env_key.strip():
        return env_key.strip()
    
    if st is not None:
        try:
            if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
                secret_key = str(st.secrets["GEMINI_API_KEY"]).strip()
                if secret_key:
                    return secret_key
        except Exception:
            pass
            
    return None


def is_live_ai_available(user_input_key: Optional[str] = None) -> bool:
    """Check if the Gemini client library is installed and an API key is present."""
    if not HAS_GENAI_LIB:
        return False
    key = resolve_api_key(user_input_key)
    return bool(key and len(key) >= 15)


def extract_json_from_response(text: str) -> Optional[Dict[str, Any]]:
    """Cleanly extract and parse a JSON object from model output (handling code fences)."""
    if not text:
        return None
    
    # Strip markdown code blocks if present
    cleaned = text.strip()
    
    # Match ```json ... ``` or ``` ... ```
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
    if match:
        json_str = match.group(1).strip()
    else:
        json_str = cleaned
    
    # Attempt to locate the first { and last }
    first_brace = json_str.find("{")
    last_brace = json_str.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        json_str = json_str[first_brace:last_brace + 1]
        
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return None


def analyze_image_with_gemini(
    image: Image.Image,
    prompt: str,
    user_api_key: Optional[str] = None,
    model_name: str = "gemini-1.5-flash"
) -> Tuple[bool, Optional[Dict[str, Any]], str]:
    """
    Sends an image and structured prompt to Gemini Vision.
    Returns: (success: bool, parsed_data: Optional[Dict], message_or_error: str)
    """
    api_key = resolve_api_key(user_api_key)
    if not api_key:
        return False, None, "No Gemini API key provided. Using simulated demo analysis."
    
    if not HAS_GENAI_LIB:
        return False, None, "google-generativeai library is not installed in the environment."
        
    try:
        genai.configure(api_key=api_key)
        
        # Candidate model names to try in order of latency and cost efficiency
        candidate_models = [model_name, "gemini-1.5-flash-latest", "gemini-2.0-flash", "gemini-1.5-pro"]
        last_error = None
        
        for candidate in candidate_models:
            try:
                model = genai.GenerativeModel(candidate)
                generation_config = {
                    "temperature": 0.2,
                    "top_p": 0.95,
                    "max_output_tokens": 2048,
                }
                
                response = model.generate_content(
                    [prompt, image],
                    generation_config=generation_config
                )
                
                if response and response.text:
                    parsed = extract_json_from_response(response.text)
                    if parsed:
                        return True, parsed, f"Success using {candidate}"
                    else:
                        # Return raw text wrapped in dict if parsing failed
                        return True, {"raw_analysis": response.text}, f"Response received from {candidate} (non-JSON)"
            except Exception as e:
                last_error = e
                continue
                
        return False, None, f"Gemini API request failed: {str(last_error)}"
        
    except Exception as exc:
        return False, None, f"Gemini service exception: {str(exc)}"


def chat_with_gemini(
    user_message: str,
    context: str = "",
    user_api_key: Optional[str] = None
) -> Tuple[bool, str]:
    """
    Text assistant query to Gemini with construction engineering context.
    """
    api_key = resolve_api_key(user_api_key)
    if not api_key:
        return False, "Gemini API key not found. Using offline knowledge engine."
        
    if not HAS_GENAI_LIB:
        return False, "google-generativeai library is not available."
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        system_instructions = (
            "You are a Senior Civil & Structural Engineer and Construction Safety Auditor specializing in "
            "Indian Standard codes (IS 456, IS 13416, NBC 2016) and OSHA regulations. "
            "Provide concise, authoritative, professional, and practical construction advice. "
            "Include safety warnings, required cure times, formwork rules, or PPE guidelines where applicable.\n\n"
        )
        
        full_prompt = f"{system_instructions}CURRENT SITE CONTEXT:\n{context}\n\nUSER QUESTION:\n{user_message}"
        response = model.generate_content(full_prompt)
        
        if response and response.text:
            return True, response.text
        return False, "Received empty response from Gemini."
    except Exception as e:
        return False, f"Gemini Chat Error: {str(e)}"
