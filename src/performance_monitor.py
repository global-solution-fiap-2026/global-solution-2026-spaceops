import time
import tracemalloc
from typing import List, Dict, Tuple, Callable
import json
from data_structures import Grafo, BinarySearchTree
from brute_force import ForcaBrutaSolver
from greedy import DijkstraSolver

class PerformanceMonitor:
    """Monitor de desempenho para algoritmos
    
    Registra:
    - Tempo de execução (ms) via time.perf_counter()
    - Memória alocada (MB) via tracemalloc
    - Operações elementares (relaxações, inserções heap, recursões)
    """
    
    def __init__(self):
        self.registros: List[Dict] = []
    
    def medir_tempo(self, funcao: Callable, *args, **kwargs) -> Tuple[float, any]:
        """Executa função e retorna (tempo_ms, resultado)"""
        inicio = time.perf_counter()
        resultado = funcao(*args, **kwargs)
        fim = time.perf_counter()
        tempo_ms = (fim - inicio) * 1000
        return tempo_ms, resultado
    
    def medir_memoria(self, funcao: Callable, *args, **kwargs) -> Tuple[float, any]:
        """Executa função e retorna (memória_mb, resultado)"""
        tracemalloc.start()
        resultado = funcao(*args, **kwargs)
        corrente, pico = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        memoria_mb = pico / (1024 * 1024)
        return memoria_mb, resultado
    
    def medir_tudo(self, funcao: Callable, *args, **kwargs) -> Tuple[float, float, any]:
        """Executa função e retorna (tempo_ms, memória_mb, resultado)"""
        tracemalloc.start()
        inicio = time.perf_counter()
        
        resultado = funcao(*args, **kwargs)
        
        fim = time.perf_counter()
        corrente, pico = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        tempo_ms = (fim - inicio) * 1000
        memoria_mb = pico / (1024 * 1024)
        
        return tempo_ms, memoria_mb, resultado
    
    def registrar_execucao(self, algoritmo: str, tamanho_n: int, 
                          tempo_ms: float, memoria_mb: float,
                          operacoes: int, melhor_custo: float) -> None:
        """Registra resultado de uma execução"""
        self.registros.append({
            "algoritmo": algoritmo,
            "tamanho_n": tamanho_n,
            "tempo_ms": tempo_ms,
            "memoria_mb": memoria_mb,
            "operacoes": operacoes,
            "melhor_custo": melhor_custo
        })
    
    def gerar_relatorio(self) -> str:
        """Gera relatório formatado dos registros"""
        if not self.registros:
            return "Nenhum registro disponível"
        
        relatorio = "=" * 100 + "\n"
        relatorio += "ANÁLISE COMPARATIVA: FORÇA BRUTA × DIJKSTRA\n"
        relatorio += "=" * 100 + "\n\n"
        
        # Tabela por algoritmo
        for algo in set(r["algoritmo"] for r in self.registros):
            registros_algo = [r for r in self.registros if r["algoritmo"] == algo]
            registros_algo.sort(key=lambda r: r["tamanho_n"])
            
            relatorio += f"\n{algo.upper()}\n"
            relatorio += "-" * 100 + "\n"
            relatorio += f"{'N':<5} {'Tempo (ms)':<15} {'Memória (MB)':<15} {'Operações':<15} {'Custo':<15}\n"
            relatorio += "-" * 100 + "\n"
            
            for r in registros_algo:
                relatorio += (f"{r['tamanho_n']:<5} "
                            f"{r['tempo_ms']:<15.3f} "
                            f"{r['memoria_mb']:<15.6f} "
                            f"{r['operacoes']:<15} "
                            f"{r['melhor_custo']:<15.2f}\n")
        
        relatorio += "\n" + "=" * 100 + "\n"
        
        # Análise de escalabilidade
        relatorio += "\nANÁLISE DE ESCALABILIDADE\n"
        relatorio += "-" * 100 + "\n"
        
        fb_registros = [r for r in self.registros if r["algoritmo"] == "força_bruta"]
        dij_registros = [r for r in self.registros if r["algoritmo"] == "dijkstra"]
        
        if fb_registros and dij_registros:
            relatorio += "\nPonto de Cruzamento:\n"
            fb_registros.sort(key=lambda r: r["tamanho_n"])
            dij_registros.sort(key=lambda r: r["tamanho_n"])
            
            # Encontrar onde Força Bruta fica mais lenta
            for i, fb_r in enumerate(fb_registros):
                dij_r_similar = next((d for d in dij_registros 
                                    if d["tamanho_n"] >= fb_r["tamanho_n"]), None)
                if dij_r_similar and fb_r["tempo_ms"] > dij_r_similar["tempo_ms"]:
                    relatorio += f"  → Dijkstra mais rápido a partir de N={fb_r['tamanho_n']}\n"
                    break
            
            relatorio += "\nRazão de Melhoria (Dijkstra / Força Bruta):\n"
            for n in sorted(set(r["tamanho_n"] for r in fb_registros)):
                fb = next((r for r in fb_registros if r["tamanho_n"] == n), None)
                dij = next((r for r in dij_registros if r["tamanho_n"] == n), None)
                
                if fb and dij:
                    razao = fb["tempo_ms"] / dij["tempo_ms"]
                    relatorio += f"  N={n}: Força Bruta é {razao:.1f}x mais lenta\n"
        
        return relatorio
    
    def salvar_json(self, caminho: str) -> None:
        """Salva registros em JSON"""
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(self.registros, f, indent=2)
    
    def carregar_json(self, caminho: str) -> None:
        """Carrega registros de JSON"""
        with open(caminho, 'r', encoding='utf-8') as f:
            self.registros = json.load(f)


def rodar_experimento_comparativo(grafo: Grafo, tamanhos_fb: List[int],
                                 tamanhos_dijkstra: List[int],
                                 bst: BinarySearchTree = None) -> PerformanceMonitor:
    """Executa experimento comparativo entre Força Bruta e Dijkstra
    
    Args:
        grafo: Grafo com dados reais
        tamanhos_fb: Lista de tamanhos N para Força Bruta (≤ 12)
        tamanhos_dijkstra: Lista de tamanhos N para Dijkstra (até 100)
        bst: Árvore binária opcional para priorização
    
    Returns:
        PerformanceMonitor com todos os registros
    """
    monitor = PerformanceMonitor()
    
    # Força Bruta
    print("\n📊 Executando Força Bruta...")
    fb = ForcaBrutaSolver(grafo)
    
    for n in tamanhos_fb:
        vertices = grafo.get_vertices()[:n]
        
        if len(vertices) < 2:
            continue
        
        origem = vertices[0]
        destino = vertices[-1]
        
        tempo_ms, (caminho, custo) = monitor.medir_tempo(
            fb.encontrar_melhor_caminho, origem, destino
        )
        
        stats = fb.get_stats()
        monitor.registrar_execucao(
            "força_bruta", n, tempo_ms, 0.0,
            stats["chamadas_recursivas"], custo
        )
        
        print(f"  N={n:3d} | {tempo_ms:8.2f}ms | Custo={custo:8.2f} | Recursões={stats['chamadas_recursivas']}")
    
    # Dijkstra
    print("\n📊 Executando Dijkstra...")
    dij = DijkstraSolver(grafo, bst)
    
    for n in tamanhos_dijkstra:
        vertices = grafo.get_vertices()[:n]
        
        if len(vertices) < 2:
            continue
        
        origem = vertices[0]
        
        tempo_ms, (caminhos, _) = monitor.medir_tempo(
            dij.encontrar_caminhos_minimos, origem
        )
        
        stats = dij.get_stats()
        custo_medio = sum(c for c, _ in caminhos.values()) / len(caminhos)
        
        monitor.registrar_execucao(
            "dijkstra", n, tempo_ms, 0.0,
            stats["relaxacoes"], custo_medio
        )
        
        print(f"  N={n:3d} | {tempo_ms:8.2f}ms | Custo médio={custo_medio:8.2f} | Relaxações={stats['relaxacoes']}")
    
    return monitor