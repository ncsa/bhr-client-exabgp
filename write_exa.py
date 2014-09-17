#!/usr/bin/env python

import socket

from mako.template import Template

from bhr_client.rest import Client
from run import ExaBgpBlocker

b = ExaBgpBlocker()
c = Client(ident=None)

t = Template(filename="./template.mako")

context = {
    "blocked": list(c.get_list()),
    'ip': socket.gethostbyaddr(socket.gethostname())[2][0]
}

print t.render(**context)
