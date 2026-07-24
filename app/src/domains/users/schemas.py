from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    username: str = Field(description="The full name of the user")
    email: EmailStr = Field(description="The email of the user")

class UserCreate(UserBase):
    password: str = Field(description="The password of the user")

class UserResponse(UserBase):
    id: int = Field(description="The unique identifier of the user")

    model_config = {
        "from_attributes": True}
    
    