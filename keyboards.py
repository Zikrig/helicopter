from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_purpose_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Отдых", callback_data="purpose_Отдых"))
    builder.row(InlineKeyboardButton(text="Свидание", callback_data="purpose_Свидание"))
    builder.row(InlineKeyboardButton(text="Трансфер", callback_data="purpose_Трансфер"))
    builder.row(InlineKeyboardButton(text="Предложение руки и сердца", callback_data="purpose_Предложение руки и сердца"))
    return builder.as_markup()

def get_day_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Не принципиально", callback_data="day_Не принципиально"))
    return builder.as_markup()

def get_people_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="До 3-х", callback_data="people_До 3-х"),
                InlineKeyboardButton(text="Более 3-х", callback_data="people_Более 3-х"))
    return builder.as_markup()

def get_budget_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="45т-55т", callback_data="budget_45т-55т"),
                InlineKeyboardButton(text="55т и выше", callback_data="budget_55т и выше"))
    return builder.as_markup()

def get_extra_kb(selected_services=None):
    if selected_services is None:
        selected_services = []
        
    services = [
        "Питание", "Проживание", "Трансфер на месте", 
        "Запись полета видео/фото", "Учебный полет"
    ]
    
    builder = InlineKeyboardBuilder()
    for service in services:
        text = f"✅ {service}" if service in selected_services else service
        builder.row(InlineKeyboardButton(text=text, callback_data=f"extra_toggle_{service}"))
    
    none_text = "✅ Ничего не нужно" if "Ничего не нужно" in selected_services else "Ничего не нужно"
    builder.row(InlineKeyboardButton(text=none_text, callback_data="extra_toggle_Ничего не нужно"))
    
    builder.row(InlineKeyboardButton(text="➡️ ДАЛЕЕ", callback_data="extra_done"))
    return builder.as_markup()

def get_phone_kb():
    buttons = [
        [KeyboardButton(text="Отправить номер телефона 📞", request_contact=True)],
        [KeyboardButton(text="Не хочу")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
