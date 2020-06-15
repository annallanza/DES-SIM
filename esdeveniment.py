import numpy
import configuracio


cnt_tipus_aliment = 0
llista_tipus_aliments = numpy.random.randint(1, 4, configuracio.aliments_a_processar + 1)
print("Llista tipus aliments: " + str(llista_tipus_aliments))

class Esdeveniment:

    tipus=0 #estat esdeveniment
    tipus_aliment = 1
    timestamp=0
    element=None

    def __init__(self,timestamp,tipus,element):
        self.timestamp=timestamp
        self.tipus=tipus

        global cnt_tipus_aliment, llista_tipus_aliments
        self.tipus_aliment = llista_tipus_aliments[cnt_tipus_aliment]
        cnt_tipus_aliment += 1

        self.element=element

    def decr_cnt(self):
        global cnt_tipus_aliment
        cnt_tipus_aliment -= 1

    def set_tipus_aliment(self,tipus_aliment):
        self.tipus_aliment = tipus_aliment
        self.decr_cnt()

    # Criteri d'ordenacio, necessari per a simular amb coherencia temporal
    def __lt__(self, other):
        return self.timestamp < other.timestamp

    def __str__(self):
        tip=["AlimentDonat","AlimentProcessat", "AlimentFinalitzat"]
        return str(round(self.timestamp, 2))+" "+tip[self.tipus]+" "+self.element.name()

    def executat(self):
        tip=["AlimentDonat","AlimentProcessat", "AlimentFinalitzat"]
        nom=self.element.name()
        txt = str(round(self.timestamp, 2)) + "\n" + "   "
        if nom == "Generador":
            txt += "El "
        else:
            txt += "L'"
        txt += nom + " executa un esdeveniment " + tip[self.tipus]
        return txt

    def encuar(self,cua):
        nom=self.element.name()
        txt= "  " + " S'afegeix un esdeveniment a la cua de l'" + nom + ". La cua passa a tenir mida " + str(cua)
        return txt

    def programat(self):
        tip=["AlimentDonat","AlimentProcessat", "AlimentFinalitzat"]
        nom=self.element.name()
        if nom == "Generador":
            txt = "   " + "El "
        else:
            txt = "   " + "L'"
        txt += nom + " programa un esdeveniment " + tip[self.tipus]+" per al temps "+str(round(self.timestamp, 2))
        return txt

    def finalitzat(self):
        tip=["AlimentDonat","AlimentProcessat", "AlimentFinalitzat"]
        nom=self.element.name()
        txt="   " + tip[self.tipus]+" pel " + nom + ". S'ha omplert una capsa de tipus "
        if self.tipus_aliment == 1:
            txt += "Pasta"
        elif self.tipus_aliment == 2:
            txt += "Arros"
        else:
            txt += "Llegums"
        return txt