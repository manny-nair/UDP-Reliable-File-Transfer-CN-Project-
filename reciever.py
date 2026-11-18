import hashlib
import socket


def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.digest()


def run_receiver_with_integrity():
    host = "0.0.0.0"
    port = 9999

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"[RECEIVER] Integrity-Checking Receiver listening on {host}:{port}...")

    output_file_path = "received_test.txt"
    expected_seq = 0
    received_hash = None

    with open(output_file_path, "wb") as f:
        while True:
            packet, addr = sock.recvfrom(2048)
            seq_num = int.from_bytes(packet[:4], "big")
            pkt_type = packet[4:5].decode("utf-8")

            if pkt_type == "E":
                # Extract the 32-byte SHA-256 hash attached to the EOF packet
                received_hash = packet[5:]
                print(
                    f"[RECEIVER] End-of-file received. Sender's Hash: {received_hash.hex()}"
                )

                ack_packet = seq_num.to_bytes(4, "big") + b"A"
                sock.sendto(ack_packet, addr)
                break

            if seq_num == expected_seq:
                payload = packet[5:]
                f.write(payload)
                print(f"[RECEIVER] Accepted packet {seq_num}")

                ack_packet = seq_num.to_bytes(4, "big") + b"A"
                sock.sendto(ack_packet, addr)
                expected_seq += 1
            elif seq_num < expected_seq:
                ack_packet = seq_num.to_bytes(4, "big") + b"A"
                sock.sendto(ack_packet, addr)

    sock.close()

    # Verify SHA-256 Integrity
    if received_hash:
        computed_hash = calculate_sha256(output_file_path)
        print(f"[VERIFICATION] Computed File SHA-256: {computed_hash.hex()}")

        if computed_hash == received_hash:
            print("[SUCCESS] SHA-256 Hash matches perfectly! File integrity verified.")
        else:
            print("[ERROR] Hash mismatch! File is corrupted.")


if __name__ == "__main__":
    run_receiver_with_integrity()
