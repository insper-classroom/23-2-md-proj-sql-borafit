### Rotas a serem implementadas:

#### GETS :
* ``/membro/{id_membro}`` informações do membro
* ``/membro/{nome}`` lista de membros com mesmo nome acompanhado do sobrenome 
    * ex: nome = Pedro 
    
        [{1 : Pedro Castro}, {5 : Pedro Mastro}, {id: nome+sobrenome}]
* ``/membro/{genero}`` lista de membros do genero digitado 
    * ex: genero = feminino

        [{2 : Giovana Cassoni}, {4 : Bruna Andrade}, {id: nome+sobrenome}]
* ``/membro/ativo/{ativo}`` lista de todos os membros que estão no estado escolhido
    * ex: ativo = 0

        [{2 : Giovana Cassoni}, {3 : Lincoln Melo}, {id: nome+sobrenome}]
* ``/membro/restricao/{restricao_medica}`` Lista de todos o membros que tem a restricao:
    * ex: restricao = Não pode fazer exercicios :)

        [{2 : Giovana Cassoni}, {3 : Lincoln Melo}, {id: nome+sobrenome}]
* ``/membro/plano/{plano_id}`` lista de todos os membros que estão no plano escolhido
    * ex: plano = 7 

        [{6 : Victor Assis}, {7 : Rafael Lima}, {id: nome+sobrenome}]
* ``/membro/plano/{nome}`` lista de todos os membros que estão no plano escolhido
    * ex: plano = Intensivo Master

        [{6 : Victor Assis}, {7 : Rafael Lima}, {id: nome+sobrenome}]
* ``/personal/{personal_id}`` Informações sobre o personal 
* ``/personal/{nome}`` lista de personais com mesmo nome acompanhado do sobrenome 
    * ex: nome = Fabio
        
        [{1 : Fabio Hage}, {5 : Fabio Bobrow}, {id: nome+sobrenome}]
* ``/personal/{genero}`` lista de personais do genero digitado 
    * ex: genero = feminino

        [{2 : Bárbara Tieko}, {3 : Paulina Achurra}, {id: nome+sobrenome}]
* ``/personal/membro/{membro_id}`` Informações do personal de um membro especificado
* ``/personal/{personal_id}/membros`` Lista de todos os membros que o personal acompanha
* ``/plano/{plano_id}`` Informações sobre o plano
* ``/plano/{plano_id}/membros`` Lista de membros que estão no plano especificado
* ``/plano/{nome}`` Informações sobre o plano
* ``/plano/{nome}/membros``  Lista de membros que estão no plano especificado 
* ``/plano/promocao`` Lista planos que possuem promoção
* ``/plano/aulas_em_grupo`` Lista planos que possuem aulas em grupo

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

# LEMBRAR de mostrar mensagens de erros e colocar exemplos!!!
