from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
import keyboards as kb

router = Router()
user_data = {}  # user_id: {'stage': str, 'amount': int, 'term': int, 'percent': float}
# - НУЖНО ЧТОБЫ БОЛЬШЕ ОДНОЙ СЕССИИ ЗА РАЗ


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать! Выберите режим погашения:', reply_markup=kb.main_kb)

@router.message(F.text == "📈 Обычное погашение")
async def handle_normal(message: Message):
    user_data[message.from_user.id] = {"stage": "normal_amount"}
    await message.answer("Вы выбрали обычное погашение. Введите сумму кредита:")

@router.message(F.text == "💵 52 недели богатства")
async def handle_wealth(message: Message):
    user_data[message.from_user.id] = {"stage": "wealth_amount"}
    await message.answer("Вы выбрали 52 недели богатства. Введите стартовую сумму:")

@router.message(F.text == "📉 Досрочное погашение")
async def handle_fast_start(message: Message):
    user_data[message.from_user.id] = {"stage": "fast_amount"}
    await message.answer("Введите сумму кредита:")

@router.message()
async def handle_fast_flow(message: Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        await message.answer("Пожалуйста, начните с команды /start или выберите режим.")
        return

    data = user_data[user_id]
    stage = data["stage"]

    # Отладка: логируем этап
    print(f"User {user_id}, Stage: {stage}, Input: {message.text}")

    # Обработка обычного погашения
    if stage.startswith("normal"):
        if stage == "normal_amount":
            if message.text.isdigit():
                data["amount"] = int(message.text)
                data["stage"] = "normal_term"
                await message.answer("Введите срок кредита в месяцах:")
            else:
                await message.answer("Введите сумму числом.")

        elif stage == "normal_term":
            if message.text.isdigit():
                data["term"] = int(message.text)
                data["stage"] = "normal_percent"
                await message.answer("Введите процентную ставку в год (%):")
            else:
                await message.answer("Введите срок числом.")

        elif stage == "normal_percent":
            try:
                percent = float(message.text.replace(",", "."))
                data["percent"] = percent

                # Расчет аннуитетного платежа
                amount = data["amount"]
                term = data["term"]
                monthly_rate = percent / 100 / 12
                annuity_payment = amount * (monthly_rate * (1 + monthly_rate) ** term) / (
                            (1 + monthly_rate) ** term - 1)
                total_payment = annuity_payment * term
                overpayment = total_payment - amount

                await message.answer(
                    f"📈 Обычное погашение (аннуитетные платежи):\n"
                    f"Сумма кредита: {amount} руб.\n"
                    f"Срок: {term} мес.\n"
                    f"Процентная ставка: {percent}% годовых\n"
                    f"Ежемесячный платеж: {round(annuity_payment, 2)} руб.\n"
                    f"Общая сумма выплат: {round(total_payment, 2)} руб.\n"
                    f"Переплата: {round(overpayment, 2)} руб."
                )
                del user_data[user_id]
            except ValueError:
                await message.answer("Введите процент числом.")

    # Обработка 52 недели богатства
    elif stage.startswith("wealth"):
        if stage == "wealth_amount":
            if message.text.isdigit():
                data["amount"] = int(message.text)
                data["stage"] = "wealth_increment"
                await message.answer("Введите еженедельный прирост суммы (например, 100 для +100 руб. каждую неделю):")
            else:
                await message.answer("Введите сумму числом.")

        elif stage == "wealth_increment":
            if message.text.isdigit():
                data["increment"] = int(message.text)
                data["stage"] = "wealth_percent"
                await message.answer("Введите годовую процентную ставку (0, если проценты не начисляются):")
            else:
                await message.answer("Введите прирост числом.")

        elif stage == "wealth_percent":
            try:
                percent = float(message.text.replace(",", "."))
                data["percent"] = percent

                # Расчет для 52 недель богатства РАБОТАЕТ
                start_amount = data["amount"]
                increment = data["increment"]
                annual_rate = data["percent"]
                weeks = 52

                # Сумма взносов по арифметической прогрессии РАБОТАЕТ
                total_contributions = 0
                weekly_payments = []
                for week in range(1, weeks + 1):
                    payment = start_amount + (week - 1) * increment
                    weekly_payments.append(payment)
                    total_contributions += payment

                # Учет процентов, если они есть
                total_with_interest = total_contributions
                if annual_rate > 0:
                    weekly_rate = annual_rate / 100 / 52
                    total_with_interest = 0
                    for week, payment in enumerate(weekly_payments, 1):
                        remaining_weeks = weeks - week
                        future_value = payment * (1 + weekly_rate) ** remaining_weeks
                        total_with_interest += future_value

                interest_earned = total_with_interest - total_contributions if annual_rate > 0 else 0

                await message.answer(
                    f"💵 52 недели богатства:\n"
                    f"Стартовая сумма: {start_amount} руб.\n"
                    f"Еженедельный прирост: {increment} руб.\n"
                    f"Процентная ставка: {annual_rate}% годовых\n"
                    f"Общая сумма взносов: {round(total_contributions, 2)} руб.\n"
                    f"Итоговая сумма с процентами: {round(total_with_interest, 2)} руб.\n"
                    f"Начисленные проценты: {round(interest_earned, 2)} руб."
                )
                del user_data[user_id]
            except ValueError:
                await message.answer("Введите процент числом.")

    # Обработка досрочного погашения
    elif stage.startswith("fast"):
        if stage == "fast_amount":
            if message.text.isdigit():
                data["amount"] = int(message.text)
                data["stage"] = "fast_term"
                await message.answer("Введите срок кредита в месяцах:")
            else:
                await message.answer("Введите сумму числом.")

        elif stage == "fast_term":
            if message.text.isdigit():
                data["term"] = int(message.text)
                data["stage"] = "fast_percent"
                await message.answer("Введите процент в месяц:")
            else:
                await message.answer("Введите срок числом.")

        elif stage == "fast_percent":
            try:
                percent = float(message.text.replace(",", "."))
                data["percent"] = percent
                data["stage"] = "fast_month"
                await message.answer("На каком месяце вы планируете досрочное погашение?")
            except ValueError:
                await message.answer("Введите процент числом.")

        elif stage == "fast_month":
            if message.text.isdigit():
                early_month = int(message.text)
                amount = data["amount"]
                term = data["term"]
                annual_rate = data["percent"]

                if not (1 <= early_month <= term):
                    await message.answer("Месяц должен быть в пределах срока кредита.")
                    return

                monthly_rate = annual_rate / 100 / 12
                payment = amount * (monthly_rate * (1 + monthly_rate) ** term) / ((1 + monthly_rate) ** term - 1)
                remaining = amount
                paid_interest = 0
                for month in range(1, early_month + 1):
                    interest = remaining * monthly_rate
                    principal = payment - interest
                    remaining -= principal
                    paid_interest += interest

                final_payment = remaining + (remaining * monthly_rate)

                await message.answer(
                    f"📉 Досрочное погашение:\n"
                    f"Сумма кредита: {amount} руб.\n"
                    f"Срок: {term} мес.\n"
                    f"Процент: {annual_rate}% годовых\n"
                    f"Досрочное погашение на {early_month} мес.\n"
                    f"Остаток долга: {round(remaining, 2)} руб.\n"
                    f"💸 К возврату: {round(final_payment, 2)} руб.\n"
                    f"Уже выплачено процентов: {round(paid_interest, 2)} руб."
                )
                del user_data[user_id]
            else:
                await message.answer("Введите месяц числом.")





'''@dp.message(CommandStart(deep_link=True))
async def cmd_start(message: Message, command: CommandObject):
    if command.args.isdigit():
        if command.args == '242':
            await message.answer(f'Привет! Ты пришел от Рустама')
    else:
        await message.answer('Ошибка')
'''

'''@dp.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Пока что бот ничего не умеет')
    '''


'''
@dp.message(F.photo)
async def handle_photo(message: Message):
    file_id = message.photo[-1].file_id
    await message.answer_photo(file_id, caption='Вот твоё фото!')
'''
#отправить фото обратно в первоначальном качестве

'''
@dp.message(Command('id'))
async def cmd_help(message: Message):
    await message.answer(f'{message.from_user.first_name}, вам нужна помощь?')
    await message.answer(f'Ваш ID: {message.from_user.id}')
команда id, выдает id пользователя
'''