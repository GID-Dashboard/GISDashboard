from .settings import *

DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'DataDashboard',
        'USER': 'dashboardadm',
        'PASSWORD': '@dmDashb0ard',
        'HOST': '172.16.55.247',
        'PORT': '5432',
    },
    'sims': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'gis111207',
        'HOST': 'GISSIMSSVR.gardenschool.edu.my\sims2008',
        'USER': 'dashboardadm',
        'PASSWORD': '@dmDashb0ard',

        'OPTIONS': {
             'driver': "ODBC Driver 17 for SQL Server",
             'extra_params': "CurrentSchema=sims",
         },
    }
}