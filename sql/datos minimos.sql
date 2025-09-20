-- ============================================================
-- 5) (Opcional) Datos de ejemplo mínimos
-- ============================================================

INSERT INTO Usuarios (idUsuario, username, passwordHash, mail) VALUES
(UUID(), 'maria', '$2b$10$HASHBCRYPT', 'maria@ejemplo.com');

INSERT INTO Tutores (idTutor, nombre, mail) VALUES
(UUID(), 'Ana Pérez', 'ana@tutores.com');

-- Toma los IDs generados 
SET @uid := (SELECT idUsuario FROM Usuarios WHERE username='maria' LIMIT 1);
SET @tid := (SELECT idTutor FROM Tutores WHERE nombre='Ana Pérez' LIMIT 1);

INSERT INTO Webinars (idWebinar, nombre, categoria, dificultad, contenidoLibre, tutorId)
VALUES (UUID(), 'Intro a IA', 'IA', 'Básico', TRUE, @tid);

SET @wid := (SELECT idWebinar FROM Webinars WHERE nombre='Intro a IA' LIMIT 1);

INSERT INTO Videos (idVideo, idWebinar, titulo, duracionSeg, libre)
VALUES (UUID(), @wid, 'Clase 1', 1800, TRUE);

SET @vid := (SELECT idVideo FROM Videos WHERE idWebinar=@wid LIMIT 1);


