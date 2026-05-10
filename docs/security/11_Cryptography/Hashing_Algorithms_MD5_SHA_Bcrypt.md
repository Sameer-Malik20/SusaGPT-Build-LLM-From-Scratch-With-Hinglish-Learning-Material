# Hashing Algorithms: Digital Fingerprints

## 1. Beginner-friendly Hinglish Explanation 🇮🇳
Bhai, **Hashing** aur **Encryption** mein ek bahut bada farak hai. 

Encryption ko "Un-lock" kiya ja sakta hai, lekin Hashing ek **One-way Street** hai. Socho aapne ek poori kitaab (File) ko ek "Mixer" mein dala aur uska ek chota "Ladoo" (Hash) bana diya. Aap ladoo dekh kar kitaab wapas nahi bana sakte, lekin agar kitaab mein ek "Full Stop" bhi badla, toh ladoo ka swaad (Hash value) bilkul badal jayega. Iska use passwords ko save karne aur file ki "Integrity" check karne ke liye hota hai. Passwords ko hamesha hash karke hi save karna chahiye taaki agar database hack ho jaye, toh hacker ko asli password na mile.

---

## 2. Deep Technical Explanation
- **Properties of a Good Hash**:
    - **One-way**: Cannot reverse it.
    - **Deterministic**: Same input always gives same output.
    - **Fast**: But not *too* fast for passwords!
    - **Avalanche Effect**: Small input change = massive output change.
    - **Collision Resistant**: Two different inputs should NEVER give the same hash.
- **Algorithms**:
    - **MD5**: Broken, very fast (Use only for checksums).
    - **SHA-1**: Also broken, avoid.
    - **SHA-256**: The industry standard for file integrity.
    - **Bcrypt / Argon2**: Slow hashes designed specifically for **Passwords**.

---

## 3. Attack Flow Diagrams
**The 'Rainbow Table' Attack vs Salting:**
```mermaid
graph TD
    subgraph "Without Salt"
    P[Password: '123456'] --> H[Hash: 'e10adc...']
    H -- "Hacker looks up in table" --> P
    end
    subgraph "With Salt"
    P2[Password: '123456'] --> S[Salt: 'random_xyz']
    S --> H2[Hash: 'f45b91...']
    H2 -- "Hacker cannot find in table" --> Fail[Hack Failed]
    end
    Note over S: Each user gets a unique salt.
```

---

## 4. Real-world Attack Examples
- **LinkedIn Breach (2012)**: 6.5 million passwords were leaked. They were hashed using SHA-1 with NO salt. Hackers were able to crack 90% of them in days.
- **Collision Attack**: Researchers proved in 2017 that they could create two different PDF files that had the exact same **SHA-1** hash. This is why we don't use SHA-1 for security anymore.

---

## 5. Defensive Mitigation Strategies
- **Always use a Salt**: A random string added to the password before hashing.
- **Use Slow Algorithms for Passwords**: **Bcrypt**, **Scrypt**, or **Argon2id**. These are designed to take a long time to run, making it impossible for a hacker to try 1 billion passwords a second.
- **Peppering**: Adding a secret key (stored on a different server) to the hash for extra security.

---

## 6. Failure Cases
- **Using MD5/SHA1 for Passwords**: These are so fast that a hacker can test billions of combinations a second.
- **Reusing Salts**: Using the same salt "mysalt123" for every user. If one is cracked, all are cracked.

---

## 7. Debugging and Investigation Guide
- **`sha256sum file.txt`**: Checking the hash of a file in Linux.
- **`bcrypt-generator`**: Testing how long it takes to generate a hash with different "Cost" factors.
- **Hashcat / John the Ripper**: Tools used by pen-testers to try and crack (brute-force) hashes to test their strength.

---

| Use Case | Recommended Algorithm | Why? |
|---|---|---|
| Password Storage | Bcrypt / Argon2id | Slow, includes Salt, hard to brute-force. |
| File Integrity | SHA-256 / SHA-3 | Fast, high collision resistance. |
| Simple Checksum | MD5 / MurmurHash | Extremely fast, security doesn't matter. |

---

## 9. Security Best Practices
- **Adjust the 'Work Factor'**: As computers get faster (every 1-2 years), increase the Bcrypt "Cost" so it stays slow enough to be secure.
- **Validate File Hashes**: When downloading a tool (like Kali Linux), always check if the hash on your PC matches the one on the website to ensure it hasn't been modified by a hacker.

---

## 10. Production Hardening Techniques
- **Argon2id**: The winner of the Password Hashing Competition. It is resistant to both GPU and ASIC-based brute force attacks.
- **Password Throttling**: Even if you use a slow hash, don't let a user try to log in more than 5 times in a minute.

---

## 11. Monitoring and Logging Considerations
- **High CPU Usage on Auth Server**: If your login server is suddenly at 100% CPU, it might be a brute-force attack attempt trying to crack your slow hashes.

---

## 12. Common Mistakes
- **Encryption instead of Hashing**: Storing passwords using AES. If the AES key is stolen, EVERY password is leaked in plain text.
- **Double Hashing**: Thinking `sha256(md5(password))` is better. It's not! It just adds complexity and might even make it weaker.

---

## 13. Compliance Implications
- **SOC2 / PCI-DSS**: Specifically require that passwords be "Rendered unreadable" using strong, salted one-way hashes.

---

## 14. Interview Questions
1. What is the difference between Hashing and Encryption?
2. Why is 'Bcrypt' better than 'SHA-256' for password storage?
3. What is a 'Salt' and why is it used?

---

## 15. Latest 2026 Security Patterns and Threats
- **Quantum Hashing Resistance**: While hashing is generally safer from Quantum computers than RSA, researchers are developing "Lattice-based" hashes for the future.
- **AI-Native Password Cracking**: Using LLMs to guess passwords based on a person's social media and public profile, making brute-force 1,000x more effective.
- **Zero-Knowledge Password Proofs**: Logging in without the server ever even seeing your password hash (using math like **PAKE**).
	
