# ⚡ Kairo — Flow State Study & AI Productivity

> **A Futuristic AI-Powered Student Productivity & Flow Platform**  
> *Built for deep focus, interactive focus timer with soundscapes, custom cursor physics, curated theme customizers, automated study planning, active recall quizzes, resume creation, and AI career mentorship.*

---

![Kairo](https://img.shields.io/badge/Kairo-v3.0-00f2fe?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Gemini API](https://img.shields.io/badge/Google%20Gemini-API-8E44AD?style=for-the-badge&logo=google&logoColor=white)

---

## 🌟 Key Features

### ⏱️ 1. Focus Timer & Deep Flow Protocol
- **Mode Switching**: Focus (25m), Short Break (5m), Long Break (15m), and Custom (50m).
- **Circular SVG Glowing Ring**: Smooth real-time animated countdown progress.
- **Ambient Focus Audio**: Built-in soundscapes (Lo-Fi, Ambient Noise) with Web Audio API.
- **Keyboard Shortcuts**: `Space` to start/pause, `R` to reset.
- **Gamified Rewards**: Earn **+50 Flow XP** per completed focus block.
- **Celebratory Pulse**: Audio completion chime and celebration animations.

### 🎨 2. Custom Cursor & Spring Physics Engine
- **Two-Layer Trailing Cursor**: Glowing neon ring with spring easing + lagging trailing orb.
- **Magnetic Pull**: Interactive elements smoothly translate toward cursor within hover radius.
- **Reduced Motion & Touch Friendly**: Automatically falls back to standard cursor on touch/mobile or when `prefers-reduced-motion` is enabled.

### 🎭 3. Curated Accent Theme Presets
Switch between 4 high-contrast curated palettes instantly app-wide:
1. ⚡ **Cyan & Violet (Default)**
2. 🌿 **Emerald & Amber**
3. 🌹 **Rose & Indigo**
4. 🌅 **Amber & Slate**

### 🏠 4. Interactive Dashboard
- **Welcome & Student Profile Card**: Personalized academic flow greeting.
- **Daily Study Streak & Check-in**: Track streak progression with flame flickering animations.
- **Flow XP & Tasks**: Live count-ups and task completion tracking.
- **Quick Action Grid**: 1-click navigation to Focus Timer, AI Assistant, and Study Planner.

### 🤖 5. Kairo AI Mentor Chatbot
- **Gemini 1.5 Flash Integration**: Real-time academic Q&A, code debugging, and concept synthesis.
- **Preset Quick Prompts**: Fast prompt chips for one-click questions.
- **Persistent Floating Chat Bubble**: Quick trigger in bottom-right corner across all pages.
- **Action Controls**: Download chat log or clear conversation history.

### 📚 6. AI Study Planner
- **Personalized Plan Generation**: Converts subjects, exam target dates, and available daily hours into daily tasks.
- **ReportLab PDF Export**: Download your study schedule as a clean PDF.

### 📝 7. AI Quiz Generator
- **Active Recall Quizzes**: Generate MCQs on any subject with instant explanations and XP rewards.
- **Editable Questions**: Customize questions and answers before taking the test.

### 📄 8. Modern Resume Builder
- **Multi-Tab Profile Editor**: Personal info, Education, Skills, Projects, Experience, and Certifications.
- **Live Glassmorphism Preview**: Real-time card rendering with PDF export.

### 🚀 9. AI Career Roadmap
- **Step-by-Step Milestones**: Tailored to student's academic year, current skills, and target dream role.
- **PDF Export**: Download full career roadmap.

### 📊 10. Learning & Focus Analytics
- **Interactive Plotly Visuals**:
  - Weekly Study Hours vs Daily Goal
  - Focus Blocks Completed & XP Velocity
  - Subject Mastery Radar Chart
  - Kairo Flow Index Gauge (0-100)

---

## 🛠️ Technology Stack

- **Frontend & App Framework**: [Streamlit](https://streamlit.io/)
- **Programming Language**: Python 3.9+
- **Styling & Physics**: CSS Glassmorphism, Google Fonts (`Outfit` & `Inter`), JavaScript spring cursor and magnetic physics
- **Audio Engine**: Web Audio API ambient sound generator
- **AI Model Engine**: [Google Generative AI (Gemini 1.5 Flash)](https://ai.google.dev/) *(with built-in intelligent fallback)*
- **Data Visualization**: [Plotly Express & Graph Objects](https://plotly.com/python/)
- **PDF Compilation**: [ReportLab](https://www.reportlab.com/)

---

## 🚀 Quick Start Guide

```bash
git clone https://github.com/malverishabh07-cyber/kairo.git
cd kairo
pip install -r requirements.txt
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
