# server.py
import socket
import threading

# 연결된 클라이언트: {addr: (conn, 공개키)}
clients = {}

# 1:1 채팅만 지원 (최대 2명)
MAX_CLIENTS = 2

# 클라이언트 처리 스레드
def handle_client(conn, addr):
    print(f"※ 새 연결: {addr}")

    # 접속자 수 초과 시 거절
    if len(clients) >= MAX_CLIENTS:
        try:
            conn.sendall("[SERVER] 최대 접속자 수(2명) 초과. 연결 종료\n".encode('utf-8'))
        except:
            pass
        conn.close()
        print(f"[-] {addr} 연결 종료 (접속 제한)")
        return

    try:
        # 클라이언트로부터 공개키 수신
        peer_pubkey_pem = conn.recv(4096)
        if not peer_pubkey_pem:
            print(f"[!] {addr} 공개키 수신 실패")
            conn.close()
            return

        clients[addr] = (conn, peer_pubkey_pem)
        print(f"[KEY] {addr} 공개키 수신 완료")

        # 이미 연결된 클라이언트들과 공개키 교환
        for other_addr, (other_conn, other_key) in clients.items():
            if other_addr != addr:
                try:
                    other_conn.sendall(b'KEY:' + peer_pubkey_pem + b'\n\n')
                    conn.sendall(b'KEY:' + other_key + b'\n\n')
                except Exception as e:
                    print(f"[!] 공개키 전파 실패: {e}")

        # 메시지 릴레이
        while True:
            data = conn.recv(8192)
            if not data:
                break

            for other_addr, (other_conn, _) in list(clients.items()):
                if other_conn != conn:
                    try:
                        other_conn.sendall(data)
                    except Exception as e:
                        print(f"[!] {other_addr} 메시지 전송 실패: {e}")

    except Exception as e:
        print(f"[!] {addr} 처리 중 오류: {e}")

    finally:
        print(f"[-] {addr} 연결 종료")
        with threading.Lock():
            if addr in clients:
                del clients[addr]
        conn.close()

# 서버 실행
if __name__ == "__main__":
    host, port = 'localhost', 12345
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen()

    print(f"[SERVER] 실행 중: {host}:{port}")

    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\n[SERVER] 종료 중...")
    finally:
        server.close()


