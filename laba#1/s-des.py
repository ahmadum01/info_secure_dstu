import time
import tkinter as tk
import string


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("600x750")  # установка размеров окна
        self.master.title("S-DES")
        self.pack()
        self.create_widgets()
        self.s_des = SDES()

    def create_widgets(self):
        # форма ввода текста
        self.text_label = tk.Label(self, text="Введите текст:", font=("Arial", 16))  # установка размера шрифта
        self.text_label.pack(pady=10)  # установка вертикального отступа между формами
        self.text_input = tk.Text(self, height=10, width=50,
                                  font=("Arial", 14))  # установка размеров формы и размера шрифта
        self.text_input.pack()

        # форма ввода ключа
        self.key_label = tk.Label(self, text="Введите ключ:", font=("Arial", 16))
        self.key_label.pack(pady=10)
        self.key_input = tk.Entry(self, font=("Arial", 14))
        self.key_input.pack()
        # button to swap text and key inputs

        # форма вывода зашифрованного/расшифрованного текста
        self.output_label = tk.Label(self, text="Результат:", font=("Arial", 16))
        self.output_label.pack(pady=10)
        self.output_text = tk.Text(self, height=10, width=50, state="disabled", font=("Arial", 14))
        self.output_text.pack()
        self.hack_button = tk.Button(self, text="Взломать", font=("Arial", 16), command=self.hack)
        self.hack_button.pack()

        # кнопки зашифровать/расшифровать
        self.encrypt_button = tk.Button(self, text="Зашифровать", font=("Arial", 16), command=self.encrypt_text)
        self.encrypt_button.pack(side="left", padx=0)  # установка горизонтального отступа между кнопками
        self.swap_button = tk.Button(self, text="Swap", font=("Arial", 16), command=self.swap_inp_text_out_text)
        self.swap_button.pack(side="left", padx=60)
        self.decrypt_button = tk.Button(self, text="Расшифровать", font=("Arial", 16), command=self.decrypt_text)
        self.decrypt_button.pack(side="left", padx=0)

    def hack(self):
        max_score = 0  # Frequency analysis score
        max_score_key = ''
        for i in range(2 ** 10 - 1):  # Brute force of ASCII characters
            key = bin(i)[2:].zfill(10)
            self.key_input.delete('0', 'end')
            self.key_input.insert('0', key)
            self.decrypt_text()
            self.update()
            time.sleep(0.002)
            decrypted_text = self.output_text.get('1.0', 'end').strip()
            decrypted_text_score = self.get_text_score(decrypted_text)

            if decrypted_text_score > max_score:
                max_score = decrypted_text_score
                max_score_key = key
        self.key_input.delete('0', 'end')
        self.key_input.insert('0', max_score_key)
        self.decrypt_text()

    def get_text_score(self, text):
        score = 0
        for letter in text:
            if letter in 'ETAOINSHRDLUetaoinshrdlu ':  # The most frequent letters
                score += 3
            elif letter in string.ascii_letters:
                score += 2
            elif letter in '.!?,-\'0123456789':
                score += 1
        return score

    def swap_inp_text_out_text(self):
        out_text = self.output_text.get("1.0", "end-1c")
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.configure(state="disabled")
        self.text_input.delete("1.0", "end")
        self.text_input.insert("1.0", out_text)


    def encrypt_text(self):
        text = self.text_input.get("1.0", "end-1c")
        key = self.key_input.get()
        if key == '':
            key = self.s_des.generate_key(text)
            self.key_input.insert('0', key)
        encrypted_text = self.s_des.text_s_des_encrypt(text, key)
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", encrypted_text)
        self.output_text.configure(state="disabled")

    def decrypt_text(self):
        text = self.text_input.get("1.0", "end-1c")
        key = self.key_input.get()
        decrypted_text = self.s_des.text_s_des_decrypt(text, key)
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", decrypted_text)
        self.output_text.configure(state="disabled")


    def encrypt(self, text, key):
        encrypted_text = ""
        for i in range(len(text)):
            char = text[i]
            if char not in string.ascii_letters:
                encrypted_text += char
            else:
                key_char = key[i % len(key)]
                encrypted_char = chr((ord(char) + ord(key_char)) % 128)
                encrypted_text += encrypted_char
        return encrypted_text

    def decrypt(self, text, key):
        decrypted_text = ""
        for i in range(len(text)):
            char = text[i]
            if char not in string.ascii_letters:
                decrypted_text += char
            else:
                key_char = key[i % len(key)]
                decrypted_char = chr((ord(char) - ord(key_char)) % 128)
                decrypted_text += decrypted_char
        return decrypted_text


class SDES:
    P10 = (3, 5, 2, 7, 4, 10, 1, 9, 8, 6)
    P8 = (6, 3, 7, 4, 8, 5, 10, 9)
    P_START = (2, 6, 3, 1, 4, 8, 5, 7)
    P_FINISH = (4, 1, 3, 5, 7, 2, 8, 6)
    P_EXTENSION = (4, 1, 2, 3, 2, 3, 4, 1)
    S_BLOCK1 = (
        ('01', '00', '11', '10'),
        ('11', '10', '01', '00'),
        ('00', '10', '01', '11'),
        ('11', '01', '11', '10'),
    )
    S_BLOCK2 = (
        ('00', '01', '10', '11'),
        ('10', '00', '01', '11'),
        ('11', '00', '01', '00'),
        ('10', '01', '00', '11'),
    )
    DIRECT_PERMUTATION = (2, 4, 3, 1)

    def permutation(self, seq, pattern) -> str:
        return ''.join([seq[elem - 1] for elem in pattern])

    def shift(self, seq, step):
        return seq[step:] + seq[:step]

    def addition_modulo(self, seq1, seq2):
        return ''.join([str(int(el1 != el2)) for el1, el2 in zip(seq1, seq2)])

    def s_transformation(self, seq, pattern):
        column = int(seq[1:3], base=2)
        row = int(seq[::3], base=2)
        return pattern[row][column]

    def gen_2_keys(self, key) -> tuple[str, str]:
        p10_res = self.permutation(key, SDES.P10)
        left, right = self.shift(p10_res[:5], 1), self.shift(p10_res[5:], 1)
        first_key = self.permutation(left + right, SDES.P8)
        left, right = self.shift(left, 2), self.shift(right, 2)
        second_key = self.permutation(left + right, SDES.P8)
        return first_key, second_key

    def base_of_round(self, left, right, key):
        r_extended = self.permutation(right, SDES.P_EXTENSION)
        r_sum_modulo = self.addition_modulo(key, r_extended)
        s1_transformed = self.s_transformation(r_sum_modulo[:4], SDES.S_BLOCK1)
        s2_transformed = self.s_transformation(r_sum_modulo[4:], SDES.S_BLOCK2)
        s_transformed = s1_transformed + s2_transformed
        direct_permuted = self.permutation(s_transformed, SDES.DIRECT_PERMUTATION)
        return self.addition_modulo(direct_permuted, left)

    def first_round(self, inp, key):
        p_start = self.permutation(inp, SDES.P_START)
        left, right = p_start[:4], p_start[4:]
        base_of_round = self.base_of_round(left, right, key)
        return right + base_of_round

    def second_round(self, first_round_result, key):
        left, right = first_round_result[:4], first_round_result[4:]
        base_of_round = self.base_of_round(left, right, key)
        return base_of_round + right

    def s_des_encrypt(self, sym: str, key: str) -> str:
        sym = bin(ord(sym))[2:].zfill(8)
        key1, key2 = self.gen_2_keys(key)
        first_round_result = self.first_round(sym, key1)
        second_round_result = self.second_round(first_round_result, key2)
        return self.permutation(second_round_result, SDES.P_FINISH)

    def s_des_decrypt(self, inp: str, key: str) -> str:
        key2, key1 = self.gen_2_keys(key)
        first_round_result = self.first_round(inp, key1)
        second_round_result = self.second_round(first_round_result, key2)
        return self.permutation(second_round_result, SDES.P_FINISH)

    def text_s_des_encrypt(self, text: str, key: str) -> str:
        return ''.join(self.s_des_encrypt(sym, key) for sym in text)

    def text_s_des_decrypt(self, text: str, key: str) -> str:
        res = ''
        for i in range(len(text) // 8):
            sym = self.s_des_decrypt(text[i * 8: (i + 1) * 8], key)
            res += chr(int(sym, base=2))
        return res

    def generate_key(self, text: str):
        return bin(ord(text[0]))[2:].zfill(8) + bin(ord(text[0]))[2:].zfill(8)[:2]


if __name__ == "__main__":
    root = tk.Tk()
    app = App(master=root)
    app.mainloop()
