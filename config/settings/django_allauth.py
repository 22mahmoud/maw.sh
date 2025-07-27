from config.env import env

ALLAUTH_INSTALLED_APPS = [
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.github",
    "allauth.socialaccount.providers.google",
]

ALLAUTH_MIDDLEWARE = [
    "allauth.account.middleware.AccountMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
ACCOUNT_ADAPTER = "src.base.adapters.AccountAdapter"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]
ACCOUNT_LOGIN_METHODS = {"email", "username"}
SOCIALACCOUNT_PROVIDERS = {
    "github": {
        "APP": {
            "client_id": env.str("GITHUB_CLIENT_ID", ""),
            "secret": env.str("GITHUB_SECRET", ""),
        },
        "SCOPE": ["read:user", "user:email"],
    },
    "google": {
        "APP": {
            "client_id": env.str("GOOGLE_CLIENT_ID", ""),
            "secret": env.str("GOOGLE_SECRET", ""),
        },
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {
            "access_type": "offline",
        },
        "OAUTH_PKCE_ENABLED": True,
        "FETCH_USERINFO": True,
    },
}

ACCOUNT_SIGNUP_FORM_HONEYPOT_FIELD = "phone_number"
ACCOUNT_EMAIL_VERIFICATION_SUPPORTS_RESEND = True
ACCOUNT_EMAIL_NOTIFICATIONS = True
ACCOUNT_USERNAME_BLACKLIST = ["admin", "root", "mod", "support"]
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
EMAIL_AUTHENTICATION_AUTO_CONNECT = True
