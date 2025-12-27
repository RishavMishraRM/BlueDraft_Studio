# 🧠 BlueDraft Studio

**BlueDraft Studio** is an advanced AI-powered content generation dashboard featuring a **Triple-Brain Architecture**. It allows users to switch seamlessly between a **Linkedin Drafting Brain**, a **Research Brain**, and a new **Profile Reviewer** for comprehensive career optimization.

![BlueDraft Studio UI](https://blue-draft-studio.vercel.app/)

## ✨ Features

- **Triple-Mode AI Engine**:
  - **Linkedin Brain 👔**: Specialized in crafting engaging, high-conversion Linkedin posts with optimal formatting and hashtags.
  - **Research Brain 🔬**: Specialized in deep-dive analysis, structured explanations, and comprehensive answers.
  - **Profile Reviewer 📋**: Analyzes your Resume (CV) and LinkedIn Profile (PDF or URL) to provide a score (1-100) and actionable improvement advice.
- **Premium UI/UX**:
  - Dark-mode first design with glassmorphism effects.
  - Smooth transitions and animations.
  - Dynamic theming (Blue for Linkedin, Purple for Research, Green for Reviewer).
- **Modern Tech Stack**: Built with FastAPI, Vanilla JS/CSS, and Groq's Llama 3 70B model. Support for PDF processing via `pypdf`.

## 🚀 Deployment

The project is deployment-ready for **Vercel** and **Render**.

### Live Demo (Vercel)
[Click here to view the live demo](https://blue-draft-studio.vercel.app/)

## 📂 Project Structure

Here is an overview of the key files and directories:

```graphql
BlueDraft_Studio/
├── static/                # Frontend Assets
│   └── index.html         # Main Single Page Application (SPA) containing HTML, CSS, and JS.
├── linked_code.py         # Main Backend Application (FastAPI). Handles API requests and Groq integration.
├── pyproject.toml         # Python project configuration and dependencies.
├── requirements.txt       # Frozen dependencies for deployment (generated from uv).
├── vercel.json            # Configuration file for Vercel deployment.
├── Procfile               # Configuration file for Render/Heroku deployment.
├── .env                   # Environment variables (API Keys). *Not committed to Git*.
└── README.md              # Project documentation.
```

## 🛠️ Local Installation

### Prerequisites
- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (Recommended) or pip
- A [Groq API Key](https://console.groq.com/)

### Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/YOUR_USERNAME/bluedraft-studio.git
    cd BlueDraft_Studio
    ```

2.  **Install Dependencies**:
    Using uv (fastest):
    ```bash
    uv sync
    ```
    Or using pip:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: This project requires `pypdf` and `python-multipart` for file handling.*

3.  **Configure Environment**:
    Create a `.env` file in the root directory and add your key:
    ```env
    GROQ_API_KEY=gsk_your_actual_key_here
    ```

4.  **Run the Server**:
    ```bash
    uv run python linked_code.py
    # OR
    uvicorn linked_code:app --reload
    ```

5.  **Open in Browser**:
    Navigate to `http://localhost:8000`.

## 🔧 Configuration Details

- **Backend**: `linked_code.py` initializes the FastAPI app using `pyproject.toml` dependencies. It defines a system prompt dictionary `SYSTEM_PROMPTS` that switches instruction sets based on the user's selected `mode`.
- **Frontend**: `static/index.html` handles the UI logic. It stores the `currentMode` state variable and dynamically swaps CSS variables (colors/gradients) and text content when the user selects a card.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## 📄 License

MIT License.
