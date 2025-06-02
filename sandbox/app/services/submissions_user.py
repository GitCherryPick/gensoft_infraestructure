from typing import List
from fastapi import HTTPException
import httpx

USER_MANAGEMENT_URL = "http://user-management-service:8006"

async def get_usernames_batch(user_ids: List[int]):
    """
    Get the username for a given user ID from the user management service.
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(f"{USER_MANAGEMENT_URL}/users/batch_users", json=user_ids)
            response.raise_for_status()
            user_data = response.json()
            return {user["id"]: user["name"] for user in user_data}
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail=f"Cannot connect to User Management Service at {USER_MANAGEMENT_URL}"
        )
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Request to User Management Service timed out"
        )
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500,
            detail=f"User Management Service error: {str(e)}"
        )
    except Exception as e:
        print("error in get_usernames_batch:", e)
        return {}