import csv
import sys
sys.path.append(".")
sys.path.append("..")
# sys.path.append("../model")

from model.modele import *

chemin1 = "./datas/DAKAR.csv"
chemin2 = "./datas/KAOLACK.csv"
chemin3 = "./datas/SAINT LOUIS.csv"
chemin4 = "./datas/THIES.csv"
chemin5 = "./datas/ZIGUINCHOR.csv"





##################################FONCTION DE LECTURE DES FICHIER CSV#########################

def lecteurcsv(chemin):
    
    data = []

    with open(chemin) as f:
        
        myreader=csv.DictReader(f)

        for row in myreader:
            
            data.append(row)
        
        return data


################################RECUPERATION DES FICHIERE SUR DES LISTES DE DICTIONNAIRE###########################################
liDakar = lecteurcsv(chemin1)
liKaolack = lecteurcsv(chemin2)
liSaint_Louis = lecteurcsv(chemin3)
liThies = lecteurcsv(chemin4)
liZig = lecteurcsv(chemin5)


###################Fonction de traitement###############################

def traitementdata(li):
    n = 0
    nli = []
    
    for i in range(len(li)):
        
        if i == 0:
            n += int(li[i]["ÉLECTEURS"])
            l = li[i]["LIEU DE VOTE"]
        
        else:
            
            if li[i]["LIEU DE VOTE"]==l:
                n+=int(li[i]["ÉLECTEURS"])
            
            else:
                ndict={}
                ndict["Departement"]=li[i-1]["DÉPARTEMENT"]
                ndict["Commune"]=li[i-1]["COMMUNES"]
                ndict["Lieu de Vote"]=li[i-1]["LIEU DE VOTE"]
                ndict["Nombre electeur"]=n
                nli.append(ndict)
                n=0
                l=li[i]["LIEU DE VOTE"]
                n+=int(li[i]["ÉLECTEURS"])

    return nli
                


################Les donnees pretes à etre inserer dans la base###################################


nliDakar=traitementdata(liDakar)
# print(nliDakar[0].keys())

nliKaolack=traitementdata(liKaolack)
nliSaint_Louis=traitementdata(liSaint_Louis)
nliThies=traitementdata(liThies)
nliZig=traitementdata(liZig)
data= {"DAKAR":nliDakar,"KAOLACK":nliKaolack,"SAINT LOUIS":nliSaint_Louis,"THIES":nliThies,"ZIGUINCHOR":nliZig}


###################### Remplissage ###########################################################

def chargerregion(data):
   for i in data:
       reg=str(i)
       region=Region(reg)
       region.remplirRegion()


def chargerdepart(datadepart,region):
    lidepart=[]
    for i in datadepart:
        depart=i["Departement"]
        if depart not in lidepart:
            lidepart.append(depart)
    for k in lidepart:
        departement=Departement(k,region)
        departement.remplissageDepart()


def chargerCom(data):
    licom=[]
    for i in data:
        com=i["Commune"]
        if com not in licom:
            licom.append(com)
            depart=i["Departement"]
            commune=Commune(com,depart)
            commune.remplissageCom()

def chargerLieu(data):
    lilieu=[]
    for i in data:
        lieu=i["Lieu de Vote"]
        if lieu not in lilieu:
            lilieu.append(lieu)
            lieuVote=Lieu_de_Vote(lieu,i["Commune"],i["Nombre electeur"])
            lieuVote.RemplirLieu()

def chargeDonnees(data):
    chargerregion(data)
    for i in data:
        reg=str(i)
        chargerdepart(data[reg],reg)
        chargerCom(data[reg])
        chargerLieu(data[reg])

# chargeDonnees(data)
############################################## 


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
    # print(dic)   
    return dic

# RecupElecteur()

def recupBureauVote():
    diclieu={}
    lieu=session.query(Lieu_de_Vote.name_lieu,Lieu_de_Vote.nombre_electeur).all()
    lieu.sort(key = lambda x: x[1],reverse=True)   
    for i in lieu:
        if len(diclieu)<10:
            diclieu[i[0]]=i[1]
    return diclieu

def recupinforeg():
    nrdic={}
    lireg=[]
    regions=session.query(Region.name_region,Departement.name_depart).filter(Region.id_region==Departement.regionId).all()

    for i in regions:
        if i[0] not in lireg:
            lireg.append(i[0])
    for j in lireg:
        lidp=[]
        for k in regions:
            if j==k[0]:
                lidp.append(k[1])
                # print(lidp)
        nrdic[j]=lidp
    return nrdic

def recupdepartcomel():
    liregdep = recupinforeg()
    licom = RecupNbrCommune()
    liel = RecupElecteur()
    region = []

    for i in liregdep:
        dic={
            "region":i,
            "departement":liregdep[i],
            "commune":licom[i],
            "electeur":liel[i]

        }
        print(dic)
        region.append(dic)
    print(region)

    return region

# recupdepartcomel()
    




def getter_info_controller():
    liregdep = recupinforeg()
    licom = RecupNbrCommune()
    liel = RecupElecteur()
    region = []

    for i in liregdep:
        dic={
            "region":i,
            "departement":liregdep[i],
            "commune":licom[i],
            "electeur":liel[i]

        }
        print(dic)
        region.append(dic)
    print(region)

    return region



    


# remplirRegion(data)
# remplissageDepart(data)







