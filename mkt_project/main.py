import logging
import re
import sqlite3
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from back import is_worker, is_admin, user_reg, add_bid, send_new_bid, get_bids, is_employee, accept_bid, cancel_bid, \
    cats, set_category, profile_bd, links_bd, is_sponsor, del_admin_bd, add_admin_bd, add_vbiv_bd, del_vbiv_bd, \
    add_tp_bd, del_tp_bd, del_worker_bd, change_about_bd, card_bd, share_worker
from db_stuff import session, About, Links, Profits, User, BASE_DIR

API_TOKEN = '6362029327:AAGoXaoOjSk7wLaAQA3qQXKPcmmtePktO1k'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    username = message.from_user.username
    user_id = message.from_user.id
    if is_worker(int(user_id)):
        #  Рабочее всякое
        print(int(user_id))
        keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard_markup.add(KeyboardButton('О проекте 💪', callback_data='about'))
        keyboard_markup.add(KeyboardButton('Направления для работы 💼', callback_data='category'))
        keyboard_markup.add(KeyboardButton('Профиль 👤', callback_data='profile'))
        if is_admin(int(user_id)): keyboard_markup.add(KeyboardButton('Админ панель', callback_data='admin'))
        await bot.send_message(text='Привет! Начнем воркать, заряду!', reply_markup=keyboard_markup, chat_id=user_id)

    else:
        try:
            user_reg(username, int(user_id))
        except:
            pass
        keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
        keyboard_markup.add(types.InlineKeyboardButton('Я прочитал и согласился с правилами ✅', callback_data='okk'))

        text = f"""
        👋 Привет,{username}, перед началом работы заполни небольшую анкету и ознакомься с правилами проекта:\n
    
        • Запрещена любая реклама, флуд, спам, коммерция, продажа услуг в чате воркеров\n
        • Запрещено оскорблять воркеров, разводить срач, вести себя неадекватно\n
        • Запрещено попрошайничество в любом его виде\n
        • Запрещено отправлять мамонтам свои реквизиты\n
        • Запрещено принимать оплату на свои реквизиты\n
        • Запрещено отправлять мамонтам свои тех. поддержки\n
        • Запрещены попытки скама или скам воркеров в любом его виде\n
        • Заблокированные пользователи не получают выплаты\n
        • ТСы проекта не несут ответственности за блокировку кошельков\n
        • ТСы проекта имеют право не принимать в команду воркера без обёяснения причин\n
        
        ✅ Если ты согласен с правилами проекта, нажми на кнопку ниже\n
        """
        image_path = f'{BASE_DIR}\\images\\team_call.jpg'
        with open(image_path, 'rb') as photo:
            await bot.send_photo(user_id, photo, caption=text, reply_markup=keyboard_markup)


# Обработчик текстовых сообщений
@dp.callback_query_handler(lambda c: c.data == 'okk')
async def send_text(message: types.Message):
    user_id = message.from_user.id
    text = 'Напишите о себе немного:\n' \
           '1) Ваш опыт работы, место ворка\n' \
           '2) Какую кассу без % делаешь за неделю\n' \
           '3) Почему ищешь новую тиму?'
    await bot.send_message(text=text, chat_id=user_id)

# Обработчик команды /bids
@dp.message_handler(commands=['bids'])
async def show_bids_list(message: types.Message):
    user_id = message.from_user.id
    if is_admin(user_id):
        await get_bids(user_id)

@dp.callback_query_handler(lambda c: c.data.startswith('accept_bidid_'))
async def process_accept(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if is_employee(user_id):
        bid_id = int(callback_query.data[int(str(callback_query.data).find('accept_bidid_'))+13:])
        user = accept_bid(bid_id)
        user.data_join = datetime.now()
        session.add(user)
        session.commit()
        await callback_query.message.edit_text('У вас новый воркер!')
        await bot.send_message(chat_id=user.tg_id, text='Вы были приняты! Перезагрузите бота для начала ворка!\n'
                                                        '🩵 /start 🩵')

@dp.callback_query_handler(lambda c: c.data.startswith('cancel_bidid_'))
async def process_cancel(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if is_employee(user_id):
        bid_id = int(callback_query.data[int(str(callback_query.data).find('cancel_bidid_'))+13:])
        user = cancel_bid(bid_id)
        await callback_query.message.edit_text('Вы отказали')
        await bot.send_message(chat_id=user.tg_id, text='Вам отказали :( Приходите в следующий раз!')

############################ Далее функционал ворка ####################################

@dp.message_handler(lambda message: message.text == 'Про нас 💪')
async def about(message: types.Message):
    user_id = message.from_user.id
    about_ = session.query(About).order_by(About.id.desc()).first()
    if about_:
        text = about_.text
    else:
        text = 'Пока тут ничего'

    image_path = f'{BASE_DIR}\\images\\about.jpg'
    with open(image_path, 'rb') as photo:
        await bot.send_photo(user_id, photo, caption=text)

@dp.message_handler(lambda message: message.text == 'Направления для работы 💼')
async def category(message: types.Message):
    user_id = message.from_user.id
    await cats(user_id)

@dp.callback_query_handler(lambda c: c.data.startswith('take_cat_'))
async def change_category(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    cat = callback_query.data[str(callback_query.data).find('take_cat_') + 9:]
    set_category(user_id, cat)
    await bot.send_message(chat_id=user_id, text='Вы выбрали новую категорию! Удачного ворка :)')

@dp.message_handler(lambda message: message.text == 'Профиль 👤')
async def profile(message: types.Message):
    user_id = message.from_user.id
    await profile_bd(user_id)

@dp.callback_query_handler(lambda c: c.data == 'links')
async def links(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await links_bd(user_id)

@dp.callback_query_handler(lambda c: c.data == 'new_link')
async def links(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    keyboard_markup.add(types.InlineKeyboardButton('Нарко', callback_data=f'new_link_narko'))
    await bot.send_message(chat_id=user_id, text='Выберите ссылку чего вам нужно сделать?', reply_markup=keyboard_markup)

@dp.callback_query_handler(lambda c: c.data == 'new_link_narko')
async def new_link_narko(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    invite_link = f'https://t.me/luminoreshop_bot?start={user_id}'
    link = Links(user_id=user_id, link=invite_link, category='нарко')
    session.add(link)
    session.commit()
    await bot.send_message(chat_id=user_id, text=f'Ваша новая ссылка: {invite_link}')

@dp.message_handler(lambda message: message.text == 'Админ панель')
async def admin(message: types.Message):
    user_id = message.from_user.id
    if is_admin(int(user_id)):
        text = 'Админ панель:'
        keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
        if is_sponsor(int(user_id)):
            keyboard_markup.add(types.InlineKeyboardButton('Опубликовать профит', callback_data='add_profit'))
            keyboard_markup.add(types.InlineKeyboardButton('Удалить админа', callback_data='del_admin'))
            keyboard_markup.add(types.InlineKeyboardButton('Добавить админа', callback_data='add_admin'))
            keyboard_markup.add(types.InlineKeyboardButton('Добавить карту', callback_data='cards'))
        keyboard_markup.add(types.InlineKeyboardButton('Добавить вбива', callback_data='add_vbiv'))
        keyboard_markup.add(types.InlineKeyboardButton('Удалить вбива', callback_data='del_vbiv'))
        keyboard_markup.add(types.InlineKeyboardButton('Добавить ТП', callback_data='add_tp'))
        keyboard_markup.add(types.InlineKeyboardButton('Удалить ТП', callback_data='del_tp'))
        keyboard_markup.add(types.InlineKeyboardButton('Выгнать воркера', callback_data='del_worker'))
        keyboard_markup.add(types.InlineKeyboardButton('Изменить "о нас"', callback_data='change_about'))
        keyboard_markup.add(types.InlineKeyboardButton('Все заявки', callback_data='bids'))
        image_path = f'{BASE_DIR}\\images\\admin.jpg'
        with open(image_path, 'rb') as photo:
            await bot.send_photo(user_id, photo, caption=text, reply_markup=keyboard_markup)


@dp.callback_query_handler(lambda c: c.data == 'add_profit')
async def add_profit_mess(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.send_message(chat_id=user_id, text='Напишите для создания нового профита, используйте четкий шаблон, если нет тп, вбива и др опций, просто пропустите их. Проценты высчитываются самостоятельно в зависимости от участия тп, вбива:\n'
                                                 ' /add_profit 1)Ник воркера\n2)Ник ТП\n3)Полная сумма снятия в USDT \n4)Категория ворка (нарко) \n')

@dp.callback_query_handler(lambda c: c.data == 'cards')
async def cards_mess(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.send_message(chat_id=user_id, text='Напишите для показа заявок: /card (кз, укр, рус) 2929293377273279237\n'
                                                 'Пример: /card кз 33787739929')

@dp.callback_query_handler(lambda c: c.data == 'bids')
async def bids_mess(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.send_message(chat_id=user_id, text='Напишите для показа заявок: /bids')

@dp.callback_query_handler(lambda c: c.data == 'del_admin')
async def del_admin_mess(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.send_message(chat_id=user_id, text='Напишите для удаления админа: /del_admin @username')


@dp.callback_query_handler(lambda c: c.data == 'add_admin')
async def add_admin_mess(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.send_message(chat_id=user_id, text='Напишите для добавления админа: /add_admin @username')

@dp.callback_query_handler(lambda c: c.data == 'add_vbiv')
async def add_vbiv_mess(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.send_message(chat_id=user_id, text='Напишите для добавления вбива: /add_vbiv @username')

@dp.callback_query_handler(lambda c: c.data == 'del_vbiv')
async def del_vbiv_mess(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.send_message(chat_id=user_id, text='Напишите для удаления вбива: /del_vbiv @username')

@dp.callback_query_handler(lambda c: c.data == 'add_tp')
async def add_tp_mess(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.send_message(chat_id=user_id, text='Напишите для добавления ТП: /add_tp @username')

@dp.callback_query_handler(lambda c: c.data == 'del_tp')
async def del_tp_mess(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.send_message(chat_id=user_id, text='Напишите для удаления ТП: /del_tp @username')

@dp.callback_query_handler(lambda c: c.data == 'del_worker')
async def del_worker_mess(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.send_message(chat_id=user_id, text='Напишите для удаления воркера: /del_worker @username')

@dp.callback_query_handler(lambda c: c.data == 'change_about')
async def change_about_mess(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.send_message(chat_id=user_id, text='Напишите для изменения "О нас": /change_about Тут какое-то описание')

@dp.message_handler(commands=['del_admin'])
async def del_admin(message: types.Message):
    user_id = message.from_user.id
    if is_sponsor(int(user_id)):
        username = message.text[str(message.text).find('@') + 1:]
        del_admin_bd(username)
        await bot.send_message(chat_id=user_id, text='Админ удален!')

@dp.message_handler(commands=['add_admin'])
async def add_admin(message: types.Message):
    user_id = message.from_user.id
    if is_sponsor(int(user_id)):
        username = message.text[str(message.text).find('@') + 1:]
        add_admin_bd(username)
        await bot.send_message(chat_id=user_id, text='Админ добавлен!')

@dp.message_handler(commands=['add_vbiv'])
async def add_vbiv(message: types.Message):
    user_id = message.from_user.id
    if is_admin(int(user_id)):
        username = message.text[str(message.text).find('@') + 1:]
        add_vbiv_bd(username)
        await bot.send_message(chat_id=user_id, text='Вбив добавлен!')

@dp.message_handler(commands=['del_vbiv'])
async def del_vbiv(message: types.Message):
    user_id = message.from_user.id
    if is_admin(int(user_id)):
        username = message.text[str(message.text).find('@') + 1:]
        del_vbiv_bd(username)
        await bot.send_message(chat_id=user_id, text='Вбив удален!')

@dp.message_handler(commands=['add_tp'])
async def add_tp(message: types.Message):
    user_id = message.from_user.id
    if is_admin(int(user_id)):
        username = message.text[str(message.text).find('@') + 1:]
        add_tp_bd(username)
        await bot.send_message(chat_id=user_id, text='ТП добавлен!')

@dp.message_handler(commands=['del_tp'])
async def del_tp(message: types.Message):
    user_id = message.from_user.id
    if is_admin(int(user_id)):
        username = message.text[str(message.text).find('@') + 1:]
        del_tp_bd(username)
        await bot.send_message(chat_id=user_id, text='ТП удален!')

@dp.message_handler(commands=['del_worker'])
async def del_worker(message: types.Message):
    user_id = message.from_user.id
    if is_admin(int(user_id)):
        username = message.text[str(message.text).find('@') + 1:]
        del_worker_bd(username)
        await bot.send_message(chat_id=user_id, text=f'Воркер @{username}, больше не воркер! Он больше не может '
                                                     f'пользоваться функционалом воркера. Не забудьте его удалить '
                                                     f'из чатов')

@dp.message_handler(commands=['change_about'])
async def change_about(message: types.Message):
    user_id = message.from_user.id
    if is_admin(int(user_id)):
        text = message.text
        change_about_bd(text.replace('/change_about ', ''))
        await bot.send_message(chat_id=user_id, text='Вы изменили информацию')

@dp.message_handler(commands=['card'])
async def card(message: types.Message):
    user_id = message.from_user.id
    if is_sponsor(int(user_id)):
        data = message.text
        country, card = data.replace('/card ', '').split(' ')
        print(country, card)
        card_bd(country, card)
        await bot.send_message(chat_id=user_id, text=f'Добавлена новая карта {country}')

@dp.message_handler(commands=['add_profit'])
async def add_profit(message: types.Message):
    user_id = message.from_user.id
    if is_sponsor(int(user_id)):
        data = message.text
        worker = data[data.find('1)')+1:data.find('2)')]
        if ')' in worker:
            worker = worker[:worker.find('3)')]

        worker = worker[1:]
        worker = worker.replace(' ', '').replace('@', '').replace('\n', '')
        print(f"aa{worker}aa")

        if '2)' in data:
            tp = data[data.find('2)') + 2:data.find('3)') - 1]
            tp = tp.replace(' ', '').replace('@', '').replace('\n', '')
        else:
            tp = 'Нету'

        cat = str(data[data.find('4)') + 2:]).replace(' ', '')
        full = str(data[data.find('3)') + 1:data.find('4)') - 1])
        float_pattern = re.compile(r'[-+]?\d*\.\d+|\d+')
        match = float_pattern.search(full)
        if match:
            full = float(match.group())
            user = session.query(User).filter(User.username == worker).first()
            prof = Profits(user_id=int(user.tg_id), username_worker=worker,
                           full_profit=full, tech_supp_username=tp, category=cat)
            share = share_worker(prof)
            text = f'💸 ЗАЛЕЕЕТ! - {full} USDT 💸\n' \
                   f'ТП: @{tp}\n' \
                   f'Часть воркера: {share} USDT\n' \
                   f'Категория: {prof.category}'



            await bot.send_message(chat_id=user_id,
                                   text=f'Профит создан!')
            await bot.send_message(chat_id='-1002014887503',
                                   text=text)

            await bot.send_message(chat_id='-1002106623204',
                                   text=text)

            await bot.send_message(chat_id=int(user.tg_id),
                                   text=text)
        else:
            await bot.send_message(chat_id=user_id, text=f'Ваша сумма профита не засчиталась, проверьте ваше сообщение с учктом шаблона')


@dp.message_handler(lambda message: message.text)
async def save_bid(message: types.Message):
    user_id = message.from_user.id
    if is_worker(user_id) == False:
        bid = add_bid(message.text, int(message.from_user.id))
        await send_new_bid(bid)
        await bot.send_message(text="Ваша заявка принята, ожидайте :)", chat_id=user_id)

if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
