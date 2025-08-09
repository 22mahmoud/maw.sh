HEALTH_CHECK = {
    "SUBSETS": {
        "startup": [
            "MigrationsHealthCheck",
            "DatabaseBackend",
            "Cache backend: default",
            "DatabaseBackend[default]",
            "RedisHealthCheck",
        ],
    },
}

DJANGO_HEALTH_CHECK_INSTALLED_APPS = [
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",
    "health_check.contrib.migrations",
    "health_check.contrib.celery",
    "health_check.contrib.celery_ping",
    "health_check.contrib.psutil",
    "health_check.contrib.s3boto3_storage",
    "health_check.contrib.redis",
    "health_check.contrib.db_heartbeat",
    "health_check.contrib.mail",
]
