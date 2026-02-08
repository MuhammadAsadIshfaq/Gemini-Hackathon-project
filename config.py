"""
Configuration file for Gemini 3 Hackathon Projects
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Model configurations
# IMPORTANT: Run 'python list_models.py' to see available models with your API key
# Then update GEMINI_FLASH_MODEL and GEMINI_PRO_MODEL below based on what's available

# For Gemini 3 Hackathon - try these model names in order:
# 1. Check if Gemini 3 models are available: "gemini-3.0-flash", "gemini-3.0-pro"
# 2. Try Gemini 2.0: "gemini-2.0-flash", "gemini-2.0-pro", "gemini-2.0-flash-thinking"
# 3. Fallback to Gemini 1.5 (these should work): "gemini-1.5-flash", "gemini-1.5-pro"

# Current configuration - Using Gemini 3 Preview models
# Model codes from official documentation:
# - Gemini 3 Flash Preview: gemini-3-flash-preview
# - Gemini 3 Pro Preview: gemini-3-pro-preview
# Both support: Thinking, Multimodal (Text/Image/Video/Audio/PDF), Large context (1M+ tokens)

GEMINI_FLASH_MODEL = "gemini-3-flash-preview"  # Fast, balanced model with thinking support
GEMINI_PRO_MODEL = "gemini-3-pro-preview"  # Most intelligent model with advanced reasoning

# Fallback models (if preview models not available):
# GEMINI_FLASH_MODEL = "gemini-1.5-flash"
# GEMINI_PRO_MODEL = "gemini-1.5-pro"

# Thinking mode configuration
THINKING_MODE = "high"  # Options: "low", "medium", "high"

# LangGraph configuration
MAX_ITERATIONS = 50

# File upload limits
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_PDF_SIZE = 50 * 1024 * 1024  # 50MB

