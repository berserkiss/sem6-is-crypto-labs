# Information Security Coursework

Labs covering classical and modern cryptography: entropy, classical ciphers, DES,
stream ciphers, public-key cryptosystems (RSA, ElGamal, Schnorr, knapsack), hashing,
and text steganography.

## Structure

| Folder | Topic |
| --- | --- |
| `L2/` | Shannon entropy of text (C#) |
| `L3/` | Number theory helpers, GCD and modular arithmetic (C#) |
| `L4/` | Trithemius cipher and letter-frequency analysis |
| `L5/` | Route transposition cipher and frequency histograms |
| `L6/` | Enigma machine simulation |
| `L7/` | DES encryption and weak/semi-weak key analysis |
| `L8/` | Linear congruential generator (PRNG) and RC4 stream cipher |
| `L9/` | Merkle-Hellman knapsack cryptosystem, encryption/decryption timing |
| `L10/` | Large-prime generation timing and RSA encryption |
| `L11/` | SHA-256 hashing performance analyzer (Express app) |
| `l12/` | Public-key primitives in JS: RSA, ElGamal, Schnorr signatures |
| `L13/` | Text steganography via kerning and line-length modification |

Each folder is self-contained. Python labs use their own virtual environment,
Node labs (`L11`, `l12`) their own `package.json`, and `L2`/`L3` are separate
.NET projects.

## Setup

Python labs:
```bash
cd <lab-folder>
python -m venv .venv
.venv\Scripts\activate  # or source .venv/bin/activate on Linux/macOS
pip install -r requirements.txt  # if present, otherwise install imports manually
```

Node labs:
```bash
cd L11  # or l12
npm install
npm start
```

.NET labs:
```bash
cd L2  # or L3
dotnet build
```

## Not tracked in this repo

- `.venv/`: Python virtual environments, just recreate them per lab
- `node_modules/`: run `npm install` in `L11`/`l12`
- `bin/`, `obj/`: .NET build output
- Lecture/practicum handouts (`pract.pdf`, course PDFs), since they're not my own work
