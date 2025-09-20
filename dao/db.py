from sqlmodel import create_engine, Session

Database_URL =  "mysql+pymysql://root:root@localhost/plataforma_webinars"
engine = create_engine(Database_URL)

class conexion:
    def __init__(self):
        self.session = Session(engine)
    def Conectar(self):
        self.session = Session(engine)
        return self.session
    def Desconectar(self):
        if self.session:
            self.session.close()
            self.session = None
        return True
    def get_session(self):
        if self.session is None:
            self.session = Session(engine)
        return self.session   