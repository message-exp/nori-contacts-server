from pydantic import BaseModel


class ContactCardResponse(BaseModel):
    contact_name: str
    contact_avatar_url: str | None = None


class ContactCardCreate(BaseModel):
    contact_name: str
    contact_avatar_url: str | None = None
