from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states import SurveyStates
import keyboards as kb
from config import config

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Привет! Я помогу Вам забронировать вертолет.\n\nКакая у вас цель аренды вертолета?",
        reply_markup=kb.get_purpose_kb()
    )
    await state.set_state(SurveyStates.purpose)

@router.message(SurveyStates.purpose)
async def process_purpose(message: types.Message, state: FSMContext):
    await state.update_data(purpose=message.text)
    await message.answer("Вас интересует конкретный день?", reply_markup=kb.get_yes_no_kb())
    await state.set_state(SurveyStates.specific_day)

@router.message(SurveyStates.specific_day)
async def process_day(message: types.Message, state: FSMContext):
    await state.update_data(specific_day=message.text)
    await message.answer("Сколько человек планирует полет?", reply_markup=kb.get_people_kb())
    await state.set_state(SurveyStates.people_count)

@router.message(SurveyStates.people_count)
async def process_people(message: types.Message, state: FSMContext):
    await state.update_data(people_count=message.text)
    await message.answer(
        "Какой маршрут/путь полета вам нужен (начальная площадка, промежуточные точки, конечная точка) и есть ли требования к экскурсии?\n\nНапишите свой вариант или нажмите /skip чтобы пропустить.",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(SurveyStates.route)

@router.message(SurveyStates.route)
@router.message(Command("skip"))
async def process_route(message: types.Message, state: FSMContext):
    route_text = message.text if message.text != "/skip" else "Пропущено"
    await state.update_data(route=route_text)
    await message.answer("Какой бюджет или диапазон цен вы готовы рассмотреть за аренду?", reply_markup=kb.get_budget_kb())
    await state.set_state(SurveyStates.budget)

@router.message(SurveyStates.budget)
async def process_budget(message: types.Message, state: FSMContext):
    await state.update_data(budget=message.text)
    await message.answer("Какие дополнительные услуги вам нужны?", reply_markup=kb.get_extra_kb())
    await state.set_state(SurveyStates.extra_services)

@router.message(SurveyStates.extra_services)
async def process_extra(message: types.Message, state: FSMContext):
    await state.update_data(extra_services=message.text)
    await message.answer("Напишите Ваш номер телефона и сообщим Вам стоимость аренды.", reply_markup=kb.get_phone_kb())
    await state.set_state(SurveyStates.phone)

@router.message(SurveyStates.phone)
@router.message(F.contact)
async def process_phone(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number if message.contact else message.text
    await state.update_data(phone=phone)
    
    data = await state.get_data()
    
    # Send results to admins
    admin_text = (
        f"Новая анкета!\n\n"
        f"Цель: {data['purpose']}\n"
        f"Конкретный день: {data['specific_day']}\n"
        f"Кол-во человек: {data['people_count']}\n"
        f"Маршрут: {data['route']}\n"
        f"Бюджет: {data['budget']}\n"
        f"Доп. услуги: {data['extra_services']}\n"
        f"Телефон: {data['phone']}\n"
        f"Пользователь: @{message.from_user.username or 'без юзернейма'} ({message.from_user.id})"
    )
    
    for admin_id in config.ADMIN_IDS:
        try:
            await message.bot.send_message(admin_id, admin_text)
        except Exception:
            pass

    # Send final message based on purpose
    purpose = data['purpose']
    
    if "Предложение руки и сердца" in purpose:
        final_msg = (
            "<b>Предложение руки и сердца:</b>\n"
            "45т полет\n"
            "5т баннер Будь моей женой\n"
            "5т баннер Я тебя люблю\n"
            "Можем два баннера соединить\n"
            "Фото/видео видеоролик включены (снимаем на айфон 16про)\n\n"
            "Цветы можете сами привезти или заказать. Мы подадим после посадки\n\n"
            "<b>План:</b>\n"
            "Вы прилетаете за девушкой. Рассаживаемся. Взлетаем пролетаем над баннером, вы дарите кольцо и летите дальше.\n"
            "После посадки подарите букет цветов.\n"
            "В течение 24 часов будет готов видеоролик."
        )
    elif purpose in ["Отдых", "Свидание"]:
        final_msg = (
            "<b>Аренда вертолета 🚁</b>\n\n"
            "Вместимость борта 3 чел и пилот.\n"
            "Включена видеосъемка🙂\n\n"
            "<b>Стоимость:</b>\n"
            "20 мин - 45тыс.\n"
            "30 мин - 55тыс.\n"
            "75 мин (полет на Павловское водохранилище до Бухты Кила либо Красный Ключ с часовой стоянкой ) - 105 тыс.\n\n"
            "Подарочные сертификаты - лучший подарок в Уфе\n"
            "Сертификат подлежит активации в течение 3 месяцев 🔝✅\n"
            "Оформление в электронном виде👍😉\n\n"
            "<b>Что посмотреть за 20, 30 маршрут:</b>\n\n"
            "<b>20 минут</b>\n"
            "Гитара Президент Отель Олимпик Парк Восточный выезд (разворот) Монумент дружбы Конгресс Холл Салават Юлаев Жд мост (разворот) Гитара (высадка)\n\n"
            "<b>30 минут</b>\n"
            "Гитара Президент Отель Олимпик Парк Восточный выезд Сипайлово (разворот) Монумент дружбы Конгресс Холл Салават Юлаев Жд мост (разворот) Жд Вокзал Гитара (высадка)"
        )
    else: # Трансфер
        final_msg = "Спасибо за обращение. Мы сделаем расчет на Ваш трансфер и отправим в ближайшее время."

    await message.answer(final_msg, parse_mode="HTML", reply_markup=types.ReplyKeyboardRemove())
    await state.clear()

