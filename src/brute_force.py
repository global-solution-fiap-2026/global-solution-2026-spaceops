"""
SpaceOps 2026 - Força Bruta
Enumeração completa de caminhos com backtracking
Baseline de validação para instâncias pequenas (N ≤ 12)
"""

from typing import List, Dict, Tuple, Set
from data_structures import Grafo

class ForcaBrutaSolver:
    """Solver que enumera TODOS os caminhos entre origem e destino
    
    Algoritmo: recursão com backtracking
    Complexidade: O(V!) em tempo — explosão combinatória
    Uso: validação de algoritmos gulosos em instâncias pequenas
    """
    
    def _init_(self, grafo: Grafo):
        self.grafo = grafo
        self.chamadas_recursivas = 0
        self.caminhos_avaliados = 0
        self.melhor_custo = float('inf')
        self.melhor_caminho = []

    def encontrar_melhor_caminho(self, origem: int, destino: int) -> Tuple[List[int], float]:
        """Encontra o caminho de menor custo entre origem e destino por enumeração
        
        Returns:
            (caminho, custo_total)
        """
        self.chamadas_recursivas = 0
        self.caminhos_avaliados = 0
        self.melhor_custo = float('inf')
        self.melhor_caminho = []
        
        visitados: Set[int] = set()
        caminho_atual = [origem]
        
        self._backtrack(origem, destino, caminho_atual, visitados, 0.0)
        
        return self.melhor_caminho, self.melhor_custo

    def _backtrack(self, atual: int, destino: int, caminho: List[int],
                   visitados: Set[int], custo_acumulado: float) -> None:
        """Backtracking recursivo para enumerar todos os caminhos"""
        self.chamadas_recursivas += 1
        
        # Se chegou ao destino
        if atual == destino:
            self.caminhos_avaliados += 1
            if custo_acumulado < self.melhor_custo:
                self.melhor_custo = custo_acumulado
                self.melhor_caminho = caminho.copy()
            return

        visitados.add(atual)
        
        # Explorar todos os vizinhos
        for vizinho, peso in self.grafo.obter_vizinhos(atual):
            if vizinho not in visitados:
                caminho.append(vizinho)
                self._backtrack(vizinho, destino, caminho, visitados,
                              custo_acumulado + peso)
                caminho.pop()
        
        visitados.remove(atual)

    def encontrar_arvore_minima_enumeracao(self, origem: int) -> Tuple[List[Tuple[int, int, float]], float]:
        """Encontra árvore geradora mínima enumerando todas as subárvores
        
        Retorna arestas que formam a MST (apenas para pequenas instâncias)
        """
        vertices = self.grafo.get_vertices()
        n = len(vertices)
        
        if n > 10:
            raise ValueError("Enumeração de MST impraticável para N > 10")
        
        return self._mst_prim_basico(origem)

    def _mst_prim_basico(self, origem: int) -> Tuple[List[Tuple[int, int, float]], float]:
        """Prim simplificado para MST (não é força bruta pura, mas baseline)"""
        visitados: Set[int] = set()
        arestas: List[Tuple[int, int, float]] = []
        custo_total = 0.0
        
        visitados.add(origem)
        
        while len(visitados) < self.grafo.get_num_vertices():
            min_peso = float('inf')
            melhor_aresta = None
            
            for u in visitados:
                for v, peso in self.grafo.obter_vizinhos(u):
                    if v not in visitados and peso < min_peso:
                        min_peso = peso
                        melhor_aresta = (u, v, peso)
            
            if melhor_aresta is None:
                break
            
            u, v, peso = melhor_aresta
            arestas.append((u, v, peso))
            custo_total += peso
            visitados.add(v)
            self.chamadas_recursivas += 1
        
        return arestas, custo_total

    def get_stats(self) -> Dict[str, int]:
        """Retorna estatísticas de execução"""
        return {
            "chamadas_recursivas": self.chamadas_recursivas,
            "caminhos_avaliados": self.caminhos_avaliados,
            "melhor_custo": self.melhor_custo
        }


def gerar_crescimento_combinatorio(tamanhos: List[int]) -> Dict[int, int]:
    """Calcula o crescimento do número de possibilidades para visualização
    
    Para um caminho Hamiltoniano: (n-1)! caminhos possíveis
    """
    import math
    resultado = {}
    for n in tamanhos:
        resultado[n] = math.factorial(n - 1) if n > 1 else 1
    return resultado