from contextlib import suppress

from .base import *  # noqa: F403

with suppress(ImportError):
    from .local import *  # type: ignore[import-not-found]  # noqa: F403
