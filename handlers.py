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

@router.callback_query(SurveyStates.purpose, F.data.startswith("purpose_"))
async def process_purpose(callback: types.CallbackQuery, state: FSMContext):
    purpose = callback.data.split("_")[1]
    await state.update_data(purpose=purpose)
    # Inline buttons can't stay after text input, so we send a message that allows both
    await callback.message.delete()
    await callback.message.answer(
        f"Цель: {purpose}\n\nНапишите желаемую дату полета или нажмите кнопку ниже:",
        reply_markup=kb.get_day_kb()
    )
    await state.set_state(SurveyStates.specific_day)
    await callback.answer()

async def handle_day_selection(day_text: str, message: types.Message, state: FSMContext):
    await state.update_data(specific_day=day_text)
    data = await state.get_data()
    purpose = data.get("purpose")
    
    # Если свидание или предложение, пропускаем вопрос о количестве людей (подразумеваем 2)
    if purpose in ["Свидание", "Предложение руки и сердца"]:
        await state.update_data(people_count="2 человека")
        await message.answer(
            f"Выбрано: {day_text}\n\nКакой маршрут/путь полета вам нужен (начальная площадка, промежуточные точки, конечная точка) и есть ли требования к экскурсии?\n\nНапишите свой вариант или нажмите /skip чтобы пропустить.",
            reply_markup=types.ReplyKeyboardRemove()
        )
        await state.set_state(SurveyStates.route)
    else:
        await message.answer(
            f"Выбрано: {day_text}\n\nСколько человек планирует полет?",
            reply_markup=kb.get_people_kb()
        )
        await state.set_state(SurveyStates.people_count)

@router.callback_query(SurveyStates.specific_day, F.data.startswith("day_"))
async def process_day_callback(callback: types.CallbackQuery, state: FSMContext):
    day = callback.data.split("_")[1]
    await callback.message.delete()
    await handle_day_selection(day, callback.message, state)
    await callback.answer()

@router.message(SurveyStates.specific_day)
async def process_day_text(message: types.Message, state: FSMContext):
    await handle_day_selection(message.text, message, state)

@router.callback_query(SurveyStates.people_count, F.data.startswith("people_"))
async def process_people(callback: types.CallbackQuery, state: FSMContext):
    count = callback.data.split("_")[1]
    await state.update_data(people_count=count)
    await callback.message.delete()
    await callback.message.answer(
        f"Кол-во человек: {count}\n\nКакой маршрут/путь полета вам нужен (начальная площадка, промежуточные точки, конечная точка) и есть ли требования к экскурсии?\n\nНапишите свой вариант или нажмите /skip чтобы пропустить.",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(SurveyStates.route)
    await callback.answer()

@router.message(SurveyStates.route)
@router.message(Command("skip"))
async def process_route(message: types.Message, state: FSMContext):
    route_text = message.text if message.text != "/skip" else "Пропущено"
    await state.update_data(route=route_text)
    await message.answer("Какой бюджет или диапазон цен вы готовы рассмотреть за аренду?", reply_markup=kb.get_budget_kb())
    await state.set_state(SurveyStates.budget)

@router.callback_query(SurveyStates.budget, F.data.startswith("budget_"))
async def process_budget(callback: types.CallbackQuery, state: FSMContext):
    budget = callback.data.split("_")[1]
    await state.update_data(budget=budget, extra_services_list=[])
    await callback.message.edit_text(f"Бюджет: {budget}\n\nКакие дополнительные услуги вам нужны? (можно выбрать несколько)")
    await callback.message.edit_reply_markup(reply_markup=kb.get_extra_kb([]))
    await state.set_state(SurveyStates.extra_services)
    await callback.answer()

@router.callback_query(SurveyStates.extra_services, F.data.startswith("extra_toggle_"))
async def toggle_extra(callback: types.CallbackQuery, state: FSMContext):
    service = callback.data.replace("extra_toggle_", "")
    data = await state.get_data()
    selected = data.get("extra_services_list", [])
    
    if service == "Ничего не нужно":
        if "Ничего не нужно" in selected:
            selected = []
        else:
            selected = ["Ничего не нужно"]
    else:
        if "Ничего не нужно" in selected:
            selected.remove("Ничего не нужно")
        
        if service in selected:
            selected.remove(service)
        else:
            selected.append(service)
    
    await state.update_data(extra_services_list=selected)
    await callback.message.edit_reply_markup(reply_markup=kb.get_extra_kb(selected))
    await callback.answer()

@router.callback_query(SurveyStates.extra_services, F.data == "extra_done")
async def process_extra_done(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = data.get("extra_services_list", [])
    
    if not selected:
        await callback.answer("Выберите хотя бы один пункт или 'Ничего не нужно'", show_alert=True)
        return

    services_str = ", ".join(selected)
    await state.update_data(extra_services=services_str)
    
    await callback.message.delete()
    await callback.message.answer(
        f"Доп. услуги: {services_str}\n\nНапишите Ваш номер телефона или нажмите кнопку ниже, и мы сообщим Вам стоимость аренды.", 
        reply_markup=kb.get_phone_kb()
    )
    await state.set_state(SurveyStates.phone)
    await callback.answer()

@router.message(SurveyStates.phone)
@router.message(F.contact)
async def process_phone(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number if message.contact else message.text
    await state.update_data(phone=phone)
    
    data = await state.get_data()
    
    admin_text = (
        f"🚁 <b>Новая анкета!</b>\n\n"
        f"<b>Цель:</b> {data['purpose']}\n"
        f"<b>Конкретный день:</b> {data['specific_day']}\n"
        f"<b>Кол-во человек:</b> {data['people_count']}\n"
        f"<b>Маршрут:</b> {data['route']}\n"
        f"<b>Бюджет:</b> {data['budget']}\n"
        f"<b>Доп. услуги:</b> {data['extra_services']}\n"
        f"<b>Телефон:</b> {data['phone']}\n\n"
        f"<b>Пользователь:</b> @{message.from_user.username or 'без юзернейма'} ({message.from_user.id})"
    )
    
    for admin_id in config.ADMIN_IDS:
        try:
            await message.bot.send_message(admin_id, admin_text, parse_mode="HTML")
        except Exception:
            pass

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
    else:
        final_msg = "Спасибо за обращение. Мы сделаем расчет на Ваш трансфер и отправим в ближайшее время."

    await message.answer(final_msg, parse_mode="HTML", reply_markup=types.ReplyKeyboardRemove())
    await state.clear()
