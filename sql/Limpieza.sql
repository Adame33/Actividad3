-- ============================================================
-- 1) Limpieza opcional: DROPs (para re-ejecutar el script)
--    (Se dropean vistas y SP antes, luego tablas en orden de FKs)
-- ============================================================
-- Vistas
DROP VIEW IF EXISTS vw_metricas_video;
DROP VIEW IF EXISTS vw_metricas_webinar;
DROP VIEW IF EXISTS vw_vista_activa_por_usuario;
DROP VIEW IF EXISTS vw_vistas_detalle;
DROP VIEW IF EXISTS vw_materiales_con_origen;
DROP VIEW IF EXISTS vw_videos_con_webinar;
DROP VIEW IF EXISTS vw_webinars_resumen;
DROP VIEW IF EXISTS vw_catalogo_videos;
DROP VIEW IF EXISTS vw_catalogo_webinars;
DROP VIEW IF EXISTS vw_catalogo_tutores;

-- Stored Procedures
DROP PROCEDURE IF EXISTS sp_create_usuario;
DROP PROCEDURE IF EXISTS sp_change_password;
DROP PROCEDURE IF EXISTS sp_deactivate_usuario;

DROP PROCEDURE IF EXISTS sp_create_tutor;
DROP PROCEDURE IF EXISTS sp_update_tutor;

DROP PROCEDURE IF EXISTS sp_create_webinar;
DROP PROCEDURE IF EXISTS sp_set_webinar_publicacion;
DROP PROCEDURE IF EXISTS sp_assign_webinar_tutor;
DROP PROCEDURE IF EXISTS sp_recount_videos_for_webinar;
DROP PROCEDURE IF EXISTS sp_update_webinar;

DROP PROCEDURE IF EXISTS sp_create_video;
DROP PROCEDURE IF EXISTS sp_update_video;
DROP PROCEDURE IF EXISTS sp_attach_video_to_webinar;

DROP PROCEDURE IF EXISTS sp_create_material;
DROP PROCEDURE IF EXISTS sp_update_material;
DROP PROCEDURE IF EXISTS sp_incrementar_descarga_material;

DROP PROCEDURE IF EXISTS sp_start_vista;
DROP PROCEDURE IF EXISTS sp_progress_vista;
DROP PROCEDURE IF EXISTS sp_switch_video;
DROP PROCEDURE IF EXISTS sp_complete_vista;
DROP PROCEDURE IF EXISTS sp_close_vista;

-- Tablas (orden inverso de dependencias)
DROP TABLE IF EXISTS MaterialApoyo;
DROP TABLE IF EXISTS VistasWebinar;
DROP TABLE IF EXISTS Videos;
DROP TABLE IF EXISTS Webinars;
DROP TABLE IF EXISTS Tutores;
DROP TABLE IF EXISTS Usuarios;