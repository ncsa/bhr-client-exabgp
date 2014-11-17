BHR Block manager that uses [ExaBGP](https://github.com/Exa-Networks/exabgp)

See the example configuration files in examples/

Site specific configuration is made up of:

    * The bhr client configuration - the environment variables for `BHR_HOST` AND `BHR_TOKEN`
    * The exabgp configuration template.

Configuration Template
======================
The configuration template is a [Mako template](http://docs.makotemplates.org/en/latest/syntax.html) for exabgp.

The lines like

    route ${b['cidr']} next-hop self community [ 64512:666 no-export ]

should be changed to match what your router is expecting.

Otherwise, the rest of the settings like `peer-as`, `local-as` should be
configured per the exabgp documentation.
