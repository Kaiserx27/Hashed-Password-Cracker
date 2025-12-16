#  Hashed Password Cracker 
The tool demonstrates how weak hashing algorithms and poor password policies can be exploited using common attack techniques.

 **Legal & Ethical Notice**  
This project is intended **ONLY for educational purposes**, password recovery of your own accounts, or systems you have **explicit permission** to test.  
 **Do NOT use this tool for illegal activities.**

---

##  Project Goals
- Understand how password hashes work
- Demonstrate common password cracking techniques
- Learn why modern systems use **salting** and **slow hashing algorithms**
- Test password strength and security implementations

---

## Features
- Supports multiple hashing algorithms:
  - `MD5`
  - `SHA1`
  - `SHA256`
  - `SHA512`
- Multiple attack methods:
  - Dictionary attack
  - Brute force attack (length & attempt limited)
  - Rainbow table lookup (precomputed)
- Interactive **CLI interface**
- Built-in safety limits to prevent misuse
- Clean and readable Python code

---

## Technologies Used
- Python 3
- `hashlib`
- `itertools`
- `string`
