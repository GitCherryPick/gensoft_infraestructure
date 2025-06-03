from sqlalchemy.orm import Session
from app.model.code_task import CodeTask
from app.model.tasks import Tasks
from app.model.tests import Tests
from app.database import SessionLocal  

def seed_task_replicators():
    db: Session = SessionLocal()

    if db.query(CodeTask).first(): 
        print("Seed omitido.")
        db.close()
        return

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
    print("✅ Seed insertado de replicator con éxito")

def seed_task_lab():
    db: Session = SessionLocal()

    if db.query(Tasks).first():
        print("Seed omitido.")
        db.close()
        return
    tareas_data = [
        {
            "title": "Sumar 2 numeros",
            "enunciado": "Implementa una funciona suma(a,b) que reciba dos numeros y retorne su suma.",
            "tests": [
                {"input": "suma(1,2)", "output": "3"},
                {"input": "suma(2,4)", "output": "6"}
            ]
        },
        {
            "title": "Es primo",
            "enunciado": "Implementa una función es_primo(n) que retorne True si el número n es primo y False en caso contrario.",
            "tests": [
                {"input": "es_primo(2)", "output": "True"},
                {"input": "es_primo(4)", "output": "False"},
                {"input": "es_primo(17)", "output": "True"}
            ],
            "pistas": ["Un número primo solo tiene dos divisores: 1 y él mismo."]
        },
        {
            "title": "Es palindromo",
            "enunciado": "Implementa una función es_palindromo(palabra) que retorne True si la palabra se lee igual al derecho y al revés.",
            "tests": [
                {"input": "es_palindromo('oso')", "output": "True"},
                {"input": "es_palindromo('hola')", "output": "False"},
                {"input": "es_palindromo('reconocer')", "output": "True"}
            ],
            "pistas": ["Puedes comparar la palabra con su versión invertida usando slicing."]
        },
        {
            "title": "Contar vocales",
            "enunciado": "Implementa una función contar_vocales(texto) que retorne cuántas vocales hay en el texto.",
            "tests": [
                {"input": "contar_vocales('hola')", "output": "2"},
                {"input": "contar_vocales('aeiou')", "output": "5"},
                {"input": "contar_vocales('zzz')", "output": "0"}
            ],
            "pistas": ["Puedes recorrer cada letra y verificar si es una vocal."]
        },
        {
            "title": "Suma de pares",
            "enunciado": "Implementa una función suma_pares(lista) que retorne la suma de todos los números pares en una lista.",
            "tests": [
                {"input": "suma_pares([1, 2, 3, 4])", "output": "6"},
                {"input": "suma_pares([10, 11, 12])", "output": "22"},
                {"input": "suma_pares([1, 3, 5])", "output": "0"}
            ],
            "pistas": ["Usa el operador % para saber si un número es par."]
        },
        {
            "title": "Invertir palabras",
            "enunciado": "Implementa una función invertir_palabras(frase) que retorne la misma frase pero con cada palabra invertida, manteniendo el orden.",
            "tests": [
                {"input": "invertir_palabras('hola mundo')", "output": "aloh odnum"},
                {"input": "invertir_palabras('python es genial')", "output": "nohtyp se laineg"},
                {"input": "invertir_palabras('amor a roma')", "output": "roma a amor"}
            ],
            "pistas": ["Puedes usar split() para separar palabras","Puedes usar [::-1] para invertir."]
        },
        {
            "title": "Máximo común divisor",
            "enunciado": "Implementa una función mcd(a, b) que retorne el máximo común divisor entre a y b.",
            "tests": [
                {"input": "mcd(12, 18)", "output": "6"},
                {"input": "mcd(7, 3)", "output": "1"},
                {"input": "mcd(20, 8)", "output": "4"}
            ],
            "pistas": [
                "Puedes usar el algoritmo de Euclides para calcular el MCD.",
                "Repite el proceso hasta que b sea 0."
            ]
        },
        {
            "title": "Ordenar lista",
            "enunciado": "Implementa una función ordenar_lista(lista) que retorne la lista ordenada de menor a mayor.",
            "tests": [
                {"input": "ordenar_lista([3, 1, 2])", "output": "[1, 2, 3]"},
                {"input": "ordenar_lista([5, 4, 3])", "output": "[3, 4, 5]"},
                {"input": "ordenar_lista([10, 20, 30])", "output": "[10, 20, 30]"}
            ],
            "pistas":["Puedes usar el método sort() o sorted()."]
        },
        {
            "title": "Número feliz",
            "enunciado": "Crea una función es_feliz(n) que determine si un número es feliz. Un número feliz es aquel que al reemplazarse por la suma de los cuadrados de sus dígitos eventualmente llega a 1.",
            "tests": [
                {"input": "es_feliz(19)", "output": "True"},
                {"input": "es_feliz(4)", "output": "False"},
                {"input": "es_feliz(1)", "output": "True"}
            ],
            "pistas": [
                "Usa un conjunto para guardar los números ya vistos.",
                "Repite el proceso hasta que llegues a 1 o entres en un ciclo."
            ]
        },
        {
            "title": "Factorial de un número",
            "enunciado": "Implementa una función factorial(n) que calcule el factorial de un número n (n!).",
            "tests": [
                {"input": "factorial(5)", "output": "120"},
                {"input": "factorial(0)", "output": "1"},
                {"input": "factorial(3)", "output": "6"}
            ],
            "pistas":[
                "El factorial de 0 es 1.",
                "Puedes usar un bucle para calcularlo."
            ]
        }
    ]

    for data in tareas_data:
        task = Tasks(title=data["title"], enunciado=data["enunciado"],pistas=data.get("pistas", []))
        db.add(task)
        db.flush()  
        # Creamos y añadimos los tests
        tests = [Tests(task_id=task.id, input=t["input"], output=t["output"]) for t in data["tests"]]
        db.add_all(tests)

    db.commit()


