#-*-coding:utf-8-*-
import xml.etree.cElementTree as et
import eggcounterv1
import re
import os
import sys
import argparser
def read():
    x = open('id.txt','r').read()
    return x
def id():
    if os.stat('eggcounter.txt').st_size == 0:
        a = 1
    else:
        file = open('eggcounter.txt')
        a = re.findall('<id>(\d+)</id>', file.read())[-1]
        a = int(a)
        a+=1
    return a


def xmain(arg):
    filename = "webvalues.txt"
    
    if os.path.exists(filename):
        dosya=open(filename).read().strip()
        if dosya !="":
        
            fst_thresh  = int(re.findall("<first_th>(.*?)</first_th>",dosya)[0])
            morph_value = int(re.findall("<morph>(.*?)</morph>",dosya)[0])
            scd_thresh  = int(re.findall("<second_th>(.*?)</second_th>",dosya)[0])
            temp_match  = re.findall("<template>(.*?)</template>",dosya)[0]
            gap         = int(re.findall("<gap>(.*?)</gap>",dosya)[0])
            bordersize  = int(re.findall("<border_size>(.*?)</border_size>",dosya)[0])
            distx       = int(re.findall("<abs_distance>(.*?)</abs_distance>",dosya)[0])
            display     = int(re.findall("<display>(.*?)</display>", dosya)[0])
        else:
            print("Lütfen Webserver'ı Çalıştırıp Uygun Değerleri Giriniz...")
            sys.exit()
    else:
        print("Lütfen WebServer'ı Çalıştırınız...")
        sys.exit()
        

    EntranceCounter, ExitCounter, list, list2 = eggcounterv1.main(arg , fst_thresh, morph_value, scd_thresh, gap, bordersize, distx, display) #int(fst_thresh), int(morph_value), int(scd_thresh), matching, int(gap), int(bordersize), int(distx))
    a = id()
    file      = open("eggcounter.txt", 'a')
    begindate = "{}:{}:{}:{}:{}:{}".format(list[0], list[1], list[2], list[3], list[4], list[5])
    enddate   = "{}:{}:{}:{}:{}:{}".format(list2[0], list2[1], list2[2], list2[3], list2[4], list2[5])
    content   ="""
<egginfo>
    <id>{}</id>
    <begindate>{}</begindate>
    <enddate>{}</enddate>
    <countedeggs>{}</countedeggs>
</egginfo>
            """.format(a, begindate, enddate, EntranceCounter)

    file.write(content)
    file.close()


if __name__ == '__main__':
    data = argparser.main()

    xmain(data)


