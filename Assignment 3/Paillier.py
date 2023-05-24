import random
from math import gcd

class Paillier:
    def __init__(self, k):
        self.k = k
        self.p, self.q = self.generate_primes()
        self.n = self.p * self.q
        self.g = self.calculate_generator()

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

    def calculate_generator(self):
        def lcm(a, b):
            return abs(a * b) // gcd(a, b)

        def find_primitive_root(p, q):
            n = p * q
            phi_n = lcm(p - 1, q - 1)
            g = random.randint(1, n - 1)
            while gcd(g, n) != 1 or pow(g, phi_n, n ** 2) == 1:
                g = random.randint(1, n - 1)
            return g

        return find_primitive_root(self.p, self.q)

    def get_public_key(self):
        return self.n, self.g

    def encrypt(self, plaintext):
        plaintext_int = int.from_bytes(plaintext, 'big')
        if plaintext_int >= self.n:
            raise ValueError("Plaintext too large for encryption")

        r = random.randint(1, self.n - 1)
        ciphertext_int = (pow(self.g, plaintext_int, self.n ** 2) * pow(r, self.n, self.n ** 2)) % (self.n ** 2)
        ciphertext = ciphertext_int.to_bytes((ciphertext_int.bit_length() + 7) // 8, 'big')
        return ciphertext

    def decrypt(self, ciphertext):
        ciphertext_int = int.from_bytes(ciphertext, 'big')
        if not self.is_ciphertext_valid(ciphertext_int):
            raise ValueError("Invalid ciphertext")

        phi_n = (self.p - 1) * (self.q - 1)
        lambda_n = phi_n // gcd(self.p - 1, self.q - 1)
        mu = pow(self.g, lambda_n, self.n ** 2) - 1
        plaintext_int = ((pow(ciphertext_int, lambda_n, self.n ** 2) - 1) // self.n * mu) % self.n
        plaintext = plaintext_int.to_bytes((plaintext_int.bit_length() + 7) // 8, 'big')
        return plaintext

    def is_ciphertext_valid(self, ciphertext_int):
        return ciphertext_int >= 0 and ciphertext_int < self.n ** 2
