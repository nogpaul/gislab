import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
url = f"postgresql+psycopg://{os.getenv('PGUSER')}:{os.getenv('PGPASSWORD')}@{os.getenv('PGHOST')}:{os.getenv('PGPORT')}/{os.getenv('PGDATABASE')}"

engine = create_engine(url, future=True)

with engine.connect() as conn:
    print(conn.execute(text("SELECT version();")).scalar())
    print(conn.execute(text("SELECT PostGIS_Full_Version();")).scalar())
