
from pydantic import BaseModel

class User(BaseModel):
    id: str or None
    username: str
    email: str