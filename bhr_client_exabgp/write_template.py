#!/usr/bin/env python

import os
import socket
from mako.template import Template

from bhr_client.rest import login_from_env

def render_config():
    c = login_from_env()
    t = Template(filename=os.getenv("BHR_TEMPLATE"))

    context = {
        "blocked": list(c.get_list()),
        'ip': socket.gethostbyaddr(socket.gethostname())[2][0]
    }

    return t.render(**context)

def main():
    print render_config()

if __name__ == "__main__":
    print render_config()
