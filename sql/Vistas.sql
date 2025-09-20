-- ============================================================
-- 3) Vistas
-- ============================================================

DROP VIEW IF EXISTS vw_catalogo_webinars;
DROP VIEW IF EXISTS vw_catalogo_videos;
DROP VIEW IF EXISTS vw_catalogo_tutores;
DROP VIEW IF EXISTS vw_webinars_resumen;
DROP VIEW IF EXISTS vw_videos_con_webinar;
DROP VIEW IF EXISTS vw_materiales_con_origen;
DROP VIEW IF EXISTS vw_vistas_detalle;
DROP VIEW IF EXISTS vw_vista_activa_por_usuario;
DROP VIEW IF EXISTS vw_metricas_webinar;
DROP VIEW IF EXISTS vw_metricas_video;



-- Catálogos planos
CREATE VIEW vw_catalogo_webinars AS
SELECT
    W.idWebinar AS id,
    W.nombre AS titulo,
    W.descripcion,
    W.categoria,
    W.dificultad,
    W.imagen,
    W.totalVideos,
    W.contenidoLibre,
    W.tutorId,
    T.nombre AS nombreTutor,
    T.foto AS fotoTutor,
    T.puesto AS puestoTutor
FROM Webinars AS W
LEFT JOIN Tutores AS T ON W.tutorId = T.idTutor;



CREATE VIEW vw_catalogo_videos AS
SELECT
    V.idVideo AS id,
    V.titulo,
    V.descripcion,
    V.url,
    V.miniatura,
    V.duracionSeg,
    V.libre,
    V.idWebinar,
    W.nombre AS nombreWebinar
FROM Videos AS V
LEFT JOIN Webinars AS W ON V.idWebinar = W.idWebinar;


CREATE VIEW vw_catalogo_tutores AS
SELECT
    idTutor AS id,
    nombre,
    mail,
    foto,
    puesto,
    urlLinkedin
FROM Tutores;



-- Webinars con conteos
CREATE VIEW vw_webinars_resumen AS
SELECT
  w.idWebinar,
  w.nombre            AS webinar,
  w.categoria,
  w.dificultad,
  w.imagen,
  w.contenidoLibre,
  w.totalVideos,
  t.idTutor,
  t.nombre            AS tutor,
  COALESCE(vs.cant_videos, 0)     AS cant_videos,
  COALESCE(mat.cant_materiales,0) AS cant_materiales,
  COALESCE(vw.cant_vistas, 0)     AS cant_vistas,
  COALESCE(vw.cant_completos, 0)  AS cant_completos
FROM Webinars w
LEFT JOIN Tutores t ON t.idTutor = w.tutorId
LEFT JOIN (
  SELECT idWebinar, COUNT(*) AS cant_videos
  FROM Videos GROUP BY idWebinar
) vs ON vs.idWebinar = w.idWebinar
LEFT JOIN (
  SELECT v.idWebinar, COUNT(m.idMaterial) AS cant_materiales
  FROM Videos v
  JOIN MaterialApoyo m ON m.idVideo = v.idVideo
  GROUP BY v.idWebinar
) mat ON mat.idWebinar = w.idWebinar
LEFT JOIN (
  SELECT webinarId,
         COUNT(*) AS cant_vistas,
         SUM(CASE WHEN completado THEN 1 ELSE 0 END) AS cant_completos
  FROM VistasWebinar
  GROUP BY webinarId
) vw ON vw.webinarId = w.idWebinar;

-- Videos con datos del webinar y tutor
CREATE VIEW vw_videos_con_webinar AS
SELECT
  v.idVideo,
  v.titulo             AS video,
  v.duracionSeg,
  v.libre,
  v.url,
  v.miniatura,
  w.idWebinar,
  w.nombre             AS webinar,
  w.categoria,
  w.dificultad,
  t.idTutor,
  t.nombre             AS tutor
FROM Videos v
JOIN Webinars w ON w.idWebinar = v.idWebinar
LEFT JOIN Tutores t ON t.idTutor = w.tutorId;

-- Materiales con origen (video + webinar)
CREATE VIEW vw_materiales_con_origen AS
SELECT
  m.idMaterial,
  m.nombre            AS material,
  m.url               AS url_material,
  m.descargas,
  m.free              AS material_free,
  v.idVideo,
  v.titulo            AS video,
  w.idWebinar,
  w.nombre            AS webinar
FROM MaterialApoyo m
JOIN Videos v    ON v.idVideo   = m.idVideo
JOIN Webinars w  ON w.idWebinar = v.idWebinar;

-- Vistas detalle (usuario + webinar + video)
CREATE VIEW vw_vistas_detalle AS
SELECT
  vw.idVista,
  vw.userId,
  u.username,
  u.mail,
  vw.webinarId,
  w.nombre         AS webinar,
  vw.videoId,
  v.titulo         AS video,
  vw.startedAt,
  vw.lastSeenAt,
  vw.posSeg,
  vw.completado,
  vw.activo
FROM VistasWebinar vw
JOIN Usuarios u ON u.idUsuario = vw.userId
JOIN Webinars w ON w.idWebinar = vw.webinarId
LEFT JOIN Videos v ON v.idVideo = vw.videoId;

-- Vista activa por usuario (una fila si hay sesión activa)
CREATE VIEW vw_vista_activa_por_usuario AS
SELECT
  d.userId,
  d.username,
  d.mail,
  d.idVista,
  d.webinarId,
  d.webinar,
  d.videoId,
  d.video,
  d.posSeg,
  d.lastSeenAt
FROM vw_vistas_detalle d
WHERE d.activo = 1;

-- Métricas por webinar
CREATE VIEW vw_metricas_webinar AS
SELECT
  d.webinarId,
  d.webinar,
  COUNT(*) AS vistas_totales,
  SUM(CASE WHEN d.completado = 1 THEN 1 ELSE 0 END) AS vistas_completas,
  SUM(d.posSeg) AS watchTime_aprox_seg
FROM vw_vistas_detalle d
GROUP BY d.webinarId, d.webinar;

-- Métricas por video
CREATE VIEW vw_metricas_video AS
SELECT
  d.videoId,
  d.video,
  d.webinarId,
  d.webinar,
  COUNT(*) AS vistas_totales,
  SUM(CASE WHEN d.completado = 1 THEN 1 ELSE 0 END) AS vistas_completas,
  SUM(d.posSeg) AS watchTime_aprox_seg
FROM vw_vistas_detalle d
WHERE d.videoId IS NOT NULL
GROUP BY d.videoId, d.video, d.webinarId, d.webinar;
