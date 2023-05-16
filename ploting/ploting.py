import matplotlib.pyplot as plt
import numpy as np

# Abrir arquivo e ler dados
with open('tactile_test.dat', 'r') as f:
    lines = f.readlines()

x = []
y = []

for line in lines:
    data = line.strip().split()
    x.append(data[0])
    y.append(float(data[1]))

# Calcular média dos valores
mean = np.mean(y)
mean_line = [mean] * len(y)

# Plotar gráfico com barras de erro e linha da média
plt.bar(x, y, yerr=np.std(y))
plt.plot(x, mean_line, linestyle='-', color='red', label=f'Média: {mean:.2f}')
plt.text(7, mean + 0.1, f'Média: {mean:.2f}', color='red', ha='center', va='bottom')

# Configurar e exibir gráfico
plt.title('Tempo de reação tátil')
plt.xlabel('Tentativa')
plt.ylabel('Tempo de reação (s)')
plt.legend(['Média'])
plt.show()
