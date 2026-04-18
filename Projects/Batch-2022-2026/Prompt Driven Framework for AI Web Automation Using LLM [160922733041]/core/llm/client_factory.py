"""Factory to create the appropriate LLM client based on configuration."""

from config import Config


def create_llm_client():
    """Create and return the LLM client based on LLM_PROVIDER config.

    Returns:
        ClaudeClient or GeminiClient instance
    """
    provider = Config.LLM_PROVIDER.lower()

    if provider == "gemini":
        from core.llm.gemini_client import GeminiClient
        return GeminiClient()
    else:
        from core.llm.claude_client import ClaudeClient
        return ClaudeClient()
