"""
SpaceOps 2026 - Estruturas de Dados
Implementação de BST e Grafo do zero (sem bibliotecas externas para a árvore)
"""

from typing import List, Tuple, Dict, Optional
import json

# ============================================================================
# CLASSE NODE E BINARYSEARCHTREE
# ============================================================================

class Node:
    """Nó da Árvore Binária de Busca"""
    def _init_(self, municipio_id: int, nome: str, indice_risco: float, 
                custo_atendimento: float, populacao: int):
        self.municipio_id = municipio_id
        self.nome = nome
        self.indice_risco = indice_risco
        self.custo_atendimento = custo_atendimento
        self.populacao = populacao
        self.esquerda = None
        self.direita = None

    def _repr_(self):
        return f"Node({self.nome}, risco={self.indice_risco:.3f})"


class BinarySearchTree:
    """Árvore Binária de Busca ordenada por índice de risco
    
    Propriedade BST: risco_esquerda < risco_pai < risco_direita
    Uso: classificar municípios por criticidade para priorização
    """
    def _init_(self):
        self.raiz = None
        self.tamanho = 0

    def inserir(self, municipio_id: int, nome: str, indice_risco: float,
                custo_atendimento: float, populacao: int) -> None:
        """Insere município mantendo propriedade BST"""
        if self.raiz is None:
            self.raiz = Node(municipio_id, nome, indice_risco, custo_atendimento, populacao)
            self.tamanho = 1
        else:
            self._inserir_recursivo(self.raiz, municipio_id, nome, indice_risco,
                                   custo_atendimento, populacao)
            self.tamanho += 1

    def _inserir_recursivo(self, no: Node, municipio_id: int, nome: str,
                          indice_risco: float, custo_atendimento: float, populacao: int):
        if indice_risco < no.indice_risco:
            if no.esquerda is None:
                no.esquerda = Node(municipio_id, nome, indice_risco, custo_atendimento, populacao)
            else:
                self._inserir_recursivo(no.esquerda, municipio_id, nome, indice_risco,
                                       custo_atendimento, populacao)
        elif indice_risco > no.indice_risco:
            if no.direita is None:
                no.direita = Node(municipio_id, nome, indice_risco, custo_atendimento, populacao)
            else:
                self._inserir_recursivo(no.direita, municipio_id, nome, indice_risco,
                                       custo_atendimento, populacao)

    def buscar_intervalo(self, r_min: float, r_max: float) -> List[Node]:
        """Retorna nós com risco em [r_min, r_max]. O(h) em tempo onde h = altura"""
        resultado = []
        self._buscar_intervalo_recursivo(self.raiz, r_min, r_max, resultado)
        return resultado

    def _buscar_intervalo_recursivo(self, no: Optional[Node], r_min: float,
                                    r_max: float, resultado: List[Node]):
        if no is None:
            return
        
        # Se risco do nó >= r_min, explore subárvore esquerda (riscos menores)
        if no.indice_risco >= r_min:
            self._buscar_intervalo_recursivo(no.esquerda, r_min, r_max, resultado)
        
        # Se risco está no intervalo, inclua
        if r_min <= no.indice_risco <= r_max:
            resultado.append(no)
        
        # Se risco do nó <= r_max, explore subárvore direita (riscos maiores)
        if no.indice_risco <= r_max:
            self._buscar_intervalo_recursivo(no.direita, r_min, r_max, resultado)

    def percurso_in_order(self) -> List[Node]:
        """Retorna municípios em ordem crescente de risco. O(n)"""
        resultado = []
        self._in_order_recursivo(self.raiz, resultado)
        return resultado

    def _in_order_recursivo(self, no: Optional[Node], resultado: List[Node]):
        if no is None:
            return
        self._in_order_recursivo(no.esquerda, resultado)
        resultado.append(no)
        self._in_order_recursivo(no.direita, resultado)

    def altura(self) -> int:
        """Retorna altura da árvore. O(n)"""
        return self._calcular_altura(self.raiz)

    def _calcular_altura(self, no: Optional[Node]) -> int:
        if no is None:
            return 0
        return 1 + max(self._calcular_altura(no.esquerda),
                       self._calcular_altura(no.direita))

    def get_tamanho(self) -> int:
        """Retorna número de nós. O(1)"""
        return self.tamanho


# ============================================================================
# CLASSE GRAFO
# ============================================================================

class Grafo:
    """Grafo ponderado não-direcionado representado como dicionário de listas de adjacência
    
    Representação: {id_municipio: [(vizinho_id, peso), ...]}
    Complexidade: O(V+E) para traversal, O(1) para busca de vizinhos
    Justificativa: grafo esparso (E << V²), melhor que matriz de adjacência
    """
    def _init_(self):
        # Adjacência: {id_municipio: [(vizinho_id, peso), ...]}
        self.adjacencia: Dict[int, List[Tuple[int, float]]] = {}
        
        # Metadados: {id_municipio: (nome, indice_risco, custo_atendimento, populacao)}
        self.vertices: Dict[int, Tuple[str, float, float, int]] = {}

    def adicionar_vertice(self, municipio_id: int, nome: str, indice_risco: float,
                         custo_atendimento: float, populacao: int) -> None:
        """Adiciona vértice ao grafo. O(1)"""
        if municipio_id not in self.adjacencia:
            self.adjacencia[municipio_id] = []
            self.vertices[municipio_id] = (nome, indice_risco, custo_atendimento, populacao)

    def adicionar_aresta(self, u: int, v: int, peso: float) -> None:
        """Adiciona aresta bidirecional (grafo não-direcionado). O(1)"""
        if u in self.adjacencia and v in self.adjacencia:
            self.adjacencia[u].append((v, peso))
            self.adjacencia[v].append((u, peso))

    def obter_vizinhos(self, municipio_id: int) -> List[Tuple[int, float]]:
        """Retorna lista de (vizinho_id, peso) para um vértice. O(1)"""
        return self.adjacencia.get(municipio_id, [])

    def get_vertices(self) -> List[int]:
        """Retorna lista de IDs de vértices. O(V)"""
        return list(self.adjacencia.keys())

    def get_num_vertices(self) -> int:
        """Retorna número de vértices. O(1)"""
        return len(self.adjacencia)

    def get_num_arestas(self) -> int:
        """Retorna número de arestas. O(V+E)"""
        total = sum(len(vizinhos) for vizinhos in self.adjacencia.values())
        return total // 2  # Grafo não-direcionado, cada aresta contada 2x

    def get_info_vertice(self, municipio_id: int) -> Optional[Tuple[str, float, float, int]]:
        """Retorna (nome, risco, custo, populacao) do município. O(1)"""
        return self.vertices.get(municipio_id)

    def salvar_json(self, caminho: str) -> None:
        """Serializa grafo para JSON"""
        dados = {
            "vertices": self.vertices,
            "adjacencia": {str(k): v for k, v in self.adjacencia.items()}
        }
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)

    @classmethod
    def carregar_json(cls, caminho: str) -> 'Grafo':
        """Carrega grafo de JSON"""
        with open(caminho, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        g = cls()
        for mid, (nome, risco, custo, pop) in dados["vertices"].items():
            g.adicionar_vertice(int(mid), nome, risco, custo, pop)
        
        processadas = set()
        for mid_str, vizinhos in dados["adjacencia"].items():
            mid = int(mid_str)
            for vizinho_id, peso in vizinhos:
                aresta = tuple(sorted([mid, vizinho_id]))
                if aresta not in processadas:
                    g.adjacencia[mid].append((vizinho_id, peso))
                    processadas.add(aresta)
        
        return g

    def _repr_(self):
        return f"Grafo(V={self.get_num_vertices()}, E={self.get_num_arestas()})"