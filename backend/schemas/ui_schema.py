from pydantic import BaseModel
from typing import List


class Component(BaseModel):
    type: str
    purpose: str


class Section(BaseModel):
    name: str
    purpose: str
    components_in_section: List[Component]


class UIStructure(BaseModel):
    page_name: str
    layout_type: str
    sections: List[Section]
    components: List[Component]