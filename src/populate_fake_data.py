from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

fake = Faker()

# Configurar número de linhas de dados a serem gerados
num_rows = 10000

data = {
    'date_time': [fake.date_time_between(start_date='-1y', end_date='now') for _ in range(num_rows)],
    'cpu': [random.uniform(0, 100) for _ in range(num_rows)],  # Exemplo de uso de CPU em percentual
    'memory': [random.uniform(0, 100) for _ in range(num_rows)],  # Exemplo de uso de memória em percentual
    'pods_number': [random.randint(1, 5) for _ in range(num_rows)],  # Número aleatório de pods
    'queue_msg': [random.randint(0, 1000) for _ in range(num_rows)],  # Número aleatório de mensagens na fila
    'queue_publish_rate': [random.uniform(0, 500) for _ in range(num_rows)],  # Taxa aleatória de publicação na fila
    'queue_ack_rate': [random.uniform(0, 500) for _ in range(num_rows)]  # Taxa aleatória de confirmação na fila
}

df = pd.DataFrame(data)

# Salvar os dados em um arquivo CSV com ponto e vírgula como separador
df.to_csv('/home/z33p/Development/pods_manager/data/data_fake.csv', sep=';', index=False)
