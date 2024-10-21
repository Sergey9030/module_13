from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


api = ""
bot = Bot(token=api)  # Бот
dp = Dispatcher(bot, storage=MemoryStorage())  # Диспетчер


kb = ReplyKeyboardMarkup(resize_keyboard=True)  # Клавиатура
bt_info = KeyboardButton(text='Информация')  # Кнопка1
bt_go = KeyboardButton(text='Рассчитать')  # Кнопка2
kb.add(bt_go, bt_info)  # Добавили кнопки в клавиатуру


class UserState(StatesGroup):
    name = State()      # Имя
    age = State()       # Возраст
    growth = State()    # Рост
    weight = State()    # Вес


@dp.message_handler(commands='start')
async def start(message):
    await message.answer('Здравствуйте.')
    await message.answer('Я бот, который расчитает для Вас необходимое количество калорий в сутки.', reply_markup=kb)
    await message.answer('Для расчета или получения информации воспользуйтесь кнопками внизу экрана.')


@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Я бот, который расчитает для Вас необходимое количество калорий в сутки.')


@dp.message_handler(text='Рассчитать')
async def set_name(message):
    await message.answer('Сообщите пожалуйста свое имя.')
    await UserState.name.set()


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
