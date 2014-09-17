#!/usr/bin/env python
from bhr_client.rest import Client
import sys
flush = sys.stdout.flush

class ExaBgpBlocker:
    def __init__(self):
        pass

    def make_route(self, action, ip):
        if ':' in ip:
            next_hop = "2001:DB8::DEAD:BEEF"
        else:
            next_hop = "192.168.127.1"

        return "%s route %s next-hop %s community [no-export]" % (
            action, ip, next_hop)

    def block_many(self, records):
        for r in records:
            print self.make_route("announce", r['cidr'])
        flush()

    def unblock_many(self, records):
        for r in records:
            print self.make_route("withdraw", r['block']['cidr'])
        flush()


def main():
    ident = sys.argv[1]

    c = Client(ident, blocker=ExaBgpBlocker())
    c.run()

if __name__ == "__main__":
    main()
