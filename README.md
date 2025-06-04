# 📦 Proyecto Sistemas Distribuidos: Manejo de la Información del Análisis de Tráfico en Región Metropolitana
### Utilizando web scraping desde [Waze Live Map](https://www.waze.com/es-419/live-map) y su almacenamiento en MongoDB Atlas.

## Requisitos

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

## 🚀 Instrucciones de ejecución
### 1. Clonar el repositorio
```
git clone https://github.com/harolbustos/SD_Waze.git
```
### 2. Construir e iniciar los contenedores
#### Dentro de la carpeta raiz del proyecto
```
docker-compose up --build
```
### 3. Ingresar al contenedor del módulo procesador
```
docker exec -it procesador_waze bash
```
### 4. Ejecutar Pig
#### Esto generará una carpeta 'resultados/' dentro del módulo procesador, en el cual se encuentran las tablas.
```
pig -x local procesar.pig 
```

## ✅ Adicionales
### Credenciales en apartado Anexos del informe
###  Consultar el total de eventos en la base de datos
``` 
curl http://localhost:8080/eventos/total
```
### Consultar el total de eventos por tipo en la base de datos
``` 
curl http://localhost:8080/eventos/por-tipo
```
### Consultar las metricas del cache
``` 
curl http://localhost:4000/cache/metricas
```
