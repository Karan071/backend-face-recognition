from app.models import Employee, Attendance
from datetime import datetime
from app.face_recognition import generate_face_embedding, compare_faces
from fastapi import HTTPException

async def register_employee(employee_id: str, name: str, email: str, department: str, photo: str):
    # Generate face embedding from the photo (this should be a base64 string)
    try:
        face_embedding = generate_face_embedding(photo)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error generating face embedding")

    employee = await Employee.create(
        employee_id=employee_id,
        name=name,
        email=email,
        department=department,
        face_embedding=face_embedding,
        photo_url=f"/static/{photo}",  # Just storing the path for now
    )
    return {"message": "Employee registered successfully"}


async def capture_attendance(photo: str):
    # Generate the face embedding from the uploaded photo
    try:
        captured_embedding = generate_face_embedding(photo)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error generating face embedding")

    # Compare the captured embedding with stored embeddings
    employees = await Employee.all()
    for employee in employees:
        similarity = compare_faces(captured_embedding, employee.face_embedding)
        if similarity >= 0.9:  # Assume 90% match threshold
            return await log_attendance(employee)
    
    raise HTTPException(status_code=400, detail="Face not recognized")


async def log_attendance(employee: Employee, action: str):
    current_time = datetime.utcnow()

    if action == "check_in":
        existing_attendance = await Attendance.filter(employee=employee).filter(check_in__isnull=False).first()
        if existing_attendance:
            raise HTTPException(status_code=400, detail="Employee already checked in")
        
        await Attendance.create(employee=employee, check_in=current_time)
        return {"message": "Check-in successful", "time": current_time}
    
    elif action == "check_out":
        attendance = await Attendance.filter(employee=employee).filter(check_in__isnull=False, check_out__isnull=True).first()
        if not attendance:
            raise HTTPException(status_code=400, detail="Employee has not checked in")

        attendance.check_out = current_time
        await attendance.save()
        return {"message": "Check-out successful", "time": current_time}
    
    else:
        raise HTTPException(status_code=400, detail="Invalid action")
