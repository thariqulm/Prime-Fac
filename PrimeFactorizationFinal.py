from factordb.factordb import FactorDB as factordb
from sympy import factorint
from func_timeout import *
import io
import rsa
import time
import cypari
import urllib.request as urec
def check_connection():
    host = "http://www.google.com"
    try:
        urec.urlopen(host)
        return True
    except:
        return False
def superscript(n):
    return "".join(["⁰¹²³⁴⁵⁶⁷⁸⁹"[ord(c)-ord('0')] for c in (n)])
def querystrip(query):
    if 'th' in query:
        num=query.replace('th','')
        return (int(num))
    elif 'st' in query:
        num=query.replace('st','')
        return (int(num))
    elif 'nd' in query:
        num=query.replace('nd','')
        return (int(num))
    elif 'rd' in query:
        num=query.replace('rd','')
        return (int(num))
#@func_set_timeout(1)
def producepari(n):
    cyp=cypari.pari('factor({})'.format(n))
    tp=sum(cyp[1])
    dp=len(cyp[0])
    res="\n"+str(n)+" = "
    for i in range(0,len(cyp[0])):
        j=i
        res=res+str(cyp[0][i])
        if cyp[1][j]!=1:
            res=res+superscript(str(cyp[1][j]))
        if i!=(dp-1):
            res=res+"×"
    if(tp==1 and dp==1):
        res="It is a Prime Number"
    elif(tp==dp):
        res=res+" ("+"%d"%tp+" distinct prime factors)"
    else:
        res=res+" ("+"%d"%tp+" prime factors, "+"%d"%dp+" distinct)"
    return res
def producersa(num):
    while True:
        bitcount=num.bit_length()
        (pub_key,priv_key)=rsa.newkeys(bitcount)
        print(pub_key.n)
        if (pub_key.n)==num:
            Ans="\n"+str(num)+" = "
            Ans=Ans+"%d"%priv_key.p+" x %d (2 distinct prime factors)"%priv_key.q
            return Ans
            break;
def producefdb(n):
    dp=0
    tp=0
    global pi_index
    f=factordb(n)
    if check_connection():
        f.connect()
        fact=f.get_factor_from_api()
        status=f.get_status()
        print(status)
        if status=="FF" or status=="P":
            ans="\n"+str(n)+" = "
            for i in range(0,len(fact)):
                dp=dp+1
                ans=ans+str(fact[i][0])
                pow=fact[i][1]
                tp=tp+pow
                if(pow!=1):
                    ans=ans+superscript ("%d"%pow)
                if(i!=len(fact)-1):
                    ans=ans+"×"
            if(tp==1 and dp==1):
                ans="It is a Prime Number"
            elif(tp==dp):
                ans=ans+" ("+"%d"%tp+" distinct prime factors)"
            else:
                ans=ans+" ("+"%d"%tp+" prime factors, "+"%d"%dp+" distinct)"
            return ans
        elif status=="CF" or status=="C" or status=="U":
            return producepari(n)
        elif status=="PRP":
            #return producersa(n)
            return producepari(n)
    else:
        print("connect to the internet & try again if it takes too long time")
        return producepari(n)
def producesympy(n):
    kcount=0
    vcount=1
    svalue=0
    primefactors_n = factorint(n)
    ans="\n"+str(n)+" = "
    for key,value in primefactors_n.items():
        kcount=kcount+1
        svalue=svalue+value
        if kcount>1:
            ans=ans+"×"
        ans=ans+str(key)
        if value!=1:
            vcount=vcount+1
            ans=ans+superscript(str(value))
        if n==key:
            ans="It is a Prime Number"
    if vcount==1 and kcount>1:
        ans=ans+" ("+"%d"%kcount+" distinct prime factors)"
    if vcount>1:
        ans=ans+" ("+"%d"%svalue+" prime factors, "+"%d"%kcount+" distinct)"
    return ans
while True:
    query=input("\nEnter a Positive Integer to factorize or Ordinal number to get the prime number: ")
    stopper=['0','exit','Exit','EXIT','quit','Quit','QUIT','close','Close','CLOSE']
    if query in stopper:
        break
    try:
        query=str(eval(query))
    except:
        pass
    t0=time.time()
    if query.isdigit():
        n=int(query)
        try:
            print(producefdb(n))
        except:
            print(producesympy(n))
    else:
        try:
            print("Depending on your query, it may take time to execute")
            print(query,"prime number is",cypari.pari('prime({})'.format(querystrip(query))))
        except:
            print("Incorrect Input")
    t1=time.time()
    print("Time taken: ",t1-t0)
