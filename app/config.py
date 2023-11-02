from dataclasses import dataclass


@dataclass
class BotConfig:
    token: str


@dataclass
class AppConfig:
    delay: int


@dataclass
class Config:
    app: AppConfig
    bot: BotConfig
