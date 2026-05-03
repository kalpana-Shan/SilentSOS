##🚨 SilentSOS
AI-Powered Invisible Emergency Signal System
"When a victim cannot say 'help', SilentSOS understands the help hidden between the lines."


##📌 Overview
SilentSOS is a covert safety system that detects distress hidden inside normal-looking text, then silently escalates through trusted contacts with live location sharing. Unlike traditional SOS apps that require explicit button presses, SilentSOS works when the user cannot openly ask for help.

##✨ Features
**Feature	Description**
    🧠 AI Distress Detection	Analyzes hidden stress intent, coercion cues, and reassurance patterns
    📧 Silent Email Alerts	Triggers alerts to trusted contacts without visible confirmation
    📍 Live Location Sharing	Sends current coordinates with Google Maps link
    🎭 Stealth Mode UI	Interface looks like a normal chat/notes app
    📊 Alert Dashboard	Complete history with risk scoring and explanations
    🔑 Safe Phrases	Personalize keywords that trigger alerts in specific contexts

##🏗️ Architecture
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (React + Vite)                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Chat UI    │  │  Contacts   │  │  Alert Dashboard    │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────┬───────────────────────────────┘
                              │ HTTP/REST API
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend (FastAPI)                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ /analyze    │  │ /contacts   │  │ /alerts             │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Risk Engine │  │ AI Service  │  │ Alert Service       │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Storage & Services                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  SQLite     │  │  Ollama     │  │  Gmail SMTP         │  │
│  │  Database   │  │  (llama3)   │  │  Email Alerts       │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

##🔧 Tech Stack
**Layer**             	     **Technology**
Frontend	           React, Vite, Tailwind CSS
Backend	             FastAPI (Python 3.11+)
AI Model	           Ollama + Llama 3 (Local/Offline)
Database             SQLite
Email Alerts         Gmail SMTP
Deployment	         Render / Railway

##📁 Project Structure
SilentSOS/
│
├── main.py                    # FastAPI application entry point
├── database.py                # SQLite database setup
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (API keys)
│
├── routes/                    # API endpoints
│   ├── analyze.py            # POST /api/analyze-message
│   ├── contacts.py           # CRUD for trusted contacts
│   └── history.py            # Alert history & stats
│
├── services/                  # Business logic
│   ├── ai_service.py         # Ollama + Llama 3 integration
│   ├── risk_engine.py        # Multi-signal risk scoring
│   ├── alert_service.py      # Alert dispatcher
│   └── email_service.py      # Gmail SMTP sender
│
├── frontend/                  # React/Vite frontend
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
└── tests/                     # Test scripts
    ├── test_email.py
    └── test_risk.py

##🚀 Getting Started
 **Prerequisites**
**Requirement**           	**Version**
  Python	                  3.10+
  Node.js                  	18+
  Ollama                   	Latest
  Gmail Account           	With App Password

##1. Clone Repository

git clone https://github.com/kalpana-Shan/SilentSOS.git
cd SilentSOS

##2. Backend Setup

# Install Python dependencies
pip install -r requirements.txt
# Create .env file (see configuration below)
# Pull and run Ollama model
ollama pull llama3
ollama run llama3
# Start backend server
uvicorn main:app --reload --port 8000

##3. Frontend Setup
# Navigate to frontend directory
cd frontend
# Install dependencies
npm install
# Start development server
npm run dev

##4. Environment Configuration
Create .env in project root: .env
# AI Model
OLLAMA_MODEL=llama3
OLLAMA_HOST=http://localhost:11434
# Email Alerts
EMAIL_ALERTS_ENABLED=true
ALERT_EMAIL=your-email@gmail.com
ALERT_PASSWORD=your-16-char-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
# Optional: Twilio SMS 
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_FROM_NUMBER=

##API Response Example
{
  "alert_id": 3,
  "semantic_score": 85,
  "context_score": 100,
  "final_score": 91,
  "risk_level": "high",
  "signals": ["⚠️ Excessive reassurance", "📵 Communication restriction"],
  "hidden_distress_reason": "Message contains reassurance and battery low at late hour",
  "confidence": "high",
  "alert_triggered": true
}

##🎯 Risk Scoring Formula
final_score = (0.55 × semantic_score) + (0.45 × context_score)
**Risk Levels:**

🟢 Low (0-39) : Monitor only
🟡 Medium (40-69) : Alert contacts
🔴 High (70-100) : Immediate alert + location sharing

**Context Factors:**
Late night (22:00 - 05:00) : +35
Location anomaly : +30
Communication restriction : +25
Excessive reassurance : +20
Distancing language : +20

##🧪 Testing
**Test Email Alerts**
python test_email.py

**Test Risk Analysis**
python test_risk.py

**Add Manual Contact**
python add_contact.py

**Run All Tests**
pytest tests/

##👥 Team
**Name**                    **Role**	                              **Responsibilities**
Kalpana Shanmugam   Full Stack + AI Integration      	Backend, AI/LLM integration, Risk engine, Deployment
Harshini T          Frontend Developer	              React UI, Dashboard, Location services

##📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

##📧 Contact
Project Lead: Kalpana Shan
GitHub: github.com/kalpana-Shan
Project Repo: github.com/kalpana-Shan/SilentSOS
Demo Link: https://youtu.be/Hgnk9wcpcnY

<div align="center">
⭐ Star this repo if you find it useful!

Built with 🛡️ for safety and 🤖 for intelligence

</div>
