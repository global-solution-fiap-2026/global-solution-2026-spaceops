"""
SpaceOps 2026 - Dijkstra
Algoritmo Guloso para caminho mínimo de fonte única
Implementação com heap para eficiência O((V+E)log V)
"""

import heapq
from typing import Dict, List, Tuple, Optional
from data_structures import Grafo, BinarySearchTree, Node

class DijkstraSolver:
    """Algoritmo de Dijkstra para encontrar caminhos mínimos
    
    Greedy Strategy: sempre expandir a aresta de menor custo acumulado
    Complexidade: O((V+E) log V) com heap
    Propriedade: ótimo para grafos com pesos não-negativos
    
    Integração SpaceOps: 
    - Encontra rota de menor custo de atendimento a partir de um hub
    - Usa BST para priorizar municípios de alto risco
    """
    
    def __init__(self, grafo: Grafo, bst: Optional[BinarySearchTree] = None):
        self.grafo = grafo
        self.bst = bst
        self.num_relaxacoes = 0
        self.heap_insercoes = 0

    def encontrar_caminhos_minimos(self, origem: int) -> Dict[int, Tuple[float, List[int]]]:
        """Dijkstra clássico: encontra caminhos mínimos para todos os vértices
        
        Args:
            origem: ID do município hub de recursos
        
        Returns:
            {destino: (custo_total, caminho)}
        """
        distancias: Dict[int, float] = {v: float('inf') for v in self.grafo.get_vertices()}
        antecessores: Dict[int, Optional[int]] = {v: None for v in self.grafo.get_vertices()}
        
        distancias[origem] = 0.0
        self.num_relaxacoes = 0
        self.heap_insercoes = 0
        
        # Fila de prioridade: (custo, vértice)
        heap: List[Tuple[float, int]] = [(0.0, origem)]
        
        visitados = set()
        
        while heap:
            custo_atual, u = heapq.heappop(heap)
            
            if u in visitados:
                continue
            
            visitados.add(u)
            
            # Se custo no heap é maior que o registrado, foi relaxado depois
            if custo_atual > distancias[u]:
                continue
            
            # Relaxar arestas saindo de u
            for vizinho, peso in self.grafo.obter_vizinhos(u):
                novo_custo = distancias[u] + peso
                
                if novo_custo < distancias[vizinho]:
                    distancias[vizinho] = novo_custo
                    antecessores[vizinho] = u
                    heapq.heappush(heap, (novo_custo, vizinho))
                    self.heap_insercoes += 1
                    self.num_relaxacoes += 1
        
        # Reconstruir caminhos
        resultado = {}
        for destino in self.grafo.get_vertices():
            caminho = self._reconstruir_caminho(antecessores, origem, destino)
            resultado[destino] = (distancias[destino], caminho)
        
        return resultado

    def encontrar_mst_dijkstra(self) -> Tuple[List[Tuple[int, int, float]], float]:
        """Variante adaptada de Dijkstra para MST (Prim's algorithm)
        
        Greedy strategy: adicionar a menor aresta que conecta um novo vértice
        à árvore já construída
        """
        vertices = self.grafo.get_vertices()
        
        if not vertices:
            return [], 0.0
        
        origem = vertices[0]
        visitados = set([origem])
        arestas_mst: List[Tuple[int, int, float]] = []
        custo_total = 0.0
        
        # Heap: (peso, u, v)
        heap: List[Tuple[float, int, int]] = []
        
        # Adicionar todas as arestas saindo da origem
        for vizinho, peso in self.grafo.obter_vizinhos(origem):
            heapq.heappush(heap, (peso, origem, vizinho))
            self.heap_insercoes += 1
        
        while heap and len(visitados) < self.grafo.get_num_vertices():
            peso, u, v = heapq.heappop(heap)
            
            if v in visitados:
                continue
            
            # v é novo vértice, adicionar aresta
            visitados.add(v)
            arestas_mst.append((u, v, peso))
            custo_total += peso
            self.num_relaxacoes += 1
            
            # Adicionar todas as arestas saindo de v
            for novo_vizinho, novo_peso in self.grafo.obter_vizinhos(v):
                if novo_vizinho not in visitados:
                    heapq.heappush(heap, (novo_peso, v, novo_vizinho))
                    self.heap_insercoes += 1
        
        return arestas_mst, custo_total

    def dijkstra_com_prioridade_risco(self, origem: int, 
                                      r_min: float = 0.7, r_max: float = 1.0) -> Dict[int, Tuple[float, List[int]]]:
        """Dijkstra que prioriza municípios de alto risco usando BST
        
        Estratégia: multiplicar pesos de arestas por 1/risco para priorizar
        municípios críticos
        """
        if not self.bst:
            return self.encontrar_caminhos_minimos(origem)
        
        # Buscar municípios críticos (alto risco)
        criticos = self.bst.buscar_intervalo(r_min, r_max)
        critico_ids = {n.municipio_id for n in criticos}
        
        distancias: Dict[int, float] = {v: float('inf') for v in self.grafo.get_vertices()}
        antecessores: Dict[int, Optional[int]] = {v: None for v in self.grafo.get_vertices()}
        
        distancias[origem] = 0.0
        
        heap: List[Tuple[float, int]] = [(0.0, origem)]
        visitados = set()
        
        while heap:
            custo_atual, u = heapq.heappop(heap)
            
            if u in visitados:
                continue
            
            visitados.add(u)
            
            if custo_atual > distancias[u]:
                continue
            
            for vizinho, peso in self.grafo.obter_vizinhos(u):
                # Se vizinho é crítico, reduzir peso (priorizar)
                peso_ajustado = peso * 0.5 if vizinho in critico_ids else peso
                novo_custo = distancias[u] + peso_ajustado
                
                if novo_custo < distancias[vizinho]:
                    distancias[vizinho] = novo_custo
                    antecessores[vizinho] = u
                    heapq.heappush(heap, (novo_custo, vizinho))
                    self.num_relaxacoes += 1
        
        resultado = {}
        for destino in self.grafo.get_vertices():
            caminho = self._reconstruir_caminho(antecessores, origem, destino)
            resultado[destino] = (distancias[destino], caminho)
        
        return resultado

    def _reconstruir_caminho(self, antecessores: Dict[int, Optional[int]], 
                            origem: int, destino: int) -> List[int]:
        """Reconstrói caminho a partir de antecessores"""
        caminho = []
        atual = destino
        
        while atual is not None:
            caminho.append(atual)
            atual = antecessores[atual]
        
        caminho.reverse()
        
        # Se não há caminho, retornar vazio
        if caminho[0] != origem:
            return []
        
        return caminho

    def get_stats(self) -> Dict[str, int]:
        """Retorna estatísticas de execução"""
        return {
            "relaxacoes": self.num_relaxacoes,
            "heap_insercoes": self.heap_insercoes
        }