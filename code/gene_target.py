import json
import os
import radix
from collections import defaultdict
def ABCToNum(n):
        dic = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'a':10,'b':11,'c':12,'d':13,'e':14,'f':15}
        return dic[n]
def NumToABC(n):
        dic = {0:'0',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:"a",11:"b",12:"c",13:"d",14:"e",15:"f"}
        return dic[n]

def IP_Gene2():
        path='download'
        kid_ipaddr=[]
        ip6Rtree = radix.Radix()
        match_pre=[]
        select_ip=defaultdict(list)
        for file_name in os.listdir(path):
                if file_name=="country_US_202265.json":
                        count=0
                        #file_path=path+ '\\'+file_name
                        file_path='country_CN_202265.json'
                        with open(file_path, encoding='utf-8') as a:
                                result=json.load(a)
                                iplist=result.get('data').get('resources').get('ipv6')
                        for ipaddr in iplist:
                                if int(ipaddr[-2:])>=32:
                                        kid_ipaddr.append(ipaddr)
                                        count+=1
                                else:
                                        if len(ipaddr)<=9:
                                                ipaddr=ipaddr[0:4]+':0000'+ ipaddr[4:]
                                        num=32-int(ipaddr[-2:])
                                        if(4>=num):
                                                for i in range (2**num):
                                                        count+=1
                                                        kid_ipaddr.append(ipaddr[:-6]+NumToABC(ABCToNum(ipaddr[-6])+i)+"::/32")
                                        elif(4<num<=8):
                                                for i in range (2**(num-4)):
                                                        for j in range (16):
                                                                count+=1
                                                                kid_ipaddr.append(ipaddr[:-7]+NumToABC(ABCToNum(ipaddr[-7])+i)+NumToABC(j)+"::/32")
                                        elif(8<num<=12):
                                                for i in range (2**(num-8)):
                                                        for j in range (16):
                                                                for k in range(16):
                                                                        count+=1
                                                                        kid_ipaddr.append(ipaddr[:-8]+NumToABC(ABCToNum(ipaddr[-8])+i)+NumToABC(j)+NumToABC(k)+"::/32")
                                        
                                        elif(12<num<=16):
                                                for i in range (2**(num-12)):
                                                        for j in range (16):
                                                                for k in range(16):
                                                                        for l in range(16):
                                                                                count+=1
                                                                                kid_ipaddr.append(ipaddr[:-9]+NumToABC(ABCToNum(ipaddr[-9])+i)+NumToABC(j)+NumToABC(k)+NumToABC(l)+"::/32")
                                        else:
                                                print(file_name[8:10])
                                                print(ipaddr)
        kid_ipaddr = set(kid_ipaddr)
        print(len(kid_ipaddr))
        for ipprefix in kid_ipaddr:
                rnode = ip6Rtree.add(ipprefix)  # 生成由前缀组成的地址树
        with open('address.txt') as f:
                count = 0
                i = 0
                active_ips = f.read().splitlines()
                active_ips.reverse()
                for ip in active_ips:
                        try:
                                node = ip6Rtree.search_best(ip)
                                if (node == None):
                                        continue
                                if node.prefix in match_pre:
                                        select_ip[node.prefix].append(ip)
                                        continue
                                else:
                                        # print(node.prefix)
                                        match_pre.append(node.prefix)
                                        select_ip[node.prefix].append(ip)

                        except:
                                print(ip)
                                continue
        print('success')
        return select_ip




                
                                

if __name__ == "__main__":
    IP_Gene2()
    print('success')
                
