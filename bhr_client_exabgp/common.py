import socket

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
