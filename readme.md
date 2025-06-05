# RAG DeepSeek Local Computer Security

This project demonstrates how to use large language models (such as DeepSeek) locally for computer security tasks, utilizing Python and Ollama on a Windows machine with WSL (Windows Subsystem for Linux).

---

## Overview

With this project, you can run and interact with powerful AI models entirely on your local computer, ensuring privacy and control over your workflow. The guide below will help you set up your environment and run your own Retrieval-Augmented Generation (RAG) pipeline for computer security applications.

---

## Setup Instructions

### 1. Install WSL and Ubuntu (Windows Only)

Open PowerShell as **Administrator** and run:
```sh
wsl --install
```
> **Restart your PC** after installation.

---

### 2. Set Up Ubuntu

- Search for "ubuntu" in the Windows search bar and open it.
- Create a **username and password** for your Ubuntu installation.

---

### 3. Install Ollama in Ubuntu

In the Ubuntu terminal, run:
```sh
curl https://ollama.ai/install.sh | sh
```

---

### 4. Test Ollama Installation

Try running a small model:
```sh
ollama run orca-mini
```
Ask something to check if it's working.  
**To stop:** Press `CTRL + D`.

---

### 5. Run DeepSeek Model

Start the DeepSeek model:
```sh
ollama run deepseek-r1:1.5b
```
When you see `>>>`, press `CTRL + D` to exit.

---

### 6. Start Ollama in Server Mode

```sh
ollama serve
```
Leave this running in the background.

---

### 7. Run Your Python Script

- Create your Python script (ex: `rag_ollama.py`) using an IDE like PyCharm or VSCode.
- While WSL and Ollama server are active, run your script on Windows.

---

## Example Workflow

Below are some example images to guide you through the setup process and project usage:


### Running Ollama and DeepSeek

![Ollama Running Screenshot](https://i.imgur.com/U2Ndrpa.png)
Example Prompts
![Example Prompts](https://i.imgur.com/mfFmdUE.png)
![Example Prompts](https://i.imgur.com/RLqDKtK.png)
![Example Prompts](https://i.imgur.com/wBfjvnc.png)
*Sample prompt results using DeepSeek model*


---

## Requirements

- Windows 10/11 with WSL (Ubuntu)
- Ollama
- Python 3.x
- PyCharm, VSCode, or another IDE

---

## Contribution & Support

Feel free to open an issue or suggest improvements! Contributions are welcome.

---

## License

This project is for educational purposes only.
