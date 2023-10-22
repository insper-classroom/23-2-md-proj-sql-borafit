from pydantic import BaseModel, Field
from datetime import date
from fastapi import FastAPI,  HTTPException
from datetime import datetime


import json

app = FastAPI()
file_json = 'exemplo.json'
# Carregando o JSON
with open(file_json, 'r') as file:
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
        if membro[f'{caracteristica}'].lower() == filtro:
            dicio[membro["membro_id"]] = f"{membro['nome']} {membro['sobrenome']}"
    return dicio

def filtra_personal_caracteristica(caracteristica,filtro):
    dicio = {}
    for personal in personais:
        if personal[f'{caracteristica}'].lower() == filtro:
            dicio[personal["personal_id"]] = f"{personal['nome']} {personal['sobrenome']}"
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
        return "Não existe ninguém cadastrado com essa restrição médica :)"
    return response_dict

@app.get("/membro/plano/nome/{nome}")
async def listar_membros_do_plano_nome(nome: str):
    nome = nome.lower() 
    id_plano = None
    for plano in planos:
        if plano["nome"] == nome:
            id_plano = plano["plano_id"]
    if id_plano is None:
        return  "Não existe nenhum plano com esse nome :("
    response_dict = filtro_membro_caracteristicas('plano_id',id_plano)
    if response_dict == {}:
        return "Não existe ninguém cadastrado nesse plano :("
    return response_dict

@app.get("/personal/nome/{nome}")
async def listar_personais_por_nome(nome:str):
    nome = nome.lower()
    response_dict = filtra_personal_caracteristica('nome',nome)
    if response_dict == {}:
        return "Não existe nenhum personal com esse nome :("
    return response_dict
    
@app.get("/personal/membro/{membro_id}")
async def informacoes_personal_de_um_membro(membro_id: int):
    personal_id = None
    for membro in membros:
        if membro['membro_id'] == membro_id:
            if membro["personal_id"] != None:
                personal_id = membro["personal_id"]
            else:
                return "O membro não tem nenhum personal :("
    for personal in personais:
        if personal["personal_id"] == personal_id:
            return personal
    return "Não existe um id para o personal ligado ao membro ;-;"
    

@app.get("/plano/id/{plano_id}")
async def informacoes_plano_id(plano_id: int):
    for plano in planos:
        if plano["plano_id"] == plano_id:
            return plano
    return "Não existe um plano com o esse id :("

@app.get("/plano/nome/{nome}")
async def infomacoes_plano_nome(nome: str):
    nome = nome.lower() 
    for plano in planos:
        if plano["nome"].lower() == nome:
            return plano
        
    #raise HTTPException(status_code=404, detail="Item not found")
    return "Não existe nenhum plano com esse nome :("
    

@app.get("/plano/promocao")
async def plano_promocao():
    response_dict = {}
    for plano in planos:
        if plano["promocao"] == 1:
            response_dict[plano['plano_id']] = f"{plano['nome']}"
    if response_dict == {}:
        return "Nao tem nenhum palno com promocao :("
    return response_dict

### DELETES:
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



# POSTS :
class Membro(BaseModel):
    membro_id: int = Field( default= len(membros)+1 ) # depois podemos utilizar uuid4()
    nome: str = Field(min_length = 2, description="Nome precisa ter pelo menos duas letras")
    sobrenome: str | None
    genero: str
    cpf: str
    plano_id: int
    ativo: int
    telefone: str | None
    email: str
    personal_id: int
    restricao_medica: str | None = None
    data_inscricao: date = Field(default = datetime.now(), description="Colocando a data atual, ou seja, na hora do cadastro")
    ultima_presenca: date | None = None

def serializar_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


@app.post("/membro")
def adicionar_membro(membro: Membro):
    membros.append(membro.dict())
    data["membro"] = membros
    with open(file_json, "w") as arquivo:
        json.dump(data, arquivo, indent=4,default=serializar_datetime)  # indent=4 para formatar o JSON de forma legível

    return membro

class Plano(BaseModel):
    plano_id: int = Field( default= len(planos)+1 )
    preco: float = Field(gt=0, description="O preço precisa ser maior que zero!")
    descricao: str | None
    nome: str
    aulas_em_grupo: int
    promocao: int

@app.post("/plano")
def adicionar_plano(plano: Plano):
    planos.append(plano.dict())
    data["plano"] = planos
    with open(file_json, "w") as arquivo:
        json.dump(data, arquivo, indent=4)  # indent=4 para formatar o JSON de forma legível
    return plano

class Personal(BaseModel):
    personal_id: int = Field( default= len(personais)+1 )
    nome : str
    sobrenome: str 
    membro_id : list[int]
    cpf: str = Field(pattern=r'^\d*$', max_length=11, min_length=11,description="O cpf deve ter 11 dígitos, não inclua os pontos ( . ) e nem o traço ( - )") # pattern só permite números
    genero: str 
    telefone: str = Field(pattern=r'^\d*$', max_length=11,description="O telefone deve ter 11 dígitos DDD+9+número , sem espaços!")
    email: str = Field(pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$',description="O email deve ser válido")
    salario: float = Field(gt=0, description="O salário precisa ser maior que zero!")

@app.post("/personal")
def adicionar_personal(personal: Personal):
    personais.append(personal.dict())
    data["personal"] = personais
    with open(file_json, "w") as arquivo:
        json.dump(data, arquivo, indent=4)  # indent=4 para formatar o JSON de forma legível
    return personal
