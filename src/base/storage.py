from django.contrib.staticfiles.storage import ManifestStaticFilesStorage as Base


def _is_excluded(name):
    return name.startswith("assets/") or name == "manifest.json"


class ManifestStaticFilesStorage(Base):
    def hashed_name(self, name, content=None, filename=None):
        if _is_excluded(name):
            return name

        return super().hashed_name(name, content, filename)
