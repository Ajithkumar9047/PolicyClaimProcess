from fastapi import Body, FastAPI, Depends, HTTPException, Request
from sqlmodel import Session, select
import uuid
from sqlalchemy.sql import func
from typing import List, AsyncGenerator

from app.models import ProcedureData
from app.schemas import ProcedureDataRequest, ProcedureDataResponse
from app.database import create_db_and_tables, get_session
from app.rate_limiter import RateLimitMiddleware

app = FastAPI()

async def lifespan(app: FastAPI) -> AsyncGenerator:
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# Add rate limiting middleware
app.add_middleware(RateLimitMiddleware, max_requests=10, window_seconds=60)

# Endpoint to handle POST requests and save data to the database
@app.post("/submit-data")
async def submit_data(data: List[ProcedureDataRequest] = Body(...), session: Session = Depends(get_session)):
    claim_id = str(uuid.uuid4())

    try:
        for index, item in enumerate(data):
            # Early validation for missing fields
            missing_fields = []
            if not item.provider_fees:
                missing_fields.append("provider_fees")
            if not item.allowed_fees:
                missing_fields.append("allowed_fees")
            if not item.member_coinsurance:
                missing_fields.append("member_coinsurance")
            if not item.member_copay:
                missing_fields.append("member_copay")

            if missing_fields:
                raise HTTPException(
                    status_code=422,
                    detail=f"Missing required fields in data item {index + 1}: {', '.join(missing_fields)}"
                )

            # Validation for monetary format with field identification
            try:
                provider_fees = float(item.provider_fees.replace('$', '').replace(',', ''))
            except ValueError as e:
                data_item_info = f"Data item {index + 1} ({item.submitted_procedure} - {item.service_date})"
                raise HTTPException(
                    status_code=422,
                    detail=f"Invalid value or type for 'provider_fees' in {data_item_info}."
                ) from e

            try:
                allowed_fees = float(item.allowed_fees.replace('$', '').replace(',', ''))
            except ValueError as e:
                data_item_info = f"Data item {index + 1} ({item.submitted_procedure} - {item.service_date})"
                raise HTTPException(
                    status_code=422,
                    detail=f"Invalid value or type for 'allowed_fees' in {data_item_info}."
                ) from e

            try:
                member_coinsurance = float(item.member_coinsurance.replace('$', '').replace(',', ''))
            except ValueError as e:
                data_item_info = f"Data item {index + 1} ({item.submitted_procedure} - {item.service_date})"
                raise HTTPException(
                    status_code=422,
                    detail=f"Invalid value or type for 'member_coinsurance' in {data_item_info}."
                ) from e

            try:
                member_copay = float(item.member_copay.replace('$', '').replace(',', ''))
            except ValueError as e:
                data_item_info = f"Data item {index + 1} ({item.submitted_procedure} - {item.service_date})"
                raise HTTPException(
                    status_code=422,
                    detail=f"Invalid value or type for 'member_copay' in {data_item_info}."
                ) from e

            net_fee = provider_fees + member_coinsurance + member_copay - allowed_fees

            procedure_data = ProcedureData(
                claim_id=claim_id,
                service_date=item.service_date,
                submitted_procedure=item.submitted_procedure,
                quadrant=item.quadrant,
                plan_group=item.plan_group,
                subscriber=item.subscriber,
                provider_npi=item.provider_npi,
                provider_fees=provider_fees,
                allowed_fees=allowed_fees,
                member_coinsurance=member_coinsurance,
                member_copay=member_copay,
                net_fee=net_fee
            )
            session.add(procedure_data)

        session.commit()
        return {"message": "Data successfully saved"}

    except HTTPException as e:
        # Handle specific validation error (missing fields or invalid format)
        return e
    except Exception as e:
        # Catch unexpected errors for better debugging
        return HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Endpoint to handle GET requests and retrieve data from the database
@app.get("/get-data", response_model=List[ProcedureDataResponse])
def get_data(session: Session = Depends(get_session)):
    procedures = session.exec(select(ProcedureData)).all()
    return procedures

# Endpoint to handle PUT requests and update data in the database
@app.put("/update-data/{procedure_id}")
def update_data(procedure_id: int, data: ProcedureDataRequest, session: Session = Depends(get_session)):
    procedure = session.get(ProcedureData, procedure_id)
    if not procedure:
        raise HTTPException(status_code=404, detail="Procedure not found")
    
    provider_fees = float(data.provider_fees.replace('$', '').replace(',', ''))
    allowed_fees = float(data.allowed_fees.replace('$', '').replace(',', ''))
    member_coinsurance = float(data.member_coinsurance.replace('$', '').replace(',', ''))
    member_copay = float(data.member_copay.replace('$', '').replace(',', ''))
    net_fee = provider_fees + member_coinsurance + member_copay - allowed_fees

    procedure.service_date = data.service_date
    procedure.submitted_procedure = data.submitted_procedure
    procedure.quadrant = data.quadrant
    procedure.plan_group = data.plan_group
    procedure.subscriber = data.subscriber
    procedure.provider_npi = data.provider_npi
    procedure.provider_fees = provider_fees
    procedure.allowed_fees = allowed_fees
    procedure.member_coinsurance = member_coinsurance
    procedure.member_copay = member_copay
    procedure.net_fee = net_fee

    session.add(procedure)
    session.commit()
    return {"message": "Data successfully updated"}

# Endpoint to handle DELETE requests and delete data from the database
@app.delete("/delete-data/{procedure_id}")
def delete_data(procedure_id: int, session: Session = Depends(get_session)):
    procedure = session.get(ProcedureData, procedure_id)
    if not procedure:
        raise HTTPException(status_code=404, detail="Procedure not found")

    session.delete(procedure)
    session.commit()
    return {"message": "Data successfully deleted"}

# Endpoint to get top 10 provider NPIs by net fees
@app.get("/top-providers", response_model=List[str])
def top_providers(session: Session = Depends(get_session)):
    stmt = select(ProcedureData.provider_npi, func.sum(ProcedureData.net_fee).label('total_net_fee')).group_by(ProcedureData.provider_npi).order_by(func.sum(ProcedureData.net_fee).desc()).limit(10)
    results = session.exec(stmt).all()
    top_providers = [result[0] for result in results]
    return top_providers

# Run the app with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
