from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *


########################Engine########################

engine=create_engine('postgresql://challenge:passer123@localhost:5432/donnees_elections')
base_session=sessionmaker(bind=engine,autocommit=False,autoflush=False)
session=base_session()
base=declarative_base()


######################Classe Region############################
class Region(base):
    __tablename__='regions'
    id_region=Column(Integer,primary_key=True)
    name_region=Column(String(50))
    departement=relationship("Departement")

    def __init__(self,id_region,name_region):
        self.id_region=id_region
        self.name_region=name_region
    

######################Classe Departement############################

class Departement(base):
    __tablename__='departement'
    id_depart=Column(Integer,primary_key=True)
    regionId=Column(Integer,ForeignKey('regions.id_region'))
    name_depart=Column(String(100))
    commune=relationship('Commune')


    def __init__(self,id_depart,name_depart ):
        self.id_depart=id_depart
        self.name_depart=name_depart



######################Classe Commune ############################

class Commune(base):
    __tablename__='commune'
    id_commune=Column(Integer,primary_key=True)
    departId=Column(Integer,ForeignKey('departement.id_depart'))
    name_commune=Column(String(100))
    lieu_de_vote=relationship('Lieu_de_Vote')



    def __init__(self,id_commune,name_commune ):
        self.id_commune=id_commune
        self.name_commune=name_commune



######################Classe Commune ############################

class Lieu_de_Vote(base):
    __tablename__='lieu_de_vote'
    id_lieu=Column(Integer,primary_key=True)
    communeId=Column(Integer,ForeignKey('commune.id_commune'))
    name_lieu=Column(String(100))
    nombre_de_vote=Column(Integer)


    def __init__(self,id_lieu,name_lieu ):
        self.id_lieu=id_lieu
        self.name_lieu=name_lieu

base.metadata.create_all(bind=engine)