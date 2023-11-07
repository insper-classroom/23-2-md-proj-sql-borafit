from sqlalchemy.orm import Session

import models, schemas
### Função auxiliares com conexão com o banco de dados

def get_membro_id(db: Session, membro_id: int):
    return db.query(models.Membro).filter(models.Membro.membro_id == membro_id).first()

def get_membro_nome(db: Session, nome: int):
    return db.query(models.Membro).filter(models.Membro.nome == nome).all()

def get_membro_genero(db: Session, genero: int):
    return db.query(models.Membro).filter(models.Membro.genero == genero).all()

def get_membro_restricao_medica(db: Session, restricao: int):
    return db.query(models.Membro).filter(models.Membro.restricao == restricao).all()

def get_membro_plano_nome(db: Session, plano_nome: str):
    #Ainda não sei se isso daqui está funcionando
    aux = db.query(models.Plano).filter(models.Membro.plano_nome == plano_nome).first()
    return db.query(models.Membro).filter(models.Membro.plano_id == aux.plano_id).all()



def get_membro_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

'''

POSTS
#/membro/{id_membro}
#/membro/{genero} 
#/membro/restricao/{restricao_medica}
/membro/plano/{nome}
/personal/{nome}
/personal/membro/{membro_id}
/plano/{plano_id}
/plano/{nome}
/plano/promocao

'''