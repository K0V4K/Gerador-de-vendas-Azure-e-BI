# Importa as bibliotecas necessárias para manipulação de dados, matemática e simulação de datas e nomes.
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker 

# --- CONFIGURAÇÃO INICIAL DO VOLUME DE DADOS ---

# Define a quantidade de linhas (registros) que serão geradas.
# Usamos 1.000.000 de registros para justificar o uso de ferramentas de Big Data.
NUM_LINHAS = 1000000  
# Define o nome do arquivo de saída.
NOME_ARQUIVO = 'dados_vendas_bigdata.csv'

# Configura o gerador de dados (Faker) para usar dados mais realistas em Português do Brasil.
fake = Faker('pt_BR') 

print(f"Iniciando a geração de {NUM_LINHAS:,} linhas...")

# --- 1. GERAÇÃO DE VARIÁVEIS CHAVE E DIMENSÕES ---

# Gera uma sequência de IDs (Identificadores únicos) para cada transação.
ids_transacao = np.arange(1, NUM_LINHAS + 1)

# Define o período de tempo para as vendas (últimos 365 dias).
data_fim = datetime.now()
data_inicio = data_fim - timedelta(days=365)

# Distribui as datas de venda de forma aleatória dentro do período definido.
datas = pd.to_datetime(np.random.choice(pd.date_range(data_inicio, data_fim), size=NUM_LINHAS))

# Define o catálogo de produtos para simulação.
produtos = ['Smartphone X', 'Notebook Pro', 'Câmera Mirrorless', 'Fone de Ouvido Max', 
            'Smartwatch Series 5', 'Console Game', 'Tablet Pro 12', 'Monitor UltraWide', 
            'SSD 1TB', 'Roteador Mesh']
# Atribui um produto aleatoriamente a cada transação.
produtos_vendidos = np.random.choice(produtos, size=NUM_LINHAS)

# Define as regiões de venda (dimensão geográfica para análise de BI).
regioes = ['Sudeste', 'Sul', 'Nordeste', 'Centro-Oeste', 'Norte']
# Distribui as vendas por região, dando maior probabilidade para o Sudeste (45% dos casos).
regioes_venda = np.random.choice(regioes, size=NUM_LINHAS, p=[0.45, 0.20, 0.15, 0.10, 0.10]) 

# --- 2. GERAÇÃO DE MÉTRICAS (FATO) ---

# Gera a quantidade de itens vendidos por transação (entre 1 e 5).
quantidades = np.random.randint(1, 6, size=NUM_LINHAS)

# Define a base de preço médio para cada produto.
precos_base = {
    'Smartphone X': 3500, 'Notebook Pro': 8000, 'Câmera Mirrorless': 6000, 
    'Fone de Ouvido Max': 800, 'Smartwatch Series 5': 1500, 'Console Game': 4500, 
    'Tablet Pro 12': 2800, 'Monitor UltraWide': 1800, 'SSD 1TB': 700, 'Roteador Mesh': 500
}

# Calcula o valor unitário: preço base com uma pequena variação aleatória de 5% (simulando descontos/promoções).
valores = np.array([
    np.random.normal(loc=precos_base[p], scale=precos_base[p]*0.05) 
    for p in produtos_vendidos
])
# Arredonda o valor para o 100 mais próximo.
valores = np.round(np.abs(valores) / 100) * 100 

# Gera um pool de nomes de clientes (simulando 1% de clientes únicos para criar recorrência).
clientes_unicos = [fake.name() for _ in range(int(NUM_LINHAS * 0.01))] 
nomes_clientes = np.random.choice(clientes_unicos, size=NUM_LINHAS)

# --- 3. MONTAGEM E EXPORTAÇÃO DO DATAFRAME ---

# Cria um DataFrame (estrutura de tabela do Pandas) combinando todas as variáveis geradas.
df = pd.DataFrame({
    'id_transacao': ids_transacao,
    # Formata a data e hora para o padrão 'AAAA-MM-DD HH:MM:SS'.
    'data_venda': datas.strftime('%Y-%m-%d %H:%M:%S'), 
    'cliente': nomes_clientes,
    'produto': produtos_vendidos,
    'quantidade': quantidades,
    'valor_unitario': valores,
    # O valor total é a métrica principal para o BI (Valor Unitário * Quantidade).
    'valor_total': valores * quantidades, 
    'regiao_venda': regioes_venda
})

# Salva o DataFrame no formato CSV (padrão para o Data Lake).
print("Gerando o arquivo CSV. Isso pode levar alguns segundos...")
df.to_csv(NOME_ARQUIVO, 
          index=False, # Impede a criação de uma coluna de índice desnecessária.
          encoding='utf-8')

print(f"\n✅ Concluído! Arquivo '{NOME_ARQUIVO}' gerado com sucesso na pasta do projeto.")
print(f"Tamanho do Dataframe (Linhas x Colunas): {df.shape}")