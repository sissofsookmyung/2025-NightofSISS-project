import socket
import base64
import threading
import os
from base64 import b64encode, b64decode
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox
import hashlib
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


# === RSA 키쌍 생성 ===
def load_or_create_keys():
    if os.path.exists("private.pem") and os.path.exists("public.pem"):
        with open("private.pem", "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
        with open("public.pem", "rb") as f:
            public_pem = f.read()
        public_key = private_key.public_key()
    else:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        with open("private.pem", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
        with open("public.pem", "wb") as f:
            f.write(public_pem)
    return private_key, public_key, public_pem
#key check
def key_fp(pem_bytes: bytes) -> str:
    d = hashlib.sha256(pem_bytes).digest()
    return ":".join(f"{b:02x}" for b in d[:8])
# === GUI 클라이언트 클래스 ===
class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("E2EE Chat Client")

        self.chat_area = scrolledtext.ScrolledText(master, state='disabled', wrap=tk.WORD)
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.input_entry = tk.Entry(master)
        self.input_entry.pack(padx=10, pady=(0, 10), fill=tk.X)
        self.input_entry.bind("<Return>", self.send_message)

    
        self.private_key, self.public_key, self.public_pem = load_or_create_keys()
        self.peer_public_key = None
        
        self.log(f"My key fp: {key_fp(self.public_pem)}")

        # 네트워크 초기화
        self.server_ip = simpledialog.askstring("서버 IP", "서버 IP 입력", initialvalue="localhost")
        self.server_port = int(simpledialog.askstring("포트 번호", "서버 포트 입력", initialvalue="12345"))
        self.username = simpledialog.askstring("이름", "사용자 이름 입력", initialvalue="익명")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.server_ip, self.server_port))
        self.sock.sendall(self.public_pem)

        # 수신 스레드 시작
        threading.Thread(target=self.receive, daemon=True).start()

    def log(self, msg):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, msg + "\n")
        self.chat_area.yview(tk.END)
        self.chat_area.config(state='disabled')

    def send_message(self, event=None):
        msg = self.input_entry.get()
        self.input_entry.delete(0, tk.END)

        if not msg.strip():
            return

        full_msg = f"[{self.username}] {msg}".encode()
        self.log(f"[me] {msg}")
        
        # AES 키 및 IV 생성
        aes_key = os.urandom(32)
        iv = os.urandom(16)
        # AES 암호화
        cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
        encryptor = cipher.encryptor()
        ct = encryptor.update(full_msg) + encryptor.finalize()
        
        self.log(f"AES ciphertext (Base64) : {base64.b64encode(ct).decode()}")
        
        # AES 키를 RSA로 암호화
        enc_key = self.peer_public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        self.log (f"RSA-encrypted AES key (Base64) : {base64.b64encode(enc_key).decode()}")
        # 전송 패킷 구성
        payload = b'\n\n'.join([
            b64encode(enc_key),
            b64encode(iv + ct)
        ])

        try:
            self.sock.sendall(payload)
            self.log("Ciphertext sent")
        except Exception as e:
            self.log(f"[전송 실패] {e}")

    def receive(self):
        while True:
            try:
                data = self.sock.recv(8192)
                if not data:
                    break

                if data.startswith(b'KEY:'):
                    peer_pem = data[4:].strip()
                    self.peer_public_key = serialization.load_pem_public_key(peer_pem)
                    self.log(f"상대방의 RSA 공개키를 받았습니다.fp={key_fp(peer_pem)}")
                else:
                    try:
                        enc_key_b64, ciphertext_b64 = data.split(b'\n\n', 1)
                        aes_key = self.private_key.decrypt(
                            b64decode(enc_key_b64),
                            padding.OAEP(
                                mgf=padding.MGF1(hashes.SHA256()),
                                algorithm=hashes.SHA256(),
                                label=None
                            )
                        )
                        iv_ct = b64decode(ciphertext_b64)
                        iv, ct = iv_ct[:16], iv_ct[16:]
                        cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
                        decryptor = cipher.decryptor()
                        msg = decryptor.update(ct) + decryptor.finalize()
                        self.log(f"[수신] {msg.decode()}")
                    except Exception as e:
                        self.log(f"[복호화 오류] {e}")

            except Exception as e:
                self.log(f"[수신 오류] {e}")
                break


# === 실행 ===
if __name__ == '__main__':
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()


