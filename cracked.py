
"""
Hashed Password Cracker

Supported attacks:
- Dictionary attack
- Brute force (limited charset/length)
- Simple rainbow table (precomputed)

Supported hashes:
- md5
- sha1
- sha256
- sha512
"""

import hashlib
import itertools
import string
import sys
import time
from typing import Dict, Optional


# ----------------------------
# Hash utilities
# ----------------------------
def hash_text(text: str, algo: str) -> str:
    h = hashlib.new(algo)
    h.update(text.encode("utf-8"))
    return h.hexdigest()


def verify_hash(plain: str, target_hash: str, algo: str) -> bool:
    return hash_text(plain, algo) == target_hash.lower()


# ----------------------------
# Dictionary attack
# ----------------------------
def dictionary_attack(
    target_hash: str,
    algo: str,
    wordlist_path: str,
    delay: float = 0.0
) -> Optional[str]:
    try:
        with open(wordlist_path, "r", errors="ignore") as f:
            for i, word in enumerate(f, 1):
                word = word.strip()
                if not word:
                    continue
                if verify_hash(word, target_hash, algo):
                    print(f"[+] Found after {i} tries")
                    return word
                if delay:
                    time.sleep(delay)
    except FileNotFoundError:
        print("[-] Wordlist file not found.")
    return None


# ----------------------------
# Brute force attack (LIMITED)
# ----------------------------
def brute_force_attack(
    target_hash: str,
    algo: str,
    charset: str,
    max_length: int,
    max_attempts: int = 500_000
) -> Optional[str]:
    attempts = 0
    start = time.time()

    for length in range(1, max_length + 1):
        for combo in itertools.product(charset, repeat=length):
            candidate = "".join(combo)
            attempts += 1

            if verify_hash(candidate, target_hash, algo):
                elapsed = time.time() - start
                print(f"[+] Found in {attempts} attempts ({elapsed:.2f}s)")
                return candidate

            if attempts >= max_attempts:
                print("[!] Max attempts reached (safety limit).")
                return None

    return None


# ----------------------------
# Simple Rainbow Table
# ----------------------------
def build_rainbow_table(
    words,
    algo: str
) -> Dict[str, str]:
    table = {}
    for w in words:
        table[hash_text(w, algo)] = w
    return table


def rainbow_lookup(
    target_hash: str,
    rainbow_table: Dict[str, str]
) -> Optional[str]:
    return rainbow_table.get(target_hash.lower())


# ----------------------------
# UI helpers
# ----------------------------
def choose_hash_algo() -> str:
    algos = ["md5", "sha1", "sha256", "sha512"]
    print("\nChoose hash algorithm:")
    for i, a in enumerate(algos, 1):
        print(f"{i}. {a}")
    idx = int(input("> "))
    return algos[idx - 1]


def main_menu():
    print("""
===============================
  Hashed Password Cracker
  (Educational / Authorized Use)
===============================
1. Dictionary attack
2. Brute force attack (limited)
3. Rainbow table lookup
0. Exit
""")


# ----------------------------
# MAIN
# ----------------------------
def main():
    main_menu()
    choice = input("> ").strip()

    if choice == "0":
        sys.exit(0)

    target_hash = input("Enter target hash: ").strip()
    algo = choose_hash_algo()

    if choice == "1":
        wordlist = input("Path to wordlist (e.g. rockyou.txt): ").strip()
        result = dictionary_attack(target_hash, algo, wordlist)
        print(f"\nResult: {result if result else 'NOT FOUND'}")

    elif choice == "2":
        print("\nCharset options:")
        print("1. digits")
        print("2. lowercase letters")
        print("3. digits + lowercase")
        c = input("> ").strip()

        if c == "1":
            charset = string.digits
        elif c == "2":
            charset = string.ascii_lowercase
        else:
            charset = string.digits + string.ascii_lowercase

        max_len = int(input("Max password length (e.g. 4): "))
        result = brute_force_attack(
            target_hash,
            algo,
            charset,
            max_len
        )
        print(f"\nResult: {result if result else 'NOT FOUND'}")

    elif choice == "3":
        print("\nRainbow table (demo words)")
        demo_words = [
            "password", "123456", "admin", "qwerty",
            "letmein", "welcome", "abc123"
        ]
        table = build_rainbow_table(demo_words, algo)
        result = rainbow_lookup(target_hash, table)
        print(f"\nResult: {result if result else 'NOT FOUND'}")

    else:
        print("Invalid option.")


if __name__ == "__main__":
    main()
