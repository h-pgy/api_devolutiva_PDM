from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# SUBPREFEITURA

@app.post("/subprefeituras/", response_model=schemas.Subprefeitura)
def create_subprefeitura(subprefeitura: schemas.SubprefeituraCreate, db: Session = Depends(get_db)):
    obj = crud.get_subprefeitura(db, sigla=subprefeitura.sigla)
    if obj:
        raise HTTPException(status_code=400, detail="Object already created")
    return crud.create_subprefeitura(db=db, subprefeitura=subprefeitura)


@app.get("/subprefeituras/", response_model=List[schemas.Subprefeitura])
def read_subprefeituras(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    objs = crud.get_subprefeituras(db, skip=skip, limit=limit)
    return objs

# DISTRITOS

@app.post("/subprefeituras/{subprefeitura_sigla}/distritos/", response_model=schemas.Distrito)
def create_distrito(subprefeitura_sigla: str, distrito: schemas.DistritoCreate, db: Session = Depends(get_db)):
    subs = crud.get_subprefeitura(db, sigla=subprefeitura_sigla)
    if not subs:
        raise HTTPException(status_code=400, detail="Subprefeitura não existente")
    obj = crud.get_distrito(db, sigla=distrito.sigla)
    if obj:
        raise HTTPException(status_code=400, detail="Object already created")
    return crud.create_distrito(db=db, distrito=distrito, subprefeitura_id=subs.id)


@app.get("/distritos/", response_model=List[schemas.Distrito])
def read_distritos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    objs = crud.get_distritos(db, skip=skip, limit=limit)
    return objs

# ENDEREÇOS

@app.post("/subprefeituras/{subprefeitura_sigla}/distritos/{distrito_sigla}/enderecos/", response_model=schemas.Endereco)
def create_endereco(subprefeitura_sigla: str, distrito_sigla: str, endereco: schemas.EnderecoCreate,
                    db: Session = Depends(get_db)):
    subs = crud.get_subprefeitura(db, sigla=subprefeitura_sigla)
    if not subs:
        raise HTTPException(status_code=400, detail="Subprefeitura não existente")
    dist = crud.get_distrito(db, sigla=distrito_sigla)
    if not dist:
        raise HTTPException(status_code=400, detail="Distrito não existente")
    obj = crud.get_endereco(db, endereco_completo=endereco.endereco_completo)
    if obj:
        raise HTTPException(status_code=400, detail="Object already created")
    return crud.create_endereco(db=db, endereco=endereco,subprefeitura_id=subs.id, distrito_id=dist.id)

# depois posso criar rota que tem que passar pela subs e pelo distrito
# por enquanto vou deixar flat mesmo a busca
# ou entao talvez seja o caso mesmo de nem ter esse endpoint...
@app.get("/enderecos/", response_model=List[schemas.Endereco])
def read_enderecos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    objs = crud.get_enderecos(db, skip=skip, limit=limit)
    return objs

# MUNICIPES

@app.post("/municipes/", response_model=schemas.Municipe)
def create_municipe(municipe: schemas.MunicipeCreate, id_endereco: Optional[int] = None,
                    db: Session = Depends(get_db)):

    if id_endereco is None:
        endereco = crud.get_endereco_by_id(db, 99999)
    else:
        endereco = crud.get_endereco_by_id(db, id_endereco)
        if not endereco:
            raise HTTPException(status_code=400, detail="Endereço não registrado")
    obj = crud.get_municipe(db, email=municipe.email)
    if obj:
        raise HTTPException(status_code=400,
                            detail=f"Municipe {municipe.f_name + ' ' + municipe.l_name} already created")
    return crud.create_municipe(db=db, municipe=municipe, id_endereco=endereco.id)


# TALVEZ PRECISE REMOVER OU PASSAR UM TOKEN PARA ESSE AQUI
@app.get("/municipes/{email}", response_model=schemas.Municipe)
def read_municipe(email: str, db: Session = Depends(get_db)):
    obj = crud.get_municipe(db, email=email)
    if obj is None:
        raise HTTPException(status_code=404, detail=f"Municipe com email {email} not found")
    return obj

# CANAIS PARTICIPACAO

@app.post("/canais_participacao/", response_model=schemas.Canal)
def create_canal(canal: schemas.CanalCreate, db: Session = Depends(get_db)):
    obj = crud.get_canal(db, nome_canal=canal.canal)
    if obj:
        raise HTTPException(status_code=400, detail="Object already created")
    return crud.create_canal(db=db, canal=canal)


@app.get("/canais_participacao/", response_model=List[schemas.Canal])
def read_canais(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    objs = crud.get_canais(db, skip=skip, limit=limit)
    return objs

# SECRETARIAS

@app.post("/secretarias/", response_model=schemas.Secretaria)
def create_secretaria(secretaria: schemas.SecretariaCreate, db: Session = Depends(get_db)):
    obj = crud.get_secretaria(db, sigla=secretaria.sigla)
    if obj:
        raise HTTPException(status_code=400, detail=f"Secretaria {secretaria.sigla} already created")
    return crud.create_secretaria(db=db, secretaria=secretaria)


@app.get("/secretarias/", response_model=List[schemas.Secretaria])
def read_secretarias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    objs = crud.get_secretarias(db, skip=skip, limit=limit)
    return objs

# EIXOS PDM

@app.post("/eixos/", response_model=schemas.Eixo)
def create_eixo(eixo: schemas.EixoCreate, db: Session = Depends(get_db)):
    obj = crud.get_eixo(db, nome=eixo.nome)
    if obj:
        raise HTTPException(status_code=400, detail=f"Eixo {eixo.nome} already created")
    return crud.create_eixo(db=db, eixo=eixo)


@app.get("/eixos/", response_model=List[schemas.Eixo])
def read_eixos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    objs = crud.get_eixos(db, skip=skip, limit=limit)
    return objs

# TEMATICAS

@app.post("/tematicas/", response_model=schemas.Tema)
def create_tema(tema: schemas.TemaCreate, db: Session = Depends(get_db)):
    obj = crud.get_tema(db, nome_tema=tema.nome)
    if obj:
        raise HTTPException(status_code=400, detail=f"Tema {tema.nome} already created")
    return crud.create_tema(db=db, tema=tema)


@app.get("/tematicas/", response_model=List[schemas.Tema])
def read_temas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    objs = crud.get_temas(db, skip=skip, limit=limit)
    return objs

# SUBTEMAS

@app.post("/tematicas/{nome_tema}/subtemas/", response_model=schemas.Subtema)
def create_subtema(subtema: schemas.SubtemaCreate, nome_tema: str, nome_eixo: Optional[str] = None,
                   db: Session = Depends(get_db)):

    tema = crud.get_tema(db, nome_tema=nome_tema)
    if not tema:
        raise HTTPException(status_code=400, detail="Tema não existente")
    if nome_eixo is None:
        nome_eixo = 'Não Informado'
    eixo = crud.get_eixo(db, nome=nome_eixo)
    if not tema:
        raise HTTPException(status_code=400, detail="Tema não existente")

    obj = crud.get_subtema(db, subtema.nome)
    if obj:
        raise HTTPException(status_code=400, detail=f"Tema {tema.nome} already created")
    return crud.create_subtema(db=db, subtema=subtema, tema_id=tema.id, eixo_id=eixo.id)


@app.get("/tematicas/{nome_tema}/subtemas/", response_model=List[schemas.Subtema])
def read_subtemas(nome_tema: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    tema = crud.get_tema(db, nome_tema=nome_tema)
    if not tema:
        raise HTTPException(status_code=400, detail="Tema não existente")
    objs = crud.get_subtemas(db, tema_id=tema.id, skip=skip, limit=limit)
    return objs

# CONTRIBUICAO

@app.post("/municipes/{email}/contribuicoes/{canal_participacao}/", response_model=schemas.Contribuicao)
def create_contribuicao(contribuicao: schemas.ContribuicaoCreate, email: str, canal_participacao: str,
                        db: Session = Depends(get_db)):

    municipe = crud.get_municipe(db, email=email)
    if not municipe:
        raise HTTPException(status_code=400, detail=f"Municipe {email} não existente")
    canal = crud.get_canal(db, nome_canal=canal_participacao)
    if not municipe:
        raise HTTPException(status_code=400, detail=f"Canal {canal_participacao} não existente")

    obj = crud.get_contribuicao(db, contribuicao.conteudo, canal.id, municipe.id)
    if obj:
        raise HTTPException(status_code=400, detail=f"Contribuicao already created")
    return crud.create_contribuicao(db, contribuicao, municipe.id, canal.id)


@app.get("/municipes/{email}/contribuicoes/", response_model=List[schemas.Contribuicao])
def read_contribuicoes_by_municipe(email_autor: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    municipe = crud.get_municipe(db, email=email_autor)
    if not municipe:
        raise HTTPException(status_code=400, detail=f"Municipe {email_autor} não existente")
    objs = crud.get_contribuicoes_by_autor(db, autor_id=municipe.id, skip=skip, limit=limit)
    return objs


@app.get("/contribuicoes/", response_model=List[schemas.Contribuicao])
def read_contribuicoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    objs = crud.get_contribuicoes(db, skip=skip, limit=limit)
    return objs


# SUGESTAO

# a sugestao é muito amarrada, então fiz  create em cima dos IDs mesmo
# precisa ter aplicação para cuidar dessa criação
@app.post("/sugestoes/", response_model=schemas.Sugestao)
def create_sugestao(sugestao: schemas.SugestaoCreate, contribuicao_id: int, subprefeitura_id: int,
                        subtema_id: int, db: Session = Depends(get_db)):

    obj = crud.get_sugestao(db, sugestao.sugestao, contribuicao_id, subprefeitura_id, subtema_id)
    if obj:
        raise HTTPException(status_code=400, detail=f"Sugestao already created")
    return crud.create_sugestao(db, sugestao, contribuicao_id, subprefeitura_id, subtema_id)


@app.get("/contribuicoes/{id_contribuicao}/sugestoes", response_model=List[schemas.Sugestao])
def read_sugestoes_by_contribuicao(id_contribuicao: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    objs = crud.get_sugestoes_by_contrib(db, contrib_id=id_contribuicao, skip=skip, limit=limit)
    return objs


@app.get("/subtemas/{id_subtema}/sugestoes", response_model=List[schemas.Sugestao])
def read_sugestoes_by_subtemas(id_subtema: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    objs = crud.get_sugestoes_by_subtema(db, subtema_id=id_subtema, skip=skip, limit=limit)
    return objs


@app.get("/subprefeituras/{sigla_subprefeitura}/sugestoes", response_model=List[schemas.Sugestao])
def read_sugestoes_by_subprefeituras(sigla_subprefeitura: str, skip: int = 0, limit: int = 100,
                                     db: Session = Depends(get_db)):

    subs = crud.get_subprefeitura(db, sigla=sigla_subprefeitura)
    if not subs:
        raise HTTPException(status_code=400, detail=f"Subprefeitura {sigla_subprefeitura} não existente!")
    objs = crud.get_sugestoes_by_subprefeitura(db, subprefeitura_id=subs.id, skip=skip, limit=limit)
    return objs


@app.get("/sugestoes/", response_model=List[schemas.Sugestao])
def read_sugestoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    objs = crud.get_sugestoes(db, skip=skip, limit=limit)
    return objs


# CATEGORIAS DE RESPOSTA

@app.post("/categorias_resposta/", response_model=schemas.CategoriaResposta)
def create_categoria_resposta(categoria: schemas.CategoriaRespostaCreate, db: Session = Depends(get_db)):
    obj = crud.get_categoria_resposta(db, categoria.nome)
    if obj:
        raise HTTPException(status_code=400, detail=f"Categoria de resposta {categoria.nome} already created")
    return crud.create_categoria_resposta(categoria)

@app.get("/categorias_resposta/", response_model=List[schemas.CategoriaResposta])
def read_categorias_resposta(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    objs = crud.get_categorias_resposta(db, skip=skip, limit=limit)
    return objs


#RESPOSTA

# Resposta obj também é complexo e é melhor a aplicação cuidar da criação
@app.post("/respostas/", response_model=schemas.Resposta)
def create_resposta(resposta: schemas.RespostaCreate, categoria_id: int, subtema_id: int,
                    secretaria_id: int, db: Session = Depends(get_db)):

    obj = crud.get_resposta(db, conteudo=resposta.conteudo, subtema_id=subtema_id,
                            secretaria_id=secretaria_id, categoria_id=categoria_id)
    if obj:
        raise HTTPException(status_code=400, detail=f"Resposta already created")
    return crud.create_resposta(db, resposta, categoria_id = categoria_id,
                                subtema_id=subtema_id, secretaria_id=secretaria_id)

@app.get("/respostas/", response_model=List[schemas.Resposta])
def read_respostas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    objs = crud.get_respostas(db, skip=skip, limit=limit)
    return objs

@app.get("/secretarias/{sigla}/respostas/", response_model=List[schemas.Resposta])
def read_respostas_by_secretaria(sigla: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    secretaria = crud.get_secretaria(db, sigla=sigla)
    if not secretaria:
        raise HTTPException(status_code=400, detail=f"Secretaria {sigla} não existente!")
    objs = crud.get_respostas_by_secretaria(db, secretaria_id=secretaria.id, skip=skip, limit=limit)
    return objs

@app.get("/subtemas/{id_subtema}/respostas/", response_model=List[schemas.Resposta])
def read_respostas_by_subtema(id_subtema: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    objs = crud.get_respostas_by_subtema(db, subtema_id=id_subtema, skip=skip, limit=limit)
    return objs

@app.get("/categorias_resposta/{id_categoria}/respostas/", response_model=List[schemas.Resposta])
def read_respostas_by_subtema(id_categoria: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    objs = crud.get_respostas_by_categoria(db, id_categoria=id_categoria, skip=skip, limit=limit)
    return objs


if __name__ == "__main__":

    models.Base.metadata.create_all(bind=engine)
