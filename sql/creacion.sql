
-- ============================================================
-- 0) Crear Base de Datos  y usarla
-- ============================================================
CREATE DATABASE  plataforma_webinars;

USE plataforma_webinars;



-- ============================================================
-- 2) Tablas
-- ============================================================

-- Usuarios / Autenticación
CREATE TABLE Usuarios (
  idUsuario     CHAR(36) NOT NULL PRIMARY KEY,
  username      VARCHAR(100) NOT NULL UNIQUE,
  passwordHash  VARCHAR(255) NOT NULL,
  mail          VARCHAR(150),
  isActive      BOOLEAN NOT NULL DEFAULT TRUE,
  createdAt     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Tutores
CREATE TABLE Tutores (
  idTutor     CHAR(36) NOT NULL PRIMARY KEY,
  nombre      VARCHAR(150) NOT NULL,
  mail        VARCHAR(150) NOT NULL,
  foto        VARCHAR(250),
  puesto      VARCHAR(150),
  urlLinkedin VARCHAR(250)
) ENGINE=InnoDB;

-- Webinars
CREATE TABLE Webinars (
  idWebinar       CHAR(36) NOT NULL PRIMARY KEY,
  nombre          VARCHAR(200) NOT NULL,
  descripcion     VARCHAR(1000),
  categoria       VARCHAR(100) NOT NULL DEFAULT 'default',
  dificultad      VARCHAR(50),
  imagen          VARCHAR(250),
  contenidoLibre  BOOLEAN NOT NULL DEFAULT TRUE,
  totalVideos     INT NOT NULL DEFAULT 0,
  tutorId         CHAR(36),
  CONSTRAINT fk_webinar_tutor FOREIGN KEY (tutorId)
    REFERENCES Tutores(idTutor) ON DELETE SET NULL ON UPDATE CASCADE,
  INDEX idx_categoria (categoria)
) ENGINE=InnoDB;


-- Videos
CREATE TABLE Videos (
  idVideo      CHAR(36) NOT NULL PRIMARY KEY,
  idWebinar    CHAR(36) NOT NULL,
  titulo       VARCHAR(200) NOT NULL,
  duracionSeg  INT NOT NULL DEFAULT 0,
  descripcion  VARCHAR(500),
  url          VARCHAR(250),
  libre        BOOLEAN NOT NULL DEFAULT TRUE,
  miniatura    VARCHAR(250),
  CONSTRAINT fk_video_webinar FOREIGN KEY (idWebinar)
    REFERENCES Webinars(idWebinar) ON DELETE CASCADE ON UPDATE CASCADE,
  INDEX idx_video_webinar (idWebinar)
) ENGINE=InnoDB;

-- Material de Apoyo
CREATE TABLE MaterialApoyo (
  idMaterial  CHAR(36) NOT NULL PRIMARY KEY,
  idVideo     CHAR(36) NOT NULL,
  nombre      VARCHAR(200) NOT NULL,
  url         VARCHAR(250) NOT NULL,
  descargas   INT NOT NULL DEFAULT 0,
  free        BOOLEAN NOT NULL DEFAULT FALSE,
  CONSTRAINT fk_material_video FOREIGN KEY (idVideo)
    REFERENCES Videos(idVideo) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Vistas / Playback
CREATE TABLE VistasWebinar (
  idVista     CHAR(36) NOT NULL PRIMARY KEY,
  userId      CHAR(36) NOT NULL,
  webinarId   CHAR(36) NOT NULL,
  videoId     CHAR(36),
  startedAt   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  lastSeenAt  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  posSeg      INT NOT NULL DEFAULT 0,
  completado  BOOLEAN NOT NULL DEFAULT FALSE,
  activo      BOOLEAN NOT NULL DEFAULT TRUE,
  CONSTRAINT fk_vista_usuario FOREIGN KEY (userId)
    REFERENCES Usuarios(idUsuario) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_vista_webinar FOREIGN KEY (webinarId)
    REFERENCES Webinars(idWebinar) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_vista_video FOREIGN KEY (videoId)
    REFERENCES Videos(idVideo) ON DELETE SET NULL ON UPDATE CASCADE,
  INDEX idx_vista_user (userId),
  INDEX idx_vista_webinar (webinarId),
  INDEX idx_vista_video (videoId),
  INDEX idx_vista_user_activo (userId, activo)
) ENGINE=InnoDB;






