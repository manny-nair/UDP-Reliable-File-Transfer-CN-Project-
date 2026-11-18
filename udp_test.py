import socket


def run_udp_test():
    # Create a UDP socket (IPv4, UDP)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to localhost and port 9999
    server_address = ("127.0.0.1", 9999)
    sock.bind(server_address)
    print(f"[INFO] UDP Server bound to {server_address}")

    # Send a message to ourselves (loopback test)
    message = b"Hello, UDP networking!"
    print(f"[INFO] Sending message: {message}")
    sock.sendto(message, server_address)

    # Receive the message
    data, address = sock.recvfrom(1024)  # buffer size 1024 bytes
    print(
        f"[SUCCESS] Received {len(data)} bytes from {address}: {data.decode('utf-8')}"
    )

    sock.close()


if __name__ == "__main__":
    run_udp_test()
