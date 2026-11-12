from typing import Optional
from pydantic import BaseModel, ConfigDict

class Payload(BaseModel):
    model_config = ConfigDict(extra='allow')
    title:Optional[str]=None
    status:Optional[str]=None
    notes:Optional[str]=None
    assigned_to:Optional[str]=None
    severity:Optional[str]=None
    tunnel:Optional[str]=None
    message:Optional[str]=None
    category:Optional[str]=None
    description:Optional[str]=None
    priority:Optional[str]=None
    reporter:Optional[str]=None
    item:Optional[str]=None
    responsible:Optional[str]=None
    due_date:Optional[str]=None
    read:Optional[bool]=None
    inspector:Optional[str]=None
    scheduled:Optional[str]=None
    observations:Optional[str]=None
    findings:Optional[str]=None
    checklist:Optional[str]=None
    threshold:Optional[float]=None
