<%def name="block_v4(cidrs)" filter="trim">
    attribute next-hop self community [ 65142:666 no-export ] nlri ${cidrs}
</%def>
<%def name="block_v6(cidrs)" filter="trim">
    attribute next-hop self community [ 65142:666 no-export ] nlri ${cidrs}
</%def>
<%def name="block(cidrs)" filter="trim">
%if ':' in cidrs:
    ${block_v6(cidrs)}
%else:
    ${block_v4(cidrs)}
%endif
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
        # auto filled in by bhr-client-exabgp-write-template
        run ${path_to_bhr_client_exabgp_loop};
    }

    neighbor 192.168.2.201 {
        description "edge-1";
    }

}
