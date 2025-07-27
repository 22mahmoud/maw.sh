import re

from django.conf import settings
from whitenoise.compress import Compressor
from whitenoise.storage import CompressedManifestStaticFilesStorage

from config.django.base import MIDDLEWARE


class CustomCompressor(Compressor):
    def should_compress(self, filename):
        if not super().should_compress(filename):
            return False

        only_paths = getattr(settings, "WHITENOISE_ONLY_COMPRESS_PATHS", None)
        if only_paths:
            return any(filename.startswith(path) for path in only_paths)

        return True


class CustomStaticFilesStorage(CompressedManifestStaticFilesStorage):
    def create_compressor(self, **kwargs):
        return CustomCompressor(**kwargs)

    def hashed_name(self, name, content=None, filename=None):
        if name.startswith(("assets/", "manifest.json")):
            return name

        return super().hashed_name(name, content, filename)


def immutable_file_test(_, url):
    return re.match(r"^.+[.-][0-9a-zA-Z_-]{8,12}\..+$", url)


MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")

WHITENOISE_ONLY_COMPRESS_PATHS = ["assets/"]
WHITENOISE_IMMUTABLE_FILE_TEST = immutable_file_test
