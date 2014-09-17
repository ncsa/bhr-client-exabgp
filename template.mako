<%def name="block_v4(b)" filter="trim">
    route ${b['cidr']} next-hop 192.168.127.1 community [ no-export ]
</%def>
<%def name="block_v6(b)" filter="trim">
    route ${b['cidr']} next-hop 2001:DB8::DEAD:BEEF community [ no-export ]
</%def>
<%def name="block(b)" filter="trim">
%if ':' in b['cidr']:
    ${block_v6(b)}
%else:
    ${block_v4(b)}
%endif
</%def>

group edgerouters {
    peer-as 65501;
    local-as 65502;
    hold-time 3600;
    router-id ${ip};
    local-address ${ip};
    graceful-restart 1200;
    group-updates;

    #md5 'bgp_key_here';
    static {
    %for b in blocked:
            ${block(b)};
    %endfor
    }
    process bhr-dynamic {
        run ./run.py bgp1;
    }

    neighbor 192.168.2.201 {
        description "edge-1";
    }

}
