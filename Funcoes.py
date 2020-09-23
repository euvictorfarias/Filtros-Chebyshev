# -*- coding: utf-8 -*-

#Importa Bibliotecas Necessárias
from math import log10, pi, sin, cos, ceil
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np


class chebyshev:
    
    # Iniciação do Objeto e seus parâmetros
    def __init__(self, tipo, Wp, Ws, Ap, As):
        self.tipo = tipo
        self.Wp = Wp
        self.Ws = Ws
        self.Ap = Ap
        self.As = As
        
    
    # Constante de Proporcionalidade
    def constProp(self):
        e = np.sqrt(pow(10, (-0.1*self.Ap)) - 1)
        self.e = e
        return e
    
    
    # Essa função define e retorna a ordem do filtro
    def ordem(self):
        if self.tipo == "PB":
            n = np.arccosh(np.sqrt(pow(10, (-0.1*self.As)) - 1) / self.e
                           ) / np.arccosh(self.Ws/self.Wp)
        elif self.tipo == "PA":
            n = np.arccosh(np.sqrt(pow(10, (-0.1*self.As)) - 1) / self.e
                           ) / np.arccosh(self.Wp/self.Ws)
        N = ceil(n)
        self.N = N
        return n, N
    
    
    # Essa função define e retorna a frequência de corte do filtro
    def freq_corte(self):
        Wc = self.Wp * np.cosh( (1/self.N) * np.arccosh(1/self.e) )
        self.Wc = Wc
        return Wc
    
    
    # Essa função define e retorna as raízes do denominador da FT
    def raizes_unit(self):
        Sk = list()
        Ok = list()
        Wk = list()
        for k in range(1, self.N+1):
            Ok.append(-np.sinh((1/self.N) * np.arcsinh(1/self.e) 
                               ) * np.sin(np.pi/(2*self.N)*(2*k - 1)))
            Wk.append(np.cosh((1/self.N) * np.arcsinh(1/self.e) 
                              ) * np.cos(np.pi/(2*self.N)*(2*k - 1)))
            Sk.append(complex(Ok[k-1], Wk[k-1]))
        self.Sk = Sk
        return Sk
    
    
    # Essa função define e retorna a FT do filtro
    def func_tranf(self):
        chebyshev.raizes_unit(self)
        poli = np.poly(self.Sk)
        coef = poli.real
        D = list()
        
        # Para um Passa Baixa
        if self.tipo == "PB":
            aux = 0
            for i in range(-self.N, 1):
                D.append(coef[aux]*pow(self.Wp, i))
                aux = aux + 1
            if self.N % 2 != 0:
                H = signal.TransferFunction(D[-1], D)
            else:
                aux = np.sqrt(1 + self.e**2)
                H = signal.TransferFunction(D[-1] * aux, D)
        
        # Para um Passa Alta
        elif self.tipo == "PA":
            den = list()
            aux = self.N
            for i in range(0, self.N+1):
                D.append(coef[aux]*pow(self.Wp, i))
                aux = aux - 1
                if i == 0:
                    den.append(D[0])
                else:
                    den.append(0) 
            if self.N % 2 != 0:
                H = signal.TransferFunction(den, D)
            else:
                aux = np.sqrt(1 + self.e**2)
                H = signal.TransferFunction(den * aux, D)
        
        self.H = H
        return H
    
    # Essa função plota o Diagrama de Bode
    def plotar(self):
        # Plotagem do Módulo
        w, y, phase = signal.bode(self.H)
        plt.figure(1)
        plt.grid(True)
        plt.xlim(0, 15000)
        plt.ylim(-50, 0)
        plt.plot(w, y)
        
        # Plotagem da Fase
        plt.figure(2)
        plt.grid(True)
        plt.xlim(0, 6000)
        plt.ylim(-300, 0)
        plt.plot(w, phase, 'r')
    
    
    
    
    
    
    
    
    
    
    
    