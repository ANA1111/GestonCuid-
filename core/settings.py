import os
import dj_database_url
from pathlib import Path

# ... (Mantenha o BASE_DIR como está) ...

# SEGURANÇA: No Railway, usamos variáveis de ambiente
SECRET_KEY = os.environ.get('SECRET_KEY', 'sua-chave-de-desenvolvimento-muito-longa')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# No Railway, precisamos liberar o host
ALLOWED_HOSTS = ['*']

# MIDDLEWARE: Adicione o Whitenoise logo após o SecurityMiddleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <-- ESSENCIAL
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ... os outros middlewares ...
]

# BANCO DE DATOS: O "pulo do gato" para o Postgres Profissional
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}",
        conn_max_age=600
    )
}

# ARQUIVOS ESTÁTICOS (CSS, JS, Imagens)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'