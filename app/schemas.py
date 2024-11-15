from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EmployeeCreate(BaseModel):
    employee_id: str
    name: str
    email: str
    department: str
    photo: str  # base64 string or path to image


class AttendanceLog(BaseModel):
    employee_id: str
    action: str  # 'check_in' or 'check_out'


class AttendanceResponse(BaseModel):
    message: str
    time: datetime
