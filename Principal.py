# -*- coding: utf-8 -*-

from Funcoes import *

# Boas Vindas
print("\nBem Vindo(a)!\n\n")
print("Tipos de Filtros: Passa-Baixa (PB) ou Passa-Alta (PA)")

# Pega o tipo de filtro e os pontos de projeto
tipo = input("Digite o tipo que deseja: ")
print("\nAgora vamos aos Pontos de Projeto ... ")
Wp = float(input("Digite a Frequência de Passagem (Wp): "))
Ws = float(input("Digite a Frequência de Rejeição (Ws): "))
Ap = float(input("Digite a Atenuação de Passagem (Ap): "))
As = float(input("Digite a Atenuação de Rejeição (As): "))

# Inicializa um Objeto da Classe Butterworth
filtro = chebyshev(tipo, Wp, Ws, Ap, As)

# Define e exibe a Constante de Proporcionalidade
e = filtro.constProp()
print("--------------------------------------------------------------------")
print("Seu filtro possui Constante (e):", e)
print("--------------------------------------------------------------------")

# Define e exibe ordem do filtro
n, N = filtro.ordem()
print("--------------------------------------------------------------------")
print("Seu filtro possui a ordem (N):", N, "(", n, ")")
print("--------------------------------------------------------------------")

# Define e exibe frequência de corte
Wc = filtro.freq_corte()
print("--------------------------------------------------------------------")
print("Seu filtro possui frequência de Corte (Wc):", Wc)
print("--------------------------------------------------------------------")

# Define e exibe Função de Transferência
H = filtro.func_tranf()
print("--------------------------------------------------------------------")
print("Sua Função de Transferência H(s) é:")
print(H)
print("--------------------------------------------------------------------")

# Plotar Gráficos
print("Deseja Plotar os gráficos de Bode?")
resposta = input("'s' ou 'n' (sem aspas): ")
if resposta == 's':
    filtro.plotar()
elif resposta == 'n':
    print("Gráfico não iniciado!")
else:
    print("Resposta não identificada.")
print("--------------------------------------------------------------------\n")
