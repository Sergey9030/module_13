from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


api = ""
bot = Bot(token=api)  # Бот
dp = Dispatcher(bot, storage=MemoryStorage())  # Диспетчер


kb = ReplyKeyboardMarkup(resize_keyboard=True)  # Клавиатура
bt_info = KeyboardButton(text='Информация')  # Кнопка1
bt_go = KeyboardButton(text='Рассчитать')  # Кнопка2
kb.add(bt_go, bt_info)  # Добавили кнопки в клавиатуру

ikb = InlineKeyboardMarkup(resize_keyboard=True)
ibt_info = InlineKeyboardButton(text='Формула расчета', callback_data='formulas')
ibt_go = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
ikb.add(ibt_go, ibt_info)


class UserState(StatesGroup):
    name = State()      # Имя
    age = State()       # Возраст
    growth = State()    # Рост
    weight = State()    # Вес

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=ikb)


@dp.message_handler(commands='start')
async def start(message):
    await message.answer('Привет', reply_markup=kb)


@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Здравствуйте.')
    await message.answer('Я бот, который расчитает для Вас необходимое количество калорий в сутки.')

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_name(call):
    await call.message.answer('Сообщите пожалуйста свое имя.')
    await UserState.name.set()
    await call.answer()


@dp.message_handler(state=UserState.name)
async def set_age(message, state):
    await state.update_data(name=message.text)
    data = await state.get_data()
    await message.answer(f'Здравствуйте {data["name"]}')
    await message.answer('Сообщите свой возраст (лет).')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    data = await state.get_data()
    await message.answer(f'{data["name"]}, {data["age"]}лет.')
    await message.answer('Сообщите свой вес (кг).')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    data = await state.get_data()
    await message.answer(f'{data["name"]}, {data["age"]}лет, {data["growth"]}кг.')
    await message.answer('Сообщите свой рост (см).')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    await message.answer(f'{data["name"]}, {data["age"]}лет, {data["growth"]}кг, {data["weight"]}см.')
    await message.answer(f'{data["name"]}, ваша норма калорий:'
                         f'{(10*data["growth"])+(6.25*data["weight"])-(5*data["age"])+5} кал/сутки.')
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
