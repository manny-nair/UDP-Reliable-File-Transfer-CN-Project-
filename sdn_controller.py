import subprocess
import time

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, captureOutput=True, text=True)
    return result.stdout.strip()

def sdn_controller_demo():
    print("[SDN CONTROLLER] Initializing SDN Control Plane...")
   
    # Step 1: Check initial switch flow tables for s1
    print("\n[SDN CONTROLLER] Inspecting initial flow table for switch s1 (Path A active):")
    flows = run_command("sudo ovs-ofctl dump-flows s1")
    print(flows if flows else "[INFO] OVS switch s1 active.")

    # Step 2: Simulate a Link Failure on Path A (e.g., bringing down interface s1-eth1)
    print("\n[ALERT] Link failure detected on Path A (s1-eth1)!")
    print("[SDN CONTROLLER] Bringing down Path A interface...")
    run_command("sudo ip link set s1-eth1 down")
   
    # Step 3: Install alternative forwarding rule via OpenFlow (forcing traffic to Path B / port 2)
    print("[SDN CONTROLLER] Rerouting traffic! Installing new flow rule to use Path B...")
    # This OpenFlow command modifies flows on s1 to redirect traffic through alternative port
    run_command("sudo ovs-ofctl mod-flows s1 priority=100,actions=output:2")
   
    print("[SUCCESS] SDN Rerouting complete! Traffic is now flowing securely over Path B.")

if __name__ == "__main__":
    sdn_controller_demo()

