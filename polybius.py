def polybius_enc(text):  # 암호화 함수
    polybius_sq = [  # 폴리비우스 암호를 위한 알파벳 2차원 배열
        ['a', 'b', 'c', 'd', 'e'],
        ['f', 'g', 'h', 'i(j)', 'k'],
        ['l', 'm', 'n', 'o', 'p'],
        ['q', 'r', 's', 't', 'u'],
        ['v', 'w', 'x', 'y', 'z']
    ]

    if text.isdigit():
        return "error: Plain text can only use alphabets and spaces."

    text = text.lower()
    rows = []
    cols = []

    for char in text:
        if char.isalpha():
            for i, row in enumerate(polybius_sq):
                for j, c in enumerate(row):
                    if char in c:
                        rows.append(str(i + 1))
                        cols.append(str(j + 1))
                        break
        elif char.isspace():
            pass
        else:
            return "error: Plain text can only use alphabets and spaces."




    return ''.join(rows + cols)



def polybius_dec(cipher):  # 복호화 함수
    polybius_sq = [
        ['a', 'b', 'c', 'd', 'e'],
        ['f', 'g', 'h', 'i(j)', 'k'],
        ['l', 'm', 'n', 'o', 'p'],
        ['q', 'r', 's', 't', 'u'],
        ['v', 'w', 'x', 'y', 'z']
    ]


    cipher = cipher.replace(" ", "")  # 공백 제거

    if not cipher.isdigit():
        return "error: The encrypted text can only contain numbers and spaces."

    text = []
    rows = cipher[:len(cipher) // 2]
    cols = cipher[len(cipher) // 2:]

    for r, c in zip(rows, cols):
        row = int(r) - 1
        col = int(c) - 1
        char = polybius_sq[row][col]
        text.append(char[0])  # ij일 경우 i로 처리

    return  ''.join(text)

if __name__ == "__main__":
    mode = input("Select either ENC or DEC: ")
    if mode.upper() == "ENC":
        text = input("Plaintext: ")
        print(polybius_enc(text))
    elif mode.upper() == "DEC":
        cipher_in = input("Ciphertext: ")
        print(polybius_dec(cipher_in))
    else:
        print("error: Select either ENC or DEC")