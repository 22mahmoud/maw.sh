import re

from whitenoise.storage import CompressedManifestStaticFilesStorage


class CustomStaticFilesStorage(CompressedManifestStaticFilesStorage):
    def hashed_name(self, name, content=None, filename=None):
        if name.startswith(("assets/", "manifest.json")):
            return name

        return super().hashed_name(name, content, filename)


def immutable_file_test(_, url):
    return re.match(r"^.+[.-][0-9a-zA-Z_-]{8,12}\..+$", url)


WHITENOISE_IMMUTABLE_FILE_TEST = immutable_file_test
