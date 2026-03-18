from config_reader import config
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats

from aiogram.types import ChatPermissions
import asyncio


logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()


async def setup_bot_commands():
    private_commands = [
    ]
    await bot.set_my_commands(
        commands=private_commands,
        scope=BotCommandScopeAllPrivateChats()
    )

    group_commands = [
    ]
    await bot.set_my_commands(
        commands=group_commands,
        scope=BotCommandScopeAllGroupChats()
    )

@dp.chat_member()
async def on_user_join(chat_member: types.ChatMemberUpdated):
    if chat_member.new_chat_member.status == "member":
        user_id = chat_member.from_user.id
        
        try:
            await bot.restrict_chat_member(
                chat_id=chat_member.chat.id,
                user_id=user_id,
                permissions=ChatPermissions(can_send_messages=False)
            )
        except Exception as e:
            logging.error(f"Ошибка при ограничении пользователя {user_id}: {e}")


@dp.message(Command("check"))
async def get_link(message: Message):
    if message.chat.type == 'private':
        await message.answer("Chech")



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await setup_bot_commands()
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())
