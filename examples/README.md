OPS Playground Examples
=======================

## multiswitch_vlan

This example boots two switches with two hosts connected to each. The first host on each switch is configured to access VLAN 100 and the second is configured to access VLAN 200. The third port of each switch serves as a trunk port.

To run, login to the Vagrant VM and execute the following:

    sudo python /vagrant/examples/mutliswitch_vlan.py

You can then test connectivity via the mininet shell:

    mininet> h1 ping h3
    mininet> h2 ping h4

To interrogate the config of each switch:

    mininet> s1 vtysh
    mininet> s2 vtysh

## lldp

This example configures LLDP on two hosts connected by four links. Only the first link is configured, the remaining links are shutdown (you can enable them manually).

To run, login to the Vagrant VM and execute the following:

    sudo python /vagrant/examples/lldp.py

It will take about 30 seconds for the discovery to take place, but then you can login to the OPS CLI and issue some show commands:

    mininet> s1 vtysh
    s1# show lldp neighbor 1
