from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./test.db"

    # App
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10

    # Google OAuth
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/login/google/callback"
    GOOGLE_AUTH_BASE_URL: str = "https://accounts.google.com/o/oauth2/v2/auth"
    GOOGLE_TOKEN_URL: str = "https://oauth2.googleapis.com/token"

    # Mail
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_FROM_NAME: str = "FastAPI App"
    MAIL_SERVER: str
    MAIL_PORT: int

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="forbid",  # default, explicit for clarity
    )

settings = Settings()
