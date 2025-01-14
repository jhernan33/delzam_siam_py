name = 'siam'
loglevel = 'info'
errorlog = '-'
accesslog = '-'
workers = 3

# config/gunicorn/conf.py

# import multiprocessing

# # Número de workers basados en la cantidad de CPUs
# workers = multiprocessing.cpu_count() * 2 + 1

# # Nivel de log
# loglevel = "info"

# # Rutas de los logs
# accesslog = "-"  # Logs de acceso en stdout
# errorlog = "-"   # Logs de error en stdout
# capture_output = True

# # Configurar el timeout (en segundos)
# timeout = 120

# # Número de conexiones simultáneas por worker
# worker_connections = 1000
