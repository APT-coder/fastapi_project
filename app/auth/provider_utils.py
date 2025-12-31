from app.models.enums import AuthProvider

def has_provider(user, provider: AuthProvider) -> bool:
    return provider.value in user.auth_providers.split(",")


def add_provider(user, provider: AuthProvider):
    providers = set(user.auth_providers.split(","))
    providers.add(provider.value)
    user.auth_providers = ",".join(sorted(providers))