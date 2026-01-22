Requisitos
Python 3.10+ y pip
MySQL 8 (u otra variante compatible con el conector mysqlclient)
virtualenv o venv para aislar dependencias

Paso a paso
Clona el repositorio y entra al directorio.
Crea y activa un entorno virtual.
Instala dependencias:
pip install -r requirements.txt
Crea tu archivo .env.
Ejecuta migraciones:
python manage.py migrate
Levanta el servidor de desarrollo:
python manage.py runserver

Variables de entorno
El proyecto utiliza un archivo .env para manejar configuraciones sensibles.


SECRET_KEY=django-insecure-bjdxedd+vn2z=w7mb7t*qdo*x8+vhak=-hmi8vmgr*891icq2%
DEBUG=True

DB_NAME=gestion_eventos
DB_USER=gestor_user
DB_PASSWORD=TuPasswordSegura123!
DB_HOST=localhost
DB_PORT=3306
