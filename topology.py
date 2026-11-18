from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import OVSSwitch, RemoteController
from mininet.log import setLogLevel, info

def create_sdn_topology():
    net = Mininet(switch=OVSSwitch, controller=None) # We will manage routing manually or via controller

    info('*** Adding SDN Controller\n')
    # For simplicity and reliability in student projects, we can attach a remote controller or use OVS built-in learning,
    # but let's define a controller slot (we can point it to a Ryu controller or custom script later)
    

    info('*** Adding Hosts\n')
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')

    info('*** Adding Switches\n')
    s1 = net.addSwitch('s1', cls=OVSSwitch, failMode='standalone')
    s2 = net.addSwitch('s2', cls=OVSSwitch, failMode='standalone')

    info('*** Creating Links (Notice the two parallel links between s1 and s2 for alternative paths)\n')
    # Link between h1 and s1
    net.addLink(h1, s1)
   
    # Two alternative paths between s1 and s2
    net.addLink(s1, s2, bw=10)
    net.addLink(s1, s2, bw=10)
   
    # Link between s2 and h2
    net.addLink(s2, h2)

    info('*** Starting Network\n')
    net.build()
    s1.start([])
    s2.start([])

    info('*** Network is live! Entering Mininet CLI. Type "exit" to quit.\n')
    CLI(net)

    info('*** Stopping Network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_sdn_topology()

