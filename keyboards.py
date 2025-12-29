from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_purpose_kb():
    buttons = [
        [KeyboardButton(text="Отдых"), KeyboardButton(text="Свидание")],
        [KeyboardButton(text="Трансфер"), KeyboardButton(text="Предложение руки и сердца")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_yes_no_kb():
    buttons = [
        [KeyboardButton(text="Да"), KeyboardButton(text="Нет")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_people_kb():
    buttons = [
        [KeyboardButton(text="До 3-х"), KeyboardButton(text="Более 3-х")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_budget_kb():
    buttons = [
        [KeyboardButton(text="45т-55т"), KeyboardButton(text="55т и выше")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_extra_kb():
    # Extra services can be multiple, but the prompt says "What extra services do you need?".
    # I'll provide them as buttons, and maybe an "Everything selected" or "Done" button.
    # However, to keep it simple for the user request, I'll just list them as buttons for single choice or comma separated.
    # The prompt says: "питание, проживание, трансфер на месте, запись полета видео/фото, учебный полет"
    buttons = [
        [KeyboardButton(text="Питание"), KeyboardButton(text="Проживание")],
        [KeyboardButton(text="Трансфер на месте"), KeyboardButton(text="Запись полета видео/фото")],
        [KeyboardButton(text="Учебный полет"), KeyboardButton(text="Ничего не нужно")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_phone_kb():
    buttons = [
        [KeyboardButton(text="Отправить номер телефона", request_contact=True)]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)

