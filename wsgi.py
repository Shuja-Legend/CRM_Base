import os
import sys
sys.path.append('/opt/bitnami/projects/CRM_Base')
os.environ.setdefault("PYTHON_EGG_CACHE", "/opt/bitnami/apps/django/django_projects/CRM_Base/egg_cache")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CRM_Base.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()