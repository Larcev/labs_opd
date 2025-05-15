from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

'''
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='catalog'),
    KeyboardButton(text='basket')],
    [KeyboardButton(text='contacts')],
    [KeyboardButton(text='location', request_location=True),
    KeyboardButton(text='Отправить контакт', request_contact=True)],

],
    resize_keyboard=True,
    input_field_placholder='Выберите пункт ниже'
)
'''

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📉 Досрочное погашение")],
        [KeyboardButton(text="📈 Обычное погашение")],
        [KeyboardButton(text="💵 52 недели богатства")]
    ],
    resize_keyboard=True
)
'''
inline_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Досрочное погашение', callback_data='fast'),
     InlineKeyboardButton(text='Обычное погашение', callback_data='normal')],
    [InlineKeyboardButton(text='52 недели богатства', callback_data='fifty_two')]
])

'''


back = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text="назад", )],
])






'''
async def catalog_builder():
    brands = ["Nike", "Adidas", "Puma", "Reebok", "New Balance",
              "Under Armour", "Vans", "Converse", "Fila", "Asics", "Skechers"]
    Keyboard = InlineKeyboardBuilder()
    for brand in brands:
        Keyboard.add(InlineKeyboardButton(text=brand, callback_data=f'item_{brand}'))

    return Keyboard.adjust(2).as_markup()
'''
