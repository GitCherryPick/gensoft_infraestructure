from typing import Dict, Any
from app.schema.exam import ExamOut
from app.schema.exam_response import ExamResponseOut

def grade_exam(exam: ExamOut, exam_response: ExamResponseOut) -> ExamResponseOut:
    total_score = 0.0
    question_map = {q.question_id: q for q in exam.questions}
    updated_responses = []

    for question_response in exam_response.question_responses:
        question_exam = question_map.get(question_response.question_id)
        if not question_exam:
            continue  # pregunta no encontrada en el examen

        points_earned = 0.0
        is_correct = False

        if question_exam.type == "seleccion_simple":
            # Suponiendo que correct_answer es un string o int
            if str(question_response.answer) == str(question_exam.correct_answer):
                is_correct = True
                points_earned = float(question_exam.points)

        elif question_exam.type == "seleccion_multiple":
            # Suponiendo que correct_answers es una lista de strings o ints
            if set(map(str, question_response.answers or [])) == set(map(str, question_exam.correct_answers or [])):
                is_correct = True
                points_earned = float(question_exam.points)

        # Actualiza la respuesta
        question_response.is_correct = is_correct
        question_response.points_earned = points_earned
        total_score += points_earned
        updated_responses.append(question_response)

    # Actualiza el objeto de respuesta
    exam_response.question_responses = updated_responses
    exam_response.total_score = total_score
    return exam_response