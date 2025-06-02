### Node version: 22.16.0

### Ejecutar imagen de la API
```bash
    sudo docker build . -t api-waze:latest
```

### Luego de montar la imagen
```bash
    sudo docker run --env-file=./.env -p 3002:3000 api-waze:latest

```