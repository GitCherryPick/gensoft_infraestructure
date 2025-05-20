from sqlalchemy.orm import Session
from app.model.code_task import CodeTask
from app.database import SessionLocal  

def seed_task_replicators():
    db: Session = SessionLocal()

    tasks = [
        CodeTask(
            title="Condicional if",
            description="Este condicional usualmente viene acompañado con un else y else if. En Python se utiliza una palabra clave diferente: 'elif'. Es tu oportunidad de trabajar con este nuevo conocimiento.",
            expected_code=(
                "this_year = 2025\n"
                "if(this_year > 2000):\n"
                "    return 'welcome new era'\n"
                "elif(this_year > 3000):\n"
                "    return 'Es el futuro'\n"
                "else:\n"
                "    return 'welcome past'"
            ),
            template_code=(
                "this_year = 2025\n"
                "if(this_year > 2000):\n"
                "    return 'welcome new era'\n"
                "elif(this_yea"
            )
        ),
        CodeTask(
            title="Sumar dos números",
            description="Completa el código para sumar dos números y retornar el resultado.",
            expected_code="a = 5\nb = 3\nreturn a + b",
            template_code="a = 5\nb = "
        ),
        CodeTask(
            title="Bucle for",
            description="Crea un bucle que imprima los números del 1 al 5.",
            expected_code="for i in range(1, 6):\n    print(i)",
            template_code=""
        ),
        CodeTask(
            title="Función de saludo",
            description="Completa la función que recibe un nombre y retorna un saludo.",
            expected_code="def greet(name):\n    return f'Hola {name}!'",
            template_code=""
        ),
        CodeTask(
            title="Condicional anidado",
            description="Trabaja con condiciones dentro de otras condiciones para tomar decisiones complejas.",
            expected_code=(
                "x = 10\n"
                "if x > 5:\n"
                "    if x < 15:\n"
                "        return 'x está entre 5 y 15'"
            ),
            template_code="x = 10\nif x > 5:\n    if"
        )
    ]

    db.add_all(tasks)
    db.commit()
    db.close()
    print("✅ Seed insertado con éxito")

