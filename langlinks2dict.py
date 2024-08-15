import sys
import gzip
import re
import codecs

titlesf=sys.argv[1]
langlinkssqlgz=sys.argv[2]
l2=sys.argv[3]
outfile=sys.argv[4]

f=gzip.open(langlinkssqlgz,'rb')

expreg=r"\([0-9]+,'.+?','.+?'\)"

titles={}

entrada=codecs.open(titlesf,"r",encoding="utf-8")
sortida=codecs.open(outfile,"w",encoding="utf-8")

for linia in entrada:
    linia=linia.rstrip()
    try:
        (id,title)=linia.split("\t")
        titles[id]=title
    except:
        pass

langlinks={}
cont=0
for line in f:
    l=line.decode("utf-8",errors="replace")
    ll=re.findall(r'\(.+?\)',l)
    for tripleta in ll:
        tripleta=tripleta.replace("(","").replace(")","")
        camps=tripleta.split(",")
        if len(camps)>2:
            id=camps[0]
            lang=camps[1][1:-1]
            title=camps[2][1:-1]
            data=[id,title,lang]
            if lang==l2 and id in titles:
                l1title=titles[id]
                cadena=l1title+"\t"+title
                print(cadena)
                sortida.write(cadena+"\n")
