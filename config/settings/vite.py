from config.env import env

DJANGO_VITE = {
    "default": {
        # "dev_mode": False,
        "dev_mode": env.bool("DJANGO_VITE_DEV", default=False),
    }
}
