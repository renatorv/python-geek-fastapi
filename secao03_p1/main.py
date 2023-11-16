
from typing import List, Optional, Any, Dict
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi import Response
from fastapi import Path
from fastapi import Query
from fastapi import Header
from fastapi import Depends

from time import sleep

from models import Curso
from models import cursos

def fake_db():
    try:
        print('Abrindo conexão com BD...')
        sleep(1)
    finally:
        print('Fechando a conexão com BD...')
        sleep(1)

app = FastAPI(
                title='API de cursos da Geek University',
                version='0.0.2',
                description='Uma API de estudos de FastAPI',
              )


@app.get('/cursos', 
         description='Retorna todos os cursos ou uma lista vazia', 
         summary='Retorna todos os cursos.',
         response_model=List[Curso],
         response_description='Corsos encontrados com sucesso!'
         )
async def get_cursos(db: Any = Depends(fake_db)):
    return cursos


@app.get('/cursos/{curso_id}')
async def get_curso(curso_id: int = Path(default=None, title='ID do curso', description='Deve ser entre 1 e 2', gt=0, lt=3), db: Any = Depends(fake_db)):
    try:
        curso = cursos[curso_id]
        return curso
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado!')


@app.post('/cursos', status_code=status.HTTP_201_CREATED, response_model=Curso)
async def post_cursos(curso: Curso, db: Any = Depends(fake_db)):
    next_id: int = len(cursos) + 1
    curso.id = next_id
    cursos.append(curso)
    return curso


@app.put('/cursos/{curso_id}')
async def put_cursos(curso_id: int, curso: Curso, db: Any = Depends(fake_db)):
    # Verificar se o curso existe na lista de cursos
    if curso_id in cursos:
        cursos[curso_id] = curso
        del curso.id

        return curso
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Não existe um curso com o id: {curso_id}')


@app.delete('/cursos/{id}')
async def delete_curso(id: int, db: Any = Depends(fake_db)):
    if id in cursos:
        del cursos[id]

        # return JSONResponse(status_code=status.HTTP_204_NO_CONTENT) => JSONResponse possui um bug no memento do curso
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Não existe um curso com o id: {id}')


@app.get('/calculadora')
async def calcular(a: int = Query(default=None, gt=5), b: int = Query(default=None, gt=10), c: Optional[int] = None,
                   x_geek: str = Header(default=None)):
    
    soma: int = a + b
    if c:
        soma = soma + c
    
    print(f'X-GEEK: {x_geek}')

    return {'resultado': soma}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, debug=True, reload=True)
