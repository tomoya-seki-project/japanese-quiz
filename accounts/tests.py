from unittest.mock import patch

from django.core.cache import cache
from django.test import SimpleTestCase, override_settings

from .views import (
    _clear_activation_email_cooldown,
    _try_start_activation_email_cooldown,
)


TEST_CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "activation-email-cooldown-tests",
    }
}


@override_settings(CACHES=TEST_CACHES)
class ActivationEmailCooldownTests(SimpleTestCase):
    def setUp(self):
        cache.clear()

    def tearDown(self):
        cache.clear()

    def test_cooldown_blocks_second_attempt_until_cleared(self):
        user_id = 123

        first_attempt = _try_start_activation_email_cooldown(
            user_id=user_id
        )
        second_attempt = _try_start_activation_email_cooldown(
            user_id=user_id
        )

        self.assertTrue(first_attempt)
        self.assertFalse(second_attempt)

        _clear_activation_email_cooldown(user_id=user_id)

        third_attempt = _try_start_activation_email_cooldown(
            user_id=user_id
        )
        self.assertTrue(third_attempt)

    def test_cache_add_failure_fails_open(self):
        with patch(
            "accounts.views.cache.add",
            side_effect=RuntimeError("cache unavailable"),
        ):
            with self.assertLogs("accounts.views", level="ERROR") as logs:
                can_send = _try_start_activation_email_cooldown(
                    user_id=123
                )

        self.assertTrue(can_send)
        self.assertIn(
            "activation_email_cooldown_add",
            logs.output[0],
        )

    def test_cache_delete_failure_does_not_raise(self):
        with patch(
            "accounts.views.cache.delete",
            side_effect=RuntimeError("cache unavailable"),
        ):
            with self.assertLogs("accounts.views", level="ERROR") as logs:
                _clear_activation_email_cooldown(user_id=123)

        self.assertIn(
            "activation_email_cooldown_delete",
            logs.output[0],
        )
