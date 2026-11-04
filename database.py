from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String)
    first_name = Column(String, default="Атлет")
    gender = Column(String)
    age = Column(Integer)
    weight = Column(Float)
    target_weight = Column(Float)
    height = Column(Float)
    goal = Column(String)
    activity = Column(String)
    fitness_level = Column(String)
    diet_type = Column(String, default="Обычное")
    injuries = Column(String, default="Нет")
    workout_location = Column(String, default="Зал")
    time_per_workout = Column(String, default="60 мин")
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    rank = Column(String, default="🥚 Новичок")
    streak = Column(Integer, default=1)
    last_active = Column(DateTime, default=datetime.datetime.utcnow)
    workouts_done = Column(Integer, default=0)
    challenges_done = Column(Integer, default=0)
    water_today = Column(Integer, default=0)
    referred_by = Column(Integer, default=0)
    referrals_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    weight_logs = relationship("WeightLog", back_populates="user")

class WeightLog(Base):
    __tablename__ = 'weight_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    weight = Column(Float)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship("User", back_populates="weight_logs")

engine = create_async_engine('sqlite+aiosqlite:///bot.db', echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        cols = [
            ("first_name", "VARCHAR DEFAULT 'Атлет'"),
            ("diet_type", "VARCHAR DEFAULT 'Обычное'"),
            ("injuries", "VARCHAR DEFAULT 'Нет'"),
            ("workout_location", "VARCHAR DEFAULT 'Зал'"),
            ("time_per_workout", "VARCHAR DEFAULT '60 мин'"),
            ("rank", "VARCHAR DEFAULT '🥚 Новичок'"),
            ("last_active", "DATETIME"),
            ("workouts_done", "INTEGER DEFAULT 0"),
            ("challenges_done", "INTEGER DEFAULT 0"),
            ("water_today", "INTEGER DEFAULT 0"),
            ("referred_by", "INTEGER DEFAULT 0"),
            ("referrals_count", "INTEGER DEFAULT 0"),
        ]
        for col, typ in cols:
            try:
                await conn.execute(text(f"ALTER TABLE users ADD COLUMN {col} {typ}"))
            except Exception:
                pass

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

async def get_user(telegram_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT * FROM users WHERE telegram_id = :tid"), {"tid": telegram_id})
        return result.fetchone()

async def create_or_update_user(data: dict):
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT * FROM users WHERE telegram_id = :tid"), {"tid": data['telegram_id']})
        user = result.fetchone()
        if user:
            await session.execute(
                text("""UPDATE users SET gender=:g, age=:a, weight=:w, target_weight=:tw, height=:h, goal=:gl, 
                        activity=:act, fitness_level=:fl, diet_type=:dt, injuries=:inj, workout_location=:wl, 
                        time_per_workout=:tpw, first_name=:fn WHERE telegram_id=:tid"""),
                {"g": data['gender'], "a": data['age'], "w": data['weight'], "tw": data['target_weight'], 
                 "h": data['height'], "gl": data['goal'], "act": data['activity'], "fl": data['fitness_level'],
                 "dt": data.get('diet_type', 'Обычное'), "inj": data.get('injuries', 'Нет'), 
                 "wl": data.get('workout_location', 'Зал'), "tpw": data.get('time_per_workout', '60 мин'),
                 "fn": data.get('first_name', 'Атлет'), "tid": data['telegram_id']}
            )
        else:
            await session.execute(
                text("""INSERT INTO users (telegram_id, username, first_name, gender, age, weight, target_weight, height, goal, activity, fitness_level, diet_type, injuries, workout_location, time_per_workout, referred_by)
                        VALUES (:tid, :un, :fn, :g, :a, :w, :tw, :h, :gl, :act, :fl, :dt, :inj, :wl, :tpw, :ref)"""),
                {"tid": data['telegram_id'], "un": data.get('username', ''), "fn": data.get('first_name', 'Атлет'),
                 "g": data['gender'], "a": data['age'], "w": data['weight'], "tw": data['target_weight'], 
                 "h": data['height'], "gl": data['goal'], "act": data['activity'], "fl": data['fitness_level'], 
                 "dt": data.get('diet_type', 'Обычное'), "inj": data.get('injuries', 'Нет'), 
                 "wl": data.get('workout_location', 'Зал'), "tpw": data.get('time_per_workout', '60 мин'),
                 "ref": data.get('referred_by', 0)}
            )
        await session.commit()

def calculate_rank(level):
    if level >= 50: return "👑 Легенда"
    if level >= 30: return "⚡ Титан"
    if level >= 15: return "🔥 Берсерк"
    if level >= 7: return "⚔️ Воин"
    if level >= 3: return "🛡 Боец"
    return "🥚 Новичок"

async def add_xp(telegram_id: int, amount: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT xp, level, rank FROM users WHERE telegram_id = :tid"), {"tid": telegram_id})
        user = result.fetchone()
        if user:
            new_xp = user.xp + amount
            new_level = (new_xp // 500) + 1
            new_rank = calculate_rank(new_level)
            await session.execute(
                text("UPDATE users SET xp = :xp, level = :lvl, rank = :rk WHERE telegram_id = :tid"),
                {"xp": new_xp, "lvl": new_level, "rk": new_rank, "tid": telegram_id}
            )
            await session.commit()

async def add_water(telegram_id: int, ml: int):
    async with AsyncSessionLocal() as session:
        await session.execute(text("UPDATE users SET water_today = water_today + :ml WHERE telegram_id = :tid"), {"ml": ml, "tid": telegram_id})
        await session.commit()

async def reset_water(telegram_id: int):
    async with AsyncSessionLocal() as session:
        await session.execute(text("UPDATE users SET water_today = 0 WHERE telegram_id = :tid"), {"tid": telegram_id})
        await session.commit()

async def increment_stat(telegram_id: int, field: str):
    async with AsyncSessionLocal() as session:
        await session.execute(text(f"UPDATE users SET {field} = {field} + 1 WHERE telegram_id = :tid"), {"tid": telegram_id})
        await session.commit()

async def get_top_users(limit=15):
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT username, first_name, level, xp, rank FROM users ORDER BY xp DESC LIMIT :l"), {"l": limit})
        return result.fetchall()

async def add_weight_log(telegram_id: int, weight: float):
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT id FROM users WHERE telegram_id = :tid"), {"tid": telegram_id})
        user = result.fetchone()
        if user:
            await session.execute(text("INSERT INTO weight_logs (user_id, weight) VALUES (:uid, :w)"), {"uid": user.id, "w": weight})
            await session.execute(text("UPDATE users SET weight = :w WHERE id = :uid"), {"w": weight, "uid": user.id})
            await session.commit()

async def get_weight_logs(telegram_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text("""SELECT w.weight, w.date FROM weight_logs w 
                    JOIN users u ON u.id = w.user_id 
                    WHERE u.telegram_id = :tid ORDER BY w.date ASC"""),
            {"tid": telegram_id}
        )
        return result.fetchall()
