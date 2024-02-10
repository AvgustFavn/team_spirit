from datetime import timedelta

from db_stuff import *
from aiogram import types, Bot

API_TOKEN = '6930385521:AAFb7zZqIbOYAzDm4y2vKtSXiRttGS2ZmqA'
bot = Bot(token=API_TOKEN)


def user_reg(username, id):
    user = User(tg_id=id, username=username)
    session.add(user)
    session.commit()


def add_bid(text, user_id_tg):
    bid = Bids(user_id=user_id_tg, text=text)
    session.add(bid)
    session.commit()
    return bid


async def send_new_bid(bid):
    text = f'📢📢Пришла новая заявка📢📢\n' \
           f'Текст завяки: {bid.text}\n'
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    keyboard_markup.add(types.InlineKeyboardButton('Добавить воркера ✅', callback_data=f'accept_bidid_{bid.id}'))
    keyboard_markup.add(types.InlineKeyboardButton('Отказать ❌', callback_data=f'cancel_bidid_{bid.id}'))
    await bot.send_message(chat_id='-1002063632581', text=text, reply_markup=keyboard_markup)


async def get_bids(user_id):
    bids = session.query(Bids).filter(Bids.status == 0)
    for bid in bids:
        text = f'📢📢Новая заявка📢📢\n' \
               f'Текст завяки: {bid.text}\n'
        keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
        keyboard_markup.add(types.InlineKeyboardButton('Добавить воркера ✅', callback_data=f'accept_bidid_{bid.id}'))
        keyboard_markup.add(types.InlineKeyboardButton('Отказать ❌', callback_data=f'cancel_bidid_{bid.id}'))
        await bot.send_message(chat_id=user_id, text=text, reply_markup=keyboard_markup)


def accept_bid(id):
    session.rollback()
    bid = session.query(Bids).filter(Bids.id == id).first()
    bid.status = 1
    user = session.query(User).filter(User.tg_id == bid.user_id).first()
    user.status = 1
    session.add(bid)
    session.add(user)
    session.commit()
    return user


def cancel_bid(id):
    session.rollback()
    bid = session.query(Bids).filter(Bids.id == id).first()
    bid.status = 2
    user = session.query(User).filter(User.tg_id == bid.user_id).first()
    session.add(bid)
    session.commit()
    return user


def is_worker(id_tg):
    session.rollback()
    user = session.query(User).filter(User.tg_id == id_tg).first()
    print(user)
    if user:
        if user.status > 0:
            return True
        else:
            return False
    else:
        return False


def is_employee(id_tg):
    session.rollback()
    user = session.query(User).filter(User.tg_id == id_tg).first()
    if user:
        if user.status > 1:
            return True
        else:
            return False
    else:
        return False


def is_admin(id_tg):
    session.rollback()
    user = session.query(User).filter(User.tg_id == id_tg).first()
    if user:
        if user.status >= 4:
            return True
        else:
            return False
    else:
        return False


def is_sponsor(id_tg):
    session.rollback()
    user = session.query(User).filter(User.tg_id == id_tg).first()
    if user:
        if user and user.status == 5:
            return True
        else:
            return False
    else:
        return False


async def cats(id_tg):
    user = session.query(User).filter(User.tg_id == id_tg).first()
    text = f'Ваша категория: {user.category}. Вы можете выбрать новое направление:'
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    keyboard_markup.add(types.InlineKeyboardButton('💖 антикино 💖', callback_data=f'take_cat_антикино'))
    keyboard_markup.add(types.InlineKeyboardButton('💊 нарко 💊', callback_data=f'take_cat_нарко'))
    keyboard_markup.add(types.InlineKeyboardButton('💶 трейд 💶', callback_data=f'take_cat_трейд'))
    keyboard_markup.add(types.InlineKeyboardButton('🖼 нфт 🖼', callback_data=f'take_cat_нфт'))
    keyboard_markup.add(types.InlineKeyboardButton('🎀 эскорт 🎀', callback_data=f'take_cat_эскорт'))
    keyboard_markup.add(types.InlineKeyboardButton('🐟 фишинг 🐟', callback_data=f'take_cat_фишинг'))
    image_path = f'{BASE_DIR}/images/direction.jpg'
    with open(image_path, 'rb') as photo:
        await bot.send_photo(id_tg, photo, caption=text, reply_markup=keyboard_markup)


def set_category(user_id, category):
    user = session.query(User).filter(User.tg_id == user_id).first()
    user.category = category
    session.add(user)
    session.commit()


async def profile_bd(user_id):
    user = session.query(User).filter(User.tg_id == user_id).first()
    profits = session.query(Profits.full_profit, Profits.share_workers).filter(Profits.user_id == user_id)
    full = 0.0
    share = 0.0
    for profit in profits:
        full += float(profit.full_profit)
        share += float(profit.share_workers)

    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    keyboard_markup.add(types.InlineKeyboardButton('Ссылки', callback_data=f'links'))
    text = f'Вы с нами с {user.data_join}\n' \
           f'Категория ворка: {user.category}\n' \
           f'Профитов, чистыми, на сумму: {share} USDT\n' \
           f'Полная сумма залетов: {full} USDT'
    image_path = f'{BASE_DIR}/images/profile.jpg'
    with open(image_path, 'rb') as photo:
        await bot.send_photo(user_id, photo, caption=text, reply_markup=keyboard_markup)


async def links_bd(user_id):
    user = session.query(User).filter(User.tg_id == user_id).first()
    cat = user.category
    current_date = datetime.now()
    two_days_ago = current_date - timedelta(days=2)
    links = session.query(Links).filter(
        and_(
            Links.user_id == user_id,
            Links.date >= two_days_ago
        )
    )
    text = f'Ваши существующие ссылки: \n'
    await bot.send_message(chat_id=user_id, text=text)
    if links:
        for link in links:
            await bot.send_message(chat_id=user_id, text=f'Ваша ссылка категории {link.category}: {link.link}')
    else:
        await bot.send_message(chat_id=user_id, text=f'У вас нету ссылок')

    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    keyboard_markup.add(types.InlineKeyboardButton('Создать новую', callback_data=f'new_link'))
    await bot.send_message(chat_id=user_id, text="Можете создать новую ссылку", reply_markup=keyboard_markup)


def del_admin_bd(username):
    try:
        user = session.query(User).filter(User.username == username).first()
        user.status = 1
        session.add(user)
        session.commit()
    except:
        pass


def add_admin_bd(username):
    try:
        user = session.query(User).filter(User.username == username).first()
        user.status = 4
        session.add(user)
        session.commit()
    except:
        pass


def add_vbiv_bd(username):
    try:
        user = session.query(User).filter(User.username == username).first()
        user.status = 3
        session.add(user)
        session.commit()
    except:
        pass


def del_vbiv_bd(username):
    try:
        user = session.query(User).filter(User.username == username).first()
        user.status = 1
        session.add(user)
        session.commit()
    except:
        pass


def add_tp_bd(username):
    try:
        user = session.query(User).filter(User.username == username).first()
        user.status = 2
        session.add(user)
        session.commit()
    except:
        pass


def del_tp_bd(username):
    try:
        user = session.query(User).filter(User.username == username).first()
        user.status = 1
        session.add(user)
        session.commit()
    except:
        pass


def del_worker_bd(username):
    try:
        user = session.query(User).filter(User.username == username).first()
        user.status = 0
        session.add(user)
        session.commit()
    except:
        pass


def change_about_bd(text):
    about = About(text=text)
    session.add(about)
    session.commit()


def card_bd(country, card):
    card = Cards(country=country, numbers=str(card))
    session.add(card)
    session.commit()


def share_worker(prof):
    percent = 70.0
    if prof.tech_supp_username != 'Нету':
        print(prof.tech_supp_username)
        percent -= 5.0
    if prof.is_reffil:
        percent -= 10.0

    print(percent)
    prof.share_workers = (prof.full_profit / 100) * percent
    prof.percent = percent
    session.add(prof)
    session.commit()
    return prof.share_workers
