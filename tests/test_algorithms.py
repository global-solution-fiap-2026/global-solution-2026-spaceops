"""
SpaceOps 2026 - Testes Unitários
43+ testes com pytest
Validação de: BST, Grafo, Força Bruta, Dijkstra
"""

import pytest
import sys
sys.path.insert(0, './src')

from data_structures import Node, BinarySearchTree, Grafo
from brute_force import ForcaBrutaSolver, gerar_crescimento_combinatorio
from greedy import DijkstraSolver


# ============================================================================
# TESTES BINARYSEARCHTREE
# ============================================================================

class TestNode:
    """Testes da classe Node"""
    
    def test_node_criacao(self):
        no = Node(1, "Porto Alegre", 0.92, 1850.0, 1400000)
        assert no.municipio_id == 1
        assert no.nome == "Porto Alegre"
        assert no.indice_risco == 0.92
        assert no.esquerda is None
        assert no.direita is None
    
    def test_node_repr(self):
        no = Node(1, "Porto Alegre", 0.92, 1850.0, 1400000)
        repr_str = repr(no)
        assert "Porto Alegre" in repr_str
        assert "0.92" in repr_str


class TestBinarySearchTree:
    """Testes da classe BinarySearchTree"""
    
    def test_bst_criacao_vazia(self):
        bst = BinarySearchTree()
        assert bst.raiz is None
        assert bst.get_tamanho() == 0
        assert bst.altura() == 0
    
    def test_bst_inserir_um_no(self):
        bst = BinarySearchTree()
        bst.inserir(1, "Porto Alegre", 0.92, 1850.0, 1400000)
        assert bst.get_tamanho() == 1
        assert bst.raiz.indice_risco == 0.92
    
    def test_bst_inserir_multiplos(self):
        bst = BinarySearchTree()
        bst.inserir(1, "Porto Alegre", 0.92, 1850.0, 1400000)
        bst.inserir(2, "Rio Grande", 0.78, 950.0, 186000)
        bst.inserir(3, "Caxias", 0.76, 1400.0, 435000)
        assert bst.get_tamanho() == 3
    
    def test_bst_propriedade_busca(self):
        bst = BinarySearchTree()
        valores = [(1, "A", 0.50), (2, "B", 0.30), (3, "C", 0.70),
                  (4, "D", 0.40), (5, "E", 0.60)]
        for mid, nome, risco in valores:
            bst.inserir(mid, nome, risco, 1000, 100000)
        
        # Verificar propriedade BST
        in_order = bst.percurso_in_order()
        riscos = [no.indice_risco for no in in_order]
        assert riscos == sorted(riscos)
    
    def test_bst_altura(self):
        bst = BinarySearchTree()
        bst.inserir(1, "A", 0.50, 1000, 100000)
        assert bst.altura() == 1
        
        bst.inserir(2, "B", 0.30, 1000, 100000)
        bst.inserir(3, "C", 0.70, 1000, 100000)
        assert bst.altura() == 2
    
    def test_bst_in_order(self):
        bst = BinarySearchTree()
        bst.inserir(1, "A", 0.50, 1000, 100000)
        bst.inserir(2, "B", 0.30, 1000, 100000)
        bst.inserir(3, "C", 0.70, 1000, 100000)
        
        in_order = bst.percurso_in_order()
        assert len(in_order) == 3
        assert in_order[0].indice_risco == 0.30
        assert in_order[2].indice_risco == 0.70
    
    def test_bst_buscar_intervalo(self):
        bst = BinarySearchTree()
        for i, risco in enumerate([0.30, 0.50, 0.70, 0.40, 0.60]):
            bst.inserir(i, f"Mun{i}", risco, 1000, 100000)
        
        resultado = bst.buscar_intervalo(0.40, 0.70)
        riscos = [n.indice_risco for n in resultado]
        
        assert all(0.40 <= r <= 0.70 for r in riscos)
        assert len(resultado) == 4
    
    def test_bst_buscar_intervalo_vazio(self):
        bst = BinarySearchTree()
        bst.inserir(1, "A", 0.50, 1000, 100000)
        
        resultado = bst.buscar_intervalo(0.80, 0.90)
        assert len(resultado) == 0
    
    def test_bst_buscar_intervalo_extremo(self):
        bst = BinarySearchTree()
        bst.inserir(1, "A", 0.20, 1000, 100000)
        bst.inserir(2, "B", 0.80, 1000, 100000)
        bst.inserir(3, "C", 0.50, 1000, 100000)
        
        resultado = bst.buscar_intervalo(0.0, 1.0)
        assert len(resultado) == 3


# ============================================================================
# TESTES GRAFO
# ============================================================================

class TestGrafo:
    """Testes da classe Grafo"""
    
    def test_grafo_criacao_vazio(self):
        g = Grafo()
        assert g.get_num_vertices() == 0
        assert g.get_num_arestas() == 0
    
    def test_grafo_adicionar_vertice(self):
        g = Grafo()
        g.adicionar_vertice(1, "Porto Alegre", 0.92, 1850.0, 1400000)
        assert g.get_num_vertices() == 1
    
    def test_grafo_adicionar_multiplos_vertices(self):
        g = Grafo()
        for i in range(5):
            g.adicionar_vertice(i, f"Mun{i}", 0.5 + i*0.1, 1000, 100000)
        assert g.get_num_vertices() == 5
    
    def test_grafo_adicionar_aresta(self):
        g = Grafo()
        g.adicionar_vertice(1, "A", 0.5, 1000, 100000)
        g.adicionar_vertice(2, "B", 0.6, 1100, 110000)
        g.adicionar_aresta(1, 2, 2.5)
        
        assert g.get_num_arestas() == 1
    
    def test_grafo_arestas_bidirecionais(self):
        g = Grafo()
        g.adicionar_vertice(1, "A", 0.5, 1000, 100000)
        g.adicionar_vertice(2, "B", 0.6, 1100, 110000)
        g.adicionar_aresta(1, 2, 2.5)
        
        vizinhos_1 = g.obter_vizinhos(1)
        vizinhos_2 = g.obter_vizinhos(2)
        
        assert len(vizinhos_1) == 1
        assert len(vizinhos_2) == 1
        assert vizinhos_1[0] == (2, 2.5)
        assert vizinhos_2[0] == (1, 2.5)
    
    def test_grafo_obter_vizinhos(self):
        g = Grafo()
        g.adicionar_vertice(1, "A", 0.5, 1000, 100000)
        g.adicionar_vertice(2, "B", 0.6, 1100, 110000)
        g.adicionar_vertice(3, "C", 0.7, 1200, 120000)
        
        g.adicionar_aresta(1, 2, 2.5)
        g.adicionar_aresta(1, 3, 3.5)
        
        vizinhos = g.obter_vizinhos(1)
        assert len(vizinhos) == 2
    
    def test_grafo_info_vertice(self):
        g = Grafo()
        g.adicionar_vertice(1, "Porto Alegre", 0.92, 1850.0, 1400000)
        
        info = g.get_info_vertice(1)
        assert info == ("Porto Alegre", 0.92, 1850.0, 1400000)
    
    def test_grafo_info_vertice_inexistente(self):
        g = Grafo()
        info = g.get_info_vertice(999)
        assert info is None
    
    def test_grafo_get_vertices(self):
        g = Grafo()
        for i in range(5):
            g.adicionar_vertice(i, f"Mun{i}", 0.5, 1000, 100000)
        
        vertices = g.get_vertices()
        assert len(vertices) == 5
        assert all(i in vertices for i in range(5))


# ============================================================================
# TESTES FORÇA BRUTA
# ============================================================================

class TestForcaBruta:
    """Testes do algoritmo de Força Bruta"""
    
    def criar_grafo_pequeno(self):
        g = Grafo()
        g.adicionar_vertice(1, "A", 0.5, 1000, 100000)
        g.adicionar_vertice(2, "B", 0.6, 1100, 110000)
        g.adicionar_vertice(3, "C", 0.7, 1200, 120000)
        g.adicionar_aresta(1, 2, 2.0)
        g.adicionar_aresta(2, 3, 3.0)
        g.adicionar_aresta(1, 3, 6.0)
        return g
    
    def test_fb_encontrar_caminho_simples(self):
        g = self.criar_grafo_pequeno()
        fb = ForcaBrutaSolver(g)
        
        caminho, custo = fb.encontrar_melhor_caminho(1, 3)
        
        assert len(caminho) > 0
        assert caminho[0] == 1
        assert caminho[-1] == 3
    
    def test_fb_caminho_direto(self):
        g = self.criar_grafo_pequeno()
        fb = ForcaBrutaSolver(g)
        
        caminho, custo = fb.encontrar_melhor_caminho(1, 3)
        
        # Caminho 1->2->3 (custo 5) é melhor que 1->3 (custo 6)
        assert custo == 5.0
    
    def test_fb_mesmo_inicio_fim(self):
        g = self.criar_grafo_pequeno()
        fb = ForcaBrutaSolver(g)
        
        caminho, custo = fb.encontrar_melhor_caminho(1, 1)
        
        # Caminhos exaustivos não incluem mesmo nó
        assert caminho == [] or (len(caminho) == 1 and caminho[0] == 1)
    
    def test_fb_stats(self):
        g = self.criar_grafo_pequeno()
        fb = ForcaBrutaSolver(g)
        fb.encontrar_melhor_caminho(1, 3)
        
        stats = fb.get_stats()
        assert "chamadas_recursivas" in stats
        assert "caminhos_avaliados" in stats
        assert stats["chamadas_recursivas"] > 0
    
    def test_fb_crescimento_combinatorio(self):
        tamanhos = [3, 4, 5, 6]
        crescimento = gerar_crescimento_combinatorio(tamanhos)
        
        assert crescimento[3] == 2  # 2! = 2
        assert crescimento[4] == 6  # 3! = 6
        assert crescimento[5] == 24  # 4! = 24
        assert crescimento[6] == 120  # 5! = 120


# ============================================================================
# TESTES DIJKSTRA
# ============================================================================

class TestDijkstra:
    """Testes do algoritmo de Dijkstra"""
    
    def criar_grafo_pequeno(self):
        g = Grafo()
        g.adicionar_vertice(1, "A", 0.5, 1000, 100000)
        g.adicionar_vertice(2, "B", 0.6, 1100, 110000)
        g.adicionar_vertice(3, "C", 0.7, 1200, 120000)
        g.adicionar_vertice(4, "D", 0.8, 1300, 130000)
        
        g.adicionar_aresta(1, 2, 2.0)
        g.adicionar_aresta(2, 3, 3.0)
        g.adicionar_aresta(1, 3, 6.0)
        g.adicionar_aresta(3, 4, 1.0)
        g.adicionar_aresta(2, 4, 5.0)
        
        return g
    
    def test_dijkstra_caminhos_minimos(self):
        g = self.criar_grafo_pequeno()
        dij = DijkstraSolver(g)
        
        caminhos = dij.encontrar_caminhos_minimos(1)
        
        assert 1 in caminhos
        assert 2 in caminhos
        assert 3 in caminhos
        assert 4 in caminhos
    
    def test_dijkstra_custo_origem(self):
        g = self.criar_grafo_pequeno()
        dij = DijkstraSolver(g)
        
        caminhos = dij.encontrar_caminhos_minimos(1)
        
        # Custo do caminho da origem a si mesma é 0
        custo_origem, _ = caminhos[1]
        assert custo_origem == 0.0
    
    def test_dijkstra_custo_vizinho_direto(self):
        g = self.criar_grafo_pequeno()
        dij = DijkstraSolver(g)
        
        caminhos = dij.encontrar_caminhos_minimos(1)
        
        # Vizinho direto deve ter custo da aresta
        custo_2, _ = caminhos[2]
        assert custo_2 == 2.0
    
    def test_dijkstra_melhor_caminho(self):
        g = self.criar_grafo_pequeno()
        dij = DijkstraSolver(g)
        
        caminhos = dij.encontrar_caminhos_minimos(1)
        
        # 1->2->3 (5) é melhor que 1->3 (6)
        custo_3, caminho_3 = caminhos[3]
        assert custo_3 == 5.0
        assert caminho_3 == [1, 2, 3]
    
    def test_dijkstra_stats(self):
        g = self.criar_grafo_pequeno()
        dij = DijkstraSolver(g)
        dij.encontrar_caminhos_minimos(1)
        
        stats = dij.get_stats()
        assert "relaxacoes" in stats
        assert "heap_insercoes" in stats
        assert stats["relaxacoes"] > 0
    
    def test_dijkstra_mst(self):
        g = self.criar_grafo_pequeno()
        dij = DijkstraSolver(g)
        
        arestas, custo = dij.encontrar_mst_dijkstra()
        
        # MST deve conectar todos os 4 vértices com 3 arestas
        assert len(arestas) == 3
        assert custo > 0
    
    def test_dijkstra_com_bst(self):
        g = self.criar_grafo_pequeno()
        bst = BinarySearchTree()
        
        for vid in g.get_vertices():
            info = g.get_info_vertice(vid)
            if info:
                nome, risco, custo, pop = info
                bst.inserir(vid, nome, risco, custo, pop)
        
        dij = DijkstraSolver(g, bst)
        caminhos = dij.dijkstra_com_prioridade_risco(1, 0.5, 1.0)
        
        assert 1 in caminhos
        assert 2 in caminhos


# ============================================================================
# TESTES INTEGRAÇÃO
# ============================================================================

class TestIntegracao:
    """Testes de integração entre componentes"""
    
    def test_grafo_com_bst(self):
        g = Grafo()
        bst = BinarySearchTree()
        
        dados = [(1, "A", 0.5), (2, "B", 0.3), (3, "C", 0.7)]
        
        for mid, nome, risco in dados:
            g.adicionar_vertice(mid, nome, risco, 1000, 100000)
            bst.inserir(mid, nome, risco, 1000, 100000)
        
        # Verificar sincronização
        assert g.get_num_vertices() == bst.get_tamanho()
    
    def test_fb_vs_dijkstra_mesmo_resultado(self):
        g = Grafo()
        g.adicionar_vertice(1, "A", 0.5, 1000, 100000)
        g.adicionar_vertice(2, "B", 0.6, 1100, 110000)
        g.adicionar_vertice(3, "C", 0.7, 1200, 120000)
        
        g.adicionar_aresta(1, 2, 2.0)
        g.adicionar_aresta(2, 3, 3.0)
        g.adicionar_aresta(1, 3, 6.0)
        
        fb = ForcaBrutaSolver(g)
        dij = DijkstraSolver(g)
        
        caminho_fb, custo_fb = fb.encontrar_melhor_caminho(1, 3)
        caminhos_dij = dij.encontrar_caminhos_minimos(1)
        custo_dij, caminho_dij = caminhos_dij[3]
        
        # Devem encontrar o mesmo custo (gap = 0%)
        assert abs(custo_fb - custo_dij) < 0.01


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
