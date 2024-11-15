import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgres://user:password@localhost:5432/attendance_db")
