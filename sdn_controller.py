"""
Monitoring SDN controller

Runs continuously. Installs Path A, then watches the link state. When the
active path's link goes down, it automatically reprograms s1 and s2 with
OpenFlow rules (via ovs-ofctl) to use the other path.

Works with your original topology.py (link order sets the ports):
  s1: port 1 = h1,  port 2 = Path A (s1-eth2), port 3 = Path B (s1-eth3)
  s2: port 1 = Path A, port 2 = Path B, port 3 = h2

Run (as root):  sudo python3 monitor_controller.py
"""
import subprocess
import time

PATHS = {
    "A": {"s1": 2, "s2": 1, "iface": "s1-eth2"},
    "B": {"s1": 3, "s2": 2, "iface": "s1-eth3"},
}
HOST_PORT = {"s1": 1, "s2": 3}
POLL_SECONDS = 0.2


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] [SDN CONTROLLER] {msg}", flush=True)


def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode != 0:
        log(f"Command failed: {cmd}\n    {r.stderr.strip()}")
    return r.stdout.strip()


def link_up(iface):
    """True if the interface exists and its operational state is 'up'."""
    try:
        with open(f"/sys/class/net/{iface}/operstate") as f:
            return f.read().strip() == "up"
    except FileNotFoundError:
        return False


def install_path(name):
    p = PATHS[name]
    for sw in ("s1", "s2"):
        run(f"ovs-ofctl del-flows {sw}")
    # s1: h1 <-> chosen inter-switch port
    run(f"ovs-ofctl add-flow s1 priority=100,in_port={HOST_PORT['s1']},actions=output:{p['s1']}")
    run(f"ovs-ofctl add-flow s1 priority=100,in_port={p['s1']},actions=output:{HOST_PORT['s1']}")
    # s2: chosen inter-switch port <-> h2
    run(f"ovs-ofctl add-flow s2 priority=100,in_port={p['s2']},actions=output:{HOST_PORT['s2']}")
    run(f"ovs-ofctl add-flow s2 priority=100,in_port={HOST_PORT['s2']},actions=output:{p['s2']}")
    log(f"Installed Path {name} on s1 and s2")


def main():
    active = "A"
    log("Starting controller")
    install_path(active)
    log("Monitoring links. Press Ctrl+C to stop.")

    while True:
        if not link_up(PATHS[active]["iface"]):
            other = "B" if active == "A" else "A"
            log(f"ALERT: link failure on Path {active} ({PATHS[active]['iface']})")
            if link_up(PATHS[other]["iface"]):
                log(f"REROUTING: Path {active} -> Path {other}")
                install_path(other)
                active = other
                log("Reroute complete")
            else:
                log("Both paths are down! Waiting...")
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("Stopped")
