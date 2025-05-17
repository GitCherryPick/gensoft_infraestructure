from datetime import datetime
from app.database import SessionLocal
from app.model.courses import Course
from app.model.module import Module
from app.model.content import Content

def seed_data():
    db = SessionLocal()
    
    try:
        existing_course = db.query(Course).filter(Course.title == "Introducción a la Programación").first()
        
        if existing_course:
            course_id = existing_course.id
        else:
            curso_python = Course(
                title="Introducción a la Programación",
                description="Curso orientado a la enseñanza de los conceptos básicos de programación utilizando el lenguaje Python. Cubre estructuras de control, tipos de datos, funciones y principios fundamentales del desarrollo de software.",
                difficulty="fácil",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            db.add(curso_python)
            db.commit()
            db.refresh(curso_python)
            
            course_id = curso_python.id
        
        modulos = [
            {
                "title": "Tipos de Datos y Variables",
                "description": "Estudia los tipos de datos fundamentales del lenguaje Python, como enteros, flotantes, cadenas de texto y valores booleanos. Introduce el uso de variables para almacenar información, así como las reglas de nomenclatura y buenas prácticas para su definición.",
                "level": "básico",
                "module_order": 1
            },
            {
                "title": "Estructuras de Control",
                "description": "Explora las estructuras que permiten controlar el flujo de ejecución de un programa. Incluye el uso de condicionales (if, elif, else) y bucles (for, while) para la toma de decisiones y la repetición de tareas dentro del código.",
                "level": "básico",
                "module_order": 2
            },
            {
                "title": "Funciones",
                "description": "Aborda el concepto de funciones como bloques reutilizables de código. Se enseña cómo definir funciones, pasar argumentos, retornar valores y aplicar principios de modularidad para mejorar la organización y legibilidad del código.",
                "level": "intermedio",
                "module_order": 3
            },
            {
                "title": "Estructuras de Datos",
                "description": "Introduce las principales estructuras de datos integradas en Python: listas, tuplas, diccionarios y conjuntos. Se analizan sus características, operaciones básicas y casos de uso comunes en la resolución de problemas.",
                "level": "intermedio",
                "module_order": 4
            },
            {
                "title": "Manejo de Errores",
                "description": "Presenta los mecanismos de gestión de errores y excepciones en Python. Se enseña cómo anticipar, detectar y manejar situaciones excepcionales durante la ejecución del programa utilizando bloques try, except y otras herramientas disponibles.",
                "level": "avanzado",
                "module_order": 5
            }
        ]
        
        modulos_ids = {}
        
        for modulo_data in modulos:
            existing_module = db.query(Module).filter(
                Module.course_id == course_id,
                Module.title == modulo_data["title"]
            ).first()
            
            if existing_module:
                modulos_ids[modulo_data["title"]] = existing_module.id
            else:
                nuevo_modulo = Module(
                    course_id=course_id,
                    title=modulo_data["title"],
                    description=modulo_data["description"],
                    level=modulo_data["level"],
                    module_order=modulo_data["module_order"]
                )
                
                db.add(nuevo_modulo)
                db.commit()
                db.refresh(nuevo_modulo)
                
                modulos_ids[modulo_data["title"]] = nuevo_modulo.id
        
        contenidos = [
            {
                "module_title": "Tipos de Datos y Variables",
                "title": "Tipos de Datos y Variables",
                "content_type": "text",
                "content": (
                    "<b>Descripción</b><br>"
                    "Este módulo introduce los tipos de datos fundamentales en Python y el uso de variables como base para la manipulación de información.&nbsp;<br><br>"

                    "<b>Tipos de datos principales</b><br>"
                    "<ul>"
                    "<li><b>int</b>: números enteros (ej. 10)</li>"
                    "<li><b>float</b>: números decimales (ej. 3.14)</li>"
                    "<li><b>str</b>: texto o cadenas de caracteres</li>"
                    "<li><b>bool</b>: valores lógicos (True / False)</li>"
                    "</ul><br>"

                    "<b>Variables en Python</b><br>"
                    "Una variable es un nombre que almacena un valor. Python permite declarar variables sin especificar su tipo, gracias al <i>tipado dinámico</i>.&nbsp;<br><br>"

                    "<b>Funciones útiles</b><br>"
                    "<ul>"
                    "<li><b>type()</b>: identifica el tipo de un valor</li>"
                    "<li><b>input()</b>: permite recibir datos desde el usuario</li>"
                    "</ul><br>"

                    "Se promueve el uso de nombres descriptivos y buenas prácticas de estilo para escribir código legible y mantenible."
                )
            },
            {
                "module_title": "Estructuras de Control",
                "title": "Estructuras de Control",
                "content_type": "text",
                "content": (
                    "<b>Descripción</b><br>"
                    "Este módulo se centra en las estructuras que permiten controlar el flujo de ejecución de un programa. A través de ellas, un programa puede tomar decisiones, ejecutar ciertas instrucciones solo cuando se cumplan condiciones específicas, o repetir acciones de manera controlada.&nbsp;<br><br>"

                    "<b>Condicionales</b><br>"
                    "Se explica cómo utilizar las sentencias <b>if</b>, <b>elif</b> y <b>else</b> para evaluar condiciones lógicas. Estas permiten ejecutar bloques de código diferentes según el valor de ciertas expresiones, lo cual es fundamental para introducir lógica en los programas.&nbsp;<br><br>"

                    "<b>Bucles</b><br>"
                    "También se estudian los bucles <b>for</b> y <b>while</b>, que permiten repetir instrucciones múltiples veces. El bucle <b>for</b> se utiliza especialmente para iterar sobre colecciones, mientras que <b>while</b> ejecuta un bloque de código mientras se cumpla una condición. Se analizan además instrucciones como <b>break</b> para salir del ciclo y <b>continue</b> para omitir la iteración actual.&nbsp;<br><br>"

                    "Este módulo incluye ejemplos prácticos y ejercicios que ayudan a comprender cómo estructurar programas dinámicos y flexibles, capaces de adaptarse a diferentes situaciones mediante decisiones y repeticiones controladas."
                )
            },
            {
                "module_title": "Funciones",
                "title": "Funciones",
                "content_type": "text",
                "content": (
                    "<b>Descripción</b><br>"
                    "Las funciones son bloques de código que encapsulan una secuencia de instrucciones para ser reutilizadas en diferentes partes de un programa. Este módulo explora la creación, invocación y utilidad de las funciones como herramienta para mejorar la organización y legibilidad del código.&nbsp;<br><br>"

                    "<b>Definición y parámetros</b><br>"
                    "Se enseña a definir funciones utilizando la palabra clave <b>def</b>, declarar parámetros que permiten recibir valores de entrada, y retornar resultados usando <b>return</b>. Se abordan también conceptos como argumentos por defecto y paso de parámetros por valor o por referencia.&nbsp;<br><br>"

                    "<b>Modularidad</b><br>"
                    "El uso de funciones promueve el principio de <i>modularidad</i>, permitiendo dividir un programa en partes más pequeñas, entendibles y reutilizables. Esto facilita el mantenimiento y la prueba del código.&nbsp;<br><br>"

                    "El módulo incluye ejemplos de funciones básicas, funciones con múltiples argumentos, y el uso de funciones anidadas. Además, se introducen conceptos iniciales de documentación y buenas prácticas, como el uso de nombres significativos y evitar duplicación de código."
                )
            },
            {
                "module_title": "Estructuras de Datos",
                "title": "Estructuras de Datos",
                "content_type": "text",
                "content": (
                    "<b>Descripción</b><br>"
                    "En este módulo se exploran las estructuras de datos fundamentales en Python, herramientas esenciales para almacenar, organizar y manipular conjuntos de información de manera eficiente.&nbsp;<br><br>"

                    "<b>Tipos principales</b><br>"
                    "<ul>"
                    "<li><b>Listas</b>: estructuras ordenadas y mutables que permiten almacenar elementos heterogéneos. Se abordan operaciones como inserción, eliminación, ordenamiento y acceso por índice.</li>"
                    "<li><b>Tuplas</b>: similares a las listas, pero inmutables. Se utilizan cuando se desea garantizar que los datos no se modifiquen.</li>"
                    "<li><b>Diccionarios</b>: estructuras de mapeo que relacionan claves con valores. Se enseñan métodos para agregar, actualizar y acceder a pares clave-valor.</li>"
                    "<li><b>Conjuntos</b>: colecciones no ordenadas que almacenan elementos únicos. Se estudian operaciones como unión, intersección y diferencia.</li>"
                    "</ul><br>"

                    "El módulo proporciona ejemplos prácticos de uso de cada estructura, enfatizando en la elección adecuada según las necesidades del problema. También se analizan diferencias clave entre ellas y su impacto en el rendimiento y legibilidad del código."
                )
            },
            {
                "module_title": "Manejo de Errores",
                "title": "Manejo de Errores",
                "content_type": "text",
                "content": (
                    "<b>Descripción</b><br>"
                    "Este módulo introduce el concepto de manejo de errores y excepciones en Python, una parte crítica del desarrollo de aplicaciones robustas y confiables.&nbsp;<br><br>"

                    "<b>Errores comunes</b><br>"
                    "Durante la ejecución de un programa, pueden ocurrir errores inesperados como divisiones por cero, referencias a variables no definidas o acceso a elementos inexistentes. Estos errores, si no son gestionados, provocan que el programa finalice de forma abrupta.&nbsp;<br><br>"

                    "<b>Bloques try-except</b><br>"
                    "Se enseña el uso de estructuras <b>try</b> y <b>except</b> para detectar y capturar excepciones de forma controlada. También se presentan las cláusulas <b>else</b> y <b>finally</b>, que permiten ejecutar acciones dependiendo de si ocurrió o no un error.&nbsp;<br><br>"

                    "<b>Excepciones personalizadas</b><br>"
                    "El módulo también cubre cómo generar errores manualmente mediante <b>raise</b>, y cómo definir excepciones propias en casos específicos.&nbsp;<br><br>"

                    "A través de ejemplos prácticos, el estudiante aprenderá a identificar riesgos, manejar errores sin comprometer la estabilidad del programa, y mejorar la experiencia del usuario frente a fallos."
                )
            },
            {
                "module_title": "Tipos de Datos y Variables",
                "title": None,
                "content_type": "pdf",
                "content": None,
                "video_url": None,
                "file_path": "storage/pdf/example_1_1.pdf",
            },
            {
                "module_title": "Estructuras de Control",
                "title": None,
                "content_type": "pdf",
                "content": None,
                "video_url": None,
                "file_path": "storage/pdf/example_2_1.pdf",
            },
            {
                "module_title": "Funciones",
                "title": None,
                "content_type": "pdf",
                "content": None,
                "video_url": None,
                "file_path": "storage/pdf/example_1_1.pdf",
            },
            {
                "module_title": "Estructuras de Datos",
                "title": None,
                "content_type": "pdf",
                "content": None,
                "video_url": None,
                "file_path": "storage/pdf/example_2_1.pdf",
            },
            {
                "module_title": "Manejo de Errores",
                "title": None,
                "content_type": "pdf",
                "content": None,
                "video_url": None,
                "file_path": "storage/pdf/example_1_1.pdf",
            },
            {
                "module_title": "Tipos de Datos y Variables",
                "title": "Video: Tipos de Datos y Variables",
                "content_type": "video",
                "content": None,
                "video_url": "https://www.youtube.com/watch?v=LKFrQXaoSMQ",
                "file_path": None,
            },
            {
                "module_title": "Estructuras de Control",
                "title": "Video: Estructuras de Control",
                "content_type": "video",
                "content": None,
                "video_url": "https://www.youtube.com/watch?v=FvMPfrgGeKs",
                "file_path": None,
            },
            {
                "module_title": "Funciones",
                "title": "Video: Funciones",
                "content_type": "video",
                "content": None,
                "video_url": "https://www.youtube.com/watch?v=89cGQjB5R4M",
                "file_path": None,
            },
            {
                "module_title": "Estructuras de Datos",
                "title": "Video: Estructuras de Datos",
                "content_type": "video",
                "content": None,
                "video_url": "https://www.youtube.com/watch?v=jzJlq35dQII&list=PLZPZq0r_RZON1eaqfafTnEexRzuHbfZX8&index=6",
                "file_path": None,
            },
            {
                "module_title": "Manejo de Errores",
                "title": "Video: Manejo de Errores",
                "content_type": "video",
                "content": None,
                "video_url": "https://www.youtube.com/watch?v=V_NXT2-QIlE",
                "file_path": None,
            }
        ]
        
        for contenido_data in contenidos:
            if contenido_data["module_title"] in modulos_ids:
                module_id = modulos_ids[contenido_data["module_title"]]
                if contenido_data["content_type"] == "pdf":
                    existing_content = db.query(Content).filter(
                        Content.module_id == module_id,
                        Content.file_path == contenido_data["file_path"]
                    ).first()
                elif contenido_data["content_type"] == "video":
                    existing_content = db.query(Content).filter(
                        Content.module_id == module_id,
                        Content.video_url == contenido_data["video_url"]
                    ).first()
                else:
                    existing_content = db.query(Content).filter(
                        Content.module_id == module_id,
                        Content.title == contenido_data["title"]
                    ).first()
                
                if existing_content:
                    if contenido_data["content_type"] == "text":
                        existing_content.content = contenido_data["content"]
                    elif contenido_data["content_type"] == "pdf":
                        existing_content.file_path = contenido_data["file_path"]
                    elif contenido_data["content_type"] == "video":
                        existing_content.video_url = contenido_data["video_url"]
                        existing_content.title = contenido_data["title"]
                    
                    db.commit()
                else:
                    nuevo_contenido = Content(
                        module_id=module_id,
                        content_type=contenido_data["content_type"],
                        title=contenido_data["title"],
                        content=contenido_data.get("content"),
                        video_url=contenido_data.get("video_url"),
                        file_path=contenido_data.get("file_path"),
                        created_at=datetime.now()
                    )
                    
                    db.add(nuevo_contenido)
                    db.commit()
                    db.refresh(nuevo_contenido)
        
        print("Datos de prueba cargados con éxito!")
        
    except Exception as e:
        db.rollback()
        print(f"Error al crear datos de prueba: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
