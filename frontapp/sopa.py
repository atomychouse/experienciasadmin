

from random import randint


class Sopa:

    def __init__(self,words):
        self.words = words
        self.tabla = []
        self.maxl = 10

        for x in range(0,10):
            columna = []
            for x in range(0,10):
                columna.append('')
            self.tabla.append(columna)   


    def initcords(self):
        self.x,self.y = randint(0,9),randint(0,9)


    def valida(self,rango):
        for x in rango:
            
            if len(self.tabla[self.y][x])==0:
                print 'ok'
            else:
                print self.tabla[self.y][x]


    def getTable(self):
        for t in self.tabla:
            print t

    def Goright(self):
        print 'derecha'
        counter = 0
        self.valida(range(0,self.flen))



    def Goleft(self):
        print 'izquierda'
        counter = 0
        rango = []
        for x in range(0,self.flen):
            rango.append(self.x - counter)
            counter+=1
        self.valida(rango)
        



    def readwords(self,word=None):
        self.word = word
        self.initcords()
        self.options = []
        if word:
            self.flen = len(word)
            linex = self.maxl-self.x
            liney = self.maxl-self.y
            if linex > self.flen-1:
                hop = 'Goright'
            else:
                hop = 'Goleft'

            if liney > self.flen:
                vop = 'Godown'
            else:
                vop = 'Goup'

        func = getattr(self,hop,None)
        func()

words = ['telcel','checo','copa','llantas']
sopa = Sopa(words=words)

sopa.readwords(word=words[1])
sopa.readwords(word=words[0])

'''

words = ['telcel','checo','copa','llantas']

tabla = []

for x in range(0,10):
    columna = range(0,10)
    tabla.append(columna)    

for waplica in words:
    
    f = waplica
    flen = len(f)
    maxl = 10
    currl = maxl - flen

    x,y = randint(0,10),randint(0,10)

    print 'inicia en ',(x,y),' y la palabra es',f

    linex = maxl - x
    liney = maxl - y
    counter = 0


    if linex > flen-1:
        print 'r'
        while counter < flen:    
            wx = x + counter
            print x,counter,wx
            
            #if type(tabla[y][wx]):
            #    tabla[y][wx] = f[counter]
                counter +=1
    else:
        print 'l'
        while counter < flen:
            wx = x - counter
            print x,counter,x,counter,wx
            #tabla[y][wx] = f[counter]
            counter +=1


for t in tabla:
    print t 

'''