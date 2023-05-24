import random
from math import gcd

class RSA:
    def __init__(self, k, e=65537):
        self.k = k
        self.e = e
        self.p, self.q = self.generate_primes()
        self.N = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.d = self.calculate_private_key()

    def generate_primes(self):
        while True:
            p = random.randint(2**(self.k-1), 2**self.k - 1)
            if self.is_prime(p):
                break

        while True:
            q = random.randint(2**(self.k-1), 2**self.k - 1)
            if self.is_prime(q) and q != p:
                break

        return p, q

    def is_prime(self, n, k=10):
        if n <= 1:
            return False

        for _ in range(k):
            a = random.randint(2, n - 1)
            if pow(a, n - 1, n) != 1:
                return False

        return True

    def calculate_private_key(self):
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            else:
                g, x, y = extended_gcd(b % a, a)
                return g, y - (b // a) * x, x

        _, d, _ = extended_gcd(self.e, self.phi)
        return d % self.phi

    def get_public_key(self):
        return self.N, self.e

    def encrypt(self, plaintext):
        plaintext_int = int.from_bytes(plaintext, 'big')
        if plaintext_int >= self.N:
            raise ValueError("Plaintext too large for encryption")

        ciphertext_int = pow(plaintext_int, self.e, self.N)
        ciphertext = ciphertext_int.to_bytes((ciphertext_int.bit_length() + 7) // 8, 'big')
        return ciphertext

    def decrypt(self, ciphertext):
        ciphertext_int = int.from_bytes(ciphertext, 'big')
        if ciphertext_int >= self.N:
            raise ValueError("Ciphertext too large for decryption")

        plaintext_int = pow(ciphertext_int, self.d, self.N)
        plaintext = plaintext_int.to_bytes((plaintext_int.bit_length() + 7) // 8, 'big')
        return plaintext
