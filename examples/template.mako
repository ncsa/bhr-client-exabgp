<%def name="block_v4(b)" filter="trim">
    route ${b['cidr']} next-hop self community [ 64512:666 no-export ]
</%def>
<%def name="block_v6(b)" filter="trim">
    route ${b['cidr']} next-hop self community [ 64512:666 no-export ]
</%def>
<%def name="block(b)" filter="trim">
%if ':' in b['cidr']:
    ${block_v6(b)}
%else:
    ${block_v4(b)}
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
    %for b in blocked:
            ${block(b)};
    %endfor
    }
    process bhr-dynamic {
        run /usr/local/bin/bhr-client-exabgp-loop;
    }

    neighbor 192.168.2.201 {
        description "edge-1";
    }

}
