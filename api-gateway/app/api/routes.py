from fastapi import APIRouter, HTTPException
import httpx
import os

router = APIRouter()

USER_MANAGEMENT_URL = os.getenv("USER_MANAGEMENT_URL")

@router.get("/institutions/{institution_id}")
async def get_institution(institution_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_MANAGEMENT_URL}/{institution_id}")
        return response.json()
    
@router.get("/users/{user_id}")
async def get_user(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_MANAGEMENT_URL}/{user_id}")
        return response.json()

@router.post("/student_transfers")
async def create_student_transfer(transfer_data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{USER_MANAGEMENT_URL}/student_transfers", json=transfer_data)
        return response.json()

@router.get("/student_transfers/{transfer_id}")
async def get_student_transfer(transfer_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_MANAGEMENT_URL}/student_transfers/{transfer_id}")
        return response.json()

@router.delete("/users/{user_username}")
async def delete_user(user_username: str):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{USER_MANAGEMENT_URL}/users/{user_username}")
        return response.json()

@router.post("/users")
async def create_user(user_data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{USER_MANAGEMENT_URL}/users", json=user_data)
        
        try:
            return response.json()
        except Exception:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Invalid JSON response: {response}"
            )