import sys
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
sys.path.append("..")




########################Engine########################

engine=create_engine('postgresql://challenge:passer123@localhost:5432/donnees_elections')
base_session=sessionmaker(bind=engine,autocommit=False,autoflush=False)
session=base_session()
base=declarative_base()


######################Classe Region############################
class Region(base):
    __tablename__='regions'
    id_region=Column(Integer,primary_key=True,autoincrement=True)
    name_region=Column(String(50))
    departement=relationship("Departement")


    def __init__(self,name_region):
        self.name_region=name_region

    def remplirRegion(self):
            session.add(self)
            session.commit()
            session.close()
        

######################Classe Departement############################

class Departement(base):
    __tablename__='departement'
    id_depart=Column(Integer,primary_key=True)
    regionId=Column(Integer,ForeignKey('regions.id_region'))
    name_depart=Column(String(100))
    commune=relationship('Commune')

    def __init__(self,name_depart ,name_region):
        self.name_depart=name_depart
        self.name_region=name_region

    def remplissageDepart(self):
        self.regionId=session.query(Region).filter(Region.name_region==self.name_region).first().id_region
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

    def remplissageCom(self):
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


base.metadata.create_all(bind=engine)

def RecupNbrCommune():
    dic={}
 
    reg=session.query(Region).all()
    for i in reg:
        commune=0
        depart=session.query(Departement).filter(Departement.regionId==i.id_region).all()
        for k in depart:
            com=session.query(Commune).filter(Commune.departId==k.id_depart).all()
            commune+=len(com)
        dic[i.name_region]=commune
    return dic

def BureauCom():
    diccom={}
    commune=session.query(Commune).all()
    for i in commune:
                lieuv=0
                lieu=session.query(Lieu_de_Vote).filter(Lieu_de_Vote.communeId==i.id_commune).all()
                lieuv+=len(lieu)
                diccom[i.name_commune]=lieuv
    ndicom={}
    for k, v in sorted(diccom.items(), key=lambda x: x[1],reverse=True):
        if len(ndicom) <10:
              ndicom[k]=v
    return ndicom

def RecupElecteur():
    dic={}
    reg=session.query(Region.name_region,func.sum(Lieu_de_Vote.nombre_electeur)).filter(Region.id_region==Departement.regionId).filter(Departement.id_depart==Commune.departId).filter(Commune.id_commune==Lieu_de_Vote.communeId).group_by(Region.name_region).all()
    for i in reg:
       dic[i[0]]=i[1]
    return dic

def recupBureauVote():
    diclieu={}
    lieu=session.query(Lieu_de_Vote.name_lieu,Lieu_de_Vote.nombre_electeur).all()
    lieu.sort(key = lambda x: x[1],reverse=True)   #index 1 means second element
    for i in lieu:
        if len(diclieu)<10:
            diclieu[i[0]]=i[1]
    return diclieu


recupBureauVote()
