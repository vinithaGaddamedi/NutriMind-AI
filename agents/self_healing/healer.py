import logging
from typing import Optional
from agents.providers.factory import AIProviderFactory

logger = logging.getLogger("SelfHealingHealer")

class SelfHealingHealer:
    """
    AI-Powered Dynamic Locator Self-Healing Engine.
    Intercepts locator failure exceptions during Playwright execution,
    analyzes the live page DOM with Gemini AI, and suggests replacement locators.
    """

    def __init__(self, provider_name: Optional[str] = None):
        self.provider = AIProviderFactory.get_provider(provider_name)

    def heal_selector(self, failed_selector: str, page_dom: str, error_message: str = "") -> Optional[str]:
        """
        Analyzes broken selector against current page DOM and returns a healed replacement selector.
        """
        logger.warning("Initiating AI Self-Healing for broken selector: '%s'", failed_selector)
        
        system_instruction = (
            "You are a Playwright QA Automation Locator Expert. "
            "Given a failed CSS/XPath selector and the current web page DOM snippet, "
            "identify the target element and return ONLY a valid, resilient Playwright locator string (CSS or text matching). "
            "Return ONLY the selector string without extra markdown or explanations."
        )

        truncated_dom = page_dom[:8000] if page_dom else ""
        prompt = f"""Failed Selector: {failed_selector}
Error Exception: {error_message}

Page DOM Snippet:
```html
{truncated_dom}
```

Output ONLY the raw healed Playwright selector string (e.g., button:has-text('Submit') or input[name='username'])."""

        try:
            healed = self.provider.generate_text(prompt, system_instruction=system_instruction)
            if healed and "Gemini Provider Notice" not in healed and "Error" not in healed:
                cleaned_selector = healed.strip().strip("`").strip("'").strip('"')
                logger.info("AI Self-Healing successfully generated replacement selector: '%s'", cleaned_selector)
                return cleaned_selector
        except Exception as err:
            logger.error("Self-healing failed to generate replacement: %s", str(err))

        # Fallback heuristic heuristics if AI is offline
        if "button" in failed_selector.lower():
            fallback = "button"
            logger.info("Using fallback self-healing heuristic selector: '%s'", fallback)
            return fallback

        return None
