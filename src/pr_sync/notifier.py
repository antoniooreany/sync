"""Notification backends for the automation toolkit."""
import logging
import json
import urllib.request
import urllib.error
from typing import Optional

logger = logging.getLogger(__name__)

class TelegramNotifier:
    """Send notifications to a Telegram chat."""
    
    def __init__(self, bot_token: Optional[str] = None, chat_id: Optional[str] = None, timeout: float = 10.0) -> None:
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.timeout = timeout

    @property
    def enabled(self) -> bool:
        return bool(self.bot_token and self.chat_id)

    def send(self, message: str) -> bool:
        """Send a message to Telegram. Returns True if successful."""
        if not self.enabled:
            logger.debug("Telegram not configured, skipping notification: %s", message)
            return False
            
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        data = json.dumps({"chat_id": self.chat_id, "text": message}).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"}
        )
        
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                if resp.status == 200:
                    return True
                logger.error("Telegram API returned status %s", resp.status)
                return False
        except urllib.error.URLError:
            logger.exception("Failed to send Telegram notification")
            return False
