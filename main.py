# main.py
from fastapi import FastAPI
import uvicorn

# conexión a BD
from dao.db import conexion

# Routers
from routes.usuarios import router as usuarios_router
from routes.tutores import router as tutores_router
from routes.webinars import router as webinars_router
from routes.videos import router as videos_router
from routes.materiales import router as materiales_router
from routes.playback import router as playback_router





def create_app() -> FastAPI:
    app = FastAPI(title="API Plataforma Webinars")

    # --- Startup / Shutdown ---
    @app.on_event("startup")
    def startup_event():
        db_conn = conexion()
        session = db_conn.get_session()
        app.state.db_session = session
        print("Conexión a la base de datos establecida.")

    @app.on_event("shutdown")
    def shutdown_event():
        sess = getattr(app.state, "db_session", None)
        if sess:
            try:
                sess.close()
                print("Sesión de BD cerrada.")
            except:
                pass

    # --- Rutas base ---
    @app.get("/")
    async def healthcheck():
        return {"message": "API funcionando correctamente"}

    # --- Registrar routers ---
    app.include_router(usuarios_router, tags=["Usuarios"])
    app.include_router(tutores_router, tags=["Tutores"])
    app.include_router(webinars_router, tags=["Webinars"])
    app.include_router(videos_router, tags=["Videos"])
    app.include_router(materiales_router, tags=["Materiales"])
    app.include_router(playback_router, tags=["Playback"])

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=8000)
