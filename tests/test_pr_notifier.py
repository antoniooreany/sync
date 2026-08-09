import pytest
from unittest.mock import patch, MagicMock
import urllib.error
from pr_sync.notifier import TelegramNotifier

def test_telegram_notifier_disabled():
    notifier = TelegramNotifier()
    assert not notifier.enabled
    
    # Should return False without throwing error
    assert notifier.send("Test message") is False

def test_telegram_notifier_enabled():
    notifier = TelegramNotifier(bot_token="token", chat_id="12345")
    assert notifier.enabled

@patch("urllib.request.urlopen")
def test_telegram_notifier_send_success(mock_urlopen):
    mock_response = MagicMock()
    mock_response.status = 200
    mock_urlopen.return_value.__enter__.return_value = mock_response
    
    notifier = TelegramNotifier(bot_token="token", chat_id="12345")
    result = notifier.send("Hello World")
    
    assert result is True
    assert mock_urlopen.called

@patch("urllib.request.urlopen")
def test_telegram_notifier_send_http_error(mock_urlopen):
    mock_response = MagicMock()
    mock_response.status = 400
    mock_urlopen.return_value.__enter__.return_value = mock_response
    
    notifier = TelegramNotifier(bot_token="token", chat_id="12345")
    result = notifier.send("Hello World")
    
    assert result is False

@patch("urllib.request.urlopen")
def test_telegram_notifier_send_url_error(mock_urlopen):
    mock_urlopen.side_effect = urllib.error.URLError("Network error")
    
    notifier = TelegramNotifier(bot_token="token", chat_id="12345")
    result = notifier.send("Hello World")
    
    assert result is False
