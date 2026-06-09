"""
SpaceOps 2026 - Visualizações
6 figuras obrigatórias:
1. Grafo de municípios (RS) com destaque
2. Grafo de municípios (MATOPIBA) com destaque
3. BST ordenada por risco
4. Comparativo de desempenho (tempo × N)
5. Tabela de estruturas de dados
6. Gap de otimalidade (FB vs Dijkstra)
"""

import matplotlib.pyplot as plt
import networkx as nx
from typing import List, Dict, Tuple
from data_structures import Grafo, BinarySearchTree, Node
import os

plt.rcParams['font.size'] = 9
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['figure.figsize'] = (14, 8)

def visualizar_grafo(grafo: Grafo, titulo: str, arquivo_saida: str,
                    arestas_destacadas: List[Tuple[int, int]] = None,
                    layout: str = 'spring') -> None:
    """Visualiza grafo com arestas destacadas (MST)
    
    Fig 1a: Grafo RS com MST destacada
    Fig 1b: Grafo MATOPIBA com MST destacada
    """
    G = nx.Graph()
    
    # Adicionar vértices com atributos
    for vertice_id in grafo.get_vertices():
        info = grafo.get_info_vertice(vertice_id)
        if info:
            nome, risco, custo, pop = info
            G.add_node(vertice_id, nome=nome, risco=risco)
    
    # Adicionar arestas
    arestas_normais = set()
    for u in grafo.get_vertices():
        for v, peso in grafo.obter_vizinhos(u):
            aresta = tuple(sorted([u, v]))
            arestas_normais.add(aresta)
    
    G.add_edges_from(arestas_normais)
    
    # Layout
    if layout == 'spring':
        pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    elif layout == 'circular':
        pos = nx.circular_layout(G)
    else:
        pos = nx.kamada_kawai_layout(G)
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Desenhar arestas normais
    nx.draw_networkx_edges(G, pos, edgelist=arestas_normais,
                          edge_color='lightgray', width=1, alpha=0.5, ax=ax)
    
    # Destacar MST se fornecido
    if arestas_destacadas:
        mst_edges = [(u, v) if u < v else (v, u) for u, v in arestas_destacadas]
        nx.draw_networkx_edges(G, pos, edgelist=mst_edges,
                              edge_color='red', width=2.5, alpha=0.8, ax=ax)
    
    # Cores dos nós por risco
    node_colors = []
    for node in G.nodes():
        info = grafo.get_info_vertice(node)
        if info:
            _, risco, _, _ = info
            node_colors.append(risco)
        else:
            node_colors.append(0.5)
    
    nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors,
                                   cmap='RdYlGn_r', node_size=500,
                                   vmin=0, vmax=1, ax=ax)
    
    # Labels
    labels = {node: grafo.get_info_vertice(node)[0][:6]
             for node in G.nodes() if grafo.get_info_vertice(node)}
    nx.draw_networkx_labels(G, pos, labels, font_size=8, ax=ax)
    
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
    ax.axis('off')
    
    # Colorbar
    cbar = plt.colorbar(nodes, ax=ax, label='Índice de Risco', shrink=0.8)
    
    plt.tight_layout()
    plt.savefig(arquivo_saida, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ {arquivo_saida}")


def visualizar_bst(bst: BinarySearchTree, titulo: str, arquivo_saida: str) -> None:
    """Visualiza BST ordenada por risco
    
    Fig 3: Diagrama da árvore com nós risco
    """
    fig, ax = plt.subplots(figsize=(14, 10))
    
    if bst.raiz is None:
        ax.text(0.5, 0.5, "Árvore vazia", ha='center', va='center', fontsize=14)
        plt.savefig(arquivo_saida, dpi=300, bbox_inches='tight')
        plt.close()
        return
    
    # Preparar dados para visualização
    nodes = []
    edges = []
    pos_dict = {}
    
    def preparar_no(no: Node, x: float, y: float, dx: float):
        if no is None:
            return
        
        nodes.append((no.municipio_id, no.nome, no.indice_risco))
        pos_dict[no.municipio_id] = (x, y)
        
        if no.esquerda:
            edges.append((no.municipio_id, no.esquerda.municipio_id))
            preparar_no(no.esquerda, x - dx, y - 1, dx / 2)
        
        if no.direita:
            edges.append((no.municipio_id, no.direita.municipio_id))
            preparar_no(no.direita, x + dx, y - 1, dx / 2)
    
    preparar_no(bst.raiz, 0, 0, 3)
    
    # Desenhar
    G = nx.DiGraph()
    G.add_nodes_from([n[0] for n in nodes])
    G.add_edges_from(edges)
    
    # Desenhar arestas
    nx.draw_networkx_edges(G, pos_dict, edgelist=edges,
                          edge_color='gray', arrows=True, width=1.5,
                          arrowsize=15, ax=ax)
    
    # Desenhar nós coloridos por risco
    node_colors = [n[2] for n in nodes]
    node_objects = nx.draw_networkx_nodes(G, pos_dict, node_color=node_colors,
                                         cmap='RdYlGn_r', node_size=800,
                                         vmin=0, vmax=1, ax=ax)
    
    # Labels com risco e nome
    labels = {n[0]: f"{n[1][:4]}\n({n[2]:.2f})" for n in nodes}
    nx.draw_networkx_labels(G, pos_dict, labels, font_size=7, ax=ax)
    
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
    ax.axis('off')
    
    cbar = plt.colorbar(node_objects, ax=ax, label='Índice de Risco', shrink=0.8)
    
    plt.tight_layout()
    plt.savefig(arquivo_saida, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ {arquivo_saida}")


def visualizar_desempenho(registros: List[Dict], arquivo_saida: str) -> None:
    """Gráfico comparativo de desempenho
    
    Fig 4: Tempo de execução × N para FB e Dijkstra
    """
    fig, ax = plt.subplots(figsize=(12, 7))
    
    fb_registros = [r for r in registros if r["algoritmo"] == "força_bruta"]
    dij_registros = [r for r in registros if r["algoritmo"] == "dijkstra"]
    
    fb_registros.sort(key=lambda r: r["tamanho_n"])
    dij_registros.sort(key=lambda r: r["tamanho_n"])
    
    if fb_registros:
        ns_fb = [r["tamanho_n"] for r in fb_registros]
        tempos_fb = [r["tempo_ms"] for r in fb_registros]
        ax.plot(ns_fb, tempos_fb, 'o-', color='red', linewidth=2.5,
               markersize=8, label='Força Bruta', alpha=0.8)
        ax.scatter(ns_fb, tempos_fb, color='red', s=100, zorder=5, alpha=0.8)
    
    if dij_registros:
        ns_dij = [r["tamanho_n"] for r in dij_registros]
        tempos_dij = [r["tempo_ms"] for r in dij_registros]
        ax.plot(ns_dij, tempos_dij, 's-', color='blue', linewidth=2.5,
               markersize=8, label='Dijkstra', alpha=0.8)
        ax.scatter(ns_dij, tempos_dij, color='blue', s=100, zorder=5, alpha=0.8)
    
    ax.set_xlabel('Número de Vértices (N)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Tempo de Execução (ms)', fontsize=12, fontweight='bold')
    ax.set_title('Análise Comparativa: Força Bruta × Dijkstra\nTempo de Execução × Tamanho da Instância',
                fontsize=13, fontweight='bold', pad=15)
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_yscale('log')
    
    # Anotações
    if fb_registros and len(fb_registros) > 1:
        ax.annotate('Força Bruta: O(V!)', xy=(fb_registros[-1]["tamanho_n"],
                    fb_registros[-1]["tempo_ms"]), xytext=(-30, -20),
                   textcoords='offset points', fontsize=10, color='red',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))
    
    if dij_registros:
        ax.annotate('Dijkstra: O((V+E)logV)', xy=(dij_registros[-1]["tamanho_n"],
                    dij_registros[-1]["tempo_ms"]), xytext=(20, 20),
                   textcoords='offset points', fontsize=10, color='blue',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig(arquivo_saida, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ {arquivo_saida}")


def visualizar_tabela_estruturas(arquivo_saida: str) -> None:
    """Tabela de estruturas de dados utilizadas
    
    Fig 5: Tabela com complexidades e justificativas
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis('tight')
    ax.axis('off')
    
    dados = [
        ["Estrutura", "Uso no Sistema", "Complexidade", "Aplicação SpaceOps"],
        ["List", "Adjacência, resultado de caminho", "O(1) insert, O(n) busca", "Lista de adjacência do grafo"],
        ["Tuple", "Par (nó, custo), aresta", "O(1) acesso", "Arestas (u, v, peso)"],
        ["Dict", "Mapeamento id → atributos", "O(1) insert/busca", "Adjacência com pesos"],
        ["Set", "Nós visitados", "O(1) insert/pertencimento", "Controle de visitados em FB"],
        ["Heap/heapq", "Fila de prioridade", "O(log n) insert/extract", "Fila em Dijkstra"],
        ["BST", "Classificação por risco", "O(h) busca, O(n) percurso", "Priorização de municípios críticos"],
        ["Grafo", "Rede de municípios", "O(V+E) traversal", "Lista adjacência para municípios"],
    ]
    
    table = ax.table(cellText=dados, cellLoc='left', loc='center',
                    colWidths=[0.15, 0.25, 0.2, 0.4])
    
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2.5)
    
    # Formatar header
    for i in range(4):
        table[(0, i)].set_facecolor('#4CAF50')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Alternância de cores
    for i in range(1, len(dados)):
        for j in range(4):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#f0f0f0')
            else:
                table[(i, j)].set_facecolor('#ffffff')
    
    plt.title('Tabela de Estruturas de Dados Utilizadas\nJustificativa de Complexidade',
             fontsize=13, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(arquivo_saida, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ {arquivo_saida}")


def visualizar_gap_otimalidade(registros: List[Dict], arquivo_saida: str) -> None:
    """Gap de otimalidade entre Força Bruta e Dijkstra
    
    Fig 6: Diferença percentual FB vs Dijkstra
    """
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Agrupar por tamanho
    tamanhos = sorted(set(r["tamanho_n"] for r in registros))
    gaps = []
    ns = []
    
    for n in tamanhos:
        fb = next((r for r in registros if r["algoritmo"] == "força_bruta" 
                  and r["tamanho_n"] == n), None)
        dij = next((r for r in registros if r["algoritmo"] == "dijkstra" 
                   and r["tamanho_n"] == n), None)
        
        if fb and dij and fb["melhor_custo"] > 0:
            gap_pct = ((dij["melhor_custo"] - fb["melhor_custo"]) 
                      / fb["melhor_custo"] * 100)
            gaps.append(abs(gap_pct))
            ns.append(n)
    
    if gaps:
        ax.bar(ns, gaps, color='green', alpha=0.7, edgecolor='darkgreen', linewidth=2)
        ax.plot(ns, gaps, 'o-', color='darkgreen', linewidth=2.5, markersize=8)
        
        for n, gap in zip(ns, gaps):
            ax.text(n, gap + 0.5, f"{gap:.1f}%", ha='center', fontsize=10,
                   fontweight='bold')
    
    ax.set_xlabel('Número de Vértices (N)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Gap de Otimalidade (%)', fontsize=12, fontweight='bold')
    ax.set_title('Gap de Otimalidade: |Dijkstra - Força Bruta| / FB\nMenor é melhor (próximo a 0%)',
                fontsize=13, fontweight='bold', pad=15)
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    ax.set_ylim(bottom=0)
    
    # Interpretação
    ax.text(0.02, 0.98, "Interpretação: Gap próximo a 0% → Dijkstra é ótimo\nGap > 0% → Dijkstra é subótimo para esta instância",
           transform=ax.transAxes, fontsize=10, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(arquivo_saida, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ {arquivo_saida}")


def gerar_todas_figuras(grafo_rs: Grafo, grafo_matopiba: Grafo,
                       bst_rs: BinarySearchTree, bst_matopiba: BinarySearchTree,
                       registros: List[Dict], arestas_mst_rs: List[Tuple[int, int]],
                       arestas_mst_matopiba: List[Tuple[int, int]],
                       pasta_saida: str = "./report") -> None:
    """Gera todas as 6 figuras obrigatórias"""
    
    os.makedirs(pasta_saida, exist_ok=True)
    
    print("\n🎨 Gerando visualizações...\n")
    
    # Fig 1a
    visualizar_grafo(grafo_rs, 
                    "Fig 1a: Rede de Resposta a Enchentes - Rio Grande do Sul\nGrafo com MST destacada (arestas em vermelho)",
                    f"{pasta_saida}/fig1a_grafo_rs.png",
                    arestas_destacadas=arestas_mst_rs)
    
    # Fig 1b
    visualizar_grafo(grafo_matopiba,
                    "Fig 1b: Triagem de Risco de Seca - MATOPIBA\nGrafo com MST destacada (arestas em vermelho)",
                    f"{pasta_saida}/fig1b_grafo_matopiba.png",
                    arestas_destacadas=arestas_mst_matopiba)
    
    # Fig 2 (aqui dividindo em 2a e 2b)
    visualizar_bst(bst_rs,
                  "Fig 2a: Árvore Binária de Busca - RS\nOrdenada por Índice de Risco",
                  f"{pasta_saida}/fig2a_bst_rs.png")
    
    visualizar_bst(bst_matopiba,
                  "Fig 2b: Árvore Binária de Busca - MATOPIBA\nOrdenada por Índice de Risco",
                  f"{pasta_saida}/fig2b_bst_matopiba.png")
    
    # Fig 3
    visualizar_desempenho(registros,
                         f"{pasta_saida}/fig3_desempenho.png")
    
    # Fig 4
    visualizar_tabela_estruturas(f"{pasta_saida}/fig4_estruturas.png")
    
    # Fig 5
    visualizar_gap_otimalidade(registros,
                              f"{pasta_saida}/fig5_gap.png")
    
    print("\n✨ Todas as figuras geradas com sucesso!")
