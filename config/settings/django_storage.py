import mimetypes
from storages.backends.s3boto3 import S3Boto3Storage

from config.env import env

AWS_S3_FILE_OVERWRITE = False
AWS_STORAGE_BUCKET_NAME = env.str("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = env.str("AWS_S3_CUSTOM_DOMAIN")
AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY", "")
AWS_S3_ENDPOINT_URL = env.str("AWS_S3_ENDPOINT_URL", "")
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "public, max-age=86400",
}


class StaticR2Storage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"
    object_parameters = {
        "CacheControl": "public, max-age=31536000, s-maxage=31536000, immutable"
    }

    def get_object_parameters(self, name):
        params = super().get_object_parameters(name)

        content_type, _ = mimetypes.guess_type(name)
        if content_type:
            params["ContentType"] = content_type

        if name.endswith(".gz"):
            params["ContentEncoding"] = "gzip"
            base_type, _ = mimetypes.guess_type(name[:-3])
            if base_type:
                params["ContentType"] = base_type

        elif name.endswith(".br"):
            params["ContentEncoding"] = "br"
            base_type, _ = mimetypes.guess_type(name[:-3])
            if base_type:
                params["ContentType"] = base_type

        return params


class MediaR2Storage(S3Boto3Storage):
    location = "media"
    default_acl = "public-read"
    object_parameters = {"CacheControl": "public, max-age=300"}


class WagtailRenditionStorage(S3Boto3Storage):
    location = "cms"
    default_acl = "public-read"
    object_parameters = {
        "CacheControl": "public, max-age=31536000, s-maxage=31536000, immutable"
    }
