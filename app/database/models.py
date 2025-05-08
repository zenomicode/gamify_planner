from typing import List, Optional

from sqlalchemy import Boolean, Integer, String, ForeignKey, BigInteger, JSON, Float, Enum
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from enum import Enum as PyEnum
from app.config import DB_URL
from datetime import date

engine = create_async_engine(url=DB_URL,
                             echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(17), unique=True)
    password: Mapped[str] = mapped_column(String(17))
    nickname: Mapped[str] = mapped_column(String(31))
    class_id: Mapped[Optional[int]] = mapped_column(ForeignKey('classes.class_id'))
    information: Mapped[Optional[str]] = mapped_column(String(511))
    level: Mapped[int] = mapped_column(default=1)
    lives: Mapped[int] = mapped_column(default=10)
    max_lives: Mapped[int] = mapped_column(default=10)
    points: Mapped[int] = mapped_column(default=0)
    max_points: Mapped[int] = mapped_column(default=100)
    gold: Mapped[int] = mapped_column(default=0)
    attack: Mapped[int] = mapped_column(default=1)
    team_id: Mapped[Optional[int]] = mapped_column(ForeignKey('teams.team_id'))
    img: Mapped[str] = mapped_column(String)
    refresh_token = mapped_column(String(512), nullable=True) 
    # Связи
    items: Mapped[list['UserItem']] = relationship(back_populates='user')
    class_: Mapped['Class'] = relationship(back_populates='users')
    team: Mapped['Team'] = relationship(back_populates='users')
    catalogs: Mapped[list['Catalog']] = relationship(back_populates='user')
    owned_teams: Mapped[list['Team']] = relationship(
        back_populates='owner_user',
        foreign_keys='Team.owner'
    )
    
class ItemRarity(PyEnum):
    COMMON = 'com'
    RARE = 'rare'

class Item(Base):
    __tablename__ = 'items'

    item_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer)
    information: Mapped[Optional[str]] = mapped_column(String(512))
    type: Mapped[ItemRarity] = mapped_column(Enum(ItemRarity))
    class_id: Mapped[Optional[int]] = mapped_column(ForeignKey('classes.class_id'))
    bonus_type: Mapped[Optional[str]] = mapped_column(String(31))
    bonus_data: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Связи
    users: Mapped[list['UserItem']] = relationship(back_populates='item')
    class_: Mapped['Class'] = relationship(back_populates='items')
    
class ActiveStatus(PyEnum):
    ACTIVE = 'true'
    INACTIVE = 'false'

class UserItem(Base):
    __tablename__ = 'user_items'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey('items.item_id'), primary_key=True)
    active: Mapped[ActiveStatus] = mapped_column(Enum(ActiveStatus), default=ActiveStatus.INACTIVE)
    
    # Связи
    user: Mapped['User'] = relationship(back_populates='items')
    item: Mapped['Item'] = relationship(back_populates='users')
    
class ActiveStatus(PyEnum):
    ACTIVE = 'true'
    INACTIVE = 'false'

class UserItem(Base):
    __tablename__ = 'user_items'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey('items.item_id'), primary_key=True)
    active: Mapped[ActiveStatus] = mapped_column(Enum(ActiveStatus), default=ActiveStatus.INACTIVE)
    
    # Связи
    user: Mapped['User'] = relationship(back_populates='items')
    item: Mapped['Item'] = relationship(back_populates='users')
    
# 4. Таблица классов
class Class(Base):
    __tablename__ = 'classes'

    class_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    information: Mapped[Optional[str]] = mapped_column(String)

    users: Mapped[list['User']] = relationship(back_populates='class_')
    items: Mapped[list['Item']] = relationship(back_populates='class_')

# 5. Таблица команд
class Team(Base):
    __tablename__ = 'teams'

    team_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(63))
    owner: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    information: Mapped[Optional[str]] = mapped_column(String(255))
    boss_id: Mapped[Optional[int]] = mapped_column(ForeignKey('bosses.boss_id'))
    boss_lives: Mapped[Optional[int]] = mapped_column(Integer)

    users: Mapped[list['User']] = relationship(back_populates='team')
    boss: Mapped['Boss'] = relationship(back_populates='teams')

# 6. Таблица боссов
class Boss(Base):
    __tablename__ = 'bosses'

    boss_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40))
    base_lives: Mapped[int]
    information: Mapped[Optional[str]] = mapped_column(String)
    level: Mapped[int]

    teams: Mapped[list['Team']] = relationship(back_populates='boss')

# 7. Таблица каталогов
class Catalog(Base):
    __tablename__ = 'catalogs'

    catalog_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    name: Mapped[str] = mapped_column(String(127))

    user: Mapped['User'] = relationship(back_populates='catalogs')
    tasks: Mapped[list['Task']] = relationship(back_populates='catalog')

# 8. Таблица задач
class TaskComplexity(PyEnum):
    EASY = 'easy'
    NORMAL = 'normal'
    HARD = 'hard'

class Task(Base):
    __tablename__ = 'tasks'

    task_id: Mapped[int] = mapped_column(primary_key=True)
    catalog_id: Mapped[int] = mapped_column(ForeignKey('catalogs.catalog_id'))
    name: Mapped[str] = mapped_column(String(127))
    complexity: Mapped[TaskComplexity] = mapped_column(Enum(TaskComplexity))
    deadline: Mapped[Optional[date]]

    catalog: Mapped['Catalog'] = relationship(back_populates='tasks')
    daily_tasks: Mapped[list['DailyTask']] = relationship(back_populates='task')

# 9. Таблица повторяющихся задач
class DayOfWeek(PyEnum):
    MON = 'mon'
    TUE = 'tue'
    WED = 'wed'
    THU = 'thu'
    FRI = 'fri'
    SAT = 'sat'
    SUN = 'sun'

class DailyTask(Base):
    __tablename__ = 'daily_task'

    daily_task_id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.task_id'))
    day_week: Mapped[DayOfWeek] = mapped_column(Enum(DayOfWeek))

    task: Mapped['Task'] = relationship(back_populates='daily_tasks')
    

    

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)