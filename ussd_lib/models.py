from typing import List, Optional, Union
from pydantic import BaseModel


class MenuOption(BaseModel):
    type: str
    response: Optional[str]
    next_menu_level: Optional[Union[int, str, None]]
    action: Optional[str]


class MenuLevel(BaseModel):
    id: Union[int, str]
    menu_level: Union[int, str]
    text: str
    menu_options: List[MenuOption]
    max_selections: Union[int, str]
    action: Optional[str] = None


class USSDSession(BaseModel):
    id: str
    session_id: str
    service_code: str
    phone_number: str
    text: str
    previous_menu_level: Union[int, str]
    current_menu_level: Union[int, str]


class IngressData(BaseModel):
    session_id: str
    service_code: str
    phone_number: str
    text: str
    network_code: str
