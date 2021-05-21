from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
#importamos Base para os modelos, que criamos no arquivo database
from .database import Base

class Subprefeitura(Base):

    __tablename__ = 'subprefeituras'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    sigla = Column(String(length=3), nullable=False)
    distritos = relationship("Distrito")
    sugestoes = relationship("Sugestao")

    def __repr__(self):
        return f'< Subprefeitura ({self.sigla}) >'

class Distrito(Base):

    __tablename__ = 'distritos'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    sigla = Column(String(length=3), nullable=False)
    id_subprefeitura = Column(Integer, ForeignKey('subprefeituras.id'))
    enderecos = relationship("Endereco")

    def __repr__(self):
        return f'< Distrito ({self.sigla}) >'

class Endereco(Base):

    __tablename__ = 'enderecos'

    id = Column(Integer, primary_key=True, index=True)
    endereco_completo = Column(String, nullable=False)
    cidade = Column(String, nullable=False)
    georreferenciado = Column(Boolean, nullable=False)

    lat = Column(String, nullable=True)
    long = Column(String, nullable=True)

    id_distrito = Column(Integer, ForeignKey('distritos.id'))
    id_subprefeitura = Column(Integer, ForeignKey('subprefeituras.id'))
    moradores = relationship("Municipe")

    def __repr__(self):
        return f'< Endereco ({self.endereco_completo[:20] + "..."}) >'


class Municipe(Base):
    __tablename__ = "municipes"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    f_name = Column(String, unique= False, nullable= False)
    l_name = Column(String, unique= False, nullable=False)

    id_endereco = Column(Integer, ForeignKey('enderecos.id'))
    contribuicoes = relationship('Contribuicao')

    def __repr__(self):
        return f'< Munícipe ({self.email}) >'

class Canal(Base):
    __tablename__ = "canais"

    id = Column(Integer, primary_key=True, index=True)
    canal = Column(String, nullable=False)
    contribuicoes = relationship('Contribuicao')

    def __repr__(self):
        return f'< Canal de participacao ({self.canal}) >'

class Contribuicao(Base):
    __tablename__ = 'contribuicoes'

    id = Column(Integer, primary_key=True, index=True)
    canal_id = Column(Integer, ForeignKey('canais.id'))
    autor_id = Column(Integer, ForeignKey('municipes.id'))
    conteudo = Column(String, nullable=False)
    sugestoes = relationship('Sugestao')

    def __repr__(self):
        return f'< Contribuicao ({self.id}) >'

class Secretaria(Base):
    __tablename__ = "secretarias"

    id = Column(Integer, primary_key=True, index=True)
    sigla = Column(String(length=5), nullable=False, unique=True)
    nome = Column(String, nullable=False, unique=True)
    respostas = relationship('Resposta')

    def __repr__(self):
        return f'< Secretaria ({self.sigla} >'

class Tema(Base):
    __tablename__ = "temas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)
    subtemas = relationship('Subtema')

    def __repr__(self):
        return f'< Tema ({self.id} >'

class Eixo(Base):
    __tablename__ = "eixos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)
    subtemas = relationship('Subtema')

    def __repr__(self):
        return f'< Eixo ({self.id} >'

class Subtema(Base):
    __tablename__ = "subtemas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)
    tema_id = Column(Integer, ForeignKey('temas.id'))
    eixo_id = Column(Integer, ForeignKey('eixos.id'))
    sugestoes = relationship('Sugestao')
    respostas = relationship('Resposta')

    def __repr__(self):
        return f'< Subtema ({self.id} >'

class Sugestao(Base):
    __tablename__ = "sugestoes"

    id = Column(Integer, primary_key=True, index=True)
    sugestao = Column(String, nullable=False, unique=True)
    contribuicao_id = Column(Integer, ForeignKey('contribuicoes.id'))
    subprefeitura_id = Column(Integer, ForeignKey('subprefeituras.id'))
    subtema_id = Column(Integer, ForeignKey('subtemas.id'))


    def __repr__(self):
        return f'< Sugestao ({self.id} >'

class CategoriaResposta(Base):
    __tablename__ = "categ_resps"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)
    respostas = relationship('Resposta')

    def __repr__(self):
        return f'< Categoria Resposta ({self.id}) >'


class Resposta(Base):
    __tablename__ = "respostas"

    id = Column(Integer, primary_key=True, index=True)
    conteudo = Column(String, nullable=False, unique=True)
    categoria_id = Column(Integer, ForeignKey('categ_resps.id'))
    subtema_id = Column(Integer, ForeignKey('subtemas.id'))
    secretaria_id = Column(Integer, ForeignKey('secretarias.id'))

    categoria = relationship("CategoriaResposta", back_populates="respostas")
    subtema = relationship("Subtema", back_populates="respostas")
    secretaria = relationship("Secretaria", back_populates="respostas")

    def __repr__(self):
        return f'< Resposta ({self.id} >'








