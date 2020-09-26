# -*- coding: utf-8 -*-

#Importa Bibliotecas Necessárias
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np


class chebyshev:
    
    # Iniciação do Objeto e seus parâmetros
    def __init__(self, tipo, Wp1, Ws1, Ap, As, Wp2 = 0, Ws2 = 0):
        self.tipo = tipo
        self.Wp = Wp1
        self.Ws = Ws1
        self.Ap = Ap
        self.As = As
        if tipo == "PF" or tipo == "RF":
            self.Wp1 = Wp1
            self.Wp2 = Wp2
            self.Ws1 = Ws1
            self.Ws2 = Ws2
        
    
    # Constante de Proporcionalidade
    def constProp(self):
        e = np.sqrt(pow(10, (-0.1*self.Ap)) - 1)
        self.e = e
        return e
    
    
    # Bandas de Passagem
    def bandas(self):
        Bp = self.Wp2 - self.Wp1
        Bs = self.Ws2 - self.Ws1
        self.Bs = Bs
        self.Bp = Bp
        return Bp, Bs
    
    
    # Essa função define e retorna a ordem do filtro
    def ordem(self):
        if self.tipo == "PB":
            n = np.arccosh(np.sqrt(pow(10, (-0.1*self.As)) - 1) / self.e
                           ) / np.arccosh(self.Ws/self.Wp)
        elif self.tipo == "PA":
            n = np.arccosh(np.sqrt(pow(10, (-0.1*self.As)) - 1) / self.e
                           ) / np.arccosh(self.Wp/self.Ws)
        elif self.tipo == "PF":
            n = np.arccosh(np.sqrt(pow(10, (-0.1*self.As)) - 1) / self.e
                           ) / np.arccosh(self.Bs/self.Bp)
        elif self.tipo == "RF":
            n = np.arccosh(np.sqrt(pow(10, (-0.1*self.As)) - 1) / self.e
                           ) / np.arccosh(self.Bp/self.Bs)
        N = int(np.ceil(n))
        self.N = N
        return n, N
    
    
    # Essa função define e retorna a frequência de corte do filtro
    def freq_corte(self):
        if self.tipo == "PB" or self.tipo == "PA":
            Wc = self.Wp * np.cosh( (1/self.N) * np.arccosh(1/self.e) )
            self.Wc = Wc
            return Wc
        elif self.tipo == "PF" or self.tipo == "RF":
            Wc1 = self.Wp1 * np.cosh( (1/self.N) * np.arccosh(1/self.e) )
            Wc2 = self.Wp2 * np.cosh( (1/self.N) * np.arccosh(1/self.e) )
            self.Wc1 = Wc1
            self.Wc2 = Wc2
            return Wc1, Wc2
    
    
    # Frequência de Ressonância
    def freq_ress(self):
        Wo = np.sqrt(self.Wp1*self.Wp2)
        self.Wo = Wo
        return Wo
    
    
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
        aux = 0
        for i in range(-self.N, 1):
            D.append(coef[aux]*pow(self.Wp, i))
            aux = aux + 1
            
        if self.N % 2 != 0:
            if self.tipo == "PB":
                num, den = signal.lp2lp(coef[-1], coef, self.Wp)
                H = signal.TransferFunction(num[-1], den)
            elif self.tipo == "PA":
                num, den = signal.lp2hp(coef[-1], coef, self.Wp)
                H = signal.TransferFunction(num, den)
            elif self.tipo == "PF":
                num, den = signal.lp2bp(coef[-1], coef, self.Wo, self.Bp)
                H = signal.TransferFunction(num, den)
            elif self.tipo == "RF":
                num, den = signal.lp2bs(coef[-1], coef, self.Wo, self.Bp)
                H = signal.TransferFunction(num, den)
        else:
            aux = 1 / np.sqrt(1 + self.e**2)
            if self.tipo == "PB":
                num, den = signal.lp2lp(coef[-1], coef, self.Wp)
                H = signal.TransferFunction(num * aux, den)
            elif self.tipo == "PA":
                num, den = signal.lp2hp(coef[-1], coef, self.Wp)
                H = signal.TransferFunction(num * aux, den)
            elif self.tipo == "PF":
                num, den = signal.lp2bp(coef[-1], coef, self.Wo, self.Bp)
                H = signal.TransferFunction(num * aux, den)
            elif self.tipo == "RF":
                num, den = signal.lp2bs(coef[-1], coef, self.Wo, self.Bp)
                H = signal.TransferFunction(num * aux, den)
        self.H = H
        return H
    
    
    # Essa função organiza a FT para ser exibida
    def org_FT(self):
        razao = self.H.den[-1]
        # Organiza o Numerador
        # for i in range(0, len(self.H.num)):
            
    
    # Essa função plota o Diagrama de Bode
    def plotar(self):
        # Plotagem do Módulo
        w, y, phase = self.H.bode(w = np.arange(0, 15000, step = 1))
        plt.figure(1)
        plt.grid(True)
        plt.xlim(0, 12000)
        plt.ylim(-70, 0)
        plt.plot(w, y)
        
        # Plotagem da Fase
        plt.figure(2)
        plt.grid(True)
        plt.xlim(0, 6000)
        plt.ylim(-360, 0)
        plt.plot(w, phase, 'r')
    
    
    
    
    
    
    
    
    
    
    
    