from typing import Annotated, Literal
from pydantic import BaseModel, Field, field_validator
from datetime import date


class TeacherApplicationCreate(BaseModel):
    teaching_since: Annotated[int, Field(ge=1000, le=9999)]
    degree: Literal["BACHELOR", "MASTER", "PHD"]
    field_of_study: str
    
    @field_validator("teaching_since", mode="after")
    @classmethod
    def validate_teaching_since(cls, value: int) -> int:
        current_year = date.today().year

        if value < current_year - 70:
            raise ValueError("The teaching start year is not reasonable.")

        if value > current_year - 1:
            raise ValueError("At least one year of experience is required.")

        return value