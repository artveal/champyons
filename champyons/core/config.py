from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pathlib import Path

load_dotenv()

APP_ROOT_PATH = Path(__file__).parent.parent # returns champyons/champyons

class Config(BaseSettings):
    app_name: str = "champyons"
    app_rootpath: Path = APP_ROOT_PATH
    debug: bool = False

    # database settings
    db_user: str = ""
    db_password: str = ""
    db_name: str = "test.db"
    
    # localization (i18n) settings
    default_locale: str = "en"
    default_lang: str = "en"
    supported_locales: list[str]|None = ["en", "es"]
    supported_langs: list[str]|None = ["en", "es"]
    locales_folder: str = "locales"
    default_domains: list[str] = ["messages", "database"]

    # tzinfo settings
    server_timezone: str = 'utc'

    @property
    def db_url(self):
        return f"sqlite:///./{self.db_name}"
    
    @property
    def root_path(self) -> Path:
        return self.app_rootpath.parent
    
    @property
    def locales_path(self) -> Path:
        return self.root_path / self.locales_folder


config = Config()