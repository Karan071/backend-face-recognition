from fastapi import FastAPI
from app.api import employee, attendance
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

# Registering the routes
app.include_router(employee.router)
app.include_router(attendance.router)

# Register Tortoise ORM
register_tortoise(
    app,
    db_url="postgres://user:password@localhost:5432/attendance_db",  # Example for PostgreSQL
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
