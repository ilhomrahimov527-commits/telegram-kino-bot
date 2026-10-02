from aiogram import Bot, Dispatcher, types
import asyncio
import os

# Укажите ваш токен бота (или используйте переменную окружения)
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def send_test_video(message: types.Message):
    # Тестовая прямая ссылка на видео
    video_url = "https://www.w3schools.com/html/mov_bbb.mp4"
    
    await message.answer_video(
        video=video_url,
        caption="🎬 Вот тестовое видео по вашей ссылке!"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())