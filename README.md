**udp_test.py	
Minimal UDP loopback test (send a message to yourself on 127.0.0.1:9999). Used to verify sockets work.
**sender.py	
Reads test.txt in 1024-byte chunks, sends them with sequence numbers, waits for ACKs, retransmits on timeout, and finishes with an EOF packet carrying the SHA-256 hash.
**reciever.py	
Listens on UDP port 9999, accepts in-order packets, discards duplicates (re-ACKing them), writes received_test.txt, then verifies the SHA-256 hash. (Filename spelling kept as in the project; consider renaming to receiver.py.)
**topology.py	
Mininet script: 2 hosts (h1, h2), 2 OVS switches (s1, s2), and two parallel links between the switches (Path A and Path B).
**topology.txt	
An earlier variant of the topology using a RemoteController and explicit interface names (s1-eth1, s1-eth2, ...).
**sdn_controller.py	
Demo "controller" that uses ovs-ofctl and ip link to simulate a failure on Path A and push a flow rule that sends traffic over Path B.
**received_test.txt	
Output file written by the receiver.
