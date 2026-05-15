from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "YemenBiz Ledger AI"
    app_env: str = "development"
    database_url: str = "sqlite:///./yemenbiz_ledger.db"

    use_openai: bool = False
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    default_currency: str = "YER"
    low_stock_threshold: int = 5

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
