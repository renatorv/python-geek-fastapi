from typing import Optional

from pydantic import BaseModel, validator

class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int # mais de 12 aulas
    horas: int # mais de 10 horas
    
    @validator('titulo')
    def validar_titulo(cls, value: str):
        palavras = value.split(' ')
        
        # Validação 1
        if len(palavras) < 3:
            raise ValueError('O título deve ter pelo menos 3 palavras.')
        # Validação 2
        if value.islower():
            raise ValueError('O título deve ser capitalizado.')
        
        # Sempre deve ser retornado 'value', após a validação
        return value

cursos = [
    Curso(id=1, titulo='Programação para leigos', aulas=112, horas=58),
    Curso(id=2, titulo='Algoritmos e lógica de programação', aulas=97, horas=67),
]