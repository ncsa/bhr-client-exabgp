#!/usr/bin/env python
from mako.template import Template
from bhr_client.rest import Client
import os
import sys
flush = sys.stdout.flush

class ExaBgpBlocker:
    def __init__(self):
        self.t = Template(filename=os.getenv("BHR_TEMPLATE"))
        self.block = self.t.get_def('block')

    def make_route(self, action, b):
        return action + " " + self.block.render(b=b).rstrip()

    def block_many(self, records):
        for r in records:
            print self.make_route("announce", r)
        flush()

    def unblock_many(self, records):
        for r in records:
            print self.make_route("withdraw", r['block'])
        flush()


def main():
    ident = sys.argv[1]

    c = Client(ident, blocker=ExaBgpBlocker())
    c.run()

if __name__ == "__main__":
    main()
