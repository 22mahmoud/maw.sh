from config.env import env

ALLAUTH_INSTALLED_APPS = [
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.github",
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
        "SCOPE": ["user"],
    }
}

ACCOUNT_SIGNUP_FORM_HONEYPOT_FIELD = "phone_number"
