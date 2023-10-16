from fastapi import FastAPI

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

@app.get('/curso')
async def get_cursos():
    return cursos

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, debug=True)
