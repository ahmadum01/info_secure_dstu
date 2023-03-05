from random import sample
from functools import lru_cache
from decimal import Decimal


class RSA:
    def __init__(self):
        self.first_pn, self.second_pn = self.get_random_prime_numbers(2)
        self.open_key = self.first_pn * self.second_pn
        self.fi = (self.first_pn - 1) * (self.second_pn - 1)
        self.open_exponent = self.get_open_exponent()
        self.secret_exponent = self.get_secret_exponent()
        self.block_length = len(hex(self.open_key)[2:])

    @lru_cache()
    def is_prime(self, n):
        if n % 2 == 0:
            return n == 2
        d = 3
        while d * d <= n and n % d != 0:
            d += 2
        return d * d > n

    def get_prime_numbers(self, quantity, from_):
        result = []
        i = from_
        while len(result) != quantity:
            if self.is_prime(i):
                result.append(i)
            i += 1
        return result

    def get_random_prime_numbers(self, quantity=1):
        return sample(self.get_prime_numbers(100, 100), quantity)

    def get_open_exponent(self):
        prime_numbers = self.get_prime_numbers(50, 3)
        for pn in prime_numbers:
            if self.fi % pn != 0:
                return pn

    def get_secret_exponent(self):
        k = 1
        while True:
            d = Decimal(self.fi * k + 1) / self.open_exponent
            if d.as_tuple().exponent == 0:
                return int(d)
            k += 1

    def encrypt_sym(self, sym):
        unicode = ord(sym)
        encrypted_sym = unicode ** self.open_exponent % self.open_key
        return hex(encrypted_sym)[2:].zfill(self.block_length)

    def decrypt_sym(self, encrypted_hex_sym):
        encrypted_sym = int(encrypted_hex_sym, base=16)
        unicode = encrypted_sym ** self.secret_exponent % self.open_key
        return chr(unicode)

    def encrypt(self, text):
        return "".join(self.encrypt_sym(sym) for sym in text)

    def decrypt(self, text):
        res = ''
        for i in range(len(text) // self.block_length):
            encrypted_hex_sym = text[i * self.block_length: (i + 1) * self.block_length]
            res += self.decrypt_sym(encrypted_hex_sym)
        return res

    def show_my_data(self):
        print(
            f"Open key: ({self.open_exponent} {self.open_key})",
            f"Secret key: ({self.secret_exponent} {self.open_key})",
            sep="\n",
        )

    def main(self):
        # self.show_my_data()
        while (option := input(
                "\nOptions:\n"
                "1) encrypt\n"
                "2) decrypt\n"
                "3) update keys\n"
                "4) show keys\n")) in "1234":
            if option == "1":
                self.first_pn, self.second_pn = int(input("p:")), int(input("q:"))
                self.show_my_data()
                text = input("Input text: ")
                print(self.encrypt(text))
            elif option == "2":
                encrypted_text = input("Input encrypted text: ")
                print(self.decrypt(encrypted_text))
            elif option == "3":
                self.__init__()
                self.show_my_data()
            elif option == '4':
                self.show_my_data()
        print("Bye!")


if __name__ == '__main__':
    rsa = RSA()
    rsa.main()

