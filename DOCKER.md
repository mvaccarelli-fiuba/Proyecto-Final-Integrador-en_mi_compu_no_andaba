# Docker Setup para Crusty Crab

Este proyecto ahora está completamente dockerizado. Todas las aplicaciones corren en contenedores orchestrados con Docker Compose.

## Componentes

- **MySQL 8.0**: Base de datos (puerto 3306)
- **Backend Flask**: API REST (puerto 5000)
- **Frontend Flask**: Interfaz web (puerto 5001)

## Requisitos

- Docker (versión 20.10+)
- Docker Compose (versión 1.29+)

## Instrucciones de uso

### Iniciar todos los servicios

```bash
docker-compose up --build
```

La primera vez tardará más por las descargas e instalaciones de dependencias.

### Acceder a la aplicación

- **Frontend**: http://localhost:5001
- **Backend API**: http://localhost:5000

### Acceder desde dispositivo externo

Reemplaza `localhost` por la **IP de tu máquina** en la red:

```bash
# En Linux/Mac: obtén tu IP
ifconfig | grep "inet "

# En Windows
ipconfig
```

Luego accede desde otro dispositivo:
- **Frontend**: http://[TU_IP]:5001
- **Backend**: http://[TU_IP]:5000

### Detener los servicios

```bash
docker-compose down
```

### Ver logs

```bash
# Todos los servicios
docker-compose logs -f

# Solo un servicio
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mysql
```

### Acceso a la base de datos

```bash
docker-compose exec mysql mysql -u tp_user -p crusty_crab
# Contraseña: 1234
```

## Cambios realizados

- ✅ Backend y Frontend ahora escuchan en `0.0.0.0` (accesible desde redes externas)
- ✅ Configuración de base de datos usa variables de entorno
- ✅ Frontend conecta al backend a través de la red de Docker
- ✅ Base de datos persiste en volumen `mysql_data`
- ✅ Healthcheck para MySQL antes de iniciar dependencias

## Notas de desarrollo

Los volúmenes están montados para desarrollo, así que los cambios en el código se reflejan al instante. Solo reinicia el contenedor si cambias `requirements.txt`.

Si necesitas instalar nuevas dependencias:

```bash
# Dentro del contenedor
docker-compose exec backend pip install [paquete]
docker-compose exec frontend pip install [paquete]

# O reconstruye
docker-compose up --build
```
