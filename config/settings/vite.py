from config.env import env

DJANGO_VITE = {"default": {"dev_mode": env.bool("DEBUG", default=True)}}
