from sqlalchemy.orm import Session
from . import models, schemas


def get_subprefeitura(db: Session, sigla: str):
    return db.query(models.Subprefeitura).filter(models.Subprefeitura.sigla == sigla).first()


def get_subprefeituras(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Subprefeitura).offset(skip).limit(limit).all()


def create_subprefeitura(db: Session, subprefeitura: schemas.SubprefeituraCreate):

    obj = models.Subprefeitura(**subprefeitura.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_distrito(db: Session, sigla: str):
    return db.query(models.Distrito).filter(models.Distrito.sigla == sigla).first()


def get_distritos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Distrito).offset(skip).limit(limit).all()


def create_distrito(db: Session, distrito: schemas.DistritoCreate, subprefeitura_id: int):

    obj = models.Distrito(**distrito.dict(), id_subprefeitura=subprefeitura_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_endereco(db: Session, endereco_completo: str):
    return db.query(models.Endereco).filter(models.Endereco.endereco_completo == endereco_completo).first()

def get_endereco_by_id(db: Session, id_endereco: int):
    return db.query(models.Endereco).filter(models.Endereco.id == id_endereco).first()


def get_enderecos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Endereco).offset(skip).limit(limit).all()


def create_endereco(db: Session, endereco: schemas.EnderecoCreate, subprefeitura_id: int, distrito_id: int):

    obj = models.Endereco(**endereco.dict(), id_subprefeitura=subprefeitura_id, id_distrito=distrito_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_municipe(db: Session, email: str):
    return db.query(models.Municipe).filter(models.Municipe.email == email).first()


def get_municipes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Municipe).offset(skip).limit(limit).all()


def create_municipe(db: Session, municipe: schemas.MunicipeCreate, id_endereco: int):

    obj = models.Municipe(**municipe.dict(), id_endereco=id_endereco)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_canal(db: Session, nome_canal: str):

    return db.query(models.Canal).filter(models.Canal.canal == nome_canal).first()


def get_canais(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Canal).offset(skip).limit(limit).all()


def create_canal(db: Session, canal: schemas.CanalCreate):

    obj = models.Canal(**canal.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_contribuicao(db: Session, conteudo: str, canal_id: int, municipe_id: int):

    contrib =  db.query(models.Contribuicao).filter(
        models.Contribuicao.conteudo == conteudo,
        models.Contribuicao.autor_id == municipe_id,
        models.Contribuicao.canal_id == canal_id
    ).first()

    return contrib


def get_contribuicoes(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Contribuicao).offset(skip).limit(limit).all()

def get_contribuicoes_by_autor(db: Session, autor_id: int, skip: int = 0, limit: int = 100):

    return db.query(models.Contribuicao).filter(
        models.Contribuicao.autor_id == autor_id).offset(skip).limit(limit).all()


def create_contribuicao(db: Session, contribuicao: schemas.ContribuicaoCreate, municipe_id: int, canal_id: int):

    obj = models.Contribuicao(**contribuicao.dict(), canal=canal_id, autor=municipe_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_secretaria(db: Session, sigla: str):

    return db.query(models.Secretaria).filter(models.Secretaria.sigla == sigla).first()


def get_secretarias(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Secretaria).offset(skip).limit(limit).all()


def create_secretaria(db: Session, secretaria: schemas.SecretariaCreate):

    obj = models.Secretaria(**secretaria.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_tema(db: Session, nome_tema: str):

    return db.query(models.Tema).filter(models.Tema.nome == nome_tema).first()


def get_temas(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Tema).offset(skip).limit(limit).all()


def create_tema(db: Session, tema: schemas.TemaCreate):

    obj = models.Tema(**tema.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_eixo(db: Session, nome: str):

    return db.query(models.Eixo).filter(models.Eixo.nome == nome).first()


def get_eixos(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Eixo).offset(skip).limit(limit).all()


def create_eixo(db: Session, eixo: schemas.EixoCreate):

    obj = models.Eixo(**eixo.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_subtema(db: Session, nome: str):

    return db.query(models.Subtema).filter(models.Subtema.nome == nome).first()


def get_subtemas(db: Session, tema_id: int, skip: int = 0, limit: int = 100):

    return db.query(models.Subtema).filter(models.Subtema.tema_id == tema_id).offset(skip).limit(limit).all()


def create_subtema(db: Session, subtema: schemas.SubtemaCreate, tema_id:int, eixo_id:int):

    obj = models.Subtema(**subtema.dict(), tema_id=tema_id, eixo_id=eixo_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_sugestao(db: Session, conteudo: str, contribuicao_id: int, subprefeitura_id: int, subtema_id: int):

    return db.query(models.Sugestao).filter(
        models.Sugestao.sugestao == conteudo,
        models.Sugestao.contribuicao_id == contribuicao_id,
        models.Sugestao.subprefeitura_id == subprefeitura_id,
        models.Sugestao.subtema_id == subtema_id,
    ).first()


def get_sugestoes_by_contrib(db: Session, contrib_id: int, skip: int = 0, limit: int = 100):

    return db.query(models.Sugestao).filter(
        models.Sugestao.contribuicao_id == contrib_id
        ).offset(skip).limit(limit).all()

def get_sugestoes_by_subtema(db: Session, subtema_id: int, skip: int = 0, limit: int = 100):

    return db.query(models.Sugestao).filter(
        models.Sugestao.subtema_id == subtema_id
        ).offset(skip).limit(limit).all()

def get_sugestoes_by_subprefeitura(db: Session, subprefeitura_id: int, skip: int = 0, limit: int = 100):

    return db.query(models.Sugestao).filter(
        models.Sugestao.subprefeitura_id == subprefeitura_id
        ).offset(skip).limit(limit).all()

def get_sugestoes(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Sugestao).offset(skip).limit(limit).all()


def create_sugestao(db: Session, sugestao: schemas.SugestaoCreate, contribuicao_id:int,
                        subprefeitura_id:int, subtema_id:int):

    obj = models.Sugestao(**sugestao.dict(), contribuicao_id=contribuicao_id,
                            subprefeitura_id=subprefeitura_id,subtema_id=subtema_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_categoria_resposta(db: Session, categoria: str):

    return db.query(models.CategoriaResposta).filter(models.CategoriaResposta.nome == categoria).first()


def get_categorias_resposta(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.CategoriaResposta).offset(skip).limit(limit).all()


def create_categoria_resposta(db: Session, categoria_resposta: schemas.CategoriaRespostaCreate):

    obj = models.CategoriaResposta(**categoria_resposta.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_resposta(db: Session, conteudo: str, categoria_id: int,  subtema_id : int, secretaria_id: int):

    return db.query(models.Resposta).filter(
        models.Resposta.conteudo == conteudo,
        models.Resposta.subtema_id == subtema_id,
        models.Resposta.secretaria_id == secretaria_id,
        models.Resposta.categoria_id == categoria_id
        ).first()


def get_respostas(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Resposta).offset(skip).limit(limit).all()


def get_respostas_by_secretaria(db: Session, secretaria_id, skip: int = 0, limit: int = 100):

    return db.query(models.Resposta).filter(
        models.Resposta.secretaria_id == secretaria_id
    ).offset(skip).limit(limit).all()

def get_respostas_by_subtema(db: Session, subtema_id: int, skip: int = 0, limit: int = 100):

    return db.query(models.Resposta).filter(
        models.Resposta.subtema_id == subtema_id
    ).offset(skip).limit(limit).all()

def get_respostas_by_categoria(db: Session, id_categoria: int, skip: int = 0, limit: int = 100):

    return db.query(models.Resposta).filter(
        models.Resposta.categoria_id == id_categoria
    ).offset(skip).limit(limit).all()


def create_resposta(db: Session, resposta: schemas.RespostaCreate, categoria_id: int,
                    subtema_id: int, secretaria_id: int):

    obj = models.Resposta(**resposta.dict(), categoria_id=categoria_id,
                          subtema_id=subtema_id, secretaria_id=secretaria_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj




