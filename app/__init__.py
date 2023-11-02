import asyncio
from app.application import Application


def run(config_path: str):
    app = Application(config_path=config_path)
    asyncio.run(app())
