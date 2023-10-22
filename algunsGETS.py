from pydantic import BaseModel
from datetime import date
from fastapi import FastAPI

import json

app = FastAPI()

# Carregando o JSON
with open('exemplo.json', 'r') as file:
    data = json.load(file)

membros = data.get("membro", [])
personais = data.get("personal", [])
planos = data.get("plano", [])
### GETS: 
@app.get("/membro/nome/{nome}")
def listar_membros_por_nome(nome: str):

    membros_dict = {}
    for membro in membros:
        if nome == membro["nome"]:
            membros_dict[membro["membro_id"]] = membro['nome'] + " " + membro['sobrenome']
    if not membros_dict:
        return "Não tem nenhum membro com esse nome"
    return membros_dict


@app.get("/membro/ativo/{ativo}")
def listar_membros_por_estado(ativo: int):
    membros_dict = {}
    for membro in membros:
        if ativo == membro["ativo"]:
            membros_dict[membro["membro_id"]] = membro['nome'] + " " + membro['sobrenome']
    if not membros_dict:
        return "Não tem nenhum membro com esse estado"
    return membros_dict


@app.get("/membro/plano/{plano_id}")
def listar_membros_por_planoID(plano_id: int):
    membros_dict = {}
    for membro in membros:
        if plano_id == membro["plano_id"]:
            membros_dict[membro["membro_id"]] = membro['nome'] + " " + membro['sobrenome']
    if not membros_dict:
        return "Não tem nenhum membro com esse plano"
    return membros_dict


@app.get("/personal/personal_id/{personal_id}")
def personal_por_personalID(personal_id: int):

    for personal in personais:
        if personal_id == personal["personal_id"]:
            return personal
    return "Não tem nenhum personal com esse id"
    

@app.get("/personal/genero/{genero}")
def listar_personal_por_genero(genero: str):
    personais = data.get("personal", [])
    personal_dict = {}
    for personal in personais:
        if genero == personal["genero"]:
            personal_dict[personal["personal_id"]] = personal['nome'] + " " + personal['sobrenome']
    if not personal_dict:
        return "Não tem nenhum personal com esse gênero"
    return personal_dict


@app.get("/personal/personal_id/{personal_id}/membros")
def listar_membros_com_personal_id(personal_id: int):
    personal_membros_dict = {}
    membros_lista = []
    personalId = 0
    for personal in personais:
        if personal_id == personal["personal_id"]:
            personalId = personal["personal_id"]
    if personalId != 0:
        for membro in membros:
            if membro["personal_id"] == personal_id:
                membros_lista.append(membro)
        personal_membros_dict[personal_id] = membros_lista
    if not personal_membros_dict:
        return "Não existe um personal com esse id"
    if not membros_lista:
        return "Nenhum membro tem esse personal"        
    return personal_membros_dict


@app.get("/plano/plano_id/{plano_id}/membros")
def listar_membro_do_plano_id(plano_id: int):
    plano_membros_dict = {}
    membros_lista = []
    planoId = 0
    for plano in planos:
        if plano_id == plano["plano_id"]:
            planoId = plano["plano_id"]
    if planoId != 0:
        for membro in membros:
            if membro["plano_id"] == plano_id:
                membros_lista.append(membro)
        plano_membros_dict[plano_id] = membros_lista
    if not plano_membros_dict:
        return "Não existe um plano com esse id"
    if not membros_lista:
        return "Não existe um membro com esse plano"
    return plano_membros_dict


@app.get("/plano/nome/{nome}/membros")
def listar_membro_do_plano_nome(nome: str):
    planoId = 0
    plano_membros_dict = {}
    membros_lista = []
    for plano in planos:
        if nome == plano["nome"]:
            planoId = plano["plano_id"]
    if planoId != 0:
        for membro in membros:
            if membro["plano_id"] == planoId:
                membros_lista.append(membro)
        plano_membros_dict[nome] = membros_lista
    if not plano_membros_dict:
        return "Não existe um plano com esse nome"
    if not membros_lista:
        return "Não existe um membro com esse plano"
    return plano_membros_dict


@app.get("/plano/aulas_em_grupo")
def listar_planos_com_aula_em_grupo():
    planos = data.get("plano", [])
    planos_dict = {}
    for plano in planos:
        if 1 == plano["aulas_em_grupo"]:
            planos_dict[plano["nome"]] = plano
    if not planos_dict:
        return "Não há nenhuma aula em grupo :("
    return planos_dict


### gets lincoln :
def filtro_membro_caracteristicas(caracteristica,filtro):
    dicio = {}
    for membro in membros:
        if membro[f'{caracteristica}'] == filtro:
            dicio[membro["membro_id"]] = f"{membro['nome']} {membro['sobrenome']}"
    return dicio

@app.get("/membro/id/{membro_id}")
async def devolve_informacoes_do_membro(membro_id: int):
    for membro in membros:
        if membro["membro_id"] == membro_id:
            return membro
    return "Não há nenhum membro com esse id :("


@app.get("/membro/genero/{genero}")
async def listar_membros_de_um_genero(genero: str):
    genero = genero.lower()
    response_dict = filtro_membro_caracteristicas('genero',genero)
    if response_dict == {}:
        return "Não existe ninguém cadastrado com esse gênero :("
    return response_dict



@app.get("/membro/restricao/{restricao_medica}")
async def listar_membros_com_restricao(restricao_medica: str):
    restricao_medica = restricao_medica.lower()
    response_dict = filtro_membro_caracteristicas('restricao_medica',restricao_medica)
    if response_dict == {}:
        return "Não existe ninguém cadastrado com essa restrição médica :("
    return response_dict

@app.get("/membro/plano/nome/{nome}")
async def listar_membros_do_plano_nome(nome: str):
    nome = nome.lower() 
    for plano in planos:
        if plano["nome"] == nome:
            id_plano = plano["plano_id"]
    response_dict = filtro_membro_caracteristicas('plano_id',id_plano)
    if response_dict == {}:
        return "Não existe ninguém cadastrado nesse plano :("
    return response_dict

# @app.get("/personal/{nome}")

# @app.get("/personal/membro/{membro_id}")

# @app.get("/plano/{plano_id}")

# @app.get("/plano/{nome}")

# @app.get("/plano/promocao")

@app.delete("/membro/{membro_id}")
def deletar_membro(membro_id: int):
    membros = data.get("membro", [])
    membro_existe = 0
    for membro in membros:
        if membro_id == membro["membro_id"]:
            membros.remove(membro)
            membro_existe = 1
    if membro_existe == 0:
        return "Não existe um membro com esse id para ser deletado"
    return membros


@app.delete("/personal/{personal_id}")
def deletar_personal(personal_id: int):
    personais = data.get("personal", [])
    personal_existe = 0
    for personal in personais:
        if personal_id == personal["personal_id"]:
            personais.remove(personal)
            personal_existe = 1
    if personal_existe == 0:
        return "Não existe um personal com esse id para ser deletado"
    return personais


@app.delete("/plano/{plano_id}")
def deletar_plano(plano_id: int):
    planos = data.get("plano", [])
    plano_existe = 0
    for plano in planos:
        if plano_id == plano["plano_id"]:
            planos.remove(plano)
            plano_existe = 1
    if plano_existe == 0:
        return "Não existe um plano com esse id para ser deletado"    
    return planos
