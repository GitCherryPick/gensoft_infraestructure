from fastapi import APIRouter
import httpx
import os

router = APIRouter()

USER_MANAGEMENT_URL = os.getenv("USER_MANAGEMENT_URL")

@router.get("/institutions/{institution_id}")
async def get_institution(institution_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_MANAGEMENT_URL}/{institution_id}")
        return response.json()