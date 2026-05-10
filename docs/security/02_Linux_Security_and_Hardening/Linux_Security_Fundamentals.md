# 🐧 Linux Security Fundamentals
> **Level:** Beginner → Intermediate | **Language:** Hinglish | **Goal:** Master permissions, SSH, firewall

---

## 🧭 Core Concepts (Concept-First)

- File Permissions: rwx, chmod, chown
- User Management: sudo, root
- SSH Hardening: Keys, config
- Firewall: UFW, iptables

---

## 1. 🔐 File Permissions

```bash
# View permissions
ls -la file.txt

# Permission types
# r = read (4)
# w = write (2)
# x = execute (1)

# chmod examples
chmod 755 file.sh        # rwx r-x r-x
chmod +x script.sh       # Add execute
chmod -w file.txt        # Remove write

# Ownership
chown user:group file.txt
chgrp group file.txt
```

---

## 2. 👤 User & Sudo Management

```bash
# Add user
sudo useradd -m -s /bin/bash username

# Delete user
sudo userdel -r username

# Add to sudo group
sudo usermod -aG sudo username

# Check sudo access
sudo -l
```

---

## 3. 🔑 SSH Hardening

```bash
# SSH config - /etc/ssh/sshd_config

# Disable root login
PermitRootLogin no

# Disable password auth
PasswordAuthentication no
PubkeyAuthentication yes

# Use strong ciphers
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com

# Disable protocol 1
Protocol 2

# Limit login attempts
MaxAuthTries 3

# Restart SSH
sudo systemctl restart sshd
```

---

## 4. 🧱 Firewall (UFW)

```bash
# Enable UFW
sudo ufw enable

# Allow SSH
sudo ufw allow ssh
# or
sudo ufw allow 22/tcp

# Allow specific port
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Deny all incoming
sudo ufw default deny incoming
sudo ufw default allow outgoing

# View status
sudo ufw status

# Delete rule
sudo ufw delete allow 80/tcp
```

---

## ✅ Checklist

- [ ] File permissions samjho aur apply kar sakte ho
- [ ] User management kar sakte ho
- [ ] SSH securely configure kar sakte ho
- [ ] Firewall setup kar sakte ho