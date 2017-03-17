<%def name="block(cidrs)" filter="trim">
    attribute next-hop self community [ 65142:666 no-export ] nlri ${cidrs}
</%def>

group edgerouters {
    peer-as 65000;
    local-as 64512;
    hold-time 3600;
    router-id ${ip};
    local-address ${ip};
    graceful-restart 1200;
    group-updates;

    md5 'hello';
    static {
    }
    process bhr-dynamic {
        run /usr/local/bin/bhr-client-exabgp-loop;
    }

    neighbor 192.168.2.201 {
        description "edge-1";
    }

}
