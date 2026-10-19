import json
from typing import Optional
from langchain_core.language_models import BaseChatModel
from app.config import settings

def get_configured_llm() -> Optional[BaseChatModel]:
    """
    Initializes configured LLM provider (Google Gemini or OpenAI).
    Returns None if no API key is provided, enabling graceful fallback reporting.
    """
    if settings.GOOGLE_API_KEY:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            model_name = settings.LLM_MODEL if "gemini" in settings.LLM_MODEL else "gemini-3.8-flash"
            return ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=settings.GOOGLE_API_KEY,
                temperature=0.2
            )
        except Exception as e:
            print(f"Warning: Failed to initialize Google Gemini LLM: {e}")
            return None
    elif settings.OPENAI_API_KEY:
        try:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model="gpt-4o-mini",
                api_key=settings.OPENAI_API_KEY,
                temperature=0.2
            )
        except Exception as e:
            print(f"Warning: Failed to initialize OpenAI LLM: {e}")
            return None
    return None
