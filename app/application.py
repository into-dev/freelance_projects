import yaml
from app.config import Config, AppConfig, BotConfig
from app.store.bot.telegram_bot import TelegramBot


class Application:
    config: Config

    def __init__(self, config_path: str):
        with open(config_path, "r") as config_file:
            config_data = yaml.safe_load(config_file)
        self.config = Config(
            app=AppConfig(delay=int(config_data["app"]["delay"])),
            bot=BotConfig(
                token=config_data["bot"]["token"],
            ),
        )

    async def __call__(self, *args, **kwargs):
        print("running...")
        bot = TelegramBot(token=self.config.bot.token, delay=int(self.config.app.delay))
        await bot.start_polling()
