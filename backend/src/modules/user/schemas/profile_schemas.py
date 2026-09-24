from pydantic import BaseModel
import uuid



class TeacherProfile(BaseModel):
    id: uuid.UUID
    