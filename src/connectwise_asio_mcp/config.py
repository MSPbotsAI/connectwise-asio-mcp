from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    mcp_http_port: int = 8080
    mcp_http_host: str = "0.0.0.0"

    # ConnectWise Asio has 3 regional servers; the Client ID prefix used to
    # mint the token indicates which one a tenant belongs to (0e30=NA,
    # 0e31=EU, 0e32=AU). Default here, override per-request via
    # X-ConnectWise-Asio-Base-Url for gateways serving tenants across regions.
    connectwise_asio_base_url: str = "https://openapi.service.itsupport247.net"


def get_settings() -> Settings:
    return Settings()
