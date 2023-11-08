from pydantic import BaseModel, Field  
from fastapi import FastAPI,  HTTPException, Path,Body,Depends
from datetime import datetime ,date
from sqlalchemy.orm import Session
from typing import Annotated
from database import SessionLocal, engine
import crud, models, schemas
from schemas import *

models.Base.metadata.create_all(bind=engine)
from sqlalchemy.orm import Session
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

### GETS MEMBROS: 


@app.get("/membro/nome/{nome}", response_model=list[schemas.MembroCreate])
def listar_membros_por_nome(nome: Annotated[str, Path(title="Nome de um membro da academia",description="Escreva o nome do membro e receba uma lista com todos os membros que tem o nome escolhido", example="Fulano")], db: Session = Depends(get_db)):
    membros_lista = crud.get_membro_nome(db, nome)
    if membros_lista is None:
        detalhe = "Não tem nenhum membro com esse nome"
        raise HTTPException(status_code=400, detail=detalhe,)
    return membros_lista


@app.get("/membro/ativo/{ativo}", response_model=list[schemas.MembroCreate])
def listar_membros_por_estado(ativo: Annotated[int, Path(title="Estado ativo ou inativo do membro",description="0 para membros inativos e 1 para membros ativos", example=1)], db: Session = Depends(get_db)):
    membros_lista = crud.get_membro_ativo(db, ativo)
    if membros_lista is None:
        detalhe = "Não tem nenhum membro com esse estado"
        raise HTTPException(status_code=400, detail=detalhe,)
    return membros_lista


@app.get("/membro/plano/{plano_id}", response_model=list[schemas.MembroCreate])
def listar_membros_por_planoID(plano_id: Annotated[int, Path(title="Identificador do plano",description="Coloque o identificador que representa o id do plano que o membro faz parte", example="3")], db: Session = Depends(get_db)):
    membros_lista = crud.get_membro_plano_id(db, plano_id)
    if membros_lista is None:
        detalhe = "Não tem nenhum membro com esse plano"
        raise HTTPException(status_code=400, detail=detalhe,)
    return membros_lista

@app.get("/membro/id/{membro_id}", response_model=schemas.MembroCreate)
def devolve_informacoes_do_membro(membro_id: Annotated[int, Path(title="Identificador do membro",description="Coloque o identificador que representa o id do membro", example=1)], db: Session = Depends(get_db)):
    membros_lista = crud.get_membro_id(db, membro_id)
    if membros_lista is None:
        detalhe = "Não tem nenhum membro com esse id"
        raise HTTPException(status_code=400, detail=detalhe,)
    return membros_lista

@app.get("/membro/genero/{genero}", response_model=list[schemas.MembroCreate])
def devolve_informacoes_do_membro(genero: Annotated[str, Path(title="Gênero do membro",description="Digite o genero com o qual o membro se identifica", example="Feminino")], db: Session = Depends(get_db)):
    membros_lista = crud.get_membro_id(db, genero)
    if membros_lista is None:
        detalhe = "Não tem nenhum membro com esse genero"
        raise HTTPException(status_code=400, detail=detalhe,)
    return membros_lista

@app.get("/membro/restricao_medica", response_model=list[schemas.MembroCreate])
def listar_membros_com_restricao(db: Session = Depends(get_db)):
    membros_lista = crud.get_membro_restricao_medica(db)
    if membros_lista is None:
        detalhe = "Não existe ninguém com restrição médica"
        raise HTTPException(status_code=400, detail=detalhe,)
    return membros_lista

@app.get("/membro/plano/nome/{nome}", response_model=list[schemas.MembroBase])
def listar_membros_do_plano_nome(nome: Annotated[str, Path(title="Nome do plano",description="Coloque o nome do plano para listar os membros que fazem parte do plano escolhido", example="Intensivo")], db: Session = Depends(get_db)):
    membros_lista = crud.get_membro_plano_nome(db, plano_nome=nome)
    if membros_lista is None:
        detalhe = "Não existe nenhum plano com esse nome ou Não existe ninguém cadastrado nesse plano"
        raise HTTPException(status_code=400, detail=detalhe,)
    return membros_lista

# ### GETS PERSONAIS
    
@app.get("/personal/personal_id/{personal_id}", response_model=schemas.PersonalBase)
def devolve_informacoes_do_membro(personal_id: Annotated[int, Path(title="Identificador do personal",description="Coloque o identificador que representa o id do personal", example=1)], db: Session = Depends(get_db)):
    personal_lista = crud.get_personal_id(db, personal_id)
    if personal_lista is None:
        detalhe = "Não tem nenhum personal com esse id"
        raise HTTPException(status_code=400, detail=detalhe,)
    return personal_lista

@app.get("/personal/genero/{genero}", response_model=list[schemas.PersonalBase])
def listar_personal_por_genero(genero: Annotated[str, Path(title="Gênero do personal",description="Digite o genero com o qual o personal se identifica", example="Masculino")], db: Session = Depends(get_db)):
    personal_lista = crud.get_personal_genero(db, genero)
    if personal_lista is None:
        detalhe = "Não tem nenhum personal com esse gênero"
        raise HTTPException(status_code=400, detail=detalhe,)
    return personal_lista

@app.get("/personal/personal_id/{personal_id}/membros", response_model=list[schemas.MembroBase])
def listar_membros_com_personal_id(personal_id: Annotated[int, Path(title="Identificador do personal",description="Coloque o identificador do personal para listar os membros que esse personal acompanha", example=1)], db: Session = Depends(get_db)):
    personal_lista = crud.get_personal_membros(db, personal_id)
    if personal_lista is None:
        detalhe = "Não existe um personal com esse id ou Nenhum membro tem esse personal"
        raise HTTPException(status_code=400, detail=detalhe,)
    return personal_lista
    
@app.get("/personal/nome/{nome}", response_model=list[schemas.PersonalBase])
def listar_personais_por_nome(nome: Annotated[str, Path(title="Nome de um personal da academia",description="Escreva o nome do personal e receba uma lista com todos os personais que tem o nome escolhido", example="Fulano")], db: Session = Depends(get_db)):
    personal_lista = crud.get_personal_nome(db, nome)
    if personal_lista is None:
        detalhe = "Não existe nenhum personal com esse nome"
        raise HTTPException(status_code=400, detail=detalhe,)
    return personal_lista
    
@app.get("/personal/membro/{membro_id}", response_model=list[schemas.PersonalBase])
def listar_personais_por_nome(membro_id: Annotated[int, Path(title="Identificador do membro",description="Coloque o identificador do membro para receber as informações do personal que acompanha o membro", example=1)], db: Session = Depends(get_db)):
    personal_lista = crud.get_personal_membro_id(db, membro_id)
    if personal_lista is None:
        detalhe = "Não existe um id para o personal ligado ao membro"
        raise HTTPException(status_code=400, detail=detalhe,)
    return personal_lista

# ### GET PLANOS
# @app.get("/plano/plano_id/{plano_id}/membros", response_model=list[Membro])
# async def listar_membro_do_plano_id(plano_id: Annotated[int, Path(title="Identificador do plano",description="Coloque o identificador do plano para receber a lista dos membros que estão nesse plano", example=1)]):
#     membros_lista = []
#     planoId = 0
#     for plano in planos:
#         if plano_id == plano["plano_id"]:
#             planoId = plano["plano_id"]
#     if planoId != 0:
#         membros_lista = filtra_e_devolve_lista_membros("plano_id",plano_id)
#     else:
#         detalhe = "Não existe um plano com esse id"
#         raise HTTPException(status_code=400, detail=detalhe)
#     if not membros_lista:
#         detalhe = "Não existe um membro com esse plano"
#         raise HTTPException(status_code=400, detail=detalhe)
#     return membros_lista


# @app.get("/plano/nome/{nome}/membros", response_model=list[Membro])
# async def listar_membro_do_plano_nome(nome: Annotated[str, Path(title="Nome do plano",description="Coloque o nome do plano para receber a lista dos membros que estão nesse plano", example="basico")]):
#     planoId = 0
#     membros_lista = []
#     for plano in planos:
#         if nome.lower() == plano["nome"].lower():
#             planoId = plano["plano_id"]
#     if planoId != 0:
#         membros_lista = filtra_e_devolve_lista_membros("plano_id",planoId)
#     else:
#         detalhe = "Não existe um plano com esse nome"
#         raise HTTPException(status_code=400, detail=detalhe)
#     if not membros_lista:
#         detalhe = "Não existe um membro com esse plano"
#         raise HTTPException(status_code=400, detail=detalhe)
#     return membros_lista


# @app.get("/plano/aulas_em_grupo", response_model=list[Plano])
# async def listar_planos_com_aula_em_grupo():
#     planos_list = []
#     for plano in planos:
#         if 1 == plano["aulas_em_grupo"]:
#             planos_list.append(Plano(**plano))
#     if not planos_list:
#         detalhe = "Não há nenhuma aula em grupo :("
#         raise HTTPException(status_code=400, detail=detalhe)
#     return planos_list



# @app.get("/plano/id/{plano_id}", response_model=Plano)
# async def informacoes_plano_id(plano_id: Annotated[int, Path(title="Identificador do plano",description="Coloque o identificador do plano para ver as informações do plano escolhido", example=1)]):
#     for plano in planos:
#         if plano["plano_id"] == plano_id:
#             return Plano(**plano)
#     detalhe = "Não existe um plano com o esse id :("
#     raise HTTPException(status_code=400, detail=detalhe)

# @app.get("/plano/nome/{nome}", response_model=Plano)
# async def infomacoes_plano_nome(nome: Annotated[str, Path(title="Nome do plano",description="Coloque o nome do plano para ver as informações do plano escolhido", example="basico")]):
#     nome = nome.lower() 
#     for plano in planos:
#         if plano["nome"].lower() == nome:
#             return Plano(**plano)
        
#     detalhe = "Não existe nenhum plano com esse nome :("
#     raise HTTPException(status_code=400, detail=detalhe)
    

# @app.get("/plano/promocao", response_model=list[Plano])
# async def plano_promocao():
#     planos_list = []
#     for plano in planos:
#         if plano["promocao"] == 1:
#             planos_list.append(Plano(**plano))
#     if  not planos_list:
#         detalhe = "Nao tem nenhum palno com promocao :("
#         raise HTTPException(status_code=400, detail=detalhe)
#     return planos_list


# def filtro_membro_caracteristicas(caracteristica,filtro):
#     dicio = {}
#     for membro in membros:
#         if membro[f'{caracteristica}'].lower() == filtro:
#             dicio[membro["membro_id"]] = f"{membro['nome']} {membro['sobrenome']}"
#     return dicio

# def filtra_personal_caracteristica(caracteristica,filtro):
#     dicio = {}
#     for personal in personais:
#         if personal[f'{caracteristica}'].lower() == filtro:
#             dicio[personal["personal_id"]] = f"{personal['nome']} {personal['sobrenome']}"
#     return dicio

# ### DELETES:
@app.delete("/membro/{membro_id}", response_model=list[MembroCreate])
def deletar_membro(membro_id: Annotated[int, Path(title="Identificador do membro",description="Coloque o identificador do membro para deletar o membro escolhido", example=1)], db: Session = Depends(get_db)):
    if crud.deletar_membro(db=db, membro_id=membro_id):
        return db.query(models.Membro).all()
    detalhe = "Não foi encontrado nenhum membro com esse id"
    raise HTTPException(status_code=400, detail=detalhe)

@app.delete("/personal/{personal_id}", response_model=list[PersonalCreate])
def deletar_personal(personal_id: Annotated[int, Path(title="Identificador do personal",description="Coloque o identificador do personal para deletar o personal escolhido", example=1)], db: Session = Depends(get_db)):
    if crud.deletar_personal(db=db, personal_id=personal_id):
        return db.query(models.Personal).all()
    detalhe = "Não foi encontrado nenhum personal com esse id"
    raise HTTPException(status_code=400, detail=detalhe)

@app.delete("/plano/{plano_id}", response_model=list[PlanoCreate])
def deletar_plano(plano_id: Annotated[int, Path(title="Identificador do plano",description="Coloque o identificador do plano para deletar o plano escolhido", example=1)], db: Session = Depends(get_db)):
    if crud.deletar_plano(db=db, plano_id=plano_id):
        return db.query(models.Plano).all()
    detalhe = "Não foi encontrado nenhum plano com esse id"
    raise HTTPException(status_code=400, detail=detalhe)

#     membro_list = []
#     membro_existe = None
#     for membro in membros:
#         if membro_id == membro["membro_id"]:
#             membros.remove(membro)
#             for personal in personais:
#                 if membro_id in personal["membro_id"]:
#                     personal["membro_id"].remove(membro_id)
#             membro_existe = 1
#             break
#     if membro_existe is None:
#         detalhe = "Não existe um membro com esse id para ser deletado"
#         raise HTTPException(status_code=400, detail=detalhe)
#     data["membro"] = membros
#     data["personal"] = personais
#     with open(file_json, "w") as arquivo:
#         json.dump(data, arquivo, indent=4) 
#     for membro in membros:
#         membro_list.append(Membro(**membro))  
#     return membro_list


# @app.delete("/personal/{personal_id}",response_model=list[Personal])
# async def deletar_personal(personal_id: Annotated[int, Path(title="Identificador do personal",description="Coloque o identificador do personal para deletar o personal escolhido", example=1)]):
#     personal_list = []
#     personal_existe = None
#     for personal in personais:
#         if personal_id == personal["personal_id"]:
#             personais.remove(personal)
#             for membro in membros:
#                 if personal_id == membro["personal_id"]:
#                     membro["personal_id"] = None 
#             personal_existe = 1
#     if personal_existe is None:
#         detalhe = "Não existe um personal com esse id para ser deletado"
#         raise HTTPException(status_code=400, detail=detalhe)
#     data["personal"] = personais
#     with open(file_json, "w") as arquivo:
#         json.dump(data, arquivo, indent=4) 
#     for personal in personais:
#         personal_list.append(Personal(**personal))  
#     return personais


# @app.delete("/plano/{plano_id}")
# async def deletar_plano(plano_id: Annotated[int, Path(title="Identificador do plano",description="Coloque o identificador do plano para deletar o plano escolhido", example=1)]):
#     plano_existe = None
#     for plano in planos:
#         if plano_id == plano["plano_id"]:
#             planos.remove(plano)
#             for membro in membros:
#                 if plano_id == membro["plano_id"]:
#                     membro["plano_id"] = 0 # Caso o plano seja apagado, o usuário fica sem plano (plano =0) até entrar em outro
#                     membro["ativo"] = 0
#             plano_existe = 1
#     if plano_existe is None:
#         detalhe = "Não existe um plano com esse id para ser deletado"    
#         raise HTTPException(status_code=400, detail=detalhe)
#     data["plano"] = planos
#     data["membro"] = membros
#     with open(file_json, "w") as arquivo:
#         json.dump(data, arquivo, indent=4) 
#     planos_list  = []
#     for plano in planos: 
#         planos_list.append(Plano(**plano))
#     return planos_list


# # POSTS :

# def serializar_datetime(obj):
#     if isinstance(obj, date):
#         return obj.isoformat()
#     raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

# def adicionar_membro_personal(membro_id,personal_id):
#     for personal in personais:
#         if personal["personal_id"] == personal_id:
#             personal["membro_id"].append(membro_id)

# def remover_membro_personal(membro_id,personal_id):
#     for personal in personais:
#         if personal["personal_id"] == personal_id:
#             personal["membro_id"].remove(membro_id)

# @app.post("/membro", status_code=201,response_model=Membro) 
# async def adicionar_membro(membro: Annotated[Membro,Body(description="Corpo para envio das informações para serem adicionadas")]):
#     membros.append(membro.dict())
#     adicionar_membro_personal(membro.membro_id,membro.personal_id)
#     data["membro"] = membros
#     with open(file_json, "w") as arquivo:
#         json.dump(data, arquivo, indent=4,default=serializar_datetime)  # indent=4 para formatar o JSON de forma legível
#     return membro


@app.post("/membro/", response_model=schemas.MembroBase)
def create_user(membro: Annotated[schemas.MembroBase,Body(description="Corpo para envio das informações para serem adicionadas")], db: Session = Depends(get_db)):
    return crud.create_membro(db=db, membro=membro)


# @app.post("/plano",status_code=201, response_model=Plano)
# async def adicionar_plano(plano:Annotated[Plano,Body(description="Corpo para envio das informações para serem adicionadas")]):
#     planos.append(plano.dict())
#     data["plano"] = planos
#     with open(file_json, "w") as arquivo:
#         json.dump(data, arquivo, indent=4, default=serializar_datetime)  # indent=4 para formatar o JSON de forma legível
#     return plano


# @app.post("/personal",status_code=201,response_model=Personal)
# async def adicionar_personal(personal: Annotated[Personal,Body(description="Corpo para envio das informações para serem adicionadas")]):
#     personais.append(personal.dict())
#     data["personal"] = personais
#     with open(file_json, "w") as arquivo:
#         json.dump(data, arquivo, indent=4, default=serializar_datetime)  # indent=4 para formatar o JSON de forma legível
#     return personal

@app.post("/personal/", response_model=schemas.PersonalCreate)
def create_personal(personal: Annotated[schemas.PersonalBase,Body(description="Corpo para envio das informações para serem adicionadas")], db: Session = Depends(get_db)):
    return crud.create_personal(db=db, personal=personal)

@app.post("/plano/", response_model=schemas.PlanoCreate)
def create_plano(plano: Annotated[schemas.PlanoBase,Body(description="Corpo para envio das informações para serem adicionadas")], db: Session = Depends(get_db)):
    return crud.create_plano(db=db, plano=plano)


# # PUTS :


# @app.put("/membro/{membro_id}",response_model=MembroUpdate)
# async def update_membro(membro_id: int, membro: Annotated[MembroUpdate,Body(description="Corpo para envio das informações a serem alteradas")]):
#     membro_aux = membro.dict()
#     membro_existe = None
#     for memb in membros:
#         if memb["membro_id"] == membro_id:
#             remover_membro_personal(membro_id,memb["personal_id"])
#             adicionar_membro_personal(membro_id,membro.personal_id)
#             for chave, valor in membro_aux.items():
#                 if valor is not None:
#                     memb[chave] = valor
#             membro_existe = 1
#     if membro_existe is None:
#         detalhe = "Não existe um membro com esse id para ser alterado"    
#         raise HTTPException(status_code=400, detail=detalhe)
#     data["membro"] = membros
#     with open(file_json, "w") as arquivo:
#         json.dump(data, arquivo, indent=4, default=serializar_datetime)  # indent=4 para formatar o JSON de forma legível
#     return membro



# @app.put("/personal/{personal_id}",response_model=PersonalUpdate)
# async def update_personal(personal_id: int, personal: Annotated[PersonalUpdate,Body(description="Corpo para envio das informações a serem alteradas")]):
#     personal_aux = personal.dict()
#     personal_existe = None
#     for pers in personais:
#         if pers["personal_id"] == personal_id:
#             for chave, valor in personal_aux.items():
#                 if valor is not None:
#                     pers[chave] = valor
#             personal_existe = 1
#     if personal_existe is None:
#         detalhe = "Não existe um personal com esse id para ser alterado"    
#         raise HTTPException(status_code=400, detail=detalhe)
#     data["personal"] = personais
#     with open(file_json, "w") as arquivo:
#         json.dump(data, arquivo, indent=4, default=serializar_datetime)  # indent=4 para formatar o JSON de forma legível
#     return personal



# @app.put("/plano/{plano_id}",response_model=PlanoUpdate)
# async def update_plano(plano_id: int, plano: Annotated[PlanoUpdate,Body(description="Corpo para envio das informações a serem alteradas")]):
#     plano_aux = plano.dict()
#     plano_existe = None
#     for plan in planos:
#         if plan["plano_id"] == plano_id:
#             for chave, valor in plano_aux.items():
#                 if valor is not None:
#                     plan[chave] = valor
#             plano_existe = 1
#     if plano_existe is None:
#         detalhe = "Não existe um plano com esse id para ser alterado"    
#         raise HTTPException(status_code=400, detail=detalhe)
#     data["plano"] = planos
#     with open(file_json, "w") as arquivo:
#         json.dump(data, arquivo, indent=4, default=serializar_datetime)  # indent=4 para formatar o JSON de forma legível
#     return plano