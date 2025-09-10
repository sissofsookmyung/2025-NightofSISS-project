def railfence_enc(text, key):
    if not text:
        return ''
    # 공백 제거 + 소문자
    chars = [c.lower() for c in text if c.isalpha()]

    if not all(c.isalpha() or c.isspace() for c in text):
        return "error: Plain text can only use alphabets and spaces."

    if key <= 0:
        return "error: Key must be a positive number."

    text_len = sum(1 for c in text if c.isalpha())
    if key < 2 or key >= text_len:
        return "error: Key must be smaller than the number of letters in the text."

    rails = [[] for _ in range(key)]
    rail = 0
    direction = 1  # 아래(+1) / 위(-1)

    for ch in chars:
        rails[rail].append(ch)
        # 현재 레일이 끝에 닿았는지 보고 방향 결정 후 이동
        if rail == 0:
            direction = 1
        elif rail == key - 1:
            direction = -1
        rail += direction

    return ''.join(''.join(r) for r in rails)


def railfence_dec(text, key):

    if not all(c.isalpha() or c.isspace() for c in text):
        return "error: Cipher text can only use alphabets and spaces."

    if key <= 0:
        return "error: Key must be a positive number."

    text_len = sum(1 for c in text if c.isalpha())
    if key < 2 or key >= text_len:
        return "error: Key must be smaller than the number of letters in the text."

    if not text:
        return ''
    # 공백 제거 + 소문자
    chars = [c.lower() for c in text if c.isalpha()]
    n = len(chars)


    # 각 문자가 어느 레일을 거치는지 기록(z)
    z = [0] * n
    rail = 0
    direction = 1
    for i in range(n):
        z[i] = rail
        if rail == 0:
            direction = 1
        elif rail == key - 1:
            direction = -1
        rail += direction

    # 각 레일에 몇 개 문자가 들어가는지 카운트
    rail_counts = [0] * key
    for r in z:
        rail_counts[r] += 1

    # 암호문을 레일별로 잘라 채워 넣기
    rails = [[] for _ in range(key)]
    idx = 0
    for i in range(key):
        for _ in range(rail_counts[i]):
            rails[i].append(chars[idx])
            idx += 1

    # z 순서대로 레일에서 문자를 꺼내 원문 복원
    result = []
    rail_pos = [0] * key
    for r in z:
        result.append(rails[r][rail_pos[r]])
        rail_pos[r] += 1

    return ''.join(result)

if __name__ == "__main__":
    mod = input("Select either ENC or DEC:  ").upper()
    if mod == 'ENC':
        text = input("Plaintext: ")
        if not all(c.isalpha() or c.isspace() for c in text):
            print("error: Plain text can only use alphabets and spaces.")
            exit()

        key_input = input("Key: ")
        if not key_input.isdigit():
            print("error: Key must be a positive number.")
            exit()
        key = int(key_input)

        # 공백 제외 실제 글자 수 기준
        text_len = sum(1 for c in text if c.isalpha())
        if key < 2 or key >= text_len:
            print("error: Key must be smaller than the number of letters in the text.")
            exit()

        enc = railfence_enc(text, key)
        print("ENC: " + enc)

    elif mod == 'DEC':
        text = input("암호문: ")
        if not all(c.isalpha() or c.isspace() for c in text):
            print("error: Cipher text can only use alphabets and spaces.")
            exit()

        key_input = input("Key: ")
        if not key_input.isdigit():
            print("error: Key must be a positive number.")
            exit()
        key = int(key_input)

        text_len = sum(1 for c in text if c.isalpha())
        if key < 2 or key >= text_len:
            print("error: Key must be smaller than the number of letters in the text.")
            exit()

        dec = railfence_dec(text, key)
        print("DEC: " + dec)

    else:
        print("error: Select either ENC or DEC")
