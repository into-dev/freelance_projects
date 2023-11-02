import asyncio
from asyncio import create_task
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from app.store.parser.projectsparser import ProjectsParser
from app.store.parser.oneclancer import OneCLancer


class TelegramBot:
    bot: Bot
    dispatcher: Dispatcher
    parser: ProjectsParser
    delay: int
    chats: dict[str, ProjectsParser]

    def __init__(self, token: str, delay: int = 60):
        self.bot = Bot(token=token, parse_mode=ParseMode.HTML)
        self.dispatcher = Dispatcher()
        self.parser = OneCLancer()
        self.delay = delay
        self.chats = {}

        @self.dispatcher.message(CommandStart())
        async def start(message: Message):
            keyboard = ReplyKeyboardBuilder()
            keyboard.button(text="Начать поиск проектов")
            await message.answer("Начать поиск проектов?",
                                 reply_markup=keyboard.as_markup(resize_keyboard=True))

        @self.dispatcher.message(F.text == "Начать поиск проектов")
        async def start_check_projects(message: Message):
            await self._start_check_projects(message=message)

        @self.dispatcher.message(F.text == "Остановить поиск")
        async def stop_check_projects(message: Message):
            await self._stop_check_projects(message=message)

    def __del__(self):
        create_task(self.dispatcher.stop_polling())

    async def _start_check_projects(self, message: Message):
        chat_id = str(message.chat.id)
        self.chats[chat_id] = OneCLancer()

        keyboard = ReplyKeyboardBuilder()
        keyboard.button(text="Остановить поиск")
        await message.answer("Поиск проектов запущен",
                             reply_markup=keyboard.as_markup(resize_keyboard=True))

        while chat_id in self.chats:
            await self.send_new_projects(chat_id)
            await asyncio.sleep(self.delay)

    async def _stop_check_projects(self, message: Message):
        chat_id = str(message.chat.id)
        if chat_id in self.chats:
            del self.chats[chat_id]

        keyboard = ReplyKeyboardBuilder()
        keyboard.button(text="Начать поиск проектов")
        await message.answer("Поиск проектов остановлен",
                             reply_markup=keyboard.as_markup(resize_keyboard=True))

    async def start_polling(self):
        await self.dispatcher.start_polling(self.bot)

    async def send_new_projects(self, chat_id: str):
        if chat_id not in self.chats:
            return

        projects = await self.chats[chat_id].get_new_projects()
        for project in projects.values():
            message = (f"<a href=\'{project['url']}\'>{project['title']}</a>\n"
                       f"Бюджет: {project['budget']}\n"
                       f"{project['customer']}, {project['date']}")
            await self.bot.send_message(chat_id=chat_id, text=message)
