\# 🧪 QA Copilot – GenAI Assistant for Manual Testers



\## 📌 Overview



QA Copilot is a Generative AI-powered assistant designed to improve the productivity of Manual QA Engineers by automating repetitive testing activities.



The application uses a locally hosted Large Language Model (LLM) through Ollama to analyze software requirements and generate comprehensive test cases.



Unlike cloud-based AI solutions, QA Copilot runs completely offline, making it suitable for organizations with strict security and data privacy requirements.



\---



\## 🎯 Problem Statement



Manual testers spend a significant amount of time:



\- Understanding requirements

\- Writing functional test cases

\- Identifying edge cases

\- Creating negative test scenarios

\- Performing requirement analysis



QA Copilot reduces this effort by leveraging Generative AI to assist testers throughout the testing lifecycle.



\---



\## 🚀 Current Features



\- ✅ Requirement-based Test Case Generation

\- ✅ Positive Test Cases

\- ✅ Negative Test Cases

\- ✅ Edge Case Identification

\- ✅ Security Test Case Suggestions

\- ✅ Local AI inference using Ollama

\- ✅ Interactive Streamlit Web UI

\- ✅ Modular and scalable project architecture



\---



\## 🚧 Planned Features



\- 📄 Requirement Analyzer

\- 📄 PDF \& Word Requirement Upload

\- 🧠 Chat with Requirement Documents (RAG)

\- 📊 Test Case Export to Excel

\- 🐞 AI Bug Report Generator

\- 📈 Regression Test Recommendation

\- 🗂 Test Data Generator

\- 📋 Daily QA Status Report Generator

\- 📚 Requirement Knowledge Base using ChromaDB

\- 🌐 REST APIs using FastAPI



\---



\## 🏗️ Architecture



```

&#x20;                User

&#x20;                  │

&#x20;                  ▼

&#x20;         Streamlit Web UI

&#x20;                  │

&#x20;                  ▼

&#x20;       Requirement Service

&#x20;                  │

&#x20;                  ▼

&#x20;       Prompt Builder Module

&#x20;                  │

&#x20;                  ▼

&#x20;         Ollama Service

&#x20;                  │

&#x20;                  ▼

&#x20;         Qwen Language Model

&#x20;                  │

&#x20;                  ▼

&#x20;     AI Generated QA Test Cases

```



\---



\## 🛠️ Technology Stack



| Component | Technology |

|------------|------------|

| Language | Python 3 |

| UI | Streamlit |

| AI Model | Qwen (via Ollama) |

| AI Runtime | Ollama |

| API Communication | Requests |

| Version Control | Git |

| Repository | GitHub |



\---



\## 📁 Project Structure



```

qa-copilot/

│

├── app.py

├── config.py

├── requirements.txt

├── README.md

│

├── prompts/

│   ├── \_\_init\_\_.py

│   └── requirement\_prompt.py

│

├── services/

│   ├── \_\_init\_\_.py

│   ├── ollama\_service.py

│   └── requirement\_service.py

│

├── utils/

│   └── \_\_init\_\_.py

│

├── uploads/

│

└── exports/

```



\---



\## ⚙️ Installation



\### Clone Repository



```bash

git clone https://github.com/ajithkumar289/qa-copilot.git



cd qa-copilot

```



\### Create Virtual Environment



Windows



```bash

python -m venv venv



venv\\Scripts\\activate

```



\### Install Dependencies



```bash

pip install -r requirements.txt

```



\### Install Ollama



Download and install Ollama from:



https://ollama.com/download



\### Download Qwen Model



```bash

ollama pull qwen2.5:3b

```



\### Start Ollama



```bash

ollama serve

```



\### Run the Application



```bash

streamlit run app.py

```



\---



\## 💻 Example Requirement



```

User should be able to login using email and password.



The application should validate the credentials and redirect the user to the dashboard after successful authentication.

```



\---



\## 🤖 Sample AI Output



The application generates:



\- Positive Test Cases

\- Negative Test Cases

\- Edge Cases

\- Security Test Cases



Each test case includes:



\- Test Case ID

\- Test Case Title

\- Test Steps

\- Expected Result



\---



\## 🎯 Project Roadmap



\### Sprint 1 ✅



\- Streamlit UI

\- Ollama Integration

\- Prompt Engineering

\- Test Case Generation

\- Modular Architecture

\- Git \& GitHub Integration



\### Sprint 2 🚀



\- Requirement Analyzer

\- Business Rule Extraction

\- Missing Requirement Detection

\- Risk Identification



\### Sprint 3



\- PDF Upload

\- DOCX Upload

\- Requirement Parsing



\### Sprint 4



\- Chat with Requirement Documents (RAG)



\### Sprint 5



\- Export Test Cases to Excel



\### Sprint 6



\- AI Bug Report Generator



\### Sprint 7



\- Test Data Generator



\### Sprint 8



\- Regression Recommendation Engine



\### Sprint 9



\- Dashboard \& Analytics



\---



\## 🎓 Learning Objectives



This project demonstrates practical experience with:



\- Generative AI

\- Prompt Engineering

\- Ollama

\- Local LLM Integration

\- Python

\- Streamlit

\- Software Architecture

\- QA Domain Knowledge

\- Git \& GitHub



\---



\## 📌 Why QA Copilot?



QA Copilot is designed to reduce repetitive manual testing activities while improving test coverage and consistency.



It serves as an AI assistant for Manual Test Engineers by accelerating requirement analysis and test design.



\---



\## 👨‍💻 Author



\*\*Ajith\*\*



QA Engineer | Learning Generative AI | Python | API Testing | Automation Enthusiast



\---



\## 📄 License



This project is licensed under the MIT License.



\---



\## ⭐ Future Vision



The long-term goal of QA Copilot is to become an end-to-end AI-powered assistant for Software Quality Assurance capable of:



\- Understanding business requirements

\- Generating complete test suites

\- Recommending regression tests

\- Creating defect reports

\- Producing test data

\- Assisting QA Engineers throughout the Software Testing Life Cycle (STLC)

