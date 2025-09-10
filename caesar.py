def makeDisk(key_shift):
    enc_disk_upper = {}
    dec_disk_upper = {}
    enc_disk_lower = {}
    dec_disk_lower = {}

    for i in range(26):
        enc_i = (i + key_shift) % 26
        enc_disk_upper[chr(i + 65)] = chr(enc_i + 65)
        dec_disk_upper[chr(enc_i + 65)] = chr(i + 65)

        enc_i = (i + key_shift) % 26
        enc_disk_lower[chr(i + 97)] = chr(enc_i + 97)
        dec_disk_lower[chr(enc_i + 97)] = chr(i + 97)

    return (enc_disk_upper, enc_disk_lower), (dec_disk_upper, dec_disk_lower)


def caesar(msg, key, mode):
    ret = ''

    if mode not in ("ENC", "DEC"):
        return "Error: Select either ENC or DEC."

    if mode == "ENC" and not all(c.isalpha() or c.isspace() for c in msg):
        return "Error: Plain text can only use alphabets and spaces."
    if mode == "DEC" and not all(c.isalpha() or c.isspace() for c in msg):
        return "Error: Cipher text can only use alphabets and spaces."

    if not key.isdigit():
        return "Error: Key must be a number."

    k = int(key) % 26
    (enc_upper, enc_lower), (dec_upper, dec_lower) = makeDisk(k)

    if mode == "ENC":
        upper_map, lower_map = enc_upper, enc_lower
    else:
        upper_map, lower_map = dec_upper, dec_lower

    for c in msg:
        if c in upper_map:
            ret += upper_map[c]
        elif c in lower_map:
            ret += lower_map[c]
        else:
            ret += c

    return ret


def main():
    mode = input("Select either ENC or DEC: ").strip().upper()

    if mode not in ("ENC", "DEC"):
        print("Select either ENC or DEC.")
        return

    msg = input("Text: ").strip()
    key = input("Key (number): ").strip()

    result = caesar(msg, key, mode)
    if result:
        print(f"{mode}:", result)


if __name__ == "__main__":
    main()