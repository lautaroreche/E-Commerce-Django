from django.contrib.staticfiles.storage import ManifestStaticFilesStorage


class ForgivingManifestStaticFilesStorage(ManifestStaticFilesStorage):
    """
    ManifestStaticFilesStorage that skips missing files instead of raising.
    Needed because Django 5.2 admin CSS references SVG files that don't
    exist in the installed package (e.g. selector-icons.svg).
    """
    def hashed_name(self, name, content=None, filename=None):
        try:
            return super().hashed_name(name, content, filename)
        except ValueError:
            return name

    def stored_name(self, name):
        try:
            return super().stored_name(name)
        except ValueError:
            return name
