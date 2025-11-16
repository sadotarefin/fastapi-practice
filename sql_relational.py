from typing import Annotated
from fastapi import FastAPI, Query, Depends, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select

class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)

class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str

class HeroPublic(HeroBase):
    id: int

class HeroCreate(HeroBase):
    secret_name: str

class HeroUpdate(HeroBase):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None

sqlite_full_name = "databse.db"
sqlite_url = f"sqlite:///{sqlite_full_name}"
connect_args = {"check_same_thread": False} #allows same sqlite db in different threads
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/heros/", response_model=HeroPublic)
def create_hero(hero: HeroCreate, session: SessionDep):
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@app.get("/heros/", response_model=list[HeroPublic])
def read_heros(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
):
    heros = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heros

@app.get("/heros/{hero_id}", response_model=HeroPublic)
def read_hero(
    hero_id: int, 
    session: SessionDep
):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Not found")
    return hero

@app.put("/heros/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Not found")
    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db
    

@app.delete("/heros/{hero_id}")
def delete_hero(
    hero_id: int,
    session: SessionDep
):
    hero = session.get(hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}