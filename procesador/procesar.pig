-- Cargar CSV
eventos = LOAD 'filtrados.csv' USING PigStorage(',') AS (
    wid:chararray,
    evento:chararray,
    descripcion:chararray,
    fecha:chararray,
    hora:chararray,
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

-- Total eventos por dia
eventos_por_dia = GROUP eventos BY fecha;
conteo_por_dia = FOREACH eventos_por_dia GENERATE group AS fecha, COUNT(eventos) AS total;

-- Total eventos por hora
eventos_por_hora = GROUP eventos BY hora;
conteo_por_hora = FOREACH eventos_por_hora GENERATE group AS hora, COUNT(eventos) AS total;

-- Total cada evento(diferenciado) por hora
eventos_por_hora_tipo = GROUP eventos BY (hora, evento);
conteo_por_hora_tipo = FOREACH eventos_por_hora_tipo GENERATE
    group.hora AS hora,
    group.evento AS tipo,
    COUNT(eventos) AS total;

-- Total cada evento(diferenciado) por dia
eventos_por_dia_tipo = GROUP eventos BY (fecha, evento);
conteo_por_dia_tipo = FOREACH eventos_por_dia_tipo GENERATE
    group.fecha AS fecha,
    group.evento AS tipo,
    COUNT(eventos) AS total;

-- Conteo por tipo y comuna
agrupado_tipo_comuna = GROUP eventos BY (evento, comuna);
conteo_tipo_comuna = FOREACH agrupado_tipo_comuna GENERATE
    group.evento AS tipo,
    group.comuna AS comuna,
    COUNT(eventos) AS total;

-- Guardar resultados
STORE conteo_comuna INTO 'resultados/por_comuna' USING PigStorage(',');
STORE conteo_tipo INTO 'resultados/por_tipo' USING PigStorage(',');
STORE conteo_tipo_comuna INTO 'resultados/por_tipo_y_comuna' USING PigStorage(',');
STORE conteo_por_dia INTO 'resultados/por_dia' USING PigStorage(',');
STORE conteo_por_hora INTO 'resultados/por_hora' USING PigStorage(',');
STORE conteo_por_hora_tipo INTO 'resultados/por_hora_y_tipo' USING PigStorage(',');
STORE conteo_por_dia_tipo INTO 'resultados/por_dia_y_tipo' USING PigStorage(',');
