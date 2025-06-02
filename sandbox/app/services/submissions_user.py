from datetime import datetime
from typing import List
from fastapi import HTTPException
import httpx
from sqlalchemy.orm import Session
from sandbox.app.model.submissions import Submission

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
    
async def get_students_of_course(task_id: int):
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{USER_MANAGEMENT_URL}/users/")
            response.raise_for_status()
            user_data = response.json()
            return user_data
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
        print("error in get_students_of_course:", e)
        return {}
    
async def generate_missing_submissions(task_id: int, db: Session):
    students = await get_students_of_course(task_id) #mejora
    
    existing_submissions = db.query(Submission).filter(
        Submission.task_id == task_id
    ).all()
    existing_user_ids = {sub.user_id for sub in existing_submissions}

    new_submissions = []
    for student in students:
        if student["id"] not in existing_user_ids:
            sub = Submission(
                user_id=student["id"],
                task_id=task_id,
                tipo_problema="task",
                score=0.0,
                status="No entregado",
                is_auto_generated=True,
                submission_date=datetime.utcnow()
            )
            new_submissions.append(sub)

    db.add_all(new_submissions)
    db.commit()
    return {"message": f"Created {len(new_submissions)} missing submissions"}