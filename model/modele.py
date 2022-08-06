from email.policy import default
import sys
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
sys.path.append("..")




########################Engine########################

engine = create_engine('postgresql://challenge:passer123@localhost:5432/donnees_elections')
base_session = sessionmaker(bind=engine,autocommit=False,autoflush=False)
session = base_session()
base = declarative_base()


######################Classe Region############################
class Region(base):
    __tablename__='regions'
    id_region = Column(Integer, primary_key = True, autoincrement = True)
    name_region = Column(String(50))
    departement = relationship("Departement")


    def __init__(self,name_region):
        self.name_region = name_region

    def remplirregion(self):
            session.add(self)
            session.commit()
            session.close()
        

######################Classe Departement############################

class Departement(base):
    __tablename__ = 'departement'
    id_depart = Column(Integer,primary_key=True)
    regionId = Column(Integer,ForeignKey('regions.id_region'))
    name_depart = Column(String(100))
    commune = relationship('Commune')

    def __init__(self,name_depart ,name_region):
        self.name_depart = name_depart
        self.name_region = name_region

    def remplissageDepart(self):
        self.regionId = session.query(Region).filter(Region.name_region == self.name_region).first().id_region
        session.add(self)
        session.commit()
               

######################Classe Commune ############################

class Commune(base):
    __tablename__='commune'
    id_commune=Column(Integer,primary_key=True,autoincrement=True)
    departId=Column(Integer,ForeignKey('departement.id_depart'))
    name_commune=Column(String(100))
    lieu_de_vote=relationship('Lieu_de_Vote')



    def __init__(self,name_commune,name_depart):
        self.name_commune=name_commune
        self.name_depart=name_depart

    def remplissagecom(self):
        self.departId=session.query(Departement).filter(Departement.name_depart==self.name_depart).first().id_depart
        session.add(self)
        session.commit()





######################Classe Lieu de Vote ############################

class Lieu_de_Vote(base):
    __tablename__='lieu_de_vote'
    id_lieu=Column(Integer,primary_key=True,autoincrement=True)
    communeId=Column(Integer,ForeignKey('commune.id_commune'))
    name_lieu=Column(String(100))
    nombre_electeur=Column(Integer)

    def __init__(self, name_lieu,name_commune,nombre_electeur ):
        self. name_lieu= name_lieu
        self.name_commune=name_commune
        self.nombre_electeur=nombre_electeur

    def RemplirLieu(self):
        self.communeId=session.query(Commune).filter(Commune.name_commune==self.name_commune).first().id_commune
        session.add(self)
        session.commit()





###################### Classe  Loader##########################

class Loader(base):
    __tablename__ = "loader"
    id_loader = Column(Integer,primary_key=True,autoincrement=True)
    loaded = Column(Boolean,default=False)

    def __init__(self, loaded):
        self.loaded=loaded

    def RemplirLoader(self):
        print("mafé")
        session.add(self)
        session.commit()
        session.close()


def get_loader_status():
    return session.query(Loader).first()

def get_loaders():
    return session.query(Loader).all()


def update_loader_status():
    session.query(Loader).filter(Loader.id_loader == 1).update({Loader.loaded : True})
    session.commit()
    session.close()


def create_loader_status():
    state = Loader(False)
    state.RemplirLoader()


base.metadata.create_all(bind=engine)



