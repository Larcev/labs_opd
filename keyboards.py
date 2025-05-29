from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

#тут кнопки, какие есть
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📉 Досрочное погашение")],
        [KeyboardButton(text="📈 Обычное погашение")],
        [KeyboardButton(text="💵 52 недели богатства")]
    ],
    resize_keyboard=True
)

#кнопка назад
back = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text="назад", )],
])
