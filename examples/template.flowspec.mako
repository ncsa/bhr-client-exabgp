<%def name="block_v4(action, cidrs)" filter="trim">
    %for cidr in cidrs:
        ${action} flow route { match { source      ${cidr}; } then { discard; } }
        ${action} flow route { match { destination ${cidr}; } then { discard; } }
    %endfor
</%def>
<%def name="block_v6(action, cidrs)" filter="trim">
    %for cidr in cidrs:
        ${action} flow route { match { source      ${cidr}; } then { discard; } }
        ${action} flow route { match { destination ${cidr}; } then { discard; } }
    %endfor
</%def>
<%def name="block(action, cidrs)" filter="trim">
## cidrs are grouped by v4 or v6. If one address is v4, they all are.
%if ':' in cidrs[0]:
    ${block_v6(action, cidrs)}
%else:
    ${block_v4(action, cidrs)}
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
