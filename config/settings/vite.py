from config.env import BASE_DIR, env

DJANGO_VITE = {
    "default": {
        # "dev_mode": False,
        "dev_mode": env.bool("DJANGO_VITE_DEV", default=False),
        "manifest_path": BASE_DIR / "static" / "manifest.json",
    }
}
