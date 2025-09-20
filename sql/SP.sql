-- ============================================================
-- 4) Stored Procedures
-- ============================================================

DELIMITER //

-- Usuarios
CREATE PROCEDURE sp_create_usuario (
  IN  p_username      VARCHAR(100),
  IN  p_passwordHash  VARCHAR(255),
  IN  p_mail          VARCHAR(150)
)
BEGIN
  DECLARE v_id CHAR(36);
  IF p_username IS NULL OR p_passwordHash IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'username y passwordHash son obligatorios';
  END IF;
  IF EXISTS (SELECT 1 FROM Usuarios WHERE username = p_username) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El username ya existe';
  END IF;
  SET v_id = UUID();
  INSERT INTO Usuarios (idUsuario, username, passwordHash, mail, isActive, createdAt)
  VALUES (v_id, p_username, p_passwordHash, p_mail, TRUE, CURRENT_TIMESTAMP);
  SELECT * FROM Usuarios WHERE idUsuario = v_id;
END//

CREATE PROCEDURE sp_change_password (
  IN  p_userId          CHAR(36),
  IN  p_newPasswordHash VARCHAR(255)
)
BEGIN
  IF p_userId IS NULL OR p_newPasswordHash IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'userId y newPasswordHash son obligatorios';
  END IF;
  UPDATE Usuarios SET passwordHash = p_newPasswordHash WHERE idUsuario = p_userId;
  IF ROW_COUNT() = 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Usuario no encontrado';
  END IF;
  SELECT idUsuario, username, mail, isActive, createdAt FROM Usuarios WHERE idUsuario = p_userId;
END//

CREATE PROCEDURE sp_deactivate_usuario (IN p_userId CHAR(36))
BEGIN
  UPDATE Usuarios SET isActive = FALSE WHERE idUsuario = p_userId;
  IF ROW_COUNT() = 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Usuario no encontrado';
  END IF;
  SELECT idUsuario, username, isActive FROM Usuarios WHERE idUsuario = p_userId;
END//


DELIMITER //
CREATE PROCEDURE sp_list_usuarios (
  IN p_q VARCHAR(100),        
  IN p_active TINYINT,        
  IN p_offset INT,
  IN p_limit INT
)
BEGIN
  DECLARE v_offset INT DEFAULT 0;
  DECLARE v_limit INT DEFAULT 50;

  SET v_offset = IFNULL(p_offset, 0);
  SET v_limit  = IFNULL(p_limit, 50);

  SELECT idUsuario, username, mail, isActive, createdAt
  FROM Usuarios
  WHERE (p_q IS NULL OR p_q = '' OR username LIKE CONCAT('%', p_q, '%') OR mail LIKE CONCAT('%', p_q, '%'))
    AND (p_active IS NULL OR isActive = p_active)
  ORDER BY createdAt DESC
  LIMIT v_offset, v_limit;
END//
DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_get_usuario_by_id (IN p_userId CHAR(36))
BEGIN
  SELECT idUsuario, username, mail, isActive, createdAt
  FROM Usuarios
  WHERE idUsuario = p_userId
  LIMIT 1;
END//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_update_usuario (
  IN p_userId   CHAR(36),
  IN p_username VARCHAR(100),
  IN p_mail     VARCHAR(150),
  IN p_isActive TINYINT
)
BEGIN
  IF NOT EXISTS (SELECT 1 FROM Usuarios WHERE idUsuario = p_userId) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Usuario no encontrado';
  END IF;

  -- si se manda username, validar unicidad
  IF p_username IS NOT NULL AND EXISTS (
    SELECT 1 FROM Usuarios WHERE username = p_username AND idUsuario <> p_userId
  ) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El username ya existe';
  END IF;

  UPDATE Usuarios
     SET username = COALESCE(p_username, username),
         mail     = COALESCE(p_mail, mail),
         isActive = COALESCE(p_isActive, isActive)
   WHERE idUsuario = p_userId;

  SELECT idUsuario, username, mail, isActive, createdAt
  FROM Usuarios
  WHERE idUsuario = p_userId;
END//
DELIMITER ;



-- Tutores

DELIMITER //
CREATE PROCEDURE sp_create_tutor (
  IN p_nombre VARCHAR(150),
  IN p_mail   VARCHAR(150),
  IN p_foto   VARCHAR(250),
  IN p_puesto VARCHAR(150),
  IN p_urlLinkedin VARCHAR(250)
)
BEGIN
  DECLARE v_id CHAR(36);
  IF p_nombre IS NULL OR p_mail IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'nombre y mail son obligatorios';
  END IF;

  SET v_id = UUID();
  INSERT INTO Tutores(idTutor, nombre, mail, foto, puesto, urlLinkedin)
  VALUES (v_id, p_nombre, p_mail, p_foto, p_puesto, p_urlLinkedin);

  SELECT * FROM Tutores WHERE idTutor = v_id;
END//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_update_tutor (
  IN p_idTutor CHAR(36),
  IN p_nombre VARCHAR(150),
  IN p_mail   VARCHAR(150),
  IN p_foto   VARCHAR(250),
  IN p_puesto VARCHAR(150),
  IN p_urlLinkedin VARCHAR(250)
)
BEGIN
  IF NOT EXISTS (SELECT 1 FROM Tutores WHERE idTutor = p_idTutor) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Tutor no encontrado';
  END IF;

  UPDATE Tutores
     SET nombre = COALESCE(p_nombre, nombre),
         mail   = COALESCE(p_mail, mail),
         foto   = COALESCE(p_foto, foto),
         puesto = COALESCE(p_puesto, puesto),
         urlLinkedin = COALESCE(p_urlLinkedin, urlLinkedin)
   WHERE idTutor = p_idTutor;

  SELECT * FROM Tutores WHERE idTutor = p_idTutor;
END//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_get_tutor_by_id (IN p_idTutor CHAR(36))
BEGIN
  SELECT idTutor, nombre, mail, foto, puesto, urlLinkedin
  FROM Tutores
  WHERE idTutor = p_idTutor
  LIMIT 1;
END//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_list_tutores (
  IN p_q VARCHAR(150),   -- busca en nombre/mail/puesto
  IN p_offset INT,
  IN p_limit INT
)
BEGIN
  DECLARE v_offset INT DEFAULT 0;
  DECLARE v_limit  INT DEFAULT 50;
  SET v_offset = IFNULL(p_offset, 0);
  SET v_limit  = IFNULL(p_limit, 50);

  SELECT idTutor, nombre, mail, foto, puesto, urlLinkedin
  FROM Tutores
  WHERE (p_q IS NULL OR p_q = '' OR
         nombre LIKE CONCAT('%', p_q, '%') OR
         mail   LIKE CONCAT('%', p_q, '%') OR
         puesto LIKE CONCAT('%', p_q, '%'))
  ORDER BY nombre
  LIMIT v_offset, v_limit;
END//
DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_list_webinars_by_tutor (
  IN p_idTutor CHAR(36),
  IN p_offset INT,
  IN p_limit INT
)
BEGIN
  DECLARE v_offset INT DEFAULT 0;
  DECLARE v_limit  INT DEFAULT 50;
  SET v_offset = IFNULL(p_offset, 0);
  SET v_limit  = IFNULL(p_limit, 50);

  IF NOT EXISTS (SELECT 1 FROM Tutores WHERE idTutor = p_idTutor) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Tutor no encontrado';
  END IF;

  SELECT w.idWebinar, w.nombre, w.categoria, w.dificultad, w.totalVideos, w.contenidoLibre
  FROM Webinars w
  WHERE w.tutorId = p_idTutor
  ORDER BY w.nombre
  LIMIT v_offset, v_limit;
END//
DELIMITER ;

-- Webinars


DELIMITER //
CREATE PROCEDURE sp_create_webinar (
  IN  p_nombre         VARCHAR(200),
  IN  p_descripcion    VARCHAR(1000),
  IN  p_categoria      VARCHAR(100),
  IN  p_dificultad     VARCHAR(50),
  IN  p_imagen         VARCHAR(250),
  IN  p_contenidoLibre TINYINT,   -- 1/0
  IN  p_tutorId        CHAR(36)   -- NULL permitido
)
BEGIN
  DECLARE v_id CHAR(36);
  IF p_nombre IS NULL OR p_nombre = '' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'nombre es obligatorio';
  END IF;
  IF p_tutorId IS NOT NULL AND NOT EXISTS (SELECT 1 FROM Tutores WHERE idTutor = p_tutorId) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'tutorId no existe';
  END IF;

  SET v_id = UUID();
  INSERT INTO Webinars (
    idWebinar, nombre, descripcion, categoria, dificultad, imagen,
    contenidoLibre, totalVideos, tutorId
  ) VALUES (
    v_id,
    p_nombre,
    p_descripcion,
    COALESCE(p_categoria, 'default'),
    p_dificultad,
    p_imagen,
    COALESCE(p_contenidoLibre, 1),
    0,
    p_tutorId
  );

  SELECT * FROM Webinars WHERE idWebinar = v_id;
END//
DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_update_webinar (
  IN p_idWebinar CHAR(36),
  IN p_nombre VARCHAR(200),
  IN p_descripcion VARCHAR(1000),
  IN p_categoria VARCHAR(100),
  IN p_dificultad VARCHAR(50),
  IN p_imagen VARCHAR(250),
  IN p_contenidoLibre TINYINT
)
BEGIN
  IF NOT EXISTS (SELECT 1 FROM Webinars WHERE idWebinar = p_idWebinar) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Webinar no encontrado';
  END IF;

  UPDATE Webinars
     SET nombre = COALESCE(p_nombre, nombre),
         descripcion = COALESCE(p_descripcion, descripcion),
         categoria = COALESCE(p_categoria, categoria),
         dificultad = COALESCE(p_dificultad, dificultad),
         imagen = COALESCE(p_imagen, imagen),
         contenidoLibre = COALESCE(p_contenidoLibre, contenidoLibre)
   WHERE idWebinar = p_idWebinar;

  SELECT * FROM Webinars WHERE idWebinar = p_idWebinar;
END//
DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_get_webinar_by_id (IN p_idWebinar CHAR(36))
BEGIN
  SELECT idWebinar, nombre, descripcion, categoria, dificultad, imagen,
         contenidoLibre, totalVideos, tutorId
  FROM Webinars
  WHERE idWebinar = p_idWebinar
  LIMIT 1;
END//
DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_list_webinars (
  IN p_q VARCHAR(200),         -- busca en nombre/descripcion
  IN p_categoria VARCHAR(100), -- filtra por categoria
  IN p_contenidoLibre TINYINT, -- 1/0 o NULL
  IN p_tutorId CHAR(36),       -- NULL = cualquiera
  IN p_offset INT,
  IN p_limit INT
)
BEGIN
  DECLARE v_offset INT DEFAULT 0;
  DECLARE v_limit  INT DEFAULT 50;
  SET v_offset = IFNULL(p_offset, 0);
  SET v_limit  = IFNULL(p_limit, 50);

  SELECT idWebinar, nombre, descripcion, categoria, dificultad, imagen,
         contenidoLibre, totalVideos, tutorId
  FROM Webinars
  WHERE (p_q IS NULL OR p_q = '' OR nombre LIKE CONCAT('%', p_q, '%') OR descripcion LIKE CONCAT('%', p_q, '%'))
    AND (p_categoria IS NULL OR categoria = p_categoria)
    AND (p_contenidoLibre IS NULL OR contenidoLibre = p_contenidoLibre)
    AND (p_tutorId IS NULL OR tutorId = p_tutorId)
  ORDER BY nombre
  LIMIT v_offset, v_limit;
END//
DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_assign_webinar_tutor (
  IN p_idWebinar CHAR(36),
  IN p_tutorId   CHAR(36)
)
BEGIN
  IF NOT EXISTS (SELECT 1 FROM Webinars WHERE idWebinar = p_idWebinar) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Webinar no encontrado';
  END IF;
  IF NOT EXISTS (SELECT 1 FROM Tutores WHERE idTutor = p_tutorId) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Tutor no encontrado';
  END IF;

  UPDATE Webinars SET tutorId = p_tutorId WHERE idWebinar = p_idWebinar;
  SELECT * FROM Webinars WHERE idWebinar = p_idWebinar;
END//
DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_list_videos_by_webinar (
  IN p_idWebinar CHAR(36),
  IN p_offset INT,
  IN p_limit INT
)
BEGIN
  DECLARE v_offset INT DEFAULT 0;
  DECLARE v_limit  INT DEFAULT 50;
  SET v_offset = IFNULL(p_offset, 0);
  SET v_limit  = IFNULL(p_limit, 50);

  IF NOT EXISTS (SELECT 1 FROM Webinars WHERE idWebinar = p_idWebinar) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Webinar no encontrado';
  END IF;

  SELECT idVideo, idWebinar, titulo, duracionSeg, descripcion, url, libre, miniatura
  FROM Videos
  WHERE idWebinar = p_idWebinar
  ORDER BY titulo
  LIMIT v_offset, v_limit;
END//
DELIMITER ;



-- Videos


DELIMITER //
CREATE PROCEDURE sp_create_video (
  IN  p_idWebinar   CHAR(36),
  IN  p_titulo      VARCHAR(200),
  IN  p_duracionSeg INT,
  IN  p_descripcion VARCHAR(500),
  IN  p_url         VARCHAR(250),
  IN  p_libre       TINYINT,
  IN  p_miniatura   VARCHAR(250)
)
BEGIN
  DECLARE v_id CHAR(36);
  IF p_idWebinar IS NULL OR p_titulo IS NULL OR p_titulo = '' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'idWebinar y titulo son obligatorios';
  END IF;
  IF NOT EXISTS (SELECT 1 FROM Webinars WHERE idWebinar = p_idWebinar) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'idWebinar no existe';
  END IF;

  SET v_id = UUID();
  INSERT INTO Videos (idVideo, idWebinar, titulo, duracionSeg, descripcion, url, libre, miniatura)
  VALUES (v_id, p_idWebinar, p_titulo, COALESCE(p_duracionSeg,0), p_descripcion, p_url, COALESCE(p_libre,1), p_miniatura);

  -- recontar videos del webinar
  UPDATE Webinars w
     SET totalVideos = (SELECT COUNT(*) FROM Videos v WHERE v.idWebinar = w.idWebinar)
   WHERE w.idWebinar = p_idWebinar;

  SELECT * FROM Videos WHERE idVideo = v_id;
END//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_update_video (
  IN p_idVideo CHAR(36),
  IN p_titulo VARCHAR(200),
  IN p_duracionSeg INT,
  IN p_descripcion VARCHAR(500),
  IN p_url VARCHAR(250),
  IN p_libre TINYINT,
  IN p_miniatura VARCHAR(250)
)
BEGIN
  IF NOT EXISTS (SELECT 1 FROM Videos WHERE idVideo = p_idVideo) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Video no encontrado';
  END IF;

  UPDATE Videos
     SET titulo = COALESCE(p_titulo, titulo),
         duracionSeg = COALESCE(p_duracionSeg, duracionSeg),
         descripcion = COALESCE(p_descripcion, descripcion),
         url = COALESCE(p_url, url),
         libre = COALESCE(p_libre, libre),
         miniatura = COALESCE(p_miniatura, miniatura)
   WHERE idVideo = p_idVideo;

  SELECT * FROM Videos WHERE idVideo = p_idVideo;
END//
DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_get_video_by_id (IN p_idVideo CHAR(36))
BEGIN
  SELECT idVideo, idWebinar, titulo, duracionSeg, descripcion, url, libre, miniatura
  FROM Videos
  WHERE idVideo = p_idVideo
  LIMIT 1;
END//
DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_list_videos (
  IN p_q VARCHAR(200),          -- busca en título/descr
  IN p_idWebinar CHAR(36),      -- NULL = cualquiera
  IN p_libre TINYINT,           -- 1/0/NULL
  IN p_offset INT,
  IN p_limit INT
)
BEGIN
  DECLARE v_offset INT DEFAULT 0;
  DECLARE v_limit  INT DEFAULT 50;
  SET v_offset = IFNULL(p_offset, 0);
  SET v_limit  = IFNULL(p_limit, 50);

  SELECT idVideo, idWebinar, titulo, duracionSeg, descripcion, url, libre, miniatura
  FROM Videos
  WHERE (p_q IS NULL OR p_q = '' OR titulo LIKE CONCAT('%',p_q,'%') OR descripcion LIKE CONCAT('%',p_q,'%'))
    AND (p_idWebinar IS NULL OR idWebinar = p_idWebinar)
    AND (p_libre IS NULL OR libre = p_libre)
  ORDER BY titulo
  LIMIT v_offset, v_limit;
END//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_attach_video_to_webinar (
  IN p_idVideo CHAR(36),
  IN p_idWebinar CHAR(36)
)
BEGIN
  IF NOT EXISTS (SELECT 1 FROM Videos WHERE idVideo = p_idVideo) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Video no encontrado';
  END IF;
  IF NOT EXISTS (SELECT 1 FROM Webinars WHERE idWebinar = p_idWebinar) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Webinar no encontrado';
  END IF;

  UPDATE Videos SET idWebinar = p_idWebinar WHERE idVideo = p_idVideo;

  UPDATE Webinars w
     SET totalVideos = (SELECT COUNT(*) FROM Videos v WHERE v.idWebinar = w.idWebinar)
   WHERE w.idWebinar = p_idWebinar;

  SELECT * FROM Videos WHERE idVideo = p_idVideo;
END//
DELIMITER ;


-- Material de Apoyo


DELIMITER //
CREATE PROCEDURE sp_create_material (
  IN p_idVideo   CHAR(36),
  IN p_nombre    VARCHAR(200),
  IN p_url       VARCHAR(500),
  IN p_free      TINYINT
)
BEGIN
  DECLARE v_id CHAR(36);
  IF p_idVideo IS NULL OR p_nombre IS NULL OR p_nombre = '' OR p_url IS NULL OR p_url = '' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'idVideo, nombre y url son obligatorios';
  END IF;
  IF NOT EXISTS (SELECT 1 FROM Videos WHERE idVideo = p_idVideo) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'idVideo no existe';
  END IF;

  SET v_id = UUID();
  INSERT INTO MaterialApoyo (idMaterial, idVideo, nombre, url, free)
  VALUES (v_id, p_idVideo, p_nombre, p_url, COALESCE(p_free,0));

  SELECT idMaterial, idVideo, nombre, url, descargas, free
  FROM MaterialApoyo WHERE idMaterial = v_id;
END//
DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_update_material (
  IN p_idMaterial CHAR(36),
  IN p_nombre     VARCHAR(200),
  IN p_url        VARCHAR(500),
  IN p_free       TINYINT
)
BEGIN
  IF NOT EXISTS (SELECT 1 FROM MaterialApoyo WHERE idMaterial = p_idMaterial) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Material no encontrado';
  END IF;

  UPDATE MaterialApoyo
     SET nombre = COALESCE(p_nombre, nombre),
         url    = COALESCE(p_url, url),
         free   = COALESCE(p_free, free)
   WHERE idMaterial = p_idMaterial;

  SELECT idMaterial, idVideo, nombre, url, descargas, free
  FROM MaterialApoyo WHERE idMaterial = p_idMaterial;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE sp_get_material_by_id (IN p_idMaterial CHAR(36))
BEGIN
  SELECT idMaterial, idVideo, nombre, url, descargas, free
  FROM MaterialApoyo
  WHERE idMaterial = p_idMaterial
  LIMIT 1;
END//
DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_list_materiales (
  IN p_q VARCHAR(200),       -- busca por nombre
  IN p_idVideo CHAR(36),     -- filtra por video
  IN p_free TINYINT,         -- 1/0/NULL
  IN p_offset INT,
  IN p_limit INT
)
BEGIN
  DECLARE v_offset INT DEFAULT 0;
  DECLARE v_limit  INT DEFAULT 50;
  SET v_offset = IFNULL(p_offset, 0);
  SET v_limit  = IFNULL(p_limit, 50);

  SELECT idMaterial, idVideo, nombre, url, descargas, free
  FROM MaterialApoyo
  WHERE (p_q IS NULL OR p_q = '' OR nombre LIKE CONCAT('%',p_q,'%'))
    AND (p_idVideo IS NULL OR idVideo = p_idVideo)
    AND (p_free IS NULL OR free = p_free)
  ORDER BY nombre
  LIMIT v_offset, v_limit;
END//
DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_delete_material (IN p_idMaterial CHAR(36))
BEGIN
  IF NOT EXISTS (SELECT 1 FROM MaterialApoyo WHERE idMaterial = p_idMaterial) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Material no encontrado';
  END IF;
  DELETE FROM MaterialApoyo WHERE idMaterial = p_idMaterial;
  SELECT 1 AS deleted;
END//
DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_increment_descarga_material (IN p_idMaterial CHAR(36))
BEGIN
  IF NOT EXISTS (SELECT 1 FROM MaterialApoyo WHERE idMaterial = p_idMaterial) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Material no encontrado';
  END IF;
  UPDATE MaterialApoyo SET descargas = descargas + 1 WHERE idMaterial = p_idMaterial;
  SELECT idMaterial, idVideo, nombre, url, descargas, free
  FROM MaterialApoyo WHERE idMaterial = p_idMaterial;
END//
DELIMITER ;


-- Playback / Visualización----------------------------
CREATE INDEX idx_vistas_user_webinar ON VistasWebinar (userId, webinarId, activo);

DELIMITER //
CREATE PROCEDURE sp_play_start(
  IN p_userId    CHAR(36),
  IN p_webinarId CHAR(36),
  IN p_videoId   CHAR(36)
)
BEGIN
  DECLARE v_id CHAR(36);
  IF NOT EXISTS (SELECT 1 FROM Usuarios  WHERE idUsuario = p_userId)    THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Usuario no existe'; END IF;
  IF NOT EXISTS (SELECT 1 FROM Webinars WHERE idWebinar = p_webinarId)  THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Webinar no existe'; END IF;
  IF p_videoId IS NOT NULL AND NOT EXISTS (SELECT 1 FROM Videos WHERE idVideo = p_videoId AND idWebinar = p_webinarId)
  THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Video no existe en el webinar'; END IF;

  -- Cerrar cualquier sesión activa previa del usuario en ese webinar
  UPDATE VistasWebinar
     SET activo = 0, lastSeenAt = NOW()
   WHERE userId = p_userId AND webinarId = p_webinarId AND activo = 1;

  SET v_id = UUID();
  INSERT INTO VistasWebinar (idVista, userId, webinarId, videoId, startedAt, lastSeenAt, posSeg, completado, activo)
  VALUES (v_id, p_userId, p_webinarId, p_videoId, NOW(), NOW(), 0, 0, 1);

  SELECT * FROM VistasWebinar WHERE idVista = v_id;
END//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_play_update(
  IN p_idVista  CHAR(36),
  IN p_videoId  CHAR(36),
  IN p_posSeg   INT
)
BEGIN
  IF NOT EXISTS (SELECT 1 FROM VistasWebinar WHERE idVista = p_idVista) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Vista no encontrada';
  END IF;

  UPDATE VistasWebinar
     SET videoId   = COALESCE(p_videoId, videoId),
         posSeg    = COALESCE(p_posSeg, posSeg),
         lastSeenAt = NOW()
   WHERE idVista = p_idVista;

  SELECT * FROM VistasWebinar WHERE idVista = p_idVista;
END//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_play_complete(
  IN p_idVista CHAR(36)
)
BEGIN
  IF NOT EXISTS (SELECT 1 FROM VistasWebinar WHERE idVista = p_idVista) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Vista no encontrada';
  END IF;

  UPDATE VistasWebinar
     SET completado = 1,
         activo = 0,
         lastSeenAt = NOW()
   WHERE idVista = p_idVista;

  SELECT * FROM VistasWebinar WHERE idVista = p_idVista;
END//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_play_stop(
  IN p_idVista CHAR(36)
)
BEGIN
  IF NOT EXISTS (SELECT 1 FROM VistasWebinar WHERE idVista = p_idVista) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Vista no encontrada';
  END IF;

  UPDATE VistasWebinar
     SET activo = 0,
         lastSeenAt = NOW()
   WHERE idVista = p_idVista;

  SELECT * FROM VistasWebinar WHERE idVista = p_idVista;
END//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_play_switch_video(
  IN p_idVista CHAR(36),
  IN p_videoId CHAR(36)
)
BEGIN
  DECLARE v_webinar CHAR(36);
  IF NOT EXISTS (SELECT 1 FROM VistasWebinar WHERE idVista = p_idVista) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Vista no encontrada';
  END IF;

  SELECT webinarId INTO v_webinar FROM VistasWebinar WHERE idVista = p_idVista LIMIT 1;
  IF NOT EXISTS (SELECT 1 FROM Videos WHERE idVideo = p_videoId AND idWebinar = v_webinar) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Video no pertenece al webinar de la vista';
  END IF;

  UPDATE VistasWebinar
     SET videoId = p_videoId,
         posSeg = 0,
         lastSeenAt = NOW()
   WHERE idVista = p_idVista;

  SELECT * FROM VistasWebinar WHERE idVista = p_idVista;
END//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_play_list_by_user(
  IN p_userId CHAR(36),
  IN p_offset INT,
  IN p_limit  INT
)
BEGIN
  DECLARE v_offset INT DEFAULT 0;
  DECLARE v_limit  INT DEFAULT 50;
  SET v_offset = IFNULL(p_offset, 0);
  SET v_limit  = IFNULL(p_limit, 50);

  SELECT * FROM VistasWebinar
  WHERE userId = p_userId
  ORDER BY startedAt DESC
  LIMIT v_offset, v_limit;
END//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_play_get_by_id(IN p_idVista CHAR(36))
BEGIN
  SELECT * FROM VistasWebinar WHERE idVista = p_idVista LIMIT 1;
END//
DELIMITER ;
