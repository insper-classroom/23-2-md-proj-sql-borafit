from pydantic import BaseModel, Field
from fastapi import FastAPI,  HTTPException
from datetime import datetime ,date

import json

app = FastAPI()
file_json = 'exemplo.json'
# Carregando o JSON
with open(file_json, 'r') as file:
    data = json.load(file)

membros = data.get("membro", [])
personais = data.get("personal", [])
planos = data.get("plano", [])

# Classes :
class Membro(BaseModel):
    membro_id: int = Field( default= len(membros)+1 ) # depois podemos utilizar uuid4()
    nome: str = Field(min_length = 2, description="Nome precisa ter pelo menos duas letras",examples=["Fulano"])
    sobrenome: str | None = None
    genero: str = Field(min_length = 5, description="Genero precisa ter pelo menos cinco letras",examples=["Não definido"])
    cpf: str = Field(pattern=r'^\d*$', max_length=11, min_length=11,description="O cpf deve ter 11 dígitos, não inclua os pontos ( . ) e nem o traço ( - )", examples=["01234567891"]) # pattern só permite números
    plano_id: int = Field( description="Identificador do plano na qual a pessoa está matriculada", examples =["1"])
    ativo: int = Field( description="0: se o membro não está ativo e 1: se o membro está ativo", examples =["0"])
    telefone: str | None = Field(pattern=r'^\d*$', min_length=11, max_length=11,description="O telefone deve ter 11 dígitos (2)DDD+9+número(8) , sem espaços!",  examples=["98765432100"])
    email: str = Field(pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$',description="O email deve ser válido" ,examples=["exemplo@email.com"])
    personal_id: int = Field(gt=0, description="Colocando o id do personal", examples =["1"])
    restricao_medica: str | None = Field(description="Informações sobre restrições médicas a serem seguidas por um membro", examples =["Problema no joelho"], default=None)
    data_inscricao: date = Field(default = datetime.now().date(), description="Colocando a data atual, ou seja, a hora do cadastro")
    ultima_presenca: date | None = Field(default = None, description="Ultimo dia que o membro frequentou a academia")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nome" : "Raul",
                    "sobrenome" : "Seixas",
                    "genero" : "Masculino",
                    "cpf" : "66569678302",
                    "plano_id" : 2,
                    "ativo": 1,
                    "telefone": "11940028922",
                    "email": "exemplo@exemplo.com",
                    "personal_id": 1,
                    "restrição_medica": "nenhuma"
                }
            ]
        }
    }
class Plano(BaseModel):
    plano_id: int = Field( default= len(planos)+1 )
    nome: str 
    descricao: str | None = Field( description="Mais detalhes sobre o plano",examples=["Plano mais completo com acompanhamento"])
    preco: float = Field(gt=0, description="O preço precisa ser maior que zero!",examples=[100])
    aulas_em_grupo: int =Field( description="0: se não oferece aulas em grupo e 1: se oferece aulas em grupo", examples = ["0"])
    promocao: int = Field( description="0: se o plano não está em promoção e 1: se o plano está em promoção",  examples = ["1"])
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nome" : "Basic",
                    "description": "Plano Basic",
                    "preco": 100.0,
                    "aulas_em_grupo": 0,
                    "promocao": 1
                }
            ]
        }
    }

class Personal(BaseModel):
    personal_id: int = Field( default= len(personais)+1 )
    nome : str = Field(min_length = 2, description="Nome precisa ter pelo menos duas letras", default=None, examples=["Roberta"])
    sobrenome: str 
    membro_id : list[int] = Field(description= "Uma lista com os identificadores dos membros da academia que o personal acompanha",examples=[2,3])
    cpf: str = Field(pattern=r'^\d*$', max_length=11, min_length=11,description="O cpf deve ter 11 dígitos, não inclua os pontos ( . ) e nem o traço ( - )",examples=["01234567891"]) # pattern só permite números
    genero: str 
    telefone: str = Field(pattern=r'^\d*$', max_length=11,description="O telefone deve ter 11 dígitos DDD+9+número , sem espaços!",examples=["11999523499"])
    email: str = Field(pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$',description="O email deve ser válido", examples=["exemplo@dominio.com"])
    salario: float = Field(gt=0, description="O salário precisa ser maior que zero!", examples=[2000.0])
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nome" : "Amethysta",
                    "sobrenome": "Perola",
                    "membro_id": [1,2],
                    "cpf": "11223344556",
                    "genero": "Feminino",
                    "telefone": "23919283746",
                    "email": "amethypearl@borafit.com",
                    "salario": 3000.0
                }
            ]
        }
    }

def filtra_e_devolve_lista_membros(nome_filtro,filtro):
    membros_lista = []
    if type(filtro) is str:
        for membro in membros:
            if filtro.lower() == membro[nome_filtro].lower():
                membros_lista.append(Membro(**membro))
    else:
        for membro in membros:
            if filtro == membro[nome_filtro]:
                membros_lista.append(Membro(**membro))
    return membros_lista
                
            
def filtra_e_devolve_lista_personais(nome_filtro,filtro):
    personais_lista = []
    if type(filtro) is str:
        for personal in personais:
            if filtro.lower() == personal[nome_filtro].lower():
                personais_lista.append(Personal(**personal))
    else:
        for personal in personais:
            if filtro == personal[nome_filtro]:
                personais_lista.append(Personal(**personal))
    return personais_lista
                


### GETS MEMBROS: 
@app.get("/membro/nome/{nome}", response_model=list[Membro])
async def listar_membros_por_nome(nome: str):
    membros_lista = filtra_e_devolve_lista_membros("nome",nome)
    if not membros_lista:
        detalhe = "Não tem nenhum membro com esse nome"
        raise HTTPException(status_code=400, detail=detalhe)
    return membros_lista


@app.get("/membro/ativo/{ativo}", response_model=list[Membro])
async def listar_membros_por_estado(ativo: int):
    membros_lista = filtra_e_devolve_lista_membros("ativo",ativo)
    if not membros_lista:
        detalhe = "Não tem nenhum membro com esse estado"
        raise HTTPException(status_code=400, detail=detalhe)
    return membros_lista


@app.get("/membro/plano/{plano_id}", response_model=list[Membro])
async def listar_membros_por_planoID(plano_id: int):
    membros_lista = filtra_e_devolve_lista_membros("plano_id",plano_id)
    if not membros_lista:
        detalhe = "Não tem nenhum membro com esse plano"
        raise HTTPException(status_code=400, detail=detalhe)
    return membros_lista

@app.get("/membro/id/{membro_id}", response_model=Membro)
async def devolve_informacoes_do_membro(membro_id: int):
    for membro in membros:
        if membro["membro_id"] == membro_id:
            response_membro = Membro(**membro)
            return response_membro
    detalhe = "Não há nenhum membro com esse id :("
    raise HTTPException(status_code=400, detail=detalhe)


@app.get("/membro/genero/{genero}", response_model=list[Membro])
async def listar_membros_de_um_genero(genero: str):
    membros_lista = filtra_e_devolve_lista_membros("genero",genero)
    if not membros_lista: 
        detalhe = "Não existe ninguém cadastrado com esse gênero :("
        raise HTTPException(status_code=400, detail=detalhe)
    return membros_lista


@app.get("/membro/restricao/{restricao_medica}", response_model=list[Membro])
async def listar_membros_com_restricao(restricao_medica: str):
    membros_lista = filtra_e_devolve_lista_membros("restricao_medica",restricao_medica)
    if not membros_lista:
        detalhe = "Não existe ninguém cadastrado com essa restrição médica :)"
        raise HTTPException(status_code=400, detail=detalhe)
    return membros_lista

@app.get("/membro/plano/nome/{nome}", response_model=list[Membro])
async def listar_membros_do_plano_nome(nome: str):
    nome = nome.lower() 
    id_plano = None
    for plano in planos:
        if plano["nome"] == nome:
            id_plano = plano["plano_id"]
    if id_plano is None:
        detalhe = "Não existe nenhum plano com esse nome :("
        raise HTTPException(status_code=400, detail=detalhe)
    membros_lista = filtra_e_devolve_lista_membros('plano_id',id_plano)
    if not membros_lista:
        detalhe = "Não existe ninguém cadastrado nesse plano :("
        raise HTTPException(status_code=400, detail=detalhe)
    return membros_lista


### GETS PERSONAIS
@app.get("/personal/personal_id/{personal_id}", response_model=Personal)
async def personal_por_personalID(personal_id: int):
    for personal in personais:
        if personal_id == personal["personal_id"]:
            response_personal = Personal(**personal)
            return response_personal
    detalhe = "Não tem nenhum personal com esse id"
    raise HTTPException(status_code=400, detail=detalhe)
    

@app.get("/personal/genero/{genero}", response_model=list[Personal])
async def listar_personal_por_genero(genero: str):
    personal_lista = filtra_e_devolve_lista_personais("genero",genero)
    if not personal_lista:
        detalhe = "Não tem nenhum personal com esse gênero"
        raise HTTPException(status_code=400, detail=detalhe)
    return personal_lista


@app.get("/personal/personal_id/{personal_id}/membros", response_model=list[Personal])
async def listar_membros_com_personal_id(personal_id: int):
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
        detalhe = "Não existe um personal com esse id"
        raise HTTPException(status_code=400, detail=detalhe)
    if not membros_lista:
        detalhe = "Nenhum membro tem esse personal"   
        raise HTTPException(status_code=400, detail=detalhe)     
    
    return personal_membros_dict


@app.get("/plano/plano_id/{plano_id}/membros")
async def listar_membro_do_plano_id(plano_id: int):
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
        detalhe = "Não existe um plano com esse id"
        raise HTTPException(status_code=400, detail=detalhe)
    if not membros_lista:
        detalhe = "Não existe um membro com esse plano"
        raise HTTPException(status_code=400, detail=detalhe)
    return plano_membros_dict


@app.get("/plano/nome/{nome}/membros")
async def listar_membro_do_plano_nome(nome: str):
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
        detalhe = "Não existe um plano com esse nome"
        raise HTTPException(status_code=400, detail=detalhe)
    if not membros_lista:
        detalhe = "Não existe um membro com esse plano"
        raise HTTPException(status_code=400, detail=detalhe)
    return plano_membros_dict


@app.get("/plano/aulas_em_grupo")
async def listar_planos_com_aula_em_grupo():
    planos = data.get("plano", [])
    planos_dict = {}
    for plano in planos:
        if 1 == plano["aulas_em_grupo"]:
            planos_dict[plano['plano_id']] = f"{plano['nome']}"
    if not planos_dict:
        detalhe = "Não há nenhuma aula em grupo :("
        raise HTTPException(status_code=400, detail=detalhe)
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







@app.get("/personal/nome/{nome}")
async def listar_personais_por_nome(nome:str):
    nome = nome.lower()
    response_dict = filtra_personal_caracteristica('nome',nome)
    if response_dict == {}:
        detalhe = "Não existe nenhum personal com esse nome :("
        raise HTTPException(status_code=400, detail=detalhe)
    return response_dict
    
@app.get("/personal/membro/{membro_id}")
async def informacoes_personal_de_um_membro(membro_id: int):
    personal_id = None
    for membro in membros:
        if membro['membro_id'] == membro_id:
            if membro["personal_id"] != None:
                personal_id = membro["personal_id"]
            else:
                detalhe = "O membro não tem nenhum personal :("
                raise HTTPException(status_code=400, detail=detalhe)
    for personal in personais:
        if personal["personal_id"] == personal_id:
            return personal
    detalhe = "Não existe um id para o personal ligado ao membro ;-;"
    raise HTTPException(status_code=400, detail=detalhe)
    

@app.get("/plano/id/{plano_id}")
async def informacoes_plano_id(plano_id: int):
    for plano in planos:
        if plano["plano_id"] == plano_id:
            return plano
    detalhe = "Não existe um plano com o esse id :("
    raise HTTPException(status_code=400, detail=detalhe)

@app.get("/plano/nome/{nome}")
async def infomacoes_plano_nome(nome: str):
    nome = nome.lower() 
    for plano in planos:
        if plano["nome"].lower() == nome:
            return plano
        
    detalhe = "Não existe nenhum plano com esse nome :("
    raise HTTPException(status_code=400, detail=detalhe)
    

@app.get("/plano/promocao")
async def plano_promocao():
    response_dict = {}
    for plano in planos:
        if plano["promocao"] == 1:
            response_dict[plano['plano_id']] = f"{plano['nome']}"
    if response_dict == {}:
        detalhe = "Nao tem nenhum palno com promocao :("
        raise HTTPException(status_code=400, detail=detalhe)
    return response_dict

### DELETES:
@app.delete("/membro/{membro_id}")
async def deletar_membro(membro_id: int):
    membro_existe = None
    for membro in membros:
        if membro_id == membro["membro_id"]:
            membros.remove(membro)
            for personal in personais:
                if membro_id in personal["membro_id"]:
                    personal["membro_id"].remove(membro_id)
            membro_existe = 1
    if membro_existe is None:
        detalhe = "Não existe um membro com esse id para ser deletado"
        raise HTTPException(status_code=400, detail=detalhe)
    data["membro"] = membros
    data["personal"] = personais
    with open(file_json, "w") as arquivo:
        json.dump(data, arquivo, indent=4) 
    return membros


@app.delete("/personal/{personal_id}")
async def deletar_personal(personal_id: int):
    personal_existe = None
    for personal in personais:
        if personal_id == personal["personal_id"]:
            personais.remove(personal)
            for membro in membros:
                if personal_id == membro["personal_id"]:
                    membro["personal_id"] = None # Caso o plano seja apagado, o usuário fica sem plano (plano =0) até entrar em outro
            personal_existe = 1
    if personal_existe is None:
        detalhe = "Não existe um personal com esse id para ser deletado"
        raise HTTPException(status_code=400, detail=detalhe)
    data["personal"] = personais
    with open(file_json, "w") as arquivo:
        json.dump(data, arquivo, indent=4) 
    return personais


@app.delete("/plano/{plano_id}")
async def deletar_plano(plano_id: int):
    plano_existe = None
    for plano in planos:
        if plano_id == plano["plano_id"]:
            planos.remove(plano)
            for membro in membros:
                if plano_id == membro["plano_id"]:
                    membro["plano_id"] = 0 # Caso o plano seja apagado, o usuário fica sem plano (plano =0) até entrar em outro
                    membro["ativo"] = 0
            plano_existe = 1
    if plano_existe is None:
        detalhe = "Não existe um plano com esse id para ser deletado"    
        raise HTTPException(status_code=400, detail=detalhe)
    data["plano"] = planos
    data["membro"] = membros
    with open(file_json, "w") as arquivo:
        json.dump(data, arquivo, indent=4) 
    return planos


# POSTS :

def serializar_datetime(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


@app.post("/membro", status_code=201) 
async def adicionar_membro(membro: Membro):
    membros.append(membro.dict())
    data["membro"] = membros
    with open(file_json, "w") as arquivo:
        json.dump(data, arquivo, indent=4,default=serializar_datetime)  # indent=4 para formatar o JSON de forma legível
    return membro



@app.post("/plano",status_code=201)
async def adicionar_plano(plano: Plano):
    planos.append(plano.dict())
    data["plano"] = planos
    with open(file_json, "w") as arquivo:
        json.dump(data, arquivo, indent=4)  # indent=4 para formatar o JSON de forma legível
    return plano


@app.post("/personal",status_code=201)
async def adicionar_personal(personal: Personal):
    personais.append(personal.dict())
    data["personal"] = personais
    with open(file_json, "w") as arquivo:
        json.dump(data, arquivo, indent=4)  # indent=4 para formatar o JSON de forma legível
    return personal

# PUTS :
class MembroUpdate(BaseModel):
    nome: str | None = Field(min_length = 2, description="Nome do membro,precisa ter pelo menos duas letras", default=None,examples=["Raul"])
    sobrenome: str | None = Field(min_length = 2, description="Sobrenome do membro, precisa ter pelo menos duas letras", default=None,examples=["Silva"])
    genero: str | None = Field(default=None,min_length = 5, description="Genero do membro, precisa ter pelo menos cinco letras",examples=["Não definido"])
    cpf: str | None = Field(default=None,pattern=r'^\d*$', max_length=11, min_length=11,description="O cpf deve ter 11 dígitos, não inclua os pontos ( . ) e nem o traço ( - )", examples=["01234567891"]) 
    plano_id: int | None = Field(default=None, description="Identificador do plano na qual a pessoa está matriculada", examples =["1"])
    ativo: int | None = Field(default=None, description="0: se o membro não está ativo e 1: se o membro está ativo", examples =["0"])
    telefone: str | None = Field(pattern=r'^\d*$', max_length=11,description="O telefone deve ter 11 dígitos DDD+9+número , sem espaços!", default=None)
    email: str | None = Field(pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$',description="O email deve ser válido", default=None)
    personal_id: int | None = Field(default=None,gt=0, description="Colocando o id do personal", examples =["1"])
    restricao_medica: str | None = Field(description="Informações sobre restrições médicas a serem seguidas por um membro", examples =["Problema no joelho"], default=None)
    ultima_presenca: date | None = Field(default = None, description="Ultimo dia que o membro frequentou a academia")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "cpf" : "66569678302",
                    "plano_id" : 1,
                    "personal_id": 1,
                    "restrição_medica": "Problema na coluna"
                }
            ]
        }
    }

@app.put("/membro/{membro_id}")
async def update_membro(membro_id: int, membro: MembroUpdate):
    membro = membro.dict()
    membro_existe = None
    for memb in membros:
        if memb["membro_id"] == membro_id:
            for chave, valor in membro.items():
                if valor is not None:
                    memb[chave] = valor
            membro_existe = 1
    if membro_existe is None:
        detalhe = "Não existe um membro com esse id para ser alterado"    
        raise HTTPException(status_code=400, detail=detalhe)
    data["membro"] = membros
    with open(file_json, "w") as arquivo:
        json.dump(data, arquivo, indent=4, default=serializar_datetime)  # indent=4 para formatar o JSON de forma legível
    return membros

class PersonalUpdate(BaseModel):
    nome: str | None = Field(min_length = 2, description="Nome precisa ter pelo menos duas letras", default=None, examples=["Roberta"])
    sobrenome: str | None = None
    membro_id: list[int] | None = Field(default=None,description= "Uma lista com os identificadores dos membros da academia que o personal acompanha",examples=[2,3])
    cpf: str | None = Field(pattern=r'^\d*$', max_length=11, min_length=11,description="O cpf deve ter 11 dígitos, não inclua os pontos ( . ) e nem o traço ( - )", default=None) # pattern só permite números
    genero: str | None = None
    telefone: str | None = Field(pattern=r'^\d*$', max_length=11,description="O telefone deve ter 11 dígitos DDD+9+número , sem espaços!", default=None)
    email: str | None = Field(pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$',description="O email deve ser válido", default=None)
    salario: float | None = Field(gt=0, description="O salário precisa ser maior que zero!", default=None)
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "membro_id" : [3],
                    "telefone" : "88938472651",
                    "salario": 2900.0
                }
            ]
        }
    }

@app.put("/personal/{personal_id}")
async def update_personal(personal_id: int, personal: PersonalUpdate):
    personal = personal.dict()
    personal_existe = None
    for pers in personais:
        if pers["personal_id"] == personal_id:
            for chave, valor in personal.items():
                if valor is not None:
                    pers[chave] = valor
            personal_existe = 1
    if personal_existe is None:
        detalhe = "Não existe um personal com esse id para ser alterado"    
        raise HTTPException(status_code=400, detail=detalhe)
    data["personal"] = personais
    with open(file_json, "w") as arquivo:
        json.dump(data, arquivo, indent=4, default=serializar_datetime)  # indent=4 para formatar o JSON de forma legível
    return personais

class PlanoUpdate(BaseModel):
    nome: str | None = None
    descricao: str | None =  Field(default=None ,description="Mais detalhes sobre o plano",examples=["Plano mais completo com acompanhamento"])
    preco: float | None = Field(default=None,gt=0, description="O preço precisa ser maior que zero!",examples=[100])
    aulas_em_grupo: int | None = Field(default=None, description="0: se não oferece aulas em grupo e 1: se oferece aulas em grupo", examples = ["0"])
    promocao: int | None = Field( default=None,description="0: se o plano não está em promoção e 1: se o plano está em promoção",  examples = ["1"])
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "preco" : 150.0,
                    "promocao" :0
                }
            ]
        }
    }

@app.put("/plano/{plano_id}")
async def update_plano(plano_id: int, plano: PlanoUpdate):
    plano = plano.dict()
    plano_existe = None
    for plan in planos:
        if plan["plano_id"] == plano_id:
            for chave, valor in plano.items():
                if valor is not None:
                    plan[chave] = valor
            plano_existe = 1
    if plano_existe is None:
        detalhe = "Não existe um plano com esse id para ser alterado"    
        raise HTTPException(status_code=400, detail=detalhe)
    data["plano"] = planos
    with open(file_json, "w") as arquivo:
        json.dump(data, arquivo, indent=4, default=serializar_datetime)  # indent=4 para formatar o JSON de forma legível
    return planos