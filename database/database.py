import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import pytz

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"), echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class Registro(Base):
    __tablename__ = "registros"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, index=True, nullable=False)
    usuario = Column(String, nullable=False)
    nome = Column(String, nullable=True)
    entrada = Column(DateTime, nullable=False)
    saida = Column(DateTime, nullable=True)
    observacao = Column(Text, nullable=True)

Base.metadata.create_all(bind=engine)

def agora():
    tz = pytz.timezone(os.getenv("TIMEZONE"))
    return datetime.now(tz).replace(tzinfo=None)

def formatar_dt(dt):
    if not dt:
        return "-", "-"
    return dt.strftime("%d/%m/%Y"), dt.strftime("%H:%M:%S")

def formatar_duracao(delta):
    total_segundos = int(delta.total_seconds())
    h, rem = divmod(total_segundos, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def formatar_segundos(total_segundos):
    h, rem = divmod(total_segundos, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"