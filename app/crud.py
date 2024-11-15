from app.models import Employee, Attendance
from tortoise.exceptions import DoesNotExist


async def create_employee(employee_id: str, name: str, email: str, department: str, face_embedding: bytes, photo_url: str):
    try:
        employee = await Employee.create(
            employee_id=employee_id,
            name=name,
            email=email,
            department=department,
            face_embedding=face_embedding,
            photo_url=photo_url
        )
        return employee
    except Exception as e:
        raise Exception(f"Error creating employee: {e}")


async def get_employee_by_id(employee_id: str):
    try:
        return await Employee.get(employee_id=employee_id)
    except DoesNotExist:
        return None
