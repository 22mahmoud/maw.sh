import re

from django.conf import settings
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage


class CustomStaticFilesStorage(ManifestStaticFilesStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        patterns = getattr(settings, "STATICFILES_HASH_EXCLUDE", [])
        self.exclude_patterns = [re.compile(p) for p in patterns]

    def should_exclude(self, name):
        return any(p.match(name) for p in self.exclude_patterns)

    def hashed_name(self, name, content=None, filename=None):
        if self.should_exclude(name):
            return name
        return super().hashed_name(name, content, filename)

    def post_process(self, paths, dry_run=False, **options):
        filtered_paths = {
            path: storage for path, storage in paths.items() if not self.should_exclude(path)
        }
        return super().post_process(filtered_paths, dry_run, **options)  # type: ignore
