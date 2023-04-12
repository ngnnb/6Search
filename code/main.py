from traceroute import traceroute
import threading
import time
from threading import Thread
from gene_target import IP_Gene2
from random_geneip import geneIP
import math
import random
from collections import defaultdict
from trans_ipv6 import tran_ipv6
new_prefixset=list()
class MyThread(Thread):
    def __init__(self, address):
        Thread.__init__(self)
        self.address = address

    def run(self):
        self.result = traceroute(self.address)

    def get_result(self):
        return self.result

def multi_thread(address_list):
    thread_pool=[]   #Thread pool
    start = time.time()
    packets_send=0
    prefix_insert=[]
    prefix_insert2=[]
    result=[]
    topo=[]
    num=-1

    for address in address_list:
        if(len(address)==1):
            prefix_insert.append(address_list.index(address))
            continue
        elif (len(address)>2):
            prefix_insert2.append(len(address)-1)
            for i in range(1,len(address)):
                thd = MyThread([address[1:]])
                thread_pool.append(thd)
        else:
            prefix_insert2.append(1)
            thd=MyThread(address[1:])
            thread_pool.append(thd)
    for thd in thread_pool:
        thd.start()
    for thd in thread_pool:
        thd.join()
        a,b=thd.get_result()
        packets_send+=b
        result.append(a)
    for i in prefix_insert2:
        temp=[]
        for j in range(i):
            temp+=result[j]
        result=result[i:]
        topo.append(temp)

    end = time.time()
    print(end - start)
    for i in prefix_insert:
        topo.insert(i,'#')
    return topo,packets_send
def split(pre,nodes):
    S=defaultdict(list)
    new_gran=int(pre[-2:])+4
    for node in nodes:
        node_pre=''
        for i in range (int(new_gran/16)):
            node_pre+=(tran_ipv6(node)[i]+':')
        node_pre+=tran_ipv6(node)[i+1][:(new_gran%16)/4]
        for i in range (4-(new_gran%16)/4):
            node_pre+='0'
        node_pre=node_pre+'::/'+str(new_gran)
        S[node_pre].append(node)
    return S
def prefix_finer(pre,nodes,threshold):
    global new_prefixset
    if len(nodes)<threshold):
        new_prefixset.append(pre)
    else:
        for pre_detial in split(pre,nodes):
            prefix_finer(pre_detial,split(pre,nodes)[pre_detial],len(node_set)/len(newpre_set)
def gene_prefix(node_set):
    newpre_set=defaultdict(list)
    global new_prefixset
    new_prefixset=[]
    for node in node_set:
        new_prefix=node.split(':')[0]+':'+node.split(':')[1]+'::/32'
        newpre_set[new_prefix].append(node)
    for newpre in newpre_set:
        prefix_finer(newpre,newpre_set[newpre],len(node_set)/len(newpre_set)
    return  new_prefixset     
if __name__ == "__main__":
    prefixss = IP_Gene2()
    all_targets=0
    all_targets2=0
    flag=0
    flag2=0
    q_value = []
    new_list = []
    all_topo = set()  # save discoverd nodes
    while True:
        address_list = []
        address_list2 = []
        if all_targets+all_targets2>=1000000:
            print(len(all_topo))
            break
        if (flag == 0):
            flag = 1
            num = -1
            for prefix in prefixss:
                address_list.append([prefix])
                num += 1
                q_value.append(2)
                for i in range(2):
                    if prefixss[prefix]==[]:
                        prefixss[prefix].append(geneIP(prefix))
                    address_list[num].append(prefixss[prefix].pop(0))
            topos, targets = multi_thread(address_list)
        elif (flag == 1):
            num = -1
            num2 = -1
            for prefix in prefixss:
                address_list.append([prefix])
                num += 1
                if num in new_list:
                    flag2=1
                    num2+=1
                    address_list2.append([prefix])
                    for i in range (int(sum(gennum)/50)):
                        if prefixss[prefix]==[]:
                            prefixss[prefix].append(geneIP(prefix))
                        address_list2[num2].append(prefixss[prefix].pop(0))
                else:
                    for i in range(gennum[num]):
                        if prefixss[prefix]==[]:
                            prefixss[prefix].append(geneIP(prefix))
                        address_list[num].append(prefixss[prefix].pop(0))
            topos, targets = multi_thread(address_list)
        all_targets+=targets
        reward = []
        for topo in topos:
            num = 0
            if topo=='#':
                reward.append(num)
                continue
            for t in topo:
                for hop in t:
                    if hop[0] in all_topo:
                        continue
                    else:
                        all_topo.add(hop[0])
                        num+=1
            reward.append(num)
        if (flag2 == 1):
            topos2, targets2 = multi_thread(address_list2)
            all_targets2 += targets2
            num = 0
            for topo in topos2:
                if topo == '#':
                    continue
                for t in topo:
                    for hop in t:
                        if hop[0] in all_topo:
                            continue
                        else:
                            all_topo.add(hop[0])
                            num += 1
        alpha=0.1
        target_num=1500
        for i in range (len(q_value)):
            q_value[i]=(1-alpha)*q_value[i]+alpha*reward[i]
        try:
            boltzmann=[math.exp(q/5) for q in q_value]
            boltzmanns=sum(boltzmann)
            pvalue=[bolt / boltzmanns for bolt in boltzmann]
        gennum=[int(target_num * p) for p in pvalue]
        live_pre=0
        for j in gennum:
            if j!=0:
                live_pre+=1
            if j>sum(gennum)/20:
                new_list.append(gennum.index(j))
                q_value[gennum.index(j)] = 0
                gennum[gennum.index(j)]=0
        if (live_pre<len(prefixss)/20):
            print('Generation of new prefix')
            q_value = []
            new_list = []
            flag = 0
            flag2 = 0
            prefixss = gene_prefix(all_topo)






