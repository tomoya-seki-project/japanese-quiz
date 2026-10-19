import re


_ACTIVATION_URL_PATTERN = re.compile(
    r"(/accounts/activate/)[^/?#]+/[^/?#]+(/?)"
)


def _redact_activation_credentials(value):
    if isinstance(value, str):
        return _ACTIVATION_URL_PATTERN.sub(
            r"\1[Filtered]/[Filtered]\2",
            value,
        )

    if isinstance(value, dict):
        return {
            key: _redact_activation_credentials(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            _redact_activation_credentials(item)
            for item in value
        ]

    if isinstance(value, tuple):
        return tuple(
            _redact_activation_credentials(item)
            for item in value
        )

    return value


def redact_sensitive_sentry_data(event, hint):
    return _redact_activation_credentials(event)