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

    def build(self, hsts=2, sws=2, **_opts):
        self.hsts = hsts
        self.sws = sws

        # Add list of hosts
        for h in irange(1, self.hsts):
            self.addHost('h%s' % h, ip='10.0.10.1%s' % h)

        # Add list of switches
        for s in irange(1, self.sws):
            self.addSwitch('s%s' %s)

        # Add links between nodes
        self.addLink('h1', 's1')
        self.addLink('h2', 's1')
        self.addLink('h3', 's2')
        self.addLink('h4', 's2')

        # Add links between switches
        self.addLink('s1', 's2')
        self.addLink('s1', 's2')
        self.addLink('s1', 's2')
        self.addLink('s1', 's2')

class myNetwork(OpsVsiTest):

    """override the setupNet routine to craete custom Topo.
    pass the global variables switch,host,link to mininet topo
    as VsiOpenSwitch, Host, OpsVsiLink
    """

    def setupNet(self):
        self.net = Mininet(topo=myTopo(hsts=4, sws=2,
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
        s1.swns_cmd("ovs-vsctl add-port bridge_normal 5")
        s1.swns_cmd("ovs-vsctl add-port bridge_normal 6")
        s1.swns_cmd("ovs-vsctl add-port bridge_normal 7")
        s1.swns_cmd("ovs-vsctl add-port bridge_normal 8")

        # s2: Assign ports to default OPS bridge in namespace
        s2.swns_cmd("ovs-vsctl add-port bridge_normal 1")
        s2.swns_cmd("ovs-vsctl add-port bridge_normal 2")
        s2.swns_cmd("ovs-vsctl add-port bridge_normal 3")
        s2.swns_cmd("ovs-vsctl add-port bridge_normal 4")
        s2.swns_cmd("ovs-vsctl add-port bridge_normal 5")
        s2.swns_cmd("ovs-vsctl add-port bridge_normal 6")
        s2.swns_cmd("ovs-vsctl add-port bridge_normal 7")
        s2.swns_cmd("ovs-vsctl add-port bridge_normal 8")

        # s1: configure
        s1.cmdCLI("conf t\nhostname s1")
        s1.cmdCLI("conf t\nvlan 1\nno shut")
        s1.cmdCLI("conf t\nvlan 100\nno shut")
        s1.cmdCLI("conf t\nvlan 200\nno shut")
        s1.cmdCLI("conf t\nint 1\nno shut\nvlan access 100")
        s1.cmdCLI("conf t\nint 2\nno shut\nvlan access 200")
        s1.cmdCLI("conf t\nint 3\nvlan trunk native 1")
        s1.cmdCLI("conf t\nint 3\nvlan trunk allowed 1")
        s1.cmdCLI("conf t\nint 3\nvlan trunk allowed 100")
        s1.cmdCLI("conf t\nint 3\nvlan trunk allowed 200")
        s1.cmdCLI("conf t\nint 3\nvlan trunk native tag")
        s1.cmdCLI("conf t\nint 3\nno shut")

        # s2: configure
        s2.cmdCLI("conf t\nhostname s2")
        s2.cmdCLI("conf t\nvlan 1\nno shut")
        s2.cmdCLI("conf t\nvlan 100\nno shut")
        s2.cmdCLI("conf t\nvlan 200\nno shut")
        s2.cmdCLI("conf t\nint 1\nno shut\nvlan access 100")
        s2.cmdCLI("conf t\nint 2\nno shut\nvlan access 200")
        s2.cmdCLI("conf t\nint 3\nvlan trunk native 1")
        s2.cmdCLI("conf t\nint 3\nvlan trunk allowed 1")
        s2.cmdCLI("conf t\nint 3\nvlan trunk allowed 100")
        s2.cmdCLI("conf t\nint 3\nvlan trunk allowed 200")
        s2.cmdCLI("conf t\nint 3\nno shut")

if __name__ == '__main__':
    # Create topology
    myNet = myNetwork()
    myNet.setConfig()

    CLI(myNet.net)

    myNet.net.stop()
