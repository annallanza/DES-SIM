import matplotlib.pyplot as plt
from generador import Generador
from agrupador import Agrupador
from esdeveniment import Esdeveniment
import estats

class Motor:
    """
    Motor de simulacio, s'encarrega de crear els primers esdeveniments que encadenaren la resta.
    """
    # Esdeveniments no processats
    esdevenimentsPendents = None

    # Temps actual de simulacio
    currentTime = 0

    #Elements del sistema
    generador=None
    agrupador1=None
    agrupador2=None
    agrupador3=None
    area_espera1=0
    area_espera2=0
    area_espera3=0

    #Traça dels esdeveniments del sistema
    traza=[]

    #Estadistics de l'execució del sistema
    cnt_capses = [0,0,0]
    mitjana_temps_omplir_capsa = [0.0, 0.0, 0.0]
    temps_inici_capsa = [0,0,0]

    def __init__(self):
        """
        Constructora per defecte
        """
        self.generador= Generador()
        self.area_espera1=0
        self.area_espera2=0
        self.area_espera3=0
        self.agrupador1 = Agrupador(1)
        self.traza.append(self.agrupador1.presentacio())
        self.agrupador2 = Agrupador(2)
        self.traza.append(self.agrupador2.presentacio())
        self.agrupador3 = Agrupador(3)
        self.traza.append(self.agrupador3.presentacio())
        self.traza.append("")
        self.esdevenimentsPendents = []
        self.currentTime = 0
        self.cnt_capses = [0,0,0]
        self.mitjana_temps_omplir_capsa = [0.0, 0.0, 0.0]
        self.temps_inici_capsa = [0,0,0]

        self.inicialitzaLlistaEsdeveniments()

    def inicialitzaLlistaEsdeveniments(self):
        self.generador.changeState()
        esd=Esdeveniment(self.generador.nextArrival(), estats.AlimentRecaptat, self.generador)
        self.esdevenimentsPendents.append(esd)
        self.traza.append("0")
        self.traza.append(esd.programat())

    # Arranca la simulacio
    def run(self):
        continuar=True #TODO mirar de treure-ho
        while len(self.esdevenimentsPendents) and continuar:
            esdeveniment = self.esdevenimentsPendents.pop(0)
            continuar=self.tractarEsdeveniment(esdeveniment)

        self.generador.changeState()
        self.generar_traça()
        self.generar_estadistics()
        self.mostrar_estadistics()

    # Controla el temps de simulacio i gestiona l'execucio de la rutina associada a cada esdeveniment
    def tractarEsdeveniment(self, esdeveniment):
        self.currentTime = esdeveniment.timestamp

        self.traza.append(esdeveniment.executat())
        if esdeveniment.tipus == estats.AlimentRecaptat:
            nextTime=self.generador.nextArrival()
            if nextTime >= 0:
                self.programar_esdeveniment_arribada(nextTime)

            if esdeveniment.tipus_aliment == 1:
                if self.agrupador1.isFree():
                    nextTime=self.agrupador1.nextEndService()
                    nextTime+=self.currentTime
                    self.traza.append(self.agrupador1.iniciServei(self.currentTime))
                    esd2=Esdeveniment(nextTime, estats.AlimentProcessat, self.agrupador1)
                    esd2.set_tipus_aliment(1)
                    self.agrupador1.changeState(estats.AgrupadorProcessant)
                    self.esdevenimentsPendents.append(esd2)
                    if self.agrupador1.get_cnt_aliments() == 0:
                        self.temps_inici_capsa[0] = self.currentTime
                    self.traza.append(esd2.programat())
                else:
                    self.area_espera1+=1
                    self.traza.append(esdeveniment.encuar(self.area_espera1))

            elif esdeveniment.tipus_aliment == 2:
                if self.agrupador2.isFree():
                    nextTime=self.agrupador2.nextEndService()
                    nextTime+=self.currentTime
                    self.traza.append(self.agrupador2.iniciServei(self.currentTime))
                    esd2=Esdeveniment(nextTime, estats.AlimentProcessat, self.agrupador2)
                    esd2.set_tipus_aliment(2)
                    self.agrupador2.changeState(estats.AgrupadorProcessant)
                    self.esdevenimentsPendents.append(esd2)
                    if self.agrupador2.get_cnt_aliments() == 0:
                        self.temps_inici_capsa[1] = self.currentTime
                    self.traza.append(esd2.programat())
                else:
                    self.area_espera2+=1
                    self.traza.append(esdeveniment.encuar(self.area_espera2))

            else:
                if self.agrupador3.isFree():
                    nextTime=self.agrupador3.nextEndService()
                    nextTime+=self.currentTime
                    self.traza.append(self.agrupador3.iniciServei(self.currentTime))
                    esd2=Esdeveniment(nextTime, estats.AlimentProcessat, self.agrupador3)
                    esd2.set_tipus_aliment(3)
                    self.agrupador3.changeState(estats.AgrupadorProcessant)
                    self.esdevenimentsPendents.append(esd2)
                    if self.agrupador3.get_cnt_aliments() == 0:
                        self.temps_inici_capsa[2] = self.currentTime
                    self.traza.append(esd2.programat())
                else:
                    self.area_espera3+=1
                    self.traza.append(esdeveniment.encuar(self.area_espera3))

        if esdeveniment.tipus == estats.AlimentProcessat:
            if esdeveniment.tipus_aliment == 1:
                self.tractar_esdeveniment_alimentProcessat(self.agrupador1, esdeveniment)
            elif esdeveniment.tipus_aliment == 2:
                self.tractar_esdeveniment_alimentProcessat(self.agrupador2, esdeveniment)
            else:
                self.tractar_esdeveniment_alimentProcessat(self.agrupador3, esdeveniment)

        self.esdevenimentsPendents.sort()

        return True

    def programar_esdeveniment_arribada(self, nextTime):
        nextTime += self.currentTime
        esd = Esdeveniment(nextTime, estats.AlimentRecaptat, self.generador)
        self.esdevenimentsPendents.append(esd)
        self.traza.append(esd.programat())

    def tractar_esdeveniment_alimentProcessat(self, agrupador, esdeveniment):
        if agrupador.augmentar_cnt_aliments():
            esd2=Esdeveniment(self.currentTime, estats.AlimentFinalitzat, agrupador)
            esd2.decr_cnt()
            self.traza.append(esd2.finalitzat())
            if agrupador.name() == "Agrupador1":
                self.actualitzar_estadistics(0)
            elif agrupador.name() == "Agrupador2":
                self.actualitzar_estadistics(1)
            else:
                self.actualitzar_estadistics(2)

        esdeveniment.element.Free()
        if esdeveniment.tipus_aliment == 1 and self.area_espera1>0:
            self.area_espera1-=1
            nextTime=esdeveniment.element.nextEndService()
            nextTime+=self.currentTime
            self.traza.append(esdeveniment.element.iniciServei(self.currentTime))
            esd3=Esdeveniment(nextTime, estats.AlimentProcessat, esdeveniment.element)
            esd3.set_tipus_aliment(1)
            self.esdevenimentsPendents.append(esd3)
            if self.agrupador1.get_cnt_aliments() == 0:
                self.temps_inici_capsa[0] = self.currentTime
            self.traza.append(esd3.programat())
        elif esdeveniment.tipus_aliment == 2 and self.area_espera2>0:
            self.area_espera2-=1
            nextTime=esdeveniment.element.nextEndService()
            nextTime+=self.currentTime
            self.traza.append(esdeveniment.element.iniciServei(self.currentTime))
            esd3=Esdeveniment(nextTime, estats.AlimentProcessat, esdeveniment.element)
            esd3.set_tipus_aliment(2)
            self.esdevenimentsPendents.append(esd3)
            if self.agrupador2.get_cnt_aliments() == 0:
                self.temps_inici_capsa[1] = self.currentTime
            self.traza.append(esd3.programat())
        elif esdeveniment.tipus_aliment == 3 and self.area_espera3>0:
            self.area_espera3-=1
            nextTime=esdeveniment.element.nextEndService()
            nextTime+=self.currentTime
            self.traza.append(esdeveniment.element.iniciServei(self.currentTime))
            esd3=Esdeveniment(nextTime, estats.AlimentProcessat, esdeveniment.element)
            esd3.set_tipus_aliment(3)
            self.esdevenimentsPendents.append(esd3)
            if self.agrupador3.get_cnt_aliments() == 0:
                self.temps_inici_capsa[2] = self.currentTime
            self.traza.append(esd3.programat())

    def actualitzar_estadistics(self, tipus):
        self.cnt_capses[tipus] += 1
        if self.cnt_capses[tipus] == 1:
            mitjana = (self.currentTime - self.temps_inici_capsa[tipus]) / self.cnt_capses[tipus]
        elif self.cnt_capses[tipus] == 2:
            mitjana = (self.mitjana_temps_omplir_capsa[tipus] + self.currentTime - self.temps_inici_capsa[tipus]) / self.cnt_capses[tipus]
        else:
            mitjana = (self.mitjana_temps_omplir_capsa[tipus] * (self.cnt_capses[tipus] - 1) + (
                        self.currentTime - self.temps_inici_capsa[tipus])) / self.cnt_capses[tipus]
        self.mitjana_temps_omplir_capsa[tipus] = mitjana

    def generar_estadistics(self):
        f = open("estadistics.txt", "w")
        f.write("Capses generades per l'Agrupador1: " + str(self.cnt_capses[0]) + "\n")
        f.write("Capses generades per l'Agrupador2: " + str(self.cnt_capses[1]) + "\n")
        f.write("Capses generades per l'Agrupador3: " + str(self.cnt_capses[2]) + "\n")
        f.write("\n")
        f.write("Mitjana del temps en omplir una capsa de l'Agrupador1: " + str(round(self.mitjana_temps_omplir_capsa[0], 2)) + "\n")
        f.write("Mitjana del temps en omplir una capsa de l'Agrupador2: " + str(round(self.mitjana_temps_omplir_capsa[1], 2)) + "\n")
        f.write("Mitjana del temps en omplir una capsa de l'Agrupador3: " + str(round(self.mitjana_temps_omplir_capsa[2], 2)) + "\n")
        f.close()

    def mostrar_estadistics(self):
        plt.figure(figsize=(5, 7))

        plt.subplot(2, 1, 1)
        plt.xlabel("Tipus d'aliment")
        plt.ylabel("Numero capses")
        noms1 = ['Pasta', 'Arros', 'Llegums']
        plt.bar(noms1, self.cnt_capses, width=0.5)

        plt.subplot(2, 1, 2)
        plt.xlabel("Tipus d'aliment")
        plt.ylabel("Temps mitjà en omplir")
        noms2 = ['Pasta', 'Arros', 'Llegums']
        plt.bar(noms2, self.mitjana_temps_omplir_capsa, width=0.5)
        plt.show()

    def generar_traça(self):
        f = open("sortida.txt", "w")
        for i in range(0,len(self.traza)):
            f.write(self.traza[i] + "\n")
        f.close()