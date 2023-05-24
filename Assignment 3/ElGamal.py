import random

class ElGamal:
    def __init__(self, g, p):
        self.g = g
        self.p = p
        self.x = random.randint(1, p - 1)
        self.h = pow(g, self.x, p)

    def get_public_key(self):
        return self.p, self.g, self.h

    def encrypt(self, plaintext):
        plaintext_int = int.from_bytes(plaintext, 'big')
        if plaintext_int >= self.p:
            raise ValueError("Plaintext too large for encryption")

        y = random.randint(1, self.p - 1)
        c1 = pow(self.g, y, self.p)
        c2 = (pow(self.h, y, self.p) * plaintext_int) % self.p
        return c1.to_bytes((c1.bit_length() + 7) // 8, 'big') + c2.to_bytes((c2.bit_length() + 7) // 8, 'big')

    def decrypt(self, ciphertext):
        c1_bytes = ciphertext[:len(ciphertext) // 2]
        c2_bytes = ciphertext[len(ciphertext) // 2:]
        c1 = int.from_bytes(c1_bytes, 'big')
        c2 = int.from_bytes(c2_bytes, 'big')
        plaintext_int = (c2 * pow(c1, self.p - 1 - self.x, self.p)) % self.p
        plaintext = plaintext_int.to_bytes((plaintext_int.bit_length() + 7) // 8, 'big')
        return plaintext
