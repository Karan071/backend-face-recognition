from tortoise import fields
from tortoise.models import Model

class Employee(Model):
    id = fields.IntField(pk=True)
    employee_id = fields.CharField(max_length=50, unique=True)
    name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255)
    department = fields.CharField(max_length=255)
    face_embedding = fields.BinaryField()
    photo_url = fields.CharField(max_length=255)

    def __str__(self):
        return self.name


class Attendance(Model):
    id = fields.IntField(pk=True)
    employee = fields.ForeignKeyField("models.Employee", related_name="attendances")
    check_in = fields.DatetimeField(null=True)
    check_out = fields.DatetimeField(null=True)

    def __str__(self):
        return f"Attendance for {self.employee.name}"
