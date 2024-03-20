import itertools
from math import perm

def sumGreaterOrEqual(bidict, variables, k):
    """
    Genera cláusulas CNF (forma normal conjuntiva) que representan la restricción 
    de que la suma de un subconjunto de variables booleanas es mayor o igual a 'k'.
    Utiliza 'itertools' para encontrar todos los subconjuntos relevantes de 'variables'.

    Args:
    bidict: Un objeto bidict que mapea las variables a sus respectivos identificadores.
    variables: Una lista de variables a considerar para la restricción.
    k: El valor mínimo de la suma del subconjunto de variables.

    Returns:
    Una tupla que contiene la cadena de restricciones CNF y el número de cláusulas generadas.
    """

    subsets = itertools.combinations(variables, len(variables)-k+1)
    clauses = perm(len(variables), len(variables)-k+1)
    constrainsts = ''
    for subet in subsets:
        for var in subet:
            constrainsts += f'{bidict[var]} '

        constrainsts += '0\n'
    return constrainsts, clauses


def sumLessOrEqual(bidict, variables, k):
    """
    Genera cláusulas CNF que representan la restricción de que la suma de un subconjunto 
    de variables booleanas es menor o igual a 'k'.
    Utiliza 'itertools' para encontrar todos los subconjuntos relevantes de 'variables'.

    Args:
    bidict: Un objeto bidict que mapea las variables a sus respectivos identificadores.
    variables: Una lista de variables a considerar para la restricción.
    k: El valor máximo de la suma del subconjunto de variables.

    Returns:
    Una tupla que contiene la cadena de restricciones CNF y el número de cláusulas generadas.
    """
    
    subsets = itertools.combinations(variables, k+1)
    clauses = perm(len(variables), k+1)
    constrainsts = ''
    for subet in subsets:
        for var in subet:
            constrainsts += f'-{bidict[var]} '

        constrainsts += '0\n'

    return constrainsts, clauses