from aiogram.fsm.state import State, StatesGroup

class SurveyStates(StatesGroup):
    purpose = State()
    specific_day = State()
    people_count = State()
    route = State()
    budget = State()
    extra_services = State()
    phone = State()

