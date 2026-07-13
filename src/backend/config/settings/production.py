"""Production settings."""

from .base import *  # noqa: F401,F403

DEBUG = False

# Ensure critical env vars are set
assert SECRET_KEY != "dev-secret-key-not-for-production", "SECRET_KEY must be set in production"  # noqa: F405

# Sentry
_sentry_dsn = os.getenv("SENTRY_DSN")  # noqa: F405
if _sentry_dsn:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=_sentry_dsn,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.2,
        send_default_pii=False,
    )

# Compressor
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
