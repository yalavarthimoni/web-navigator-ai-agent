# AI Navigator Agent / Web Navigator AI Agent

## Project Summary

### Problem Understanding
Efficient web browsing often involves repetitive tasks such as searching, extracting information, and filling forms. Non-technical users struggle to automate these tasks, and cloud-based AI tools raise privacy and dependency concerns. There is a clear need for a **local, intelligent solution** that can understand natural language instructions and autonomously perform web operations on a personal computer.

### Proposed Prototype Solution
We propose a **locally running AI Navigator Agent** capable of interpreting natural language commands and autonomously controlling a browser. Leveraging a locally hosted Large Language Model (LLM) for instruction parsing combined with browser automation (Chrome Headless or VM-based), the agent executes commands like:

> “Search for laptops under 50k and list top 5”

The agent navigates websites, extracts structured data, and presents results clearly to the user. Optional enhancements include multi-step reasoning, task memory, error handling, and a basic GUI for seamless interaction.

### Uniqueness and Impact
Unlike cloud-dependent solutions, our agent operates entirely offline, ensuring **user privacy and data security**. Its autonomous, multi-step web execution reduces time spent on repetitive browsing tasks, making the web more accessible to both technical and non-technical users. By combining **LLM reasoning with browser automation**, the system delivers a scalable, practical solution for AI-assisted web navigation, data extraction, and workflow automation.

---

## Problem Statement Chosen
**Build an AI Agent that can take natural language instructions and autonomously drive the web on a local computer.**

---

## Detailed Proposal & Prototype Plan
Our AI Navigator Agent allows users to issue simple commands and retrieves top results while performing automated actions like search, selection, and checkout.

### Frontend
- Intuitive search bar for natural language queries  
- Display of top 5 product results with details: name, price, rating, and key features  
- Option to select a product and proceed to checkout  

### Backend / Agent
- Locally hosted LLM to parse instructions  
- Browser automation using Chrome Headless or VM-based browsers  
- Task execution: search, navigate, extract text, click elements, fill forms  
- Multi-step task memory and error handling for robust automation  

### Checkout Flow
- Capture user details: name, address, payment info  
- Automatically fill Flipkart checkout form for the selected product  
- Redirect user to Flipkart for final payment

---

## Features
- **Instruction Parsing via LLM**  
- **Autonomous Browser Control**  
- **Task Execution:** search, click, extract, form filling  
- **Structured Output Return**  
- **Local, Cloud-independent Setup**  
- **Optional:** Multi-step reasoning, GUI interface, task memory  

---

## Tech Stack
- **Python** – core logic and automation  
- **Playwright / Selenium** – browser automation  
- **SpeechRecognition & pyttsx3** – voice commands and assistant responses  
- **Locally hosted LLM** – instruction understanding & planning  
- **React/Vite** – frontend UI for search and checkout  

---

## Team Contributions

| Team Member | College | Contribution |
|-------------|--------|--------------|
| Monika | Vignan University | Team lead, system workflow, project coordination, frontend checkout flow |
| Vaishnavi | Vignan’s Lara | Input handling, voice recognition, AI assistant responses, error handling |
| Premsai | KLU | Backend command processing, execution logic, browser automation, Flipkart integration |

<img width="1237" height="669" alt="image" src="https://github.com/user-attachments/assets/a1a046c0-f7b4-4fca-a8b7-c38b8b4387ef" />

<img width="1608" height="838" alt="image" src="https://github.com/user-attachments/assets/8428bc65-3639-4df1-8d06-19d07e819a0c" />

<img width="1481" height="848" alt="image" src="https://github.com/user-attachments/assets/823f447c-2048-4121-8cf6-889c26e71008" />

<img width="1129" height="857" alt="image" src="https://github.com/user-attachments/assets/c65b449e-d9b5-48d2-92fa-8acde605b61d" />




