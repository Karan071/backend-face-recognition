from fastapi import APIRouter, File, UploadFile
from app.services import register_employee
from app.schemas import EmployeeCreate

router = APIRouter()

@router.post("/register")
async def register_employee_route(employee: EmployeeCreate, photo: UploadFile = File(...)):
    # Save the uploaded file (image)
    photo_path = f"/static/{photo.filename}"  # For simplicity, we're storing the filename
    return await register_employee(
        employee.employee_id, employee.name, employee.email, employee.department, photo_path
    )
