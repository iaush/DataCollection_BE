from typing import Optional, List
from pydantic import BaseModel, validator
import html


#defination of the classes for server side validation of the request body
class UserCreate(BaseModel):
    email: str
    password: str
    contact_num : Optional[int] = None
    company : Optional[str] = None
    name : Optional[str] = None
    is_member : Optional[bool] = False
    role : Optional[str] = None

    
    @validator('*', pre=True)
    def escape_html(cls, value):
        if isinstance(value, str):
            return html.escape(value)
        return value
    
class UserResponse(BaseModel):
    email: str
    company: Optional[str]
    is_member: Optional[bool]
    number : Optional[str]
    # contact_num: Optional[str]
    name: Optional[str]
    role: Optional[str]

    @validator('*', pre=True)
    def escape_html(cls, value):
        if isinstance(value, str):
            return html.escape(value)
        return value


class LoginRequest(BaseModel):
    username: str
    password: str