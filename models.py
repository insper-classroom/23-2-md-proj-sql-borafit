from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from database import Base
'''
Os models desse arquivo são os do SqlAlchemy,
não confundir com os do Pydantic, que estarão no schema.py
'''
class Membro(Base):
    __tablename__ = 'membros'  # Nome da tabela no banco de dados

    membro_id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    sobrenome = Column(String(50))
    genero = Column(String(50), nullable=False)
    cpf = Column(String(11), nullable=False, unique=True)
    plano_id = Column(Integer, nullable=False)
    ativo = Column(Integer, nullable=False)
    telefone = Column(String(11))
    email = Column(String(100), nullable=False, unique=True)
    personal_id = Column(Integer)
    restricao_medica = Column(String(100), default="nenhuma")
    data_inscricao = Column(Date, default=Date.now())
    ultima_presenca = Column(Date)

    def __init__(self, nome, sobrenome, genero, cpf, plano_id, ativo, telefone, email, personal_id, restricao_medica, ultima_presenca):
        self.nome = nome
        self.sobrenome = sobrenome
        self.genero = genero
        self.cpf = cpf
        self.plano_id = plano_id
        self.ativo = ativo
        self.telefone = telefone
        self.email = email
        self.personal_id = personal_id
        self.restricao_medica = restricao_medica
        self.ultima_presenca = ultima_presenca

    def __repr__(self):
        return f"<Membro(nome='{self.nome}', cpf='{self.cpf}')>"