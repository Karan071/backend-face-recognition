from fastapi import APIRouter, UploadFile, File
from app.services import capture_attendance, log_attendance
from app.schemas import AttendanceLog

router = APIRouter()

@router.post("/capture")
async def capture_attendance_route(photo: UploadFile = File(...)):
    # Save the uploaded photo temporarily
    photo_path = f"/static/{photo.filename}"
    return await capture_attendance(photo_path)


@router.post("/log")
async def log_attendance_route(attendance: AttendanceLog):
    return await log_attendance(attendance.employee_id, attendance.action)
