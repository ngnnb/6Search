from ipaddress import ip_address
import ipaddress
import random
def str2hex(s):
    odata = 0;
    su =s.upper()
    for c in su:
        tmp=ord(c)
        if tmp <= ord('9') :
            odata = odata << 4
            odata += tmp - ord('0')
        elif ord('A') <= tmp <= ord('F'):
            odata = odata << 4
            odata += tmp - ord('A') + 10
    return odata

def geneIP(prefix):
    count=0
    IPlist=prefix.split('/')
    int_prefix=int(IPlist[1])
    IPaddr1=IPlist[0][:-2]
    IPaddr1list=IPaddr1.split(':')
    for i in range (len(IPaddr1list)):
        count+=str2hex(IPaddr1list[i])*(2**(112-i*16))
    random_select=random.getrandbits(128-int_prefix)
    num=random_select+count
    IPaddr2=str(ip_address(num))
    return IPaddr2

                        
