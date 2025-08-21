🪪 Sistema de Registro de Cédulas + API REST con FastAPI y MySQL

API backend para manejar autenticación de usuarios y registro/consulta de cédulas.
Desarrollado con FastAPI + SQLAlchemy + MySQL.


Instalacion del Back End de manera local y sencilla.

Por favor, a la hora de crear la cedula, si gusta probar creala con la siguiente estructura 2-0000-0000
Esto con el fin de que no se genere errores o bugs inesperados con el bot de discord.

1. Descargar o Clona el repositorio en tu computadora.
2. Abre Visual Studio Code y carga la carpeta del proyecto.
3. Abre la terminal integrada con Ctrl + ñ o Terminal > New Terminal.
4. Crear un entorno virtual (opcional pero recomendado):
Ejecuta el entorno virtual aplicando el paso 3 + esta linea de codigo: python -m venv venv

5. Activar el entorno virtual:
* En Windows. venv\Scripts\activate
* En Linux/Mac. source venv/bin/activate

6. Instalar las dependencias:
pip install -r requirements.txt

7. Configurar variables de entorno (Las variables de entorno estan previamente configuradas para la facilidad de la persona que acceda a este repositorio) * ver nota de abajo.

8. Ejecutar el backend:
uvicorn app.main:app --reload

8. Abrir en el navegador:
Puedes escribir esto en tu navegado: http://127.0.0.1:8000/docs
O puedes dar Control + click izquiero en el link que sale en la consola de VS Code.

🔑 Flujo de Autenticación (IMPORTANTE)

Antes de usar los endpoints de /usuarios, necesitas registrarte y loguearte para obtener un token JWT.

1️⃣ Registro de usuario de autenticación
Buscar en la interfaz grafica de Swagger UI lo siguiente:

POST /auth/register le da click, luego en "Try it out"
Rellenar los datos con la siguiente estructura:
***No usar Admin de Username**
{
  "username": "user a Eleccion",
  "password": "Contra a Eleccion",
  "email": "correoa@eleccion.com"
}

2️⃣ Login
Buscar en la interfaz grafica de Swagger UI lo siguiente:

POST /auth/login le da click, luego en "Try it out"

Rellenar los campos que aparecen en rojo de required username y password

Debe aparecer una respuesta similar a la siguiente:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR...",
  "token_type": "bearer"
}

⚠️ Guarda ese access_token. Lo necesitas en el Authorization Header:

Despues vas en la parte superior de la pagina buscando un boton de color verde con un candado con el siguiente nombre de "Autorize"
Precionas. Pones tus datos de username y password luego en client_secret pones el access_token que se te dio en el paso 2. Luego al boton
verde de autorize y LISTO. Ya tienes acceso a los Endpoints de Usuarios.


Endpoints disponibles
Método          Endpoint                    Descripción
GET	            /usuarios	                Listar todos los usuarios
POST	        /usuarios/crear usuario     Permite crear un nuevo usuario (Si gusta probar esta funcion debe utilizar las ceduldas de 2-0000-0000)
GET	            /usuarios/{cedula}          Consultar usuario por cédula
PUT	            /usuarios/{cedula}	        Actualizar usuario por cédula
DELETE	        /usuarios/{cedula}	        Eliminar usuario por cédula


Nota linea 25:
Todas las variables que estan que estan establecidas en el .env son variables reales establecidas en una base de datos MySQL de mi propiedad Justin Padilla Moya.
Queda a eleccion del profesor si las quiere modificar de la linea 1 a la 5
