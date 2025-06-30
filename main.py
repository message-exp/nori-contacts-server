from typing import Union
from enum import Enum
from pydantic import BaseModel

from fastapi import FastAPI

app = FastAPI()


class NetworkType(str, Enum):
    """
    Enum representing different types of networks.
    """

    TELEGRAM = "Telegram"
    DISCORD = "Discord"


class Network(BaseModel):
    """
    Represents a network that a contact can be associated with.
    """

    network: NetworkType
    """ The type of network, e.g., Telegram, Discord """

    user_id: str
    """ The user_id of the contact in the network, e.g., Telegram user ID, Discord user ID, etc. """


class Contact(BaseModel):
    """
    Represents a contact in the system.
    """

    owner_user_id: str
    """ The owner of the contact """

    name: str
    """ The name of the contact """

    avatar: Union[str, None] = None
    """ The avatar of the contact (TODO) """

    networks: Union[list[Network], None] = None
    """ A list of networks the contact is associated with, e.g., Telegram, Discord, etc. """


contacts = []


@app.get("/")
def get_contacts():
    """
    Returns all contacts that belong to the user.
    """
    return {"contacts": ["Alice", "Bob", "Charlie"]}


@app.post("/")
def new_contact(contact: Contact):
    """
    Create a new contact.
    """
    return {"contact": contact}


@app.put("/{contact_id}")
def update_contact(contact_id: int, contact: Contact):
    """
    Update an existing contact.
    """
    return {"contact_id": contact_id, "contact": contact}


@app.delete("/{contact_id}")
def delete_contact(contact_id: int):
    """
    Delete a contact.
    """
    return {"contact_id": contact_id}
