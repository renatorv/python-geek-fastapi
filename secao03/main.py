from typing import Optional
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi import Response
from fastapi import Path
from fastapi import Query

from models import Curso

app = FastAPI()

cursos = {
    1: {
        "titulo": "Programação para leigos",
        "aulas": 112,
        "horas": 58
    },
    2: {
        "titulo": "Algoritmos e lógica de programação",
        "aulas": 87,
        "horas": 67
    },
}


@app.get('/cursos')
async def get_cursos():
    return cursos


@app.get('/cursos/{curso_id}')
async def get_curso(curso_id: int = Path(default=None, title='ID do curso', description='Deve ser entre 1 e 2', gt=0, lt=3)):
    try:
        curso = cursos[curso_id]
        return curso
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado!')


@app.post('/cursos', status_code=status.HTTP_201_CREATED)
async def post_cursos(curso: Curso):
    next_id: int = len(cursos) + 1
    cursos[next_id] = curso
    del curso.id
    return curso


@app.put('/cursos/{curso_id}')
async def put_cursos(curso_id: int, curso: Curso):
    # Verificar se o curso existe na lista de cursos
    if curso_id in cursos:
        cursos[curso_id] = curso
        del curso.id

        return curso
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Não existe um curso com o id: {curso_id}')


@app.delete('/cursos/{id}')
async def delete_curso(id: int):
    if id in cursos:
        del cursos[id]

        # return JSONResponse(status_code=status.HTTP_204_NO_CONTENT) => JSONResponse possui um bug no memento do curso
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Não existe um curso com o id: {id}')


@app.get('/calculadora')
async def calcular(a: int = Query(default=None, gt=5), b: int = Query(default=None, gt=10), c: Optional[int] = None):
    soma: int = a + b
    if c:
        soma = soma + c

    return {'resultado': soma}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, debug=True, reload=True)
