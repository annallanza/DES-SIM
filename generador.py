from scipy.stats import expon
import configuracio
import estats

class Generador:

    state = 0
    index=-1
    tempsArribada = []

    def __init__(self):
        self.state=estats.GeneradorInactiu
        self.index=-1
        self.tempsArribada = expon.rvs(size=configuracio.aliments_a_processar, loc=configuracio.loc_temps_entre_arribades, scale=configuracio.scale_temps_entre_arribades)
        for i in range(len(self.tempsArribada)):
            while self.tempsArribada[i] < 0:
                self.tempsArribada[i] = expon.rvs(size=1, loc=configuracio.loc_temps_entre_arribades, scale=configuracio.scale_temps_entre_arribades)
            self.tempsArribada[i] = round(self.tempsArribada[i], 2)

    def nextArrival(self):
        self.index+=1
        if self.index == len(self.tempsArribada):
            return -1
        return self.tempsArribada[self.index]

    def name(self):
        return "Generador"

    def changeState(self):
        self.state = (self.state + 1) % 2