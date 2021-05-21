from typing import List, Optional
from pydantic import BaseModel


class RespostaBase(BaseModel):

    conteudo: str

class RespostaCreate(RespostaBase):

    pass


class Resposta(RespostaBase):

    id: int
    categoria_id: int
    subtema_id: int
    secretaria_id: int
    class Config:
        orm_mode = True


class SugestaoBase(BaseModel):

    sugestao: str

class SugestaoCreate(SugestaoBase):

    pass


class Sugestao(SugestaoBase):

    id: int
    contribuicao_id: int
    subprefeitura_id: int
    subtema_id: int
    class Config:
        orm_mode = True

class ContribuicaoBase(BaseModel):

    conteudo: str

class ContribuicaoCreate(ContribuicaoBase):

    pass

class Contribuicao(ContribuicaoBase):

    id: int
    canal_id: int
    autor_id: int
    sugestoes: List[Sugestao] = []

    class Config:
        orm_mode = True

class MunicipeBase(BaseModel):

    email: str
    f_name: str
    l_name: str

class MunicipeCreate(MunicipeBase):

    pass


class Municipe(MunicipeBase):

    id: int
    endereco_id: int
    contribuicoes: List[Contribuicao] = []

    class Config:
        orm_mode = True

class EnderecoBase(BaseModel):

    endereco_completo: str
    cidade: str
    georreferenciado: bool
    lat: str
    long: str



class EnderecoCreate(EnderecoBase):

    pass


class Endereco(EnderecoBase):

    id: int
    id_distrito: int
    id_subprefeitura: int
    moradores: List[Municipe] = []

    class Config:
        orm_mode = True

class DistritoBase(BaseModel):

    nome: str
    sigla: str


class DistritoCreate(DistritoBase):

    pass


class Distrito(DistritoBase):

    id: int
    id_subprefeitura: int
    enderecos: List[Endereco] = []
    sugestoes: List[Sugestao] = []

    class Config:
        orm_mode = True

class SubprefeituraBase(BaseModel):

    nome: str
    sigla: str

class SubprefeituraCreate(SubprefeituraBase):

    pass

class Subprefeitura(SubprefeituraBase):

    id: int
    distritos: List[Distrito] = []
    sugestoes: List[Sugestao] = []

    class Config:
        orm_mode = True


class CanalBase(BaseModel):

    canal: str


class CanalCreate(CanalBase):

    pass


class Canal(CanalBase):

    id: int
    contribuicoes: List[Contribuicao] = []

    class Config:
        orm_mode = True


class SecretariaBase(BaseModel):

    sigla: str
    nome: int


class SecretariaCreate(SecretariaBase):

    pass


class Secretaria(SecretariaBase):
    id: int
    sugestoes: List[Sugestao] = []

    class Config:
        orm_mode = True


class SubtemaBase(BaseModel):

    nome: str


class SubtemaCreate(SubtemaBase):

    pass


class Subtema(SubtemaBase):

    id: int
    tema_id: int
    eixo_id: int
    sugestoes: List[Sugestao] = []

    class Config:
        orm_mode = True


class TemaBase(BaseModel):

    nome: str


class TemaCreate(TemaBase):

    pass


class Tema(TemaBase):
    id: int
    subtemas: List[Subtema] = []

    class Config:
        orm_mode = True

class EixoBase(BaseModel):

    nome: str


class EixoCreate(EixoBase):

    pass


class Eixo(EixoBase):

    id: int
    subtemas: List[Subtema] = []

    class Config:
        orm_mode = True


class CategoriaRespostaBase(BaseModel):

    nome: str


class CategoriaRespostaCreate(CategoriaRespostaBase):

    pass


class CategoriaResposta(CategoriaRespostaBase):

    id: int
    respostas: List[Resposta] = []
    class Config:
        orm_mode = True






