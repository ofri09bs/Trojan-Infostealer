# 🐍 Trojan Infostealer and keylogger (Snake Game)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Security](https://img.shields.io/badge/Cyber%20Security-Research-red.svg)
![Educational](https://img.shields.io/badge/Purpose-Educational-green.svg)

> **⚠️ DISCLAIMER**
>
> This project was developed for **educational and academic research purposes only** .
> Using this code for malicious purposes, attacking computers without permission, or stealing data is **illegal**. The developer assumes no responsibility for any misuse of this code.

---

## 📖 Overview

This project demonstrates the creation of a simulated **Advanced Persistent Threat (APT)** disguised within a legitimate application.
The software presents a classic, innocent-looking **Snake game** (written in Pygame) to the user, while running a sophisticated **Infostealer** and **Keylogger** mechanism in the background.

The software **Encrypts** all the collected data and sends it to a **Discord server** , using WebHooks. To Decrypt the file , use decrypt_tool.py


The project demonstrates the following Red Team techniques:

* **Evasion:** Running malicious code in a separate thread behind a legitimate process to avoid detection.
* **Reconnaissance:** Extensive collection of system and network data.
* **Cryptography:** Encrypting stolen data using **AES-128** before transmission.
* **Data Exfiltration:** Exfiltrating data via an encrypted and legitimate channel (**Discord Webhooks**).

---

## 🕵️ Malware Capabilities

The malicious payload (`spyware.py`) includes extensive data collection capabilities:

| Category | Collected Data | Technical Method |
| :--- | :--- | :--- |
| **Network Identity** | Internal/External IP, MAC Address | `socket`, `requests`, `uuid` |
| **System Fingerprint** | Hostname, Username, OS Version, Architecture | `platform`, `os` |
| **Wireless Security** | Saved WiFi Network Names (SSID) | `netsh wlan show profiles` |
| **User Data** | Full Computer info (GPU,CPU,RAM...), Keystrokes (Keylogger) | `ctypes`, `pynput` |
| **Software Audit** | Installed Software, Active Processes,Desktop programs | `PowerShell`, `tasklist` |

And more!

---

## 🏗️ Architecture and Code Structure

The project is built modularly to separate the UI (Game), the Payload (Spyware), and the Encryption logic.

### 📂 File Structure

```text
📦 Trojan-Infostealer
 ┣ 📜 SnakeGame.py       # (The Dropper) The main UI game. Triggers the spyware thread.
 ┣ 📜 spyware.py         # (The Payload) The "Brain". Gathers info, runs keylogger & exfiltrates data.
 ┣ 📜 crypto_module.py   # (Encryption) Shared AES-128 (ECB) + Base64 library.
 ┗ 📜 decrypt_tool.py    # (Blue Team Tool) Server-side tool to decrypt exfiltrated logs.

