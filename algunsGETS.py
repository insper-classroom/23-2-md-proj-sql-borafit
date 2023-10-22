from pydantic import BaseModel
from datetime import date
from fastapi import FastAPI

import json

app = FastAPI()

# Carregando o JSON
with open('exemplo.json', 'r') as file:
    data = json.load(file)


@app.get("/membro/nome/{nome}")
def listar_membros_por_nome(nome: str):
    membros = data.get("membro", [])
    membros_dict = {}
    for membro in membros:
        if nome == membro["nome"]:
            membros_dict[membro["membro_id"]] = membro['nome'] + " " + membro['sobrenome']
    if not membros_dict:
        return "Não tem nenhum membro com esse nome"
    return membros_dict


@app.get("/membro/ativo/{ativo}")
def listar_membros_por_estado(ativo: int):
    membros = data.get("membro", [])
    membros_dict = {}
    for membro in membros:
        if ativo == membro["ativo"]:
            membros_dict[membro["membro_id"]] = membro['nome'] + " " + membro['sobrenome']
    if not membros_dict:
        return "Não tem nenhum membro com esse estado"
    return membros_dict


@app.get("/membro/plano/{plano_id}")
def listar_membros_por_planoID(plano_id: int):
    membros = data.get("membro", [])
    membros_dict = {}
    for membro in membros:
        if plano_id == membro["plano_id"]:
            membros_dict[membro["membro_id"]] = membro['nome'] + " " + membro['sobrenome']
    if not membros_dict:
        return "Não tem nenhum membro com esse plano"
    return membros_dict


@app.get("/personal/personal_id/{personal_id}")
def personal_por_personalID(personal_id: int):
    personais = data.get("personal", [])
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
    personais = data.get("personal", [])
    membros = data.get("membro", [])
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
    planos = data.get("plano", [])
    membros = data.get("membro", [])
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
    planos = data.get("plano", [])
    membros = data.get("membro", [])
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

