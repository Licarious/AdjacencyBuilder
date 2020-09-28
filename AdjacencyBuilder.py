from PIL import Image
from os import path
import time
import glob

game = "IR" #CK3 or IR

class ProvinceDefinition:
    id = 0
    red = 0
    green = 0
    blue = 0
    name = ""
    other_info = ""
    lastKnownY = -1
class PotentialAdjacency:
    fromID = 0
    toID = 0
    overID = 0
    x1=-1
    x2=-1
    y1=-1
    y2=-1
    

riverList = []
tmpRiverList = []
riverProvList = []
provList = []
provColorList = []
tupleList = []
adjList = []
fullProvList = []
fullProvColorList = []

tmpAdjList = []
objAdjList = []
directAdj = []

baronlyList = []
barrolyNameList = []

riverArray = []
riverBorderArray = []
riverBoldBorderArray = []

mapDefinition = open("Input/definition.csv")
defaultMap = open("Input/default.map")
provMap = Image.open("Input/provinces.png")
borderIDList = []
total=0

def readProvinceDeff():
    for province in mapDefinition:
        if province.strip().startswith("#"):
            pass
        else:
            tmpline = province.strip().split(';')
            try:
                province = ProvinceDefinition()
                province.red = int(tmpline[1])
                province.id = int(tmpline[0].lstrip("#"))
                province.green = int(tmpline[2])
                province.blue = int(tmpline[3])
                province.name = tmpline[4]
                provList.append(province)
            except:
                pass
            try:
                province = ProvinceDefinition()
                province.red = int(tmpline[1])
                province.id = int(tmpline[0].lstrip("#"))
                province.green = int(tmpline[2])
                province.blue = int(tmpline[3])
                province.name = tmpline[4]
                fullProvList.append(province)
                fullProvColorList.append((province.red,province.green,province.blue))
            except:
                pass
    pass
def getRangeList(line, tmpList):
    if "RANGE" in line:
        x1=0
        x2=0
        #print(line)
        words = line.split(" ")
        for word in words:
            if "#" in word:
                break
            else:
                try:
                    if x1 == 0:
                        x1 = int(word)
                    elif x2 == 0:
                        x2 = int(word)
                except:
                    pass
        for i in range(x1,x2+1):
            tmpList.append(i)
        #print("%s,%s"%(x1,x2))
    elif "LIST" in line:
        words = line.split(" ")
        for word in words:
            if "#" in word:
                break
            else:
                try:
                    tmpList.append(int(word))
                except:
                    pass
    pass
def getRiverProvinces():
    for line in defaultMap:
        if line.strip().startswith("#"):
            pass
        elif line.strip().startswith("river_provinces"):
            getRangeList(line, riverList)
    pass  
def drawMat(riverProvList,name):
    xRange= range(0,provMap.size[0],1)
    yRange= range(0,provMap.size[1],1)
    drawReader = provMap.load()
    drawingMap = Image.open("Input/provinces.png")
    drawingMap.putalpha(0)
    riverMat = drawingMap.load()
    z=0
    dis = 5

    tupleList = []
    lastY = []
    for prov in riverProvList:
        tupleList.append((prov.red,prov.green,prov.blue))
        lastY.append(-1)

    print("Drawing Maps:")
    tmpTotal = len(tupleList)
    count = 0

    for y in yRange:
        if y%128 ==0:
            #print("%i%%"%((y*100)/provMap.size[1]))
            for i, prov in enumerate(lastY):
                if prov>-1 and prov<y-(provMap.size[1]/40):
                    #print(tupleList[i])
                    del lastY[i]
                    del tupleList[i]
                    i-=1
                    count+=1
            if tmpTotal>0 and count>0:
                #print(count)
                print("%f%%"%((count*1000/tmpTotal)/10))
            if tupleList==0:
                break
        for x in xRange:
            if drawReader[x,y] in tupleList:
                riverMat[x,y] = (0,0,0,255)
                lastY[tupleList.index(drawReader[x,y])] = y
    drawingMap.save("Output/%s.png"%name)
def drawBorderMat(name):
    xRange= range(0,provMap.size[0],1)
    yRange= range(0,provMap.size[1],1)
    if "River" in name:
        tmpDrawingMap = Image.open("Output/RiverMat.png")
    else:
        tmpDrawingMap = Image.open("Output/SeaMat.png")
    drawReader = tmpDrawingMap.load()
    drawingBorderMap = Image.open("Input/provinces.png")
    drawingBorderMap.putalpha(0)
    riverBorderMat = drawingBorderMap.load()
    for y in yRange:
        for x in xRange:
            if drawReader[x,y] == (0,0,0,255):
                #print("%s,%s"%(x,y))
                if y>0:
                    if not drawReader[x,y-1] == (0,0,0,255):
                        riverBorderMat[x,y-1] = (0,0,0,255)
                if y<provMap.size[1]-1:
                    if not drawReader[x,y+1] == (0,0,0,255):
                        riverBorderMat[x,y+1] = (0,0,0,255)
                if x>0:
                    if not drawReader[x-1,y] == (0,0,0,255):
                        riverBorderMat[x-1,y] = (0,0,0,255)
                if x<provMap.size[0]-1:
                    if not drawReader[x+1,y] == (0,0,0,255):
                        riverBorderMat[x+1,y] = (0,0,0,255)
                #print("%s - %i,%i"%(prov.name,x,y))
    drawingBorderMap.save("Output/%s.png"%name)
def drawBoldBorderMat(name):
    xRange= range(0,provMap.size[0],1)
    yRange= range(0,provMap.size[1],1)
    if "River" in name:
        tmpDrawingMap = Image.open("Output/RiverMat.png")
    else:
        tmpDrawingMap = Image.open("Output/SeaMat.png")
    drawReader = tmpDrawingMap.load()
    drawingBorderMap = Image.open("Input/provinces.png")
    drawingBorderMap.putalpha(0)
    riverBorderMat = drawingBorderMap.load()
    for y in yRange:
        for x in xRange:
            if drawReader[x,y] == (0,0,0,255):
                #print("%s,%s"%(x,y))
                for i in range(0,3):
                    if y-i>0:
                        if not drawReader[x,y-i] == (0,0,0,255):
                            riverBorderMat[x,y-i] = (0,0,0,255)
                    if y+i<provMap.size[1]-1:
                        if not drawReader[x,y+i] == (0,0,0,255):
                            riverBorderMat[x,y+i] = (0,0,0,255)
                    if x-i>0:
                        if not drawReader[x-i,y] == (0,0,0,255):
                            riverBorderMat[x-i,y] = (0,0,0,255)
                    if x+i<provMap.size[0]-1:
                        if not drawReader[x+i,y] == (0,0,0,255):
                            riverBorderMat[x+i,y] = (0,0,0,255)
                    #print("%s - %i,%i"%(prov.name,x,y))
                if y>0 and x>0:
                    if not drawReader[x-1,y-1] == (0,0,0,255):
                        riverBorderMat[x-1,y-1] = (0,0,0,255)
                if y<provMap.size[1]-1 and x>0:
                    if not drawReader[x-1,y+1] == (0,0,0,255):
                        riverBorderMat[x-1,y+1] = (0,0,0,255)
                if y<provMap.size[1]-1 and x<provMap.size[0]-1:
                    if not drawReader[x+1,y+1] == (0,0,0,255):
                        riverBorderMat[x+1,y+1] = (0,0,0,255)
                if y>0 and x<provMap.size[0]-1:
                    if not drawReader[x+1,y-1] == (0,0,0,255):
                        riverBorderMat[x+1,y-1] = (0,0,0,255)
    drawingBorderMap.save("Output/%s.png"%name)


def directConections(x,y):
    #print("%i,%i"%(x,y))
    if x+1 < len(riverArray[y]):
        tmpTuple = (fullProvList[fullProvColorList.index(provMap.getpixel((x,y)))].id, fullProvList[fullProvColorList.index(provMap.getpixel((x+1,y)))].id)
        if tmpTuple[0] == tmpTuple[1]:
            pass
        else:
            tmpTuple2 = (tmpTuple[1],tmpTuple[0])
            if tmpTuple in directAdj or tmpTuple2 in directAdj:
                pass
            else:
                directAdj.append(tmpTuple)
    if y+1 < len(riverArray):
        tmpTuple = (fullProvList[fullProvColorList.index(provMap.getpixel((x,y)))].id, fullProvList[fullProvColorList.index(provMap.getpixel((x,y+1)))].id)
        if tmpTuple[0] == tmpTuple[1]:
            pass
        else:
            tmpTuple2 = (tmpTuple[1],tmpTuple[0])
            if tmpTuple in directAdj or tmpTuple2 in directAdj:
                pass
            else:
                directAdj.append(tmpTuple)
    if y-1 >= 0:
        tmpTuple = (fullProvList[fullProvColorList.index(provMap.getpixel((x,y)))].id, fullProvList[fullProvColorList.index(provMap.getpixel((x,y-1)))].id)
        if tmpTuple[0] == tmpTuple[1]:
            pass
        else:
            tmpTuple2 = (tmpTuple[1],tmpTuple[0])
            if tmpTuple in directAdj or tmpTuple2 in directAdj:
                pass
            else:
                directAdj.append(tmpTuple)
    if x-1 >= 0:
        tmpTuple = (fullProvList[fullProvColorList.index(provMap.getpixel((x,y)))].id, fullProvList[fullProvColorList.index(provMap.getpixel((x-1,y)))].id)
        if tmpTuple[0] == tmpTuple[1]:
            pass
        else:
            tmpTuple2 = (tmpTuple[1],tmpTuple[0])
            if tmpTuple in directAdj or tmpTuple2 in directAdj:
                pass
            else:
                directAdj.append(tmpTuple)
                
    pass

def radialVector2(x,y):
    lenght = 8   
    if riverArray[y][x+1] == 1:
        for i in range(2,lenght):
            if x+i > len(riverArray[y]):
                break
            if riverBorderArray[y][x+i] == 1:
                tmpTuple = (fullProvList[fullProvColorList.index(provMap.getpixel((x,y)))].id, fullProvList[fullProvColorList.index(provMap.getpixel((x+i,y)))].id)
                if tmpTuple[0] == tmpTuple[1]:
                    pass
                else:
                    tmpTuple2 = (tmpTuple[1],tmpTuple[0])
                    if tmpTuple in tmpAdjList or tmpTuple2 in tmpAdjList or tmpTuple in directAdj or tmpTuple2 in directAdj:
                        pass
                    else:
                        tmpAdjList.append(tmpTuple)
                        print("%s ~ %s"%(fullProvList[fullProvColorList.index(provMap.getpixel((x,y)))].name,fullProvList[fullProvColorList.index(provMap.getpixel((x+i,y)))].name))
                        try:
                            adj = PotentialAdjacency()
                            adj.fromID = tmpTuple[0]
                            adj.toID = tmpTuple[1]
                            adj.overID = fullProvList[fullProvColorList.index(provMap.getpixel((x+1,y)))].id
                            objAdjList.append(adj)
                        except:
                            pass
                        break
        pass
    if riverArray[y+1][x+1] == 1:
        for i in range(2,lenght):
            if x+i > len(riverArray[y]) or y+i > len(riverArray):
                break
            if riverBorderArray[y+i][x+i] == 1:
                tmpTuple = (fullProvList[fullProvColorList.index(provMap.getpixel((x,y)))].id, fullProvList[fullProvColorList.index(provMap.getpixel((x+i,y+i)))].id)
                if tmpTuple[0] == tmpTuple[1]:
                    pass
                else:
                    tmpTuple2 = (tmpTuple[1],tmpTuple[0])
                    if tmpTuple in tmpAdjList or tmpTuple2 in tmpAdjList or tmpTuple in directAdj or tmpTuple2 in directAdj:
                        pass
                    else:
                        tmpAdjList.append(tmpTuple)
                        print("%s ~ %s"%(fullProvList[fullProvColorList.index(provMap.getpixel((x,y)))].name,fullProvList[fullProvColorList.index(provMap.getpixel((x+i,y+i)))].name))
                        try:
                            adj = PotentialAdjacency()
                            adj.fromID = tmpTuple[0]
                            adj.toID = tmpTuple[1]
                            adj.overID = fullProvList[fullProvColorList.index(provMap.getpixel((x+1,y+1)))].id
                            objAdjList.append(adj)
                        except:
                            pass
                        break
        pass
    if riverArray[y+1][x] == 1:
        for i in range(2,lenght):
            if y+i > len(riverArray):
                break
            if riverBorderArray[y+i][x] == 1:
                tmpTuple = (fullProvList[fullProvColorList.index(provMap.getpixel((x,y)))].id, fullProvList[fullProvColorList.index(provMap.getpixel((x,y+i)))].id)
                if tmpTuple[0] == tmpTuple[1]:
                    pass
                else:
                    tmpTuple2 = (tmpTuple[1],tmpTuple[0])
                    if tmpTuple in tmpAdjList or tmpTuple2 in tmpAdjList or tmpTuple in directAdj or tmpTuple2 in directAdj:
                        pass
                    else:
                        tmpAdjList.append(tmpTuple)
                        print("%s ~ %s"%(fullProvList[fullProvColorList.index(provMap.getpixel((x,y)))].name,fullProvList[fullProvColorList.index(provMap.getpixel((x,y+i)))].name))
                        try:
                            adj = PotentialAdjacency()
                            adj.fromID = tmpTuple[0]
                            adj.toID = tmpTuple[1]
                            adj.overID = fullProvList[fullProvColorList.index(provMap.getpixel((x,y+1)))].id
                            objAdjList.append(adj)
                        except:
                            pass
                        break
        pass
    if riverArray[y-1][x+1] == 1:
        for i in range(2,lenght):
            if x+i > len(riverArray[y]) or y-i <0:
                break
            if riverBorderArray[y-i][x+i] == 1:
                tmpTuple = (fullProvList[fullProvColorList.index(provMap.getpixel((x,y)))].id, fullProvList[fullProvColorList.index(provMap.getpixel((x+i,y-i)))].id)
                if tmpTuple[0] == tmpTuple[1]:
                    pass
                else:
                    tmpTuple2 = (tmpTuple[1],tmpTuple[0])
                    if tmpTuple in tmpAdjList or tmpTuple2 in tmpAdjList or tmpTuple in directAdj or tmpTuple2 in directAdj:
                        pass
                    else:
                        tmpAdjList.append(tmpTuple)
                        print("%s ~ %s"%(fullProvList[fullProvColorList.index(provMap.getpixel((x,y)))].name,fullProvList[fullProvColorList.index(provMap.getpixel((x+i,y-i)))].name))
                        try:
                            adj = PotentialAdjacency()
                            adj.fromID = tmpTuple[0]
                            adj.toID = tmpTuple[1]
                            adj.overID = fullProvList[fullProvColorList.index(provMap.getpixel((x+1,y-1)))].id
                            objAdjList.append(adj)
                        except:
                            pass
                        break
        pass

    

    pass
def radialChecker2():
    xRange= range(0,provMap.size[0],1)
    yRange= range(0,provMap.size[1],1)
    borderMat = Image.open("Output/RiverBorderMat.png")
    riverBorderMat = borderMat.load()
    rMat = Image.open("Output/RiverMat.png")
    riverMat = rMat.load()
    bbMat = Image.open("Output/RiverBoldBorderMat.png")
    boldMat = bbMat.load()
    print("Gathering River Data:")
    for y in yRange:
        tmpBorderArray = []
        tmpRiverArray = []
        tmpBoldArray = []
        if y%512 ==0:
            print("\t%i%%"%((y*100)/provMap.size[1]))
            #print()
        for x in xRange:
            if riverBorderMat[x,y] == (0,0,0,255):
                #radialVector(x,y)
                tmpBorderArray.append(1)
            else:
                tmpBorderArray.append(0)
            if riverMat[x,y] == (0,0,0,255):
                #radialVector(x,y)
                tmpRiverArray.append(1)
            else:
                tmpRiverArray.append(0)
            if boldMat[x,y] == (0,0,0,255):
                #radialVector(x,y)
                tmpBoldArray.append(1)
            else:
                tmpBoldArray.append(0)
        riverBorderArray.append(tmpBorderArray)
        riverArray.append(tmpRiverArray)
        riverBoldBorderArray.append(tmpBoldArray)
        #sum1 = sum(tmpBorderArray)
        
    count = 0
    count2 = 0
    print("Getting Direct Conections:")
    for y in range(0,len(riverBoldBorderArray)):
        
        if y%512 ==0:
            print("\t%i%%"%((y*100)/provMap.size[1]))
        if sum(riverBoldBorderArray[y]) >0:
            #print(sum(riverBorderArray[y]))
            count +=1
            for x in range(0,len(riverBoldBorderArray[y])):
                if riverBoldBorderArray[y][x] == 1:
                    directConections(x,y)
                    count2 +=1

    print("Generating Adjacencies:")
    for y in range(0,len(riverBorderArray)):
        
        if y%512 ==0:
            print("\t%i%%"%((y*100)/provMap.size[1]))
        if sum(riverBorderArray[y]) >0:
            #print(sum(riverBorderArray[y]))
            count +=1
            for x in range(0,len(riverBorderArray[y])):
                if riverBorderArray[y][x] == 1:
                    radialVector2(x,y)
                    count2 +=1
    #print(count)
    #print(count2)   
    pass

def getBaronies():
    landedTitles = open("Input/00_landed_titles.txt",'r',encoding='utf-8',errors='ignore')
    indintation = 0
    tmpBar= ""
    for line in landedTitles:
        if indintation == 4:
            if line.strip().startswith("b_"):
                tmpBar=line.strip().split(" ")[0]
        if indintation == 5:
            if line.strip().startswith("province"):
                for word in line.strip().split(" "):
                    try:
                        tmpID = int(word)
                        baronlyList.append(tmpID)
                        barrolyNameList.append(tmpBar)
                    except:
                        pass
        if "{" in line or "}" in line:
            #print("l: "+line)
            for element in list(line.strip()):
                if "{" in element:
                    indintation +=1
                    #print("s: "+element)
                elif "}" in element:
                    indintation -=1
                    #print("e: "+element)
                elif "#" in element:
                    #print("c: "+element)
                    break
    pass
def getSettlement():
    provFiles=glob.glob("Input/provinces/*.txt")
    for file in provFiles:
        landedTitles = open(file,'r',encoding='utf-8',errors='ignore')
        #print(file)
        indintation = 0
        tmpBar= ""
        tmpID = -1
        checker = 0
        for line in landedTitles:
            if indintation == 0:
                if "=" in line:
                    word = line.strip().strip("\ufeff").split("=")
                    try:
                        tmpID = int(word[0].strip())
                        tmpBar = word[1].replace("{","").replace("#","").strip()
                        #baronlyList.append(tmpID)
                        #barrolyNameList.append(tmpBar)
                    except:
                        pass
            if indintation == 1:
                if "terrain" in line:
                    if "\"\"" in line:
                        pass
                    else:
                        checker+=1
                if "religion" in line:
                    if "\"\"" in line:
                        pass
                    else:
                        checker+=1
                if checker >1:
                    if tmpID>-1:
                        baronlyList.append(tmpID)
                        barrolyNameList.append(tmpBar)
                        tmpBar= ""
                        tmpID = -1
                        checker = 0
            if "{" in line or "}" in line:
                #print("l: "+line)
                for element in list(line.strip()):
                    if "{" in element:
                        indintation +=1
                        #print("s: "+element)
                    elif "}" in element:
                        indintation -=1
                        if indintation == 0:
                            checker = 0
                        #print("e: "+element)
                    elif "#" in element:
                        #print("c: "+element)
                        break

    pass
def writeAdj():
    adjCSV = open("Output/adjacencies.csv", "w", encoding='utf-8-sig')
    adjVFile = open("Input/adjacencies.csv")
    adjCSV.write("From;To;Type;Through;start_x;start_y;stop_x;stop_y;Comment\n")
    count = 0
    #print("Discarded Adjacencies:")
    for line in adjVFile:
        if ";sea;" in line:
            adjCSV.write(line)
    for adj in objAdjList:
        if adj.fromID in baronlyList and adj.toID in baronlyList:
            if adj.overID in riverList:
                if game.upper() == "CK3":
                    adjCSV.write("%s;%s;river_large;%s;-1;-1;-1;-1;%s ~ %s\n"%(adj.fromID,adj.toID,adj.overID,barrolyNameList[baronlyList.index(adj.fromID)],barrolyNameList[baronlyList.index(adj.toID)]))
                elif game.upper() == "IR":
                    adjCSV.write("%s;%s;river_large;%s;0;0;0;0;%s ~ %s\n"%(adj.fromID,adj.toID,adj.overID,barrolyNameList[baronlyList.index(adj.fromID)],barrolyNameList[baronlyList.index(adj.toID)]))
                count +=1
        else:
            #print("%s ~ %s"%(adj.fromID,adj.toID))
            pass
    adjCSV.write("-1;-1;;-1;-1;-1;-1;-1;")
    adjCSV.close()
    print("Created Adjacencies: %i"%count)

ts = time.time()
readProvinceDeff()
getRiverProvinces()
riverList = list(dict.fromkeys(riverList))
for id in riverList:
    for prov in provList:
        if id == prov.id:
            #print(prov.name)
            riverProvList.append(prov)
            provColorList.append((prov.red,prov.green,prov.blue))
            break
    pass
total = len(riverProvList)
print("%i rivers"%total)
drawMat(riverProvList,"RiverMat")
drawBorderMat("RiverBorderMat")
drawBoldBorderMat("RiverBoldBorderMat")
radialChecker2()
if game.upper() == "CK3":
    getBaronies()
elif game.upper() == "IR":
    getSettlement()
else:
    print("%s is not a recognised game"%game)
writeAdj()

print("Direct Adj: %i"%len(directAdj))
ts2 = time.time()
print("%g Seconds"%(ts2 - ts))