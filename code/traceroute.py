

from time import sleep
import time
from sockets import ICMPv4Socket, ICMPv6Socket
from models import ICMPRequest, Hop
from exceptions import TimeExceeded, ICMPLibError
from utils import *
from Shine import shine

discoverd_list=set()
def traceroute(address_list, count=2, interval=0.05, timeout=2, first_hop=10,
        max_hops=30, fast=False, id=None, source=None, family=None,
        **kwargs):
    all_packet=0
    result = []
    global discoverd_list
    for address in address_list:
        if is_hostname(address):
            address = resolve(address, family)[0]

        if is_ipv6_address(address):
            Socket = ICMPv6Socket
        else:
            Socket = ICMPv4Socket

        id = id or unique_identifier()
        ttl = first_hop
        host_reached = False
        hops = []

        packets_sent = 0
        with Socket(source) as sock:
            while ttl > 0:      
                reply = None
                rtts = []
                for sequence in range(count):
                    request = ICMPRequest(
                        destination=address,
                        id=id,
                        sequence=sequence,
                        ttl=ttl,
                        **kwargs)
                    try:
                        sock.send(request)
                        packets_sent += 1
                        reply = sock.receive(request, timeout)
                        rtt = (reply.time - request.time) * 1000
                        rtts.append(rtt)
                        reply.raise_for_status()

                    except TimeExceeded:
                        continue

                    except ICMPLibError:
                        break

                if reply:
                    if reply.source in discoverd_list:
                        break
                    else:
                        hop = [reply.source, ttl]
                        discoverd_list.add(reply.source)
                        hops.append(hop)

                ttl -= 1
            ttl = first_hop+1

            while not host_reached and ttl <= max_hops:  
                reply = None
                rtts = []
                for sequence in range(count):
                    request = ICMPRequest(
                        destination=address,
                        id=id,
                        sequence=sequence,
                        ttl=ttl,
                        **kwargs)
                    try:
                        sock.send(request)
                        packets_sent += 1
                        reply = sock.receive(request, timeout)
                        rtt = (reply.time - request.time) * 1000
                        rtts.append(rtt)
                        reply.raise_for_status()
                        host_reached = True
                    except TimeExceeded:
                        continue

                    except ICMPLibError:
                        break

                if reply:
                    if reply.source in discoverd_list:
                        break
                    else:
                        hop = [reply.source, ttl]
                        discoverd_list.add(reply.source)
                        hops.append(hop)
                ttl += 1

        result.append(hops)
        all_packet+=packets_sent

        #print(all_packet)
        last_distance=0
        '''
        for hop in hops:
            if last_distance + 1 != hop[1]:
                print('*')
            #print(hop[1], hop[0])

            last_distance = hop[1]
        #print('ok')
        '''
    return result,all_packet




