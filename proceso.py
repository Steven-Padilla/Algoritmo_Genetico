import matplotlib.pyplot as plt
import math
from random import *
from individuo import *


def decimal(genotipo):
    numero_decimal = 0
    for posicion, posicion_numero in enumerate(genotipo[::-1]):
        numero_decimal += int(posicion_numero) * 2 ** posicion
    return numero_decimal


def f(x):
    return (math.log(abs(x))) * (math.cos(x)) * math.sin(x) * (math.cos(x ** 2))


class Proceso:
    a = 0
    b = 0
    resolucion = 0
    intervalo = 0
    valor = 0
    bits = 0
    tam_pob_inicial = 4  # randrange(10)
    tam_pob_maxima = 0
    prob_mut_ind = 0
    prob_mut_gen = 0
    delta = 0
    individuos = []
    peores_individuos = []
    mejores_individuos = []
    individuos_poda = []
    epocas = 0

    # configuración e inicialización del AG
    def __init__(self, a, b, resolucion, pob_maxima, prob_ind, prob_gen, numero_epocas):
        self.a = a
        self.b = b
        self.tam_pob_maxima = pob_maxima
        self.resolucion = resolucion
        self.prob_mut_ind = prob_ind
        self.prob_mut_gen = prob_gen
        self.epocas = numero_epocas
        self.intervalo = self.tamanio_intervalo()
        self.valor = self.valores()
        self.bits = self.cantidad_bits()
        self.delta = self.calcular_delta()

        for i in range(self.epocas):
            self.iniciar_poblacion()
            self.cruza()
            self.mutacion()
            self.poda()
            self.grafica2()
        self.grafica()
        # self.grafica_curva()

    def iniciar_poblacion(self):
        genotipo = ""
        for i in range(self.tam_pob_inicial):
            for _ in range(self.bits):
                genotipo += str(randint(0, 1))
            self.crear_individuo(genotipo, i)
            genotipo = ""

    def crear_individuo(self, genotipo, k):
        valor_i = decimal(genotipo)
        valor_fenotipo = self.fenotipo(valor_i)
        aptitud = f(valor_fenotipo)
        nuevo_individuo = Individuo(k, genotipo, valor_i, valor_fenotipo, aptitud)
        self.individuos.append(nuevo_individuo)

    def maximo(self):
        if self.a > self.b:
            return self.a
        return self.b

    def minimo(self):
        if self.a < self.b:
            return self.a
        return self.b

    def tamanio_intervalo(self):
        return self.maximo() - self.minimo()

    def valores(self):
        return (self.intervalo / self.resolucion) + 1

    def cantidad_bits(self):
        for i in range(100):
            if 2 ** i >= self.valor:
                return i

    def calcular_delta(self):
        return self.intervalo / 2 ** self.bits

    def fenotipo(self, valor_decimal):
        return self.a + (valor_decimal * self.delta)

    def cruza(self):
        i_aux = 0
        contador = 0
        punto_cruza = randint(0, len(self.individuos[0].genotipo))
        for i in range(len(self.individuos)):
            contador += 1
            if contador == 2:
                individuo_1 = self.individuos[i_aux]
                individuo_2 = self.individuos[i]
                nuevo_genotipo1 = individuo_1.genotipo[:punto_cruza] + individuo_2.genotipo[punto_cruza::]
                nuevo_genotipo2 = individuo_2.genotipo[:punto_cruza] + individuo_1.genotipo[punto_cruza::]
                self.individuos.append(Individuo(len(self.individuos), nuevo_genotipo1, 20, 0, 0))
                self.individuos.append(Individuo(len(self.individuos), nuevo_genotipo2, 20, 0, 0))
            else:
                i_aux = i

    def mutacion(self):
        nuevo_ind = ""
        contador = 0
        mutacion_ind = []
        indices_mutan_ind = []
        mutacion_gen = []
        indices_mutan_gen = []
        bit = ""
        tamanio = len(self.individuos)
        for i in range(len(self.individuos)):
            mutacion_ind.append(uniform(0, self.prob_mut_ind))

        for i in range(len(self.individuos)):
            if mutacion_ind[i] <= self.prob_mut_ind:
                indices_mutan_ind.append(i)

        # Mutación del gen
        if len(indices_mutan_ind) != 0:
            for i in range(len(indices_mutan_ind)):
                mutacion_gen.clear()
                for m in range(len(self.individuos[0].genotipo)):
                    mutacion_gen.append(uniform(0, self.prob_mut_gen + 1))
                for j in range(len(mutacion_gen)):
                    if mutacion_gen[j] <= self.prob_mut_gen:
                        indices_mutan_gen.append(j)
                if len(indices_mutan_gen) != 0:
                    for k in range(len(indices_mutan_gen)):
                        nuevo_ind = self.individuos[indices_mutan_ind[i]].genotipo
                        nuevo_ind = list(nuevo_ind)
                        try:
                            bit = nuevo_ind[indices_mutan_gen[k]]
                        except IndexError:
                            print(len(indices_mutan_gen), k)
                        if bit == '0':
                            try:
                                nuevo_ind[indices_mutan_gen[k]] = '1'
                                nuevo_ind = "".join(nuevo_ind)
                            except IndexError:
                                print(k)
                        else:
                            try:
                                nuevo_ind[indices_mutan_gen[k]] = '0'
                                nuevo_ind = "".join(nuevo_ind)
                            except IndexError:
                                print(k)
                self.individuos[indices_mutan_ind[i]].set_genotipo(nuevo_ind)

        while contador < tamanio:
            if self.individuos[contador].i == 20:
                genotipo = self.individuos[contador].genotipo
                id = self.individuos[contador].id
                self.individuos.pop(contador)
                self.crear_individuo(genotipo, id)
                contador = 0
            else:
                contador += 1

        for k in self.individuos:
            print(f" {k.id}\t{k.genotipo}\t{k.i}\t{k.fenotipo}\t{k.aptitud}")

    def poda(self):
        tam_poda = len(self.individuos) - self.tam_pob_maxima
        print("\n")
        self.individuos.sort(key=lambda x: x.aptitud, reverse=False)
        for k in self.individuos:
            print(f" {k.id}\t{k.genotipo}\t{k.i}\t{k.fenotipo}\t{k.aptitud}")

        self.mejores_individuos.append(self.individuos[len(self.individuos) - 1])
        self.peores_individuos.append(self.individuos[0])
        print("\n")
        if len(self.individuos) > self.tam_pob_maxima:
            for i in range(tam_poda):
                self.individuos_poda.append(self.individuos.pop(0))

        for k in self.individuos:
            print(f" {k.id}\t{k.genotipo}\t{k.i}\t{k.fenotipo}\t{k.aptitud}")
        print('\n')

    def grafica(self):
        aptitud = []
        list_epocas = []
        mejor_individuo = self.individuos[len(self.individuos) - 1]
        for i in range(self.epocas):
            list_epocas.append(i + 1)
        for k in self.mejores_individuos:
            aptitud.append(k.aptitud)
            print(f" {k.id}\t{k.genotipo}\t{k.i}\t{k.fenotipo}\t{k.aptitud}")

        fig, ax = plt.subplots()
        plt.text(1, aptitud[len(aptitud) - 1], f"Aptitud del mejor individuo {mejor_individuo.aptitud}")
        ax.plot(list_epocas, aptitud)
        plt.show()
    
    def grafica2(self):
        list_y=[]
        list_x=[]
        puntosX=[]
        puntosY=[]
        for x in range(10):
            list_x.append(x+1)
        
        for y in list_x:
            list_y.append(f(y))

        # print(list_y)
        fig,ax=plt.subplots()
        for i in self.individuos:
            puntosX.append(i.aptitud)
            puntosY.append(i.fenotipo)
        ax.scatter([2,4,6,8,10],puntosY)
        ax.plot(list_x,list_y)
        plt.show()
