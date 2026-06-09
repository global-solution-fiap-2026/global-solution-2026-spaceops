"""
SpaceOps 2026 - Script Principal
Carrega cenários brasileiros, executa Força Bruta e Dijkstra, gera visualizações
"""

import json
import sys
sys.path.insert(0, './src')

from data_structures import Grafo, BinarySearchTree
from brute_force import ForcaBrutaSolver
from greedy import DijkstraSolver
from performance_monitor import PerformanceMonitor, rodar_experimento_comparativo
from visualizations import gerar_todas_figuras


def carregar_cenario(arquivo_json: str) -> tuple:
    """Carrega cenário de arquivo JSON
    
    Returns:
        (grafo, bst)
    """
    with open(arquivo_json, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    grafo = Grafo()
    bst = BinarySearchTree()
    
    # Adicionar vértices
    for mun in dados["municipios"]:
        mid = mun["id"]
        nome = mun["nome"]
        risco = mun["indice_risco"]
        custo = mun["custo_atendimento"]
        pop = mun["populacao"]
        
        grafo.adicionar_vertice(mid, nome, risco, custo, pop)
        bst.inserir(mid, nome, risco, custo, pop)
    
    # Adicionar arestas
    for aresta in dados["arestas"]:
        u, v, peso = aresta
        grafo.adicionar_aresta(u, v, peso)
    
    return grafo, bst


def executar_cenario(cenario_nome: str, arquivo_json: str) -> tuple:
    """Executa cenário completo
    
    Returns:
        (grafo, bst, registros_monitor, arestas_mst)
    """
    print(f"\n{'='*80}")
    print(f"CENÁRIO: {cenario_nome}")
    print(f"{'='*80}\n")
    
    # Carregar
    print(f"📂 Carregando {arquivo_json}...")
    grafo, bst = carregar_cenario(arquivo_json)
    
    print(f"   ✓ {grafo.get_num_vertices()} municípios")
    print(f"   ✓ {grafo.get_num_arestas()} conexões")
    print(f"   ✓ Árvore BST altura={bst.altura()}")
    
    # Dijkstra MST
    print(f"\n🔵 Executando Dijkstra (MST)...")
    dij_mst = DijkstraSolver(grafo, bst)
    arestas_mst, custo_mst = dij_mst.encontrar_mst_dijkstra()
    print(f"   ✓ MST custo: {custo_mst:.2f}")
    print(f"   ✓ Arestas MST: {len(arestas_mst)}")
    
    # Experimento comparativo
    print(f"\n📊 Experimento comparativo (tamanhos pequenos)...")
    vertices_n = grafo.get_num_vertices()
    
    tamanhos_fb = list(range(3, min(vertices_n + 1, 8), 1))
    tamanhos_dij = list(range(5, vertices_n + 1, 2))
    
    monitor = rodar_experimento_comparativo(grafo, tamanhos_fb, tamanhos_dij, bst)
    
    return grafo, bst, monitor.registros, arestas_mst


def main():
    """Executa projeto completo"""
    
    print("\n" + "="*80)
    print("🛰️  SPACEOPS 2026 - MONITORAMENTO DE RISCOS AMBIENTAIS")
    print("="*80)
    
    # Executar cenários
    cenarios = [
        ("Rio Grande do Sul - Resposta a Enchentes", "data/raw/cenario_rs.json"),
        ("MATOPIBA - Triagem de Risco de Seca", "data/raw/cenario_matopiba.json")
    ]
    
    grafos = {}
    bsts = {}
    todos_registros = []
    arestas_msts = {}
    
    for nome, arquivo in cenarios:
        try:
            g, b, regs, mst = executar_cenario(nome, arquivo)
            
            chave = "rs" if "RS" in nome or "Rio" in nome else "matopiba"
            grafos[chave] = g
            bsts[chave] = b
            todos_registros.extend(regs)
            arestas_msts[chave] = mst
        except Exception as e:
            print(f"❌ Erro ao executar {nome}: {e}")
            import traceback
            traceback.print_exc()
    
    # Imprimir relatório
    print(f"\n{'='*80}")
    print("📈 RELATÓRIO DE DESEMPENHO")
    print(f"{'='*80}\n")
    
    monitor = PerformanceMonitor()
    monitor.registros = todos_registros
    print(monitor.gerar_relatorio())
    
    # Salvar registros
    monitor.salvar_json("data/processed/resultados_desempenho.json")
    print("\n✅ Registros salvos em data/processed/resultados_desempenho.json")
    
    # Gerar visualizações
    try:
        if "rs" in grafos and "matopiba" in grafos:
            print(f"\n{'='*80}")
            print("🎨 GERANDO VISUALIZAÇÕES")
            print(f"{'='*80}")
            
            gerar_todas_figuras(
                grafo_rs=grafos["rs"],
                grafo_matopiba=grafos["matopiba"],
                bst_rs=bsts["rs"],
                bst_matopiba=bsts["matopiba"],
                registros=todos_registros,
                arestas_mst_rs=arestas_msts["rs"],
                arestas_mst_matopiba=arestas_msts["matopiba"],
                pasta_saida="./report"
            )
    except Exception as e:
        print(f"❌ Erro ao gerar visualizações: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n{'='*80}")
    print("✨ PROJETO COMPLETO!")
    print(f"{'='*80}\n")
    print("📁 Arquivos gerados:")
    print("   ✓ data/processed/resultados_desempenho.json")
    print("   ✓ report/fig1a_grafo_rs.png")
    print("   ✓ report/fig1b_grafo_matopiba.png")
    print("   ✓ report/fig2a_bst_rs.png")
    print("   ✓ report/fig2b_bst_matopiba.png")
    print("   ✓ report/fig3_desempenho.png")
    print("   ✓ report/fig4_estruturas.png")
    print("   ✓ report/fig5_gap.png")
    print("\n🚀 Próximo passo: Executar pytest para validação\n")


if __name__ == "__main__":
    main()
