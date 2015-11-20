#!/usr/bin/env python

from mininet.net import *
from mininet.topo import *
from mininet.node import *
from mininet.link import *
from mininet.cli import *
from mininet.log import *
from mininet.util import *
from subprocess import *
from subprocess import *
from opsvsi.docker import *
from opsvsi.opsvsitest import *
import select

class myTopo(Topo):

    def build(self, hsts=0, sws=2, **_opts):
        self.hsts = hsts
        self.sws = sws

        # Add list of switches
        for s in irange(1, self.sws):
            self.addSwitch('s%s' %s)

        # Add links between switches
        self.addLink('s1', 's2')
        self.addLink('s1', 's2')
        self.addLink('s1', 's2')
        self.addLink('s1', 's2')

class myNetwork(OpsVsiTest):

    """override the setupNet routine to create custom Topo.
    pass the global variables switch,host,link to mininet topo
    as VsiOpenSwitch, Host, OpsVsiLink
    """

    def setupNet(self):
        self.net = Mininet(topo=myTopo(hsts=0, sws=2,
                                       hopts=self.getHostOpts(),
                                       sopts=self.getSwitchOpts()),
                           switch=VsiOpenSwitch,
                           host=Host,
                           link=OpsVsiLink, controller=None,
                           build=True)

    def setConfig(self):
        s1 = self.net.switches[ 0 ]
        s2 = self.net.switches[ 1 ]

        # s1: Assign ports to default OPS bridge in namespace
        s1.swns_cmd("ovs-vsctl add-port bridge_normal 1")
        s1.swns_cmd("ovs-vsctl add-port bridge_normal 2")
        s1.swns_cmd("ovs-vsctl add-port bridge_normal 3")
        s1.swns_cmd("ovs-vsctl add-port bridge_normal 4")

        # s2: Assign ports to default OPS bridge in namespace
        s2.swns_cmd("ovs-vsctl add-port bridge_normal 1")
        s2.swns_cmd("ovs-vsctl add-port bridge_normal 2")
        s2.swns_cmd("ovs-vsctl add-port bridge_normal 3")
        s2.swns_cmd("ovs-vsctl add-port bridge_normal 4")

        # s1: configure
        s1.cmdCLI("conf t\nhostname s1")
        s1.cmdCLI("conf t\nfeature lldp")
        s1.cmdCLI("conf t\nint 1\nlldp reception")
        s1.cmdCLI("conf t\nint 1\nlldp transmission")
        s1.cmdCLI("conf t\nint 1\nno shut")

        # s2: configure
        s2.cmdCLI("conf t\nhostname s2")
        s2.cmdCLI("conf t\nfeature lldp")
        s2.cmdCLI("conf t\nint 1\nlldp reception")
        s2.cmdCLI("conf t\nint 1\nlldp transmission")
        s2.cmdCLI("conf t\nint 1\nno shut")

if __name__ == '__main__':
    # Create topology
    myNet = myNetwork()
    myNet.setConfig()

    CLI(myNet.net)

    myNet.net.stop()
