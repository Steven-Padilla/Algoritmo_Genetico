class Individuo():

    def __init__(self, id, genotipo, i, fenotipo, aptitud):
        self.id = id
        self.genotipo = genotipo
        self.i = i
        self.fenotipo = fenotipo
        self.aptitud = aptitud

    def set_genotipo(self, nuevo_genotipo):
        self.genotipo = nuevo_genotipo
