def vigenere_encrypt(plaintext, key):
    if not key.isalpha():
        return "Error: Key values can only use alphabets."

    ciphertext = ''
    key = key.upper()
    key_len = len(key)
    key_index = 0

    for char in plaintext:
        if char.isalpha():
            shift = ord(key[key_index % key_len]) - ord('A')
            if char.isupper():
                base = ord('A')
                enc_char = chr((ord(char) - base + shift) % 26 + base)
            else:
                base = ord('a')
                enc_char = chr((ord(char) - base + shift) % 26 + base)
            ciphertext += enc_char
            key_index += 1
        else:
            ciphertext += char
    return ciphertext


def vigenere_decrypt(ciphertext, key):
    if not key.isalpha():
        return "Error: Key values can only use alphabets."

    plaintext = ''
    key = key.upper()
    key_len = len(key)
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index % key_len]) - ord('A')
            if char.isupper():
                base = ord('A')
                dec_char = chr((ord(char) - base - shift + 26) % 26 + base)
            else:
                base = ord('a')
                dec_char = chr((ord(char) - base - shift + 26) % 26 + base)
            plaintext += dec_char
            key_index += 1
        else:
            plaintext += char
    return plaintext


def vigenere(msg, key, mode):

    # mode 검증
    if mode not in ("ENC", "DEC"):
        return "Error: Select either ENC or DEC."

    # 텍스트 검증
    if not all(c.isalpha() or c.isspace() for c in msg):
        if mode == "ENC":
            return "Error: Plain text can only use alphabets and spaces."
        else:
            return "Error: Cipher text can only use alphabets and spaces."

    # key 검증
    if not key.isalpha():
        return "Error: Key values can only use alphabets."

    if len(key) >= len(msg.replace(" ", "")):
        return "Error: Key must be shorter than text length."

    if mode == "ENC":
        return vigenere_encrypt(msg, key)
    else:
        return vigenere_decrypt(msg, key)
