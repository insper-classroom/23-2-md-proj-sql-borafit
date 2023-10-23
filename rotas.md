## Rotas implementadas:

#### GETS :
* ``/membro/id/{id_membro}`` informações do membro
* ``/membro/nome/{nome}`` dicionario de membros com mesmo nome acompanhado do sobrenome 
    * ex: nome = Pedro 
    
        {1 : "Pedro Castro", 5 : "Pedro Mastro", id: nome+sobrenome}
* ``/membro/genero/{genero}`` dicionario de membros do genero digitado 
    * ex: genero = feminino

        {2 : "Giovana Cassoni", 4 : "Bruna Andrade", id: nome+sobrenome}
* ``/membro/ativo/{ativo}`` dicionario de todos os membros que estão no estado escolhido
    * ex: ativo = 0

        {2 : "Giovana Cassoni", 3 : "Lincoln Melo", id: nome+sobrenome}
* ``/membro/restricao/{restricao_medica}`` dicionario de todos o membros que tem a restricao:
    * ex: restricao = Não pode fazer exercicios :)

        {2 : Giovana Cassoni, 3 : Lincoln Melo, id: nome+sobrenome}
* ``/membro/plano/{plano_id}`` dicionario de todos os membros que estão no plano escolhido
    * ex: plano = 7 

        {6 : Victor Assis, 7 : Rafael Lima, id: nome+sobrenome}
* ``/membro/plano/nome/{nome}`` dicionario de todos os membros que estão no plano escolhido
    * ex: plano = Intensivo Master

        {6 : Victor Assis, 7 : Rafael Lima, id: nome+sobrenome}
* ``/personal/personal_id/{personal_id}`` informações sobre o personal 
* ``/personal/nome/{nome}`` dicionario de personais com mesmo nome acompanhado do sobrenome 
    * ex: nome = Fabio
        
        {1 : Fabio Hage, 5 : Fabio Bobrow, id: nome+sobrenome}
* ``/personal/genero/{genero}`` dicionario de personais do genero digitado 
    * ex: genero = feminino

        {2 : Bárbara Tieko, 3 : Paulina Achurra, id: nome+sobrenome}
* ``/personal/membro/{membro_id}`` informações do personal de um membro especificado
* ``/personal/personal_id/{personal_id}/membros`` dicionario de todos os membros que o personal acompanha
    * ex: personal_id = 2

        {2 : [
            {
                "membro_id": 1,
                "nome": "Pedro",
                "sobrenome": "Silva",
                "genero": "Masculino",
                "cpf": "12345678901",
                "plano_id": 1,
                "ativo": 1,
                "data_inscricao": "2023-10-20T12:00:00",
                "ultima_presenca": "2023-10-20T18:30:00",
                "telefone": "999999999",
                "email": "pedros@example.com",
                "personal_id": 2,
                "restricao_medica": "Nenhuma"
            },
            {
                "membro_id": 2,
                "nome": "Giovana",
                "sobrenome": "Santos",
                "genero": "Feminino",
                "cpf": "98765432109",
                "plano_id": 2,
                "ativo": 1,
                "data_inscricao": "2023-10-21T10:30:00",
                "ultima_presenca": "2023-10-21T17:15:00",
                "telefone": "888888888",
                "email": "giovanas@example.com",
                "personal_id": 2,
                "restricao_medica": "Nenhuma"
            }
        ]}
* ``/plano/id/{plano_id}`` informações sobre o plano
* ``/plano/plano_id/{plano_id}/membros`` dicionario de membros que estão no plano especificado
    * ex: plano_id = 1

        {2 : Giovana Cassoni, 3 : Lincoln Melo, id: nome+sobrenome}
* ``/plano/nome/{nome}`` informações sobre o plano
* ``/plano/nome/{nome}/membros``  dicionario de membros que estão no plano especificado 
    * ex: nome = Basico

        {1 : [
            {
                "membro_id": 1,
                "nome": "Pedro",
                "sobrenome": "Silva",
                "genero": "Masculino",
                "cpf": "12345678901",
                "plano_id": 1,
                "ativo": 1,
                "data_inscricao": "2023-10-20T12:00:00",
                "ultima_presenca": "2023-10-20T18:30:00",
                "telefone": "999999999",
                "email": "pedros@example.com",
                "personal_id": 1,
                "restricao_medica": "Nenhuma"
            },
            {
                "membro_id": 2,
                "nome": "Giovana",
                "sobrenome": "Santos",
                "genero": "Feminino",
                "cpf": "98765432109",
                "plano_id": 1,
                "ativo": 1,
                "data_inscricao": "2023-10-21T10:30:00",
                "ultima_presenca": "2023-10-21T17:15:00",
                "telefone": "888888888",
                "email": "giovanas@example.com",
                "personal_id": 2,
                "restricao_medica": "Nenhuma"
            }
        ]}
* ``/plano/promocao`` dicionario de planos que possuem promoção
    * ex: {2 : Premium, 3 : Intensivo, id: nome}
* ``/plano/aulas_em_grupo`` dicionario planos que possuem aulas em grupo
    * ex: {1 : Basico, 2 : Premium, id: nome}

#### POSTS:
Aqui recebemos uma formatação em json para adicionar.

* ``/membro``
* ``/plano``
* ``/personal``

#### DELETE:
* ``/membro/{membro_id}``  deleta o membro 
* ``/personal/{personal_id}`` deleta o personal
* ``/plano/{plano_id}``       deleta o plano

#### PUT/UPDATE:
Aqui recebemos um json para dar o update. ps: não precisa passar o json inteiro, apenas as informações que se deseja mudar

* ``membro/{membro_id}`` 
* ``personal/{personal_id}``
* ``plano/{plano_id}``
