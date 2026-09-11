import random
import time
import base64
import matplotlib.pyplot as plt

def generate_super_increasing(z):
    sequence = []
    sum_so_far = 0
    for i in range(z - 1):
        num = random.randint(1, 1000) + sum_so_far
        sequence.append(num)
        sum_so_far += num
    senior = 2**100 + random.randint(0, 1000)
    sequence.append(senior)
    return sequence

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return None
    return (x % m + m) % m

def generate_public_key(private_key, a, n):
    return [(di * a) % n for di in private_key]

def encrypt_char(char, public_key, encoding):
    if encoding == 'Base64':
        base64_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        try:
            binary = format(base64_chars.index(char), '06b').zfill(len(public_key))
        except ValueError:
            return None
    else:  # ASCII
        binary = format(ord(char), '08b').zfill(len(public_key))
    return sum(pk for i, pk in enumerate(public_key) if binary[i] == '1')

def decrypt_char(cipher, private_key, a_inv, n, encoding):
    s = (cipher * a_inv) % n
    binary = ''
    for di in reversed(private_key):
        if s >= di:
            binary = '1' + binary
            s -= di
        else:
            binary = '0' + binary
    if encoding == 'Base64':
        base64_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        return base64_chars[int(binary, 2)]
    else:
        return chr(int(binary, 2))

def run_experiment(fio, encoding, z, runs=10):
    if encoding == 'Base64':
        base64_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        fio = base64.b64encode(fio.encode()).decode().rstrip('=')
        if not all(c in base64_chars for c in fio):
            return None, None, None, None, None, None
    elif z < 8:
        return None, None, None, None, None, None  # ASCII требует z >= 8

    encrypt_times = []
    decrypt_times = []
    private_key, public_key, encrypted, decrypted = None, None, None, None

    for _ in range(runs):
        private_key = generate_super_increasing(z)
        n = sum(private_key) + 1000
        a = random.randint(1, 1000)
        while gcd(a, n) != 1:
            a = random.randint(1, 1000)
        a_inv = mod_inverse(a, n)
        public_key = generate_public_key(private_key, a, n)

        start_time = time.time()
        encrypted = []
        for c in fio:
            cipher = encrypt_char(c, public_key, encoding)
            if cipher is None:
                return None, None, None, None, None, None
            encrypted.append(cipher)
        encrypt_times.append(time.time() - start_time)

        start_time = time.time()
        decrypted = ''.join(decrypt_char(c, private_key, a_inv, n, encoding) for c in encrypted)
        decrypt_times.append(time.time() - start_time)

    encrypt_time = sum(encrypt_times) / runs
    decrypt_time = sum(decrypt_times) / runs

    return encrypt_time, decrypt_time, private_key, public_key, encrypted, decrypted

def plot_performance(results):
    base64_z = [res['z'] for res in results if res['encoding'] == 'Base64']
    base64_encrypt = [res['encrypt_time'] for res in results if res['encoding'] == 'Base64']
    base64_decrypt = [res['decrypt_time'] for res in results if res['encoding'] == 'Base64']
    ascii_z = [res['z'] for res in results if res['encoding'] == 'ASCII']
    ascii_encrypt = [res['encrypt_time'] for res in results if res['encoding'] == 'ASCII']
    ascii_decrypt = [res['decrypt_time'] for res in results if res['encoding'] == 'ASCII']

    # График для шифрования
    plt.figure(figsize=(10, 6))
    plt.plot(base64_z, base64_encrypt, marker='o', label='Base64 Encryption')
    plt.plot(ascii_z, ascii_encrypt, marker='s', label='ASCII Encryption')
    plt.xlabel('Key Length (z)')
    plt.ylabel('Time (seconds)')
    plt.title('Encryption Time vs Key Length')
    plt.grid(True)
    plt.legend()
    plt.savefig('encryption_time.png')
    plt.close()

    # График для расшифрования
    plt.figure(figsize=(10, 6))
    plt.plot(base64_z, base64_decrypt, marker='o', label='Base64 Decryption')
    plt.plot(ascii_z, ascii_decrypt, marker='s', label='ASCII Decryption')
    plt.xlabel('Key Length (z)')
    plt.ylabel('Time (seconds)')
    plt.title('Decryption Time vs Key Length')
    plt.grid(True)
    plt.legend()
    plt.savefig('decryption_time.png')
    plt.close()

def main():
    while True:
        print("\nKnapsack Cipher Console Application")
        print("1. Generate Keys, Encrypt, and Decrypt")
        print("2. Analyze Performance")
        print("3. Exit")
        choice = input("Select an option (1-3): ")

        if choice == '3':
            break

        fio = input("Enter Full Name (ФИО, e.g., Puzyrova Hanna Sergeeyna): ")
        if not fio:
            print("Error: Full Name is required")
            continue

        encoding = input("Select encoding (Base64/ASCII): ")
        if encoding not in ['Base64', 'ASCII']:
            print("Error: Choose Base64 or ASCII")
            continue

        if choice == '1':
            try:
                z = int(input("Enter key length (z, min 6 for Base64, 8 for ASCII): "))
                if z < (6 if encoding == 'Base64' else 8):
                    print(f"Error: z must be at least {'6' if encoding == 'Base64' else '8'} for {encoding}")
                    continue
            except ValueError:
                print("Error: Invalid key length (z)")
                continue

            encrypt_time, decrypt_time, private_key, public_key, encrypted, decrypted = run_experiment(fio, encoding, z)
            if encrypt_time is None:
                print(f"Error: Invalid characters for {encoding} encoding or z too small")
                continue

            print(f"\nPrivate Key: {private_key}")
            print(f"Public Key: {public_key}")
            print(f"Encrypted Message: {encrypted}")
            print(f"Decrypted Message: {decrypted}")
            print(f"Encryption Time: {encrypt_time:.6f} seconds")
            print(f"Decryption Time: {decrypt_time:.6f} seconds")

        elif choice == '2':
            encodings = ['Base64', 'ASCII']
            z_values = [6, 8, 20, 30, 40, 50, 60, 70, 80]
            results = []

            print("\nPerformance Analysis")
            print("FIO:", fio)
            print("----------------------------------------")
            for encoding in encodings:
                for z in z_values:
                    if encoding == 'ASCII' and z < 8:
                        continue
                    encrypt_time, decrypt_time, _, _, _, _ = run_experiment(fio, encoding, z)
                    if encrypt_time is None:
                        print(f"Error: Invalid characters for {encoding}, z={z}")
                        continue
                    results.append({
                        'encoding': encoding,
                        'z': z,
                        'encrypt_time': encrypt_time,
                        'decrypt_time': decrypt_time
                    })
                    print(f"Encoding: {encoding}, z={z}")
                    print(f"Encryption Time: {encrypt_time:.6f} seconds")
                    print(f"Decryption Time: {decrypt_time:.6f} seconds")
                    print("----------------------------------------")

            print("\nResults Table:")
            print("| Encoding | z  | Encryption Time (s) | Decryption Time (s) |")
            print("|----------|----|---------------------|---------------------|")
            for res in results:
                print(f"| {res['encoding']:<8} | {res['z']:<2} | {res['encrypt_time']:.6f} | {res['decrypt_time']:.6f} |")

            plot_performance(results)

if __name__ == "__main__":
    main()