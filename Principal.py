# -*- coding: utf-8 -*-
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# Dados do Problema
Wp = 1000
Ap = -1
Ws = 5000
As = -40

# Constante de Proporcionalidade
e = np.sqrt(pow(10, (-0.1*Ap)) - 1)
print(f'e = {e:.5f}')

# Ordem do Filtro
N = np.arccosh(np.sqrt(pow(10, (-0.1*As)) - 1) / e) / np.arccosh(Ws/Wp)
print(f'n = {N:.5f}')
N = int(np.ceil(N))
print("N =", N)

# Frequência de Corte
Wc = Wp * np.cosh( (1/N) * np.arccosh(1/e) )
print(f'Wc = {Wc:.5f}')

# Polos do Sistema
Sk = list()
Ok = list()
Wk = list()
for k in range(1, N+1):
    Ok.append(-np.sinh((1/N) * np.arcsinh(1/e) ) * np.sin(np.pi/(2*N)*(2*k - 1)))
    Wk.append(np.cosh((1/N) * np.arcsinh(1/e) ) * np.cos(np.pi/(2*N)*(2*k - 1)))
    Sk.append(complex(Ok[k-1], Wk[k-1]))
print("Sk =", Sk)
 
# Polinômio do Denominador
poli = np.poly(Sk)
coef = poli.real

# Função de Transferência
D = list()
if N % 2 != 0:
    aux = 0
    for i in range(-N, 1):
        D.append(coef[aux]*pow(Wp, i))
        aux = aux + 1
    H = signal.TransferFunction(D[-1], D)
    
else:
    aux = np.sqrt(1 + e**2)
    H = signal.TransferFunction(D[-1], D)
print("H =", H)

 # Plotagem do Módulo
w, y, phase = signal.bode(H)
plt.figure(1)
plt.grid(True)
plt.xlim(0, 1000)
plt.ylim(-5, 0)
plt.plot(w, y)

# Plotagem da Fase
plt.figure(2)
plt.grid(True)
plt.xlim(0, 6000)
plt.ylim(-300, 0)
plt.plot(w, phase, 'r')













