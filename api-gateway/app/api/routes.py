from fastapi import Query,APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Request, Response 
import httpx
import os
from typing import Optional
from fastapi.responses import StreamingResponse, JSONResponse

router = APIRouter()

# Service URLs with defaults
SERVICES = {
    "user": os.getenv("USER_MANAGEMENT_URL", "http://user-management-service:8000"),
    "content": os.getenv("CONTENT_MANAGEMENT_URL", "http://content-management-service:8003"),
    "sandbox": os.getenv("SANDBOX_URL", "http://sandbox:8002"),
    "ai": os.getenv("AI_ASSISTANCE_URL", "http://ai-assistance-service:8005")
}

async def call_service(
    service_name: str,
    method: str,
    endpoint: str,
    data: Optional[dict] = None,
    params: Optional[dict] = None,
    files: Optional[dict] = None,
    stream: bool = False
):
    """
    Generic function to call any microservice
    """
    if service_name not in SERVICES:
        raise HTTPException(
            status_code=500,
            detail=f"Unknown service: {service_name}"
        )
    
    url = f"{SERVICES[service_name]}{endpoint}"
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(
                method,
                url,
                json=None if files else data,  #
                data=data if files else None,  #
                files=files,
                params=params
            )
            response.raise_for_status()
            if stream:
                return response
            return response.json()
            
    except httpx.HTTPStatusError as e:
        detail = f"Error from {service_name} service: {e.response.text}"
        raise HTTPException(
            status_code=e.response.status_code,
            detail=detail
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"{service_name.capitalize()} service unavailable: {str(e)}"
        )

@router.get("/storage/{path:path}")
async def get_static_file(path: str):
    """
    Proxy endpoint for static files from content service
    """
    try:
        response = await call_service(
            "content",
            "GET",
            f"/storage/{path}",
            stream=True
        )
       
        return StreamingResponse(
            content=response.aiter_bytes(),
            status_code=response.status_code,
            media_type=response.headers.get("content-type"),
            headers=dict(response.headers)
        )
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"File not found: {str(e)}"
        )


# User Management Endpoints
# User Management Endpoints
# User Management Endpoints

@router.get("/users/")
async def get_all_users(skip: int = 0, limit: int = 100):
    return await call_service("user", "GET", "/users/", params={"skip": skip, "limit": limit})

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    return await call_service("user", "GET", f"/users/{user_id}")

@router.post("/student_transfers")
async def create_student_transfer(transfer_data: dict):
    return await call_service("user", "POST", "/student_transfers", data=transfer_data)

@router.get("/student_transfers/{transfer_id}")
async def get_student_transfer(transfer_id: int):
    return await call_service("user", "GET", f"/student_transfers/{transfer_id}")

@router.delete("/users/{user_username}")
async def delete_user(user_username: str):
    return await call_service("user", "DELETE", f"/users/{user_username}")

@router.post("/users/")
async def create_user(user_data: dict):
    return await call_service("user", "POST", "/users/", data=user_data)

@router.post("/auth/login")
async def login(login_data: dict):
    try:
        response = await call_service("user", "POST", "/auth/login", data=login_data)
        return JSONResponse(
            content=response,
            headers={"accept": "application/json"}
        )
    except HTTPException as e:
        return JSONResponse(
            content={"detail": str(e.detail)},
            status_code=e.status_code,
            headers={"accept": "application/json"}
        )

# Password Reset Endpoints
@router.post("/auth/password-reset/request")
async def request_password_reset(reset_request: dict):
   return await call_service("user", "POST", "/password-reset/request", data=reset_request)

@router.post("/auth/password-reset/confirm")
async def confirm_password_reset(reset_confirm: dict):
    return await call_service("user", "POST", "/password-reset/confirm", data=reset_confirm)

# institutions
@router.get("/institutions/{institution_id}")
async def get_institution(institution_id: int):
    return await call_service("user", "GET", f"/institutions/{institution_id}")

@router.post("/institutions")
async def create_institution(institution_data: dict):
    return await call_service("user", "POST", "/institutions", data=institution_data)

@router.get("/institutions/")
async def list_institutions(skip: int = 0, limit: int = 10):
    return await call_service("user", "GET", "/institutions", params={"skip": skip, "limit": limit})

@router.put("/institutions/{institution_id}")
async def update_institution(institution_id: int, institution_data: dict):
    return await call_service("user", "PUT", f"/institutions/{institution_id}", data=institution_data)

@router.delete("/institutions/{institution_id}")
async def delete_institution(institution_id: int):
    return await call_service("user", "DELETE", f"/institutions/{institution_id}")

# Content Management Endpoints
# Content Management Endpoints
# Content Management Endpoints

@router.get("/contents/{content_id}")
async def get_content(content_id: int):
    return await call_service("content", "GET", f"/contents/{content_id}")

@router.post("/contents/")
async def create_content(content_data: dict):
    return await call_service("content", "POST", "/contents/", data=content_data)

@router.get("/contents/")
async def get_contents(skip: int = 0, limit: int = 100):
    return await call_service("content", "GET", "/contents/", params={"skip": skip, "limit": limit})

@router.get("/contents/module/{module_id}")
async def get_contents_by_module(module_id: int):
    return await call_service("content", "GET", f"/contents/module/{module_id}")

@router.get("/contents/module/{module_id}/type/{content_type}")
async def get_module_contents_by_type(module_id: int, content_type: str):
    return await call_service("content", "GET", f"/contents/module/{module_id}/type/{content_type}")

@router.put("/contents/{content_id}")
async def update_content(content_id: int, content_data: dict):
    return await call_service("content", "PUT", f"/contents/{content_id}", data=content_data)

@router.delete("/contents/{content_id}")
async def delete_content(content_id: int):
    return await call_service("content", "DELETE", f"/contents/{content_id}")

@router.post("/contents/text")
async def create_text_content(content_data: dict):
    return await call_service("content", "POST", "/contents/text", data=content_data)

@router.post("/contents/url")
async def create_url_content(content_data: dict):
    return await call_service("content", "POST", "/contents/url", data=content_data)

@router.post("/contents/upload/pdf")
async def upload_pdf_content(
    file: UploadFile = File(...),
    module_id: int = Form(...),
    title: Optional[str] = Form(None)
):
    files = {"file": (file.filename, file.file, file.content_type)}
    data = {"module_id": module_id, "title": title}
    return await call_service("content", "POST", "/contents/upload/pdf", files=files, data=data)

@router.post("/contents/upload/image")
async def upload_image_content(
    file: UploadFile = File(...),
    module_id: int = Form(...),
    title: Optional[str] = Form(None)
):
    files = {"file": (file.filename, file.file, file.content_type)}
    data = {"module_id": module_id, "title": title}
    return await call_service("content", "POST", "/contents/upload/image", files=files, data=data)

@router.post("/contents/upload/video")
async def upload_video_content(
    file: UploadFile = File(...),
    module_id: int = Form(...),
    title: Optional[str] = Form(None)
):
    files = {"file": (file.filename, file.file, file.content_type)}
    data = {"module_id": module_id, "title": title}
    return await call_service("content", "POST", "/contents/upload/video", files=files, data=data)

@router.post("/contents/upload/slide")
async def upload_slide_content(
    file: UploadFile = File(...),
    module_id: int = Form(...),
    title: Optional[str] = Form(None)
):
    files = {"file": (file.filename, file.file, file.content_type)}
    data = {"module_id": module_id, "title": title}
    return await call_service("content", "POST", "/contents/upload/slide", files=files, data=data)

@router.get("/contents/types")
async def get_content_types():
    return await call_service("content", "GET", "/content-types")

# Exercise Endpoints (Content Management)
@router.post("/exercises/")
async def create_exercise(exercise_data: dict):
    return await call_service("content", "POST", "/exercises/", data=exercise_data)

@router.get("/exercises/")
async def get_exercises():
    return await call_service("content", "GET", "/exercises/")

@router.put("/exercises/{exercise_id}")
async def update_exercise(exercise_id: int, exercise_data: dict):
    return await call_service("content", "PUT", f"/exercises/{exercise_id}", data=exercise_data)

@router.delete("/exercises/{exercise_id}")
async def delete_exercise(exercise_id: int):
    return await call_service("content", "DELETE", f"/exercises/{exercise_id}")

@router.get("/exercises/instructor/{instructor_id}")
async def get_exercises_by_instructor(instructor_id: int):
    return await call_service("content", "GET", f"/exercises/instructor/{instructor_id}")

@router.get("/exercises/last")
async def get_last_exercise():
    return await call_service("content", "GET", "/exercises/last")

@router.get("/exercises/{exercise_id}")
async def get_exercise(exercise_id: int):
    return await call_service("content", "GET", f"/exercises/{exercise_id}")

# Course Endpoints (Content Management)
@router.post("/courses/")
async def create_course(course_data: dict):
    return await call_service("content", "POST", "/courses/", data=course_data)

@router.get("/courses/")
async def get_courses(skip: int = 0, limit: int = 100):
    return await call_service("content", "GET", "/courses/", params={"skip": skip, "limit": limit})

@router.get("/courses/{course_id}")
async def get_course(course_id: int):
    return await call_service("content", "GET", f"/courses/{course_id}")

@router.put("/courses/{course_id}")
async def update_course(course_id: int, course_data: dict):
    return await call_service("content", "PUT", f"/courses/{course_id}", data=course_data)

@router.delete("/courses/{course_id}")
async def delete_course(course_id: int):
    return await call_service("content", "DELETE", f"/courses/{course_id}")

@router.get("/courses/default/id")
async def get_default_course_id():
    return await call_service("content", "GET", "/courses/default/id")

# Module Endpoints (Content Management)
@router.post("/modules/")
async def create_module(module_data: dict):
    return await call_service("content", "POST", "/modules/", data=module_data)

@router.get("/modules/")
async def get_modules(skip: int = 0, limit: int = 100):
    return await call_service("content", "GET", "/modules/", params={"skip": skip, "limit": limit})

@router.get("/modules/course/{course_id}")
async def get_modules_by_course(course_id: int):
    return await call_service("content", "GET", f"/modules/course/{course_id}")

@router.get("/modules/{module_id}")
async def get_module(module_id: int):
    return await call_service("content", "GET", f"/modules/{module_id}")

@router.put("/modules/{module_id}")
async def update_module(module_id: int, module_data: dict):
    return await call_service("content", "PUT", f"/modules/{module_id}", data=module_data)

@router.delete("/modules/{module_id}")
async def delete_module(module_id: int):
    return await call_service("content", "DELETE", f"/modules/{module_id}")

# Module Endpoints (Content Management)
@router.post("/exercises/")
async def create_exercise(exercise_data: dict):
    return await call_service("content", "POST", "/exercises/", data=exercise_data)

# sandbox service
# sandbox service
# sandbox service
# sandbox service
@router.post("/sandbox/run")
async def run_python_code(code_data: dict):
    return await call_service("sandbox", "POST", "/run", data=code_data)

@router.post("/sandbox/execute")
async def execute_python_function(execution_data: dict):
    return await call_service("sandbox", "POST", "/execute", data=execution_data)

# Task Management Endpoints
@router.post("/tasks")
async def create_coding_task(task_data: dict):
    return await call_service("sandbox", "POST", "/tasks", data=task_data)

@router.get("/tasks/getScore")
async def get_score(
    task_id: int = Query(..., description="ID de la tarea"),
    user_id: int = Query(..., description="ID del usuario")
):
    return await call_service(
        "sandbox",
        "GET",
        "/tasks/getScore",
        params={"task_id": task_id, "user_id": user_id}
    )



@router.get("/tasks/{task_id}")
async def get_coding_task(task_id: int):
    return await call_service("sandbox", "GET", f"/tasks/{task_id}")

@router.get("/tasks")
async def list_coding_tasks():
    return await call_service("sandbox", "GET", "/tasks")

@router.put("/tasks/{task_id}")
async def update_coding_task(task_id: int, task_update: dict):
    return await call_service("sandbox", "PUT", f"/tasks/{task_id}", data=task_update)

@router.delete("/tasks/{task_id}")
async def delete_coding_task(task_id: int):
    return await call_service("sandbox", "DELETE", f"/tasks/{task_id}")

# --- Hint Endpoints (Fixed) ---
@router.post("/hints/")
async def create_hint(hint_data: dict):
    """Crea una nueva pista"""
    return await call_service("sandbox", "POST", "/hints/", data=hint_data)

@router.get("/hints/{hint_id}")
async def get_hint(hint_id: int):
    """Obtiene una pista por ID"""
    return await call_service("sandbox", "GET", f"/hints/{hint_id}")

@router.put("/hints/{hint_id}")
async def update_hint(hint_id: int, hint_data: dict):
    """Actualiza una pista existente"""
    return await call_service("sandbox", "PUT", f"/hints/{hint_id}", data=hint_data)

@router.delete("/hints/{hint_id}")
async def delete_hint(hint_id: int):
    """Elimina una pista"""
    return await call_service("sandbox", "DELETE", f"/hints/{hint_id}")

@router.get("/hints/")
async def list_hints():
    """Obtiene todas las pistas"""
    return await call_service("sandbox", "GET", "/hints")
# Submission Endpoints
@router.post("/enviar")
async def submit_solution(submission_data: dict):
    return await call_service("sandbox", "POST", "/enviar", data=submission_data)

# Test Case Management
@router.post("/sandbox/tasks/{task_id}/tests")
async def add_test_case(task_id: int, test_data: dict):
    return await call_service("sandbox", "POST", f"/tasks/{task_id}/tests", data=test_data)

@router.delete("/sandbox/tests/{test_id}")
async def delete_test_case(test_id: int):
    return await call_service("sandbox", "DELETE", f"/tests/{test_id}")

@router.post("/sandbox/taskcode")
async def create_task(task: dict):
    return await call_service("sandbox", "POST", "/taskcode", data=task)

@router.get("/sandbox/taskcode")
async def get_all_tasks(skip: int = 0, limit: int = 100):
    return await call_service("sandbox", "GET", "/taskcode/", params={"skip": skip, "limit": limit})

@router.get("/sandbox/taskcode/{id}")
async def read(id: int):
    return await call_service("sandbox", "GET", f"/taskcode/{id}")

@router.put("/sandbox/taskcode/{id}")
async def update_task(id: int, task: dict):
    return await call_service("sandbox", "PUT", f"/taskcode/{id}", data=task)

@router.delete("/sandbox/taskcode/{id}")
async def delete_task(id: int):
    return await call_service("sandbox", "DELETE", f"/taskcode/{id}")

@router.get("/sandbox/taskcode/{id}/template")
async def get_template(id: int):
    return await call_service("sandbox", "GET", f"/taskcode/{id}/template")

@router.post("/sandbox/codereplicated")
async def submit_code(submission: dict):
    return await call_service("sandbox", "POST", "/codereplicated", data=submission)

@router.post("/sandbox/ai-feedback/replicator")
async def ai_feedback_replicator(input: dict):
    return await call_service("sandbox", "POST", "/ai-feedback/replicator", data=input)

@router.post("/sandbox/ai-feedback/lab")
async def ai_feedback_lab(input: dict):
    return await call_service("sandbox", "POST", "/ai-feedback/lab", data=input)

@router.post("/sandbox/submissions")
async def create_submission(submission_data: dict):
    return await call_service("sandbox", "POST", "/submissions", data=submission_data)

@router.get("/sandbox/submissions")
async def get_all_submissions(skip: int = 0, limit: int = 100):
    return await call_service("sandbox", "GET", "/submissions/", params={"skip": skip, "limit": limit})

@router.get("/sandbox/submissions/{submission_id}")
async def get_with_submission_id(submission_id: int):
    return await call_service("sandbox", "GET", f"/submissions/{submission_id}")

@router.put("/sandbox/submissions/{submission_id}")
async def update_with_submission_id(submission_id: int, submission_data:dict):
    return await call_service("sandbox", "PUT", f"/submissions/{submission_id}", data=submission_data)

@router.delete("/sandbox/submissions/{submission_id}")
async def delete_with_submission_id(submission_id: int):
    return await call_service("sandbox", "DELETE", f"/submissions/{submission_id}")

@router.get("/sandbox/submissions/task/{task_id}")
async def get_submissions_by_task_id(task_id: int):
    return await call_service("sandbox", "GET", f"/submissions/task/{task_id}")

@router.get("/sandbox/submissions/task/{task_id}/{user_id}")
async def get_submissions_by_task_and_user(task_id: int, user_id: int):
    return await call_service("sandbox", "GET", f"/submissions/task/{task_id}/{user_id}")

@router.put("/sandbox/task/{task_id}/close")
async def close_task(task_id: int):
    return await call_service("sandbox", "PUT", f"/task/{task_id}/close")

@router.get("/sandbox/submissions/task/{task_id}/generate-missing-submissions")
async def generate_missing_submissions(task_id: int):
    return await call_service("sandbox", "GET", f"/submissions/task/{task_id}/generate-missing-submissions")

@router.post("/sandbox/ai-feedback/lab-test")
async def feedback_student_in_lab(input: dict):
    return await call_service("sandbox", "POST", "/ai-feedback/lab-test", data=input)

## Replication Submissions Endpoints
@router.post("/replication-submissions/")
async def create_replication_submission(submission_data: dict):
    return await call_service("sandbox", "POST", "/replication-submissions/", data=submission_data)

@router.get("/replication-submissions/")
async def get_all_replication_submissions(skip: int = 0, limit: int = 100):
    return await call_service("sandbox", "GET", "/replication-submissions/", params={"skip": skip, "limit": limit})

@router.get("/replication-submissions/{submission_id}")
async def get_replication_submission(submission_id: int):
    return await call_service("sandbox", "GET", f"/replication-submissions/{submission_id}")

@router.get("/replication-submissions/user/{user_id}")
async def get_replication_submissions_by_user(user_id: int, skip: int = 0, limit: int = 100):
    return await call_service("sandbox", "GET", f"/replication-submissions/user/{user_id}", 
                             params={"skip": skip, "limit": limit})

@router.get("/replication-submissions/user/{user_id}/exercise/{exercise_id}")
async def get_replication_submissions_by_user_and_exercise(user_id: int, exercise_id: int):
    return await call_service("sandbox", "GET", f"/replication-submissions/user/{user_id}/exercise/{exercise_id}")

@router.put("/replication-submissions/{submission_id}")
async def update_replication_submission(submission_id: int, submission_data: dict):
    return await call_service("sandbox", "PUT", f"/replication-submissions/{submission_id}", data=submission_data)

@router.delete("/replication-submissions/{submission_id}")
async def delete_replication_submission(submission_id: int):
    return await call_service("sandbox", "DELETE", f"/replication-submissions/{submission_id}")

# Exams Routes
@router.post("/exams")
async def create_exam(examn_data: dict):
    return await call_service("sandbox", "POST", "/exams", data=examn_data)

@router.get("/exams/last")
async def get_last_exam():
    return await call_service("sandbox", "GET", "/exams/last")

@router.post("/grade/exam")
async def submit_exam(response_data: dict):
    return await call_service("sandbox", "POST", "/grade/exam", data=response_data)

# ai assistance service
@router.post("/ai/ask")
async def ask_ai(question: dict):
    return await call_service("ai", "POST", "/ai/ask", data=question)

@router.post("/ai/ask-feedback/replicator")
async def ask_ai_feedback_replicator(question: dict):
    return await call_service("ai", "POST", "/ai/ask-feedback/replicator", data=question)

@router.get("/ai/saved/{user_id}")
async def get_saved(user_id: str):
    return await call_service("ai", "GET", f"/ai/saved/{user_id}")

@router.post("/ai/chat")
async def chat(input_data: dict):
    return await call_service("ai", "POST", "/ai/chat", data=input_data)

@router.post("/ai/ask-feedback/lab")
async def ask_ai_feedback_labs(question: dict):
    return await call_service("ai", "POST", "/ai/ask-feedback/lab", data=question)

@router.post("/ai/ai-feedaback/lab-test")
async def ask_ai_feedback_labs_test(question: dict):
    return await call_service("ai", "POST", "/ai/ai-feedback/lab-test", data=question)

# Feedback Tasks Endpoints
@router.post("/feedback/exercise")
async def create_feedback_task(task: dict):
    return await call_service("user", "POST", "/feedback/exercise", data=task)

@router.get("/feedback/exercise/{task_id}")
async def get_feedback_task(task_id: int):
    return await call_service("user", "GET", f"/feedback/exercise/{task_id}")

@router.put("/feedback/exercise/{task_id}")
async def update_feedback_task(task_id: int, task:dict):
    return await call_service("user", "PUT", f"/feedback/exercise/{task_id}", data=task)