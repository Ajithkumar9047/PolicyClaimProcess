from datetime import date
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

from sqlmodel import Field

class ProcedureDataRequest(BaseModel):
    service_date: Optional[datetime] = Field(default_factory=datetime.now)
    submitted_procedure:  Optional[str]= Field(default=None)
    quadrant: Optional[str]= Field(default=None)
    plan_group: Optional[str]= Field(default=None)
    subscriber:  Optional[str]= Field(default=None)
    provider_npi: str
    provider_fees: str
    allowed_fees: str
    member_coinsurance: str
    member_copay: str

class ProcedureDataResponse(BaseModel):
    id: int
    claim_id: str
    service_date: str
    submitted_procedure: str
    quadrant: Optional[str]
    plan_group: str
    subscriber: str
    provider_npi: str
    provider_fees: float
    allowed_fees: float
    member_coinsurance: float
    member_copay: float
    net_fee: float
    
    
    
