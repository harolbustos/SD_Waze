-- Cargar CSV
eventos = LOAD 'filtrados.csv' USING PigStorage(',') AS (
    wid:chararray,
    evento:chararray,
    descripcion:chararray,
    fecha:chararray,
    comuna:chararray,
    lat:double,
    lon:double,
    timestamp:long
);

-- Agrupación por comuna
agrupado_comuna = GROUP eventos BY comuna;
conteo_comuna = FOREACH agrupado_comuna GENERATE group AS comuna, COUNT(eventos) AS total;

-- Agrupación por tipo
agrupado_tipo = GROUP eventos BY evento;
conteo_tipo = FOREACH agrupado_tipo GENERATE group AS tipo_evento, COUNT(eventos) AS total;

-- Agrupación por fecha
agrupado_fecha = GROUP eventos BY fecha;
conteo_fecha = FOREACH agrupado_fecha GENERATE group AS fecha, COUNT(eventos) AS total;

-- Estadísticas por comuna (coordenadas)
estadisticas = FOREACH agrupado_comuna GENERATE
    group AS comuna,
    COUNT(eventos) AS total,
    AVG(eventos.lat) AS lat_promedio,
    MIN(eventos.lat) AS lat_min,
    MAX(eventos.lat) AS lat_max,
    AVG(eventos.lon) AS lon_promedio,
    MIN(eventos.lon) AS lon_min,
    MAX(eventos.lon) AS lon_max;

-- Conteo por tipo y comuna
agrupado_tipo_comuna = GROUP eventos BY (evento, comuna);
conteo_tipo_comuna = FOREACH agrupado_tipo_comuna GENERATE
    group.evento AS tipo,
    group.comuna AS comuna,
    COUNT(eventos) AS total;

-- Guardar resultados
STORE conteo_comuna INTO 'resultados/por_comuna' USING PigStorage(',');
STORE conteo_tipo INTO 'resultados/por_tipo' USING PigStorage(',');
STORE conteo_fecha INTO 'resultados/por_fecha' USING PigStorage(',');
STORE estadisticas INTO 'resultados/estadisticas' USING PigStorage(',');
STORE conteo_tipo_comuna INTO 'resultados/por_tipo_y_comuna' USING PigStorage(',');
