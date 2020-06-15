import configuracio
import estats

class Agrupador:
    tempsServei = 2
    instancia=1
    state=0
    cnt_aliments = 0

    def __init__(self,instancia):
        self.instancia=instancia
        self.state=estats.AgrupadorBuit
        self.cnt_aliments = 0

    def isFree(self):
        return self.state == estats.AgrupadorBuit

    def Free(self):
        self.state=estats.AgrupadorBuit

    def nextEndService(self):
        self.state=estats.AgrupadorProcessant
        return configuracio.temps_processament_agrupador

    def name(self):
        return "Agrupador"+str(self.instancia)

    def presentacio(self):
        txt = "L'" + self.name() + " agrupa aliments de tipus "
        if self.instancia == 1:
            txt += "Pasta"
        elif self.instancia == 2:
            txt += "Arros"
        else:
            txt += "Llegums"
        return txt

    def iniciServei(self,temps):
        return "   " + self.name() + " inicia processament"

    def augmentar_cnt_aliments(self):
        self.cnt_aliments += 1
        self.cnt_aliments = self.cnt_aliments % configuracio.capacitat_capsa
        return self.cnt_aliments == 0

    def changeState(self, state):
        self.state = state

    def get_cnt_aliments(self):
        return self.cnt_aliments