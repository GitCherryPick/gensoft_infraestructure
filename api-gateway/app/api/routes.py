from fastapi import APIRouter, HTTPException
import httpx
import os

router = APIRouter()
USER_MANAGEMENT_URL = os.getenv("USER_MANAGEMENT_URL", "http://user-management-service:8006")  # Valor por defecto

async def make_request(method: str, endpoint: str, **kwargs):
    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.request(
                method,
                f"{USER_MANAGEMENT_URL}{endpoint}",
                **kwargs
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Error from user service: {e.response.text}"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"User service unavailable: {str(e)}"
        )

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    return await make_request("GET", f"/users/{user_id}")

@router.get("/institutions/{institution_id}")
async def get_institution(institution_id: int):
    return await make_request("GET", f"/institutions/{institution_id}")

@router.post("/student_transfers")
async def create_student_transfer(transfer_data: dict):
    return await make_request("POST", "/student_transfers", json=transfer_data)

@router.get("/student_transfers/{transfer_id}")
async def get_student_transfer(transfer_id: int):
    return await make_request("GET", f"/student_transfers/{transfer_id}")

@router.delete("/users/{user_username}")
async def delete_user(user_username: str):
    return await make_request("DELETE", f"/users/{user_username}")

@router.post("/users/")
async def create_user(user_data: dict):
    return await make_request("POST", "/users/", json=user_data)