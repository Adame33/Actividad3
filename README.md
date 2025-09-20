Plataforma de Webinars
Este proyecto es una plataforma de webinars, diseñada para gestionar usuarios, tutores, y contenido multimedia de forma eficiente. El sistema se apoya en una base de datos robusta para manejar la información de webinars, videos, material de apoyo y la actividad de los usuarios.

Tecnologías Utilizadas
Backend: Python

Base de Datos: MySQL

Gestión de Entorno: venv

Manejo de Dependencias: pip

Estructura del Proyecto
El proyecto se compone de los siguientes elementos principales:

app.py: El archivo principal de la aplicación.

requirements.txt: Lista de dependencias de Python necesarias para el proyecto.

sql/: Directorio que contiene todos los scripts SQL para la base de datos.

creacion.sql: Script para la creación de la base de datos y todas las tablas.

SP.sql: Archivo que contiene los procedimientos almacenados.

Vistas.sql: Archivo con las vistas de la base de datos.

datos_minimos.sql: Script para insertar datos iniciales y de prueba.

limpieza.sql: Script para limpiar la base de datos (opcional).

consultas_rapidas.sql: Archivo con consultas de ejemplo útiles (opcional).

Pasos para la Ejecución del Proyecto
Sigue estos pasos para configurar y ejecutar el proyecto en tu entorno local.

1. Configuración del Entorno Virtual de Python
Es altamente recomendable usar un entorno virtual para aislar las dependencias del proyecto.

python -m venv venv

2. Activación del Entorno Virtual
Activa el entorno virtual.

Windows:

.\venv\Scripts\activate

macOS / Linux:

source venv/bin/activate

3. Instalación de Dependencias
Instala todas las librerías necesarias del proyecto.

pip install -r requirements.txt

4. Configuración de la Base de Datos
Antes de iniciar la aplicación, debes configurar la base de datos en MySQL. Ejecuta los scripts SQL en el siguiente orden para asegurar que la base de datos se configure correctamente:

creacion.sql

SP.sql

Vistas.sql

datos_minimos.sql

Puedes ejecutar estos archivos utilizando tu cliente de MySQL preferido.

5. Ejecución de la Aplicación
Una vez que la base de datos esté lista, puedes iniciar la aplicación.

python .\app.py

La aplicación ahora debería estar funcionando en tu entorno local.
