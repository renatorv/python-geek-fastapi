from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
# esse import gerava alguns Warnings, então foi implementado o Bypass abaixo
from sqlmodel import select

from models.curso_model import CursoModel
from core.deps import get_session


# Bypass: warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar
 
SelectOfScalar.inherit_cache = True # type: ignore
Select.inherit_cache = True # type: ignore
# Fim Bypass

router = APIRouter()

# POST CURSO
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CursoModel)
async def post_curso(curso: CursoModel, db: AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(titulo=curso.titulo, aulas=curso.aulas, horas=curso.horas)

    db.add(novo_curso)
    await db.commit()

    return novo_curso

# GET CURSOS
@router.get('/', response_model=List(CursoModel))
async def get_custos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        cursos: List[CursoModel] = result.scalars().all()
        
        return cursos
        