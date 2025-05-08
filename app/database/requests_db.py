from app.database.models import async_session, User, Config, Payment
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import desc
from datetime import datetime

def connection(func):
    async def inner(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return inner

# @connection
# async def get_user(session: AsyncSession, tg_id):
#     # Материализуем результат
#     result = await session.execute(select(User).where(User.tg_id == tg_id))
#     return result.scalar_one_or_none()  # Возвращаем первый результат или None

# @connection
# async def get_user_id(session: AsyncSession, tg_id):
#     result = await session.scalar(select(User.id).where(User.tg_id == tg_id))
#     return result

# @connection
# async def get_user_tg_nickname(session: AsyncSession, tg_nickname):
#     result = await session.scalar(select(User.tg_nickname).where(User.tg_nickname == tg_nickname))
#     return result

# @connection
# async def increase_count_ref(session: AsyncSession, tg_id):
#     stmt = (
#         update(User)
#         .where(User.tg_id == tg_id)
#         .values(count_ref=User.count_ref + 1)
#     )
#     await session.execute(stmt)
#     await session.commit()


# @connection
# async def add_user(session: AsyncSession, tg_id: int, tg_nickname, ref_id=None):
#     # Проверяем существование пользователя в текущей сессии
#     existing_user = await session.scalars(
#         select(User).where(User.tg_id == tg_id)
#     )
#     user = existing_user.first()
    
#     if user:
#         return user
    
#     if ref_id == "":
#         ref_id = None
#     else:
#         try:
#             ref_id = int(ref_id)
#             if await get_user(tg_id=ref_id) != None:
#                 await increase_count_ref(tg_id=ref_id)
#             else:
#                 ref_id = None
#         except:
#             ref_id = None
        
#     now = str(datetime.now().strftime("%d %b %Y"))
#     new_user = User(tg_id=tg_id, tg_nickname=tg_nickname, poliсy=True, offer=True, rules=True, acceptance_date=now, ref=ref_id)
#     session.add(new_user)
#     await session.commit()
#     await session.refresh(new_user)
    
#     return new_user


# @connection
# async def get_last_config_id(session):
#     query = select(Config).order_by(desc(Config.id)).limit(1)
#     last_config = await session.scalar(query)
#     if last_config:
#         return last_config.id
#     else:
#         return 0

# @connection
# async def get_bonus_points(session: AsyncSession, tg_id):
#     bonus = await session.scalar(select(User.bonus_points).where(User.tg_id == tg_id))
#     return bonus

# @connection
# async def increase_bonus_points(session: AsyncSession, tg_id, amount):
#     amount = round(amount * 0.2)
#     stmt = (
#         update(User)
#         .where(User.tg_id == tg_id)
#         .values(bonus_points=User.bonus_points + amount)
#     )
#     await session.execute(stmt)
#     await session.commit()

# @connection
# async def increment_count_pay(session: AsyncSession, user_id: int):
#     stmt = (
#         update(User)
#         .where(User.id == user_id)
#         .values(count_pay=User.count_pay + 1)
#     )
#     await session.execute(stmt)
#     await session.commit()
    
# @connection
# async def set_config(session: AsyncSession, user_id, time, info="", admin_hand=False):
#     num_config = await get_last_config_id()
#     info = str(num_config)
#     vpn = RequestVPN()
#     seconds = int(datetime.now().timestamp()) + time
#     config = ""
#     if admin_hand:
#         info += "adm"
#         config = await vpn.add_user(info, seconds)
#     else:
#         info += "usr"
#         config = await vpn.add_user(info, seconds)

#     new_config = Config(
#             config = config,
#             datatime = str(seconds),
#             info = info,
#             admin_hand = admin_hand,
#             user_id = user_id
#     )
#     session.add(new_config)
#     await session.commit()
#     await session.refresh(new_config)
#     return config


# @connection
# async def set_payment(session: AsyncSession, tarrif: str, type_pay: str, cash: int, check_payment, venue, config_id, user_id):
#     # class Payment(Base):
#     # __tablename__ = "payments"
    
#     # id: Mapped[int] = mapped_column(primary_key=True)
#     # datatime: Mapped[str] = mapped_column(String)
#     # tariff: Mapped[str] = mapped_column(String)
#     # type_pay: Mapped[str] = mapped_column(String)
#     # cash: Mapped[float] = mapped_column(float)
#     # check_payment: Mapped[dict] = mapped_column(JSON)
#     # venue: Mapped[str] = mapped_column(String)
#     # config_id: Mapped[int] = mapped_column(ForeignKey("configs.id"))
#     # user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    
#     new_payment = Payment(
#         datatime = str(datetime.now().strftime("%d %b %Y")),
#         tariff = tarrif,
#         type_pay = type_pay,
#         cash = cash,
#         check_payment = check_payment,
#         venue = venue,
#         config_id = config_id,
#         user_id = user_id)
        
#     session.add(new_payment)
#     await increment_count_pay(user_id=user_id)
#     await session.commit()
#     await session.refresh(new_payment)
    
#     return None
    
    
# @connection
# async def get_politics(session: AsyncSession, tg_id):
#     policy = await session.scalar(select(User.politic).where(User.tg_id == tg_id))
    
# @connection
# async def get_all_users(session: AsyncSession):
#     result = await session.execute(select(User.tg_id))
#     return result.scalars().all()

# @connection
# async def delete_config(session: AsyncSession, config: str):
#     await session.execute(delete(Config).where(Config.config == config))
#     await session.commit()


# @connection
# async def get_user_configs_dict(session: AsyncSession, user_id: int):
#     stmt = (
#         select(Config.config, Config.datatime)
#         .where(Config.user_id == user_id)
#     )
#     result = await session.execute(stmt)
#     configs = []
#     now = datetime.now().timestamp()
    
    
#     for r in result:
#         if int(r.datatime) < now:
#             await delete_config(config=r.config)
#             continue
#         configs.append({"config": r.config, "datatime": r.datatime})
    
#     return configs

# @connection
# async def get_trial_users(session: AsyncSession):
#     stmt = select(User.tg_id).where(
#         (User.trial == False) & 
#         (User.count_pay == 0)
#     )
#     result = await session.execute(stmt)
#     return result.scalars().all()

# @connection
# async def set_trial(session: AsyncSession, user_id):
#     stmt = (
#         update(User)
#         .where(User.id == user_id)
#         .values(trial = True)
#     )
#     await session.execute(stmt)
#     await session.commit()