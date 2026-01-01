# 🚀 BlueDraft Studio: The Professional Content Suite

BlueDraft Studio is a premium, AI-powered platform designed to optimize your professional presence across specialized workflows. Featuring a unique **"Quad-Brain" architecture**, it provides tailored intelligence for LinkedIn drafting, deep research, profile auditing, and content refinement.

---

## 📂 Project Structure

```text
BlueDraft_Studio/
├── static/
│   └── index.html       # Premium Glassmorphism Frontend (Unified UI)
├── main.py              # FastAPI Backend (AI Logic & Routing)
├── vercel.json          # Deployment configuration for Vercel
├── Procfile             # Deployment configuration for Render/Heroku
├── pyproject.toml       # Python project metadata and dependencies
├── requirements.txt     # Standard dependency list
├── uv.lock              # UV lockfile for deterministic builds
├── .python-version      # Target Python version (3.12)
├── .env                 # Environment variables (API Keys)
└── README.md            # Comprehensive project documentation
```

---

## 🧠 The Quad-Brain Architecture

The platform is structured around four specialized AI modules, each with its own "Brain" and dedicated system prompts:

1.  **Drafting Brain**: Engineered to create viral, high-engagement LinkedIn content using proven psychological triggers.
2.  **Research Brain**: A technical specialist optimized for deep-dives, fact-checking, and structured technical analysis.
3.  **Profile Reviewer**: A sophisticated auditor that parses your CV PDF and compares it against your LinkedIn profile/URL to provide a numerical score and GAP analysis. 
4.  **Post Improver**: A creative suite with three sub-strategies:
    *   **🔥 Hook Only**: Generates high-impact "scroll-stoppers".
    *   **✍️ Clarity & Flow**: Refines drafts for professional readability.
    *   **📈 Engagement**: Optimizes structure and CTAs for social growth.

---

## 🛠️ Tech Stack & Architecture

*   **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.12) — High-performance asynchronous web framework.
*   **AI Engine**: [Groq](https://groq.com/) — Leveraging `llama-3.3-70b-versatile` for ultra-fast, intelligent inference.
*   **Frontend**: Vanilla HTML5/CSS3/JS — Optimized for zero-dependency speed and premium glassmorphism aesthetics.
*   **PDF Parsing**: [PyPDF](https://pypdf.readthedocs.io/) — Used for extracting text from resumes and profiles.
*   **Deployment**: Ready for [Vercel](https://vercel.com/) and [Render](https://render.com/).

---

## 🚀 Live Launch & Deployment

### 1. Local Development
1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd BlueDraft_Studio
   ```
2. **Install dependencies** (Recommended: using `uv`):
   ```bash
   uv sync
   ```
3. **Configure Environment**:
   Create a `.env` file in the root directory and add your key:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```
4. **Launch the server**:
   ```bash
   uv run python main.py
   ```
   *The app will be available at `http://localhost:8000`.*

### 2. Vercel Deployment
The project includes a `vercel.json` configuration for seamless one-click deployments.
- Connect your GitHub repo to Vercel.
- Add `GROQ_API_KEY` to Vercel's **Environment Variables**.
- Vercel will automatically detect the Python configuration.

---

## 📱 Professional UI/UX Philosophy
Designed with a "Cinematic" philosophy, BlueDraft Studio provides:
*   **Glassmorphism Architecture**: Real-time backdrop blurs, noise textures, and mesh gradients.
*   **Dynamic Theming**: The interface visually adapts its color palette (Deep Blue, Purple, Green, Orange) based on the selected AI Brain.
*   **Interactive Terminal**: A high-end "Neural Glass Terminal" mockup on the landing page showcases simulated AI agent workflows.
*   **Mobile-First Design**: Optimized touch targets and list-view cards for a premium mobile experience.

---

## 🔒 Security & Privacy
- **Stateless Analysis**: Uploaded PDFs are processed in memory and never stored on the server.
- **Environment Safety**: API keys are handled strictly through server-side environment variables.

---

*Developed with precision for the next generation of professional workflows.*
