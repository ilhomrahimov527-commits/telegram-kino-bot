import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiohttp import web

API_TOKEN = os.getenv("BOT_TOKEN")

router = Router()
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@router.message(Command("start"))
async def start_cmd(message: Message):
  await message.answer(
      "🎬 Привет! Напиши название фильма (например: *Мстители*), и я отправлю"
      " тебе тестовое видео."
  )


# Обработка поиска фильма по тексту
@router.message(F.text & ~F.text.startswith("/"))
async def handle_movie_search(message: Message):
  query = message.text.strip()
  await message.answer(f"🔍 Ищу фильм «{query}»...")

  # Имитация задержки поиска
  await asyncio.sleep(1)

  # Тестовая прямая ссылка на видеофайл для проверки отправки
  test_video_url = "https://www.w3schools.com/html/mov_bbb.mp4"

  await message.answer_video(
      video=test_video_url,
      caption=(
          f"🎥 **Фильм по вашему запросу: {query.capitalize()}**\n\n📝 Описание:"
          " Это тестовый видеофайл, который подтверждает, что бот успешно"
          " отправляет видео из облака!\n\n🤖 Работает через Render 24/7."
      ),
      supports_streaming=True,
  )


# Веб-сервер для поддержки активности бота на Render
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
  print("Бот запущен и готов к работе!")
  await bot.delete_webhook(drop_pending_updates=True)
  await asyncio.gather(web_server(), dp.start_polling(bot))


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  asyncio.run(main())