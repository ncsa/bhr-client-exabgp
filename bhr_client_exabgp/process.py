#!/usr/bin/env python
from mako.template import Template
from bhr_client.rest import login_from_env
from bhr_client.block_manager import BlockManager
from bhr_client_exabgp.common import get_ips
import argparse
import os
import sys
flush = sys.stdout.flush


def iterwindow(l, slice=50):
    """Generate sublists from an iterator
    >>> list(iterwindow(iter(range(10)),11))
    [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
    >>> list(iterwindow(iter(range(10)),9))
    [[0, 1, 2, 3, 4, 5, 6, 7, 8], [9]]
    >>> list(iterwindow(iter(range(10)),5))
    [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]
    >>> list(iterwindow(iter(range(10)),3))
    [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    >>> list(iterwindow(iter(range(10)),1))
    [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9]]
    """

    assert(slice > 0)
    a = []

    for x in l:
        if len(a) >= slice:
            yield a
            a = []
        a.append(x)

    if a:
        yield a


BATCHSIZE = int(os.getenv("BHR_EXABGP_BATCH_SIZE", "50"))


def write(msg):
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()


class ExaBgpBlocker:
    def __init__(self):
        self.t = Template(filename=os.getenv("BHR_TEMPLATE"))
        self.block = self.t.get_def('block')
        self.ipv4, self.ipv6 = get_ips()

    def make_routes(self, action, cidrs):
        return self.block.render(action, cidrs, ipv4=self.ipv4, ipv6=self.ipv6).rstrip("\t\n ;")

    def send_lots_of_routes(self, action, cidrs):
        v4 = [c for c in cidrs if ':' not in c]
        v6 = [c for c in cidrs if ':' in c]

        for batch in iterwindow(v4, BATCHSIZE):
            write(self.make_routes(action, batch))

        for batch in iterwindow(v6, BATCHSIZE):
            write(self.make_routes(action, batch))

    def block_many(self, records):
        cidrs = [b['cidr'] for b in records]
        self.send_lots_of_routes("announce", cidrs)

    def unblock_many(self, records):
        cidrs = [r['block']['cidr'] for r in records]
        self.send_lots_of_routes("withdraw", cidrs)


def go(mode):
    client = login_from_env()
    blocker = ExaBgpBlocker()
    m = BlockManager(client, blocker)
    if mode == "backfill":
        m.block_all_expected()
    else:
        m.run()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["backfill", "run"])
    args = parser.parse_args()
    go(args.mode)


if __name__ == "__main__":
    main()
