# backend/app/agents/config.py

from agents import ModelSettings

# LLM model name (change to o4-mini or whatever you prefer)
MODEL_NAME = "gpt-4o"

# Default settings: force tool use when required
DEFAULT_MODEL_SETTINGS = ModelSettings(tool_choice="required")