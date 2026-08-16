import logging
import allure
from agents.automation.healer_agent import HealerAgent as SelfHealingHealer

logger = logging.getLogger("BasePage")

class BasePage:
    """
    Enterprise BasePage Object incorporating AI Self-Healing, logging, and Allure tracing.
    """
    def __init__(self, page):
        self.page = page
        self.healer = SelfHealingHealer()

    def navigate(self, url: str):
        with allure.step(f"Navigate to {url}"):
            logger.info("Navigating to URL: %s", url)
            self.page.goto(url)

    def get_title(self) -> str:
        return self.page.title()

    def safe_click(self, selector: str, timeout: int = 5000):
        """
        Attempts click on primary selector. If Playwright timeout occurs,
        triggers AI Self-Healing to find a replacement selector and retries.
        """
        with allure.step(f"Safe Click on selector '{selector}'"):
            try:
                self.page.locator(selector).click(timeout=timeout)
                logger.info("Successfully clicked selector: '%s'", selector)
            except Exception as err:
                logger.warning("Primary selector '%s' failed. Invoking AI Self-Healing...", selector)
                dom = self.page.content()
                healed_selector = self.healer.heal_selector(selector, dom, str(err))

                if healed_selector:
                    allure.attach(
                        f"Primary selector '{selector}' failed.\nHealed selector: '{healed_selector}'",
                        name="🤖 AI Self-Healing Event",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    self.page.locator(healed_selector).first.click(timeout=timeout)
                    logger.info("Self-healing successful! Clicked healed selector: '%s'", healed_selector)
                else:
                    raise err

    def safe_fill(self, selector: str, value: str, timeout: int = 5000):
        """
        Attempts fill on primary selector. If Playwright timeout occurs,
        triggers AI Self-Healing to find a replacement selector and retries.
        """
        with allure.step(f"Safe Fill on selector '{selector}'"):
            try:
                self.page.locator(selector).fill(value, timeout=timeout)
                logger.info("Successfully filled selector: '%s'", selector)
            except Exception as err:
                logger.warning("Primary selector '%s' failed to fill. Invoking AI Self-Healing...", selector)
                dom = self.page.content()
                healed_selector = self.healer.heal_selector(selector, dom, str(err))

                if healed_selector:
                    allure.attach(
                        f"Primary selector '{selector}' failed.\nHealed selector: '{healed_selector}'",
                        name="🤖 AI Self-Healing Event",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    self.page.locator(healed_selector).first.fill(value, timeout=timeout)
                    logger.info("Self-healing successful! Filled healed selector: '%s'", healed_selector)
                else:
                    raise err
