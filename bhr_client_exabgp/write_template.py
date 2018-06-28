#!/usr/bin/env python

from distutils.spawn import find_executable
import os
import socket
from mako.template import Template

from bhr_client.rest import login_from_env

from bhr_client_exabgp.common import get_ips

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
