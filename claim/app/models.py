from sqlmodel import SQLModel, Field
from typing import Optional

class ProcedureData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
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
