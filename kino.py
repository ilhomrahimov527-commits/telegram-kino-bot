import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiohttp import web

# Токен берется из переменных окружения Render для безопасности
API_TOKEN = os.getenv("BOT_TOKEN")

router = Router()
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@router.message(Command("start"))
async def start_cmd(message: Message):
  await message.answer(
      "🎬 Привет! Бот успешно запущен в облаке Render и готов к работе!"
  )


# Здесь будет ваша логика поиска фильмов и отправки видео
@router.message(F.text & ~F.text.startswith("/"))
async def search_movie(message: Message):
  await message.answer(f"🔍 Ищу фильм: {message.text}...")


# Простейший веб-сервер для Render, чтобы бот не «засыпал»
async def handle(request):
  return web.Response(text="Bot is running!")


async def web_server():
  app = web.Application()
  app.add_routes([web.get("/", handle)])
  runner = web.AppRunner(app)
  await runner.setup()
  port = int(os.getenv("PORT", 10000))
  site = web.TCPSite(runner, "0.0.0.0", port)
  await site.start()


async def main():
  dp.include_router(router)

  # Запускаем и веб-сервер, и поллинг бота одновременно
  await asyncio.gather(web_server(), dp.start_polling(bot))


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  asyncio.run(main())