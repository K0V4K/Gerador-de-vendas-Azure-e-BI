import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker 

NUM_LINHAS = 1000000  
NOME_ARQUIVO = 'dados_vendas_bigdata.csv'
fake = Faker('pt_BR') 

print(f"Iniciando a geração de {NUM_LINHAS:,} linhas...")
ids_transacao = np.arange(1, NUM_LINHAS + 1)

data_fim = datetime.now()
data_inicio = data_fim - timedelta(days=365)

datas = pd.to_datetime(np.random.choice(pd.date_range(data_inicio, data_fim), size=NUM_LINHAS))
produtos = ['Smartphone X', 'Notebook Pro', 'Câmera Mirrorless', 'Fone de Ouvido Max', 
            'Smartwatch Series 5', 'Console Game', 'Tablet Pro 12', 'Monitor UltraWide', 
            'SSD 1TB', 'Roteador Mesh']
produtos_vendidos = np.random.choice(produtos, size=NUM_LINHAS)
regioes = ['Sudeste', 'Sul', 'Nordeste', 'Centro-Oeste', 'Norte']

regioes_venda = np.random.choice(regioes, size=NUM_LINHAS, p=[0.45, 0.20, 0.15, 0.10, 0.10]) 
quantidades = np.random.randint(1, 6, size=NUM_LINHAS)

precos_base = {
    'Smartphone X': 3500, 'Notebook Pro': 8000, 'Câmera Mirrorless': 6000, 
    'Fone de Ouvido Max': 800, 'Smartwatch Series 5': 1500, 'Console Game': 4500, 
    'Tablet Pro 12': 2800, 'Monitor UltraWide': 1800, 'SSD 1TB': 700, 'Roteador Mesh': 500
}
valores = np.array([
    np.random.normal(loc=precos_base[p], scale=precos_base[p]*0.05) 
    for p in produtos_vendidos
])
valores = np.round(np.abs(valores) / 100) * 100 
clientes_unicos = [fake.name() for _ in range(int(NUM_LINHAS * 0.01))] 
nomes_clientes = np.random.choice(clientes_unicos, size=NUM_LINHAS)

df = pd.DataFrame({
    'id_transacao': ids_transacao,
   
    'data_venda': datas.strftime('%Y-%m-%d %H:%M:%S'), 
    'cliente': nomes_clientes,
    'produto': produtos_vendidos,
    'quantidade': quantidades,
    'valor_unitario': valores,
   
    'valor_total': valores * quantidades, 
    'regiao_venda': regioes_venda
})

print("Gerando o arquivo CSV. Isso pode levar alguns segundos...")
df.to_csv(NOME_ARQUIVO, 
          index=False, 
          encoding='utf-8')

print(f"\n✅ Concluído! Arquivo '{NOME_ARQUIVO}' gerado com sucesso na pasta do projeto.")

print(f"Tamanho do Dataframe (Linhas x Colunas): {df.shape}")
