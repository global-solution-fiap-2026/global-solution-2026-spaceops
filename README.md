# SpaceOps 2026 — Monitoramento de Riscos Ambientais

**Global Solution FIAP | Dynamic Programming**  
**Disciplina:** Estruturas de Dados e Algoritmos  
**Professor:** André Marques  
**Período:** 1º Semestre de 2026

---

## Identificação do Grupo

| RA | Nome |
|---|---|
| **564382** | Gabriel Viana de Souza |
| **561714** | Rafael Falaguasta Ferraz |
| **565288** | Victor Simoes Altieri |

---

## 📋 Resumo do Projeto

Sistema de monitoramento e triagem de riscos ambientais em municípios brasileiros usando:
- **Estruturas de Dados:** Árvore Binária de Busca (BST), Grafo (lista de adjacência)
- **Algoritmos:** Força Bruta (backtracking) vs. Dijkstra (guloso)
- **Cenários Reais:** Rio Grande do Sul (enchentes 2024) e MATOPIBA (seca)
- **Análise:** Comparação de desempenho, gap de otimalidade, escalabilidade empírica

**Alinhamento ODS:** 2, 9, 11, 13 (Fome Zero, Indústria e Inovação, Cidades Sustentáveis, Ação Climática)

---

## 🏗️ Estrutura do Repositório

```
global-solution-2026-spaceops/
├── README.md                          # Este arquivo
├── requirements.txt                   # Dependências Python
├── main.py                            # Script principal
│
├── data/
│   ├── raw/
│   │   ├── cenario_rs.json           # Dados brutos RS
│   │   └── cenario_matopiba.json     # Dados brutos MATOPIBA
│   └── processed/
│       └── resultados_desempenho.json # Resultados da execução
│
├── src/
│   ├── data_structures.py            # BST e Grafo (implementação do zero)
│   ├── brute_force.py                # Algoritmo Força Bruta (backtracking)
│   ├── greedy.py                     # Algoritmo Dijkstra (guloso)
│   ├── performance_monitor.py        # Instrumentação (tempo, memória)
│   └── visualizations.py             # 6 figuras obrigatórias
│
├── notebooks/
│   └── analise_resultados.ipynb      # Análise interativa + escala de decisão
│
├── tests/
│   └── test_algorithms.py            # 43+ testes unitários (pytest)
│
└── report/
    ├── fig1a_grafo_rs.png            # Grafo RS com MST
    ├── fig1b_grafo_matopiba.png      # Grafo MATOPIBA com MST
    ├── fig2a_bst_rs.png              # BST RS
    ├── fig2b_bst_matopiba.png        # BST MATOPIBA
    ├── fig3_desempenho.png           # Tempo × N
    ├── fig4_estruturas.png           # Tabela de estruturas
    ├── fig5_gap.png                  # Gap de otimalidade
    └── relatorio_final.pdf           # Relatório técnico
```

---

## 🚀 Instalação e Execução

### 1. Clonar repositório
```bash
git clone https://github.com/Gabrielvianaana/global-solution-2026-spaceops.git
cd global-solution-2026-spaceops
```

### 2. Criar ambiente virtual (opcional, recomendado)
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt --break-system-packages
```

### 4. Executar projeto
```bash
python main.py
```

**Output esperado:**
- ✅ Carregamento de 2 cenários (RS e MATOPIBA)
- ✅ Execução de Força Bruta (N ≤ 8)
- ✅ Execução de Dijkstra (N até 10)
- ✅ Relatório comparativo
- ✅ 7 figuras PNG em `report/`

### 5. Executar testes
```bash
pytest tests/test_algorithms.py -v --tb=short
```

**Espera:** 43+ testes passando

---

## 🧬 Descrição dos Módulos

### `data_structures.py`
**Implementação do zero (sem bibliotecas externas para BST)**

#### Classe `Node`
- Nó da BST com atributos: `municipio_id`, `nome`, `indice_risco`, `custo_atendimento`, `populacao`
- Ponteiros: `esquerda`, `direita`

#### Classe `BinarySearchTree`
- **Propriedade:** `risco_esquerda < risco_pai < risco_direita`
- **Operações:**
  - `inserir(mid, nome, risco, custo, pop)` — O(h)
  - `buscar_intervalo(r_min, r_max)` — O(h) amortizado
  - `percurso_in_order()` — O(n), retorna ordenado por risco
  - `altura()` — O(n)
  - `get_tamanho()` — O(1)

#### Classe `Grafo`
- **Representação:** Dicionário de listas de adjacência `{id: [(vizinho, peso), ...]}`
- **Justificativa:** Grafo esparso; O(V+E) para traversal vs O(V²) para matriz
- **Operações:**
  - `adicionar_vertice(mid, nome, risco, custo, pop)` — O(1)
  - `adicionar_aresta(u, v, peso)` — O(1)
  - `obter_vizinhos(mid)` — O(1)
  - `get_vertices()` — O(V)
  - `get_num_vertices()` — O(1)
  - `get_num_arestas()` — O(V+E)

---

### `brute_force.py`
**Força Bruta com backtracking**

#### Classe `ForcaBrutaSolver`
- **Estratégia:** Enumeração exaustiva de todos os caminhos de s a t
- **Complexidade:** O(V!) em tempo, O(V) em espaço (recursão)
- **Uso:** Validação em instâncias pequenas (N ≤ 12)
- **Métodos:**
  - `encontrar_melhor_caminho(origem, destino)` → `(caminho, custo)`
  - `get_stats()` → contadores de recursão e caminhos avaliados

#### Função `gerar_crescimento_combinatorio(tamanhos)`
- Calcula (n-1)! para visualizar explosão combinatória

---

### `greedy.py`
**Algoritmo de Dijkstra**

#### Classe `DijkstraSolver`
- **Estratégia:** Sempre expandir aresta de menor custo acumulado
- **Complexidade:** O((V+E) log V) com heap
- **Propriedade:** Ótimo para pesos não-negativos; gap = 0% em instâncias do projeto
- **Métodos:**
  - `encontrar_caminhos_minimos(origem)` → `{destino: (custo, caminho)}`
  - `encontrar_mst_dijkstra()` → `(arestas, custo_total)`
  - `dijkstra_com_prioridade_risco(origem, r_min, r_max)` → prioriza municípios críticos
  - `get_stats()` → relaxações e inserções heap

---

### `performance_monitor.py`
**Instrumentação de desempenho**

#### Classe `PerformanceMonitor`
- **Medições:**
  - Tempo: `time.perf_counter()` em ms
  - Memória: `tracemalloc` em MB
  - Operações: contadores elementares
- **Métodos:**
  - `medir_tempo(func, *args)` → (tempo_ms, resultado)
  - `medir_memoria(func, *args)` → (mem_mb, resultado)
  - `registrar_execucao()` → salva registro estruturado
  - `gerar_relatorio()` → tabela comparativa
  - `salvar_json()`, `carregar_json()`

#### Função `rodar_experimento_comparativo(grafo, tamanhos_fb, tamanhos_dijkstra)`
- Executa ambos algoritmos em múltiplos tamanhos
- Retorna monitor com todos os registros

---

### `visualizations.py`
**6 Figuras obrigatórias**

| Figura | Nome | Conteúdo |
|--------|------|----------|
| **1a** | `fig1a_grafo_rs.png` | Grafo RS, arestas MST em vermelho |
| **1b** | `fig1b_grafo_matopiba.png` | Grafo MATOPIBA, arestas MST em vermelho |
| **2a** | `fig2a_bst_rs.png` | Árvore BST RS com nós coloridos por risco |
| **2b** | `fig2b_bst_matopiba.png` | Árvore BST MATOPIBA com nós coloridos por risco |
| **3** | `fig3_desempenho.png` | Tempo × N (log), FB vs Dijkstra |
| **4** | `fig4_estruturas.png` | Tabela estruturas de dados + complexidade |
| **5** | `fig5_gap.png` | Gap de otimalidade \|Dijkstra - FB\| / FB |

**Função principal:**
- `gerar_todas_figuras(grafo_rs, grafo_matopiba, bst_rs, bst_matopiba, registros, mst_rs, mst_matopiba, pasta_saida)`

---

## 📊 Cenários Brasileiros

### Cenário A: Rio Grande do Sul
- **Contexto:** Enchentes de 2024
- **Dados:** 12 municípios afetados (Porto Alegre, Rio Grande, Pelotas, etc.)
- **Objetivo:** MST de cobertura mínima para equipes de resposta + caminhos mínimos de Porto Alegre
- **Fonte:** Defesa Civil RS + DNIT

### Cenário B: MATOPIBA
- **Contexto:** Triagem de risco de seca
- **Dados:** 10 municípios críticos (Maranhão, Tocantins, Piauí, Bahia)
- **Objetivo:** Priorização por risco (NDVI + precipitação) + rota ótima de atendimento
- **Fonte:** NDVI MODIS/NASA + INMET

---

## 🔍 Análise Comparativa

### Força Bruta vs. Dijkstra

| Aspecto | Força Bruta | Dijkstra |
|---------|-------------|----------|
| **Complexidade** | O(V!) | O((V+E) log V) |
| **Qualidade** | Ótimo (garantido) | Ótimo (para pesos ≥ 0) |
| **Gap de otimalidade** | 0% (baseline) | 0% (iguala FB) |
| **Escalabilidade** | N ≤ 12 | N até 100+ |
| **Custo computacional** | Inviável para N > 12 | Eficiente |
| **Uso prático** | Validação teórica | Produção |

### Escala de Decisão (4 níveis)

| Nível | Solução | Qualidade | Custo | Viabilidade |
|-------|---------|-----------|-------|-------------|
| **1 (Melhor)** | Dijkstra + BST (MATOPIBA) | Gap=0% | O((V+E)logV) | ✅ Alta |
| **2** | Dijkstra + BST (RS, N=12) | Gap=0% | O((V+E)logV) | ✅ Alta |
| **3** | Força Bruta (RS, N=12) | Gap=0% | O(V!) | ⚠️ Limitada |
| **4 (Pior)** | Força Bruta (N > 12) | Ótima (teórica) | Inviável | ❌ Não escalável |

**Recomendação:** Dijkstra com priorização via BST para municípios críticos (risco > 0.75)

---

## 📝 Relatório Técnico

Seções obrigatórias (≤ 12 páginas):

1. **Identificação:** Grupo com RM/NOME + cenários escolhidos
2. **Modelagem:** Grafo + BST + justificativa de estruturas
3. **Complexidade teórica:** T(n) e S(n) para ambos algoritmos
4. **Resultados:** Figuras 1-5 com interpretações (≥ 3 linhas cada)
5. **Escala de decisão:** 4 níveis com gap e análise
6. **Conclusão:** Recomendação prática + ODS
7. **Referências:** Cormen, Sedgewick, INPE, IBGE, DNIT

**Gerado automaticamente:** `relatorio_final.pdf` (com imagens dos report/)

---

## 🧪 Testes Unitários

**Total:** 43+ testes com pytest

**Cobertura:**
- BST: 10 testes (inserção, busca intervalo, in-order, altura)
- Grafo: 8 testes (vértices, arestas, vizinhos)
- Força Bruta: 5 testes (caminho, validação, stats)
- Dijkstra: 8 testes (caminhos, MST, prioridade, stats)
- Integração: 3 testes (coerência, validação cruzada)

**Executar:**
```bash
pytest tests/test_algorithms.py -v
```

**Esperado:**
```
test_node_criacao PASSED
test_bst_inserir_multiplos PASSED
...
43 passed in X.XXs
```

---

## 📈 Interpretação dos Resultados

### Fig 1a/1b: Grafos com MST
- **Leitura:** Arestas vermelhas = árvore geradora mínima de menor custo
- **Cores dos nós:** Verde (risco baixo) → Vermelho (risco alto)
- **Insight:** Distribuição de risco não necessariamente correlaciona com posição geográfica

### Fig 2a/2b: BST
- **Leitura:** Árvore ordenada por risco crescente (esquerda < raiz < direita)
- **Altura:** Indica balanceamento; altura = O(log n) ideal, O(n) pior caso
- **Uso:** Busca rápida de municípios críticos via `buscar_intervalo(0.75, 1.0)`

### Fig 3: Desempenho
- **Eixo Y (log):** Diferenças exponenciais visíveis
- **Ponto de cruzamento:** Onde Dijkstra fica mais rápido que Força Bruta
- **Insight:** Força Bruta inviável para N > 10 em tempo aceitável

### Fig 4: Estruturas
- **Justificativa:** Por que lista adjacência > matriz para grafo esparso
- **Trade-offs:** Memória vs. Tempo para cada operação

### Fig 5: Gap
- **Gap = 0%:** Dijkstra encontrou solução ótima (igual a Força Bruta)
- **Gap > 0%:** Dijkstra subótimo (não acontece neste projeto)
- **Métrica:** Validação empírica da qualidade

---



---

## 📋 Checklist de Entrega

- [ ] Repositório GitHub público
- [ ] README.md em português
- [ ] `requirements.txt` com dependências
- [ ] Código-fonte em `src/` (5 módulos)
- [ ] Dados em `data/raw/` (2 cenários)
- [ ] Testes em `tests/` (43+ testes, pytest)
- [ ] Notebook Jupyter em `notebooks/`
- [ ] Relatório PDF em `report/`
- [ ] 7 figuras PNG em `report/`
- [ ] Histórico de commits distribuído
- [ ] Documentação em docstrings (Google style)

---

## 🔗 Referências

**Livros:**
- Cormen, T. et al. (2022). *Introduction to Algorithms*, 4th Ed. MIT Press
- Sedgewick, R. & Wayne, K. (2011). *Algorithms*, 4th Ed. Addison-Wesley

**Dados Geoespaciais:**
- NASA Earthdata: earthdata.nasa.gov
- INPE PRODES/DETER: terrabrasilis.dpi.inpe.br
- IBGE: ibge.gov.br/geociencias
- DNIT: dnit.gov.br

**Documentação Python:**
- heapq: docs.python.org/3/library/heapq.html
- tracemalloc: docs.python.org/3/library/tracemalloc.html
- networkx: networkx.org

---

## 📞 Contato

**Equipe SpaceOps**
- Gabriel Viana de Souza (RM 564382)
- Rafael Falaguasta Ferraz (RM 561714)
- Victor Simoes Altieri (RM 565288)

**Repositório:** https://github.com/Gabrielvianaana/global-solution-2026-spaceops

---

**Desenvolvido para FIAP — Global Solution 2026**  
**Disciplina:** Estruturas de Dados e Algoritmos  
**Professor:** André Marques
