#!/usr/bin/env python

from distutils.spawn import find_executable
import os
import socket
from mako.template import Template

from bhr_client.rest import login_from_env

def get_ips():
    v4 = None
    v6 = None
    for res in socket.getaddrinfo(socket.gethostname(), 80):
        af, socktype, proto, canonname, sa = res
        if af == socket.AF_INET6:
            v6 = sa[0]
        else:
            v4 = sa[0]

    return v4, v6

def render_config():
    c = login_from_env()
    t = Template(filename=os.getenv("BHR_TEMPLATE"))

    path_to_bhr_client_exabgp_loop = find_executable("bhr-client-exabgp-loop")
    if not path_to_bhr_client_exabgp_loop:
        raise RuntimeError("Can not find bhr-client-exabgp-loop in $PATH")

    ipv4, ipv6 = get_ips()
    context = {
        "blocked": [],
        'ip': ipv4,
        'ipv6': ipv6,
        "path_to_bhr_client_exabgp_loop": path_to_bhr_client_exabgp_loop,
    }

    return t.render(**context)

def main():
    print render_config()

if __name__ == "__main__":
    print render_config()
