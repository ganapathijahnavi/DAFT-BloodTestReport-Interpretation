# DAFT-BloodTestReport-Interpretation
## Domain-Adaptive Fine-Tuning of Lightweight Large Language Models for Personalized Blood Test Report Interpretation
DAFT is a lightweight AI system that converts complex blood test reports into patient-friendly interpretations using a fine-tuned TinyLLaMA (1.1B) model with LoRA adaptation. The hybrid architecture combines deterministic laboratory value parsing with controlled natural language generation, achieving 97.9% accuracy with only 2.1% hallucination rate—significantly outperforming medical baselines like BioBERT (9.4%), ClinicalBERT (11.8%), and BioGPT (7.1%). Deployed as a full-stack web application (React + FastAPI) with 2.3s inference time, DAFT demonstrates that task-specific architectural design and domain adaptation can deliver production-ready medical AI without enterprise-scale infrastructure or privacy compromises.

### Hybrid Design Philosophy
- **Deterministic Component**: Laboratory value extraction (100% accuracy)
- **Generative Component**: Natural language explanation (controlled by structured input)
- **Result**: Best of both worlds - factual accuracy + human readability

---

## 🚀 Tech Stack

### Backend
- **Model**: TinyLLaMA (1.1B parameters)
- **Fine-tuning**: LoRA (Low-Rank Adaptation) - r=16, α=32
- **Framework**: PyTorch, Hugging Face Transformers, PEFT
- **API**: FastAPI
- **Deployment**: Hugging Face Spaces

### Frontend
- **Framework**: React + TypeScript
- **Styling**: Modern responsive design
- **Hosting**: Netlify CDN
- **Features**: Multi-file upload, session management

### Training Infrastructure
- **Dataset**: 850 manually curated samples (680 train / 85 val / 85 test)
- **Validation**: Inter-rater agreement κ=0.83 (3 medical professionals)
- **Hardware**: NVIDIA GPU (12GB VRAM)
- **Training Time**: ~8 hours

---

## 📂 Project Structure
    ┌─────────────────┐
    │ Blood Test PDF │
    │ or Image │
    └────────┬────────┘
    │
    ▼
    ┌─────────────────┐
    │ OCR Module │ ← Text Extraction
    └────────┬────────┘
    │
    ▼
    ┌─────────────────┐
    │ Lab Value │ ← Deterministic Parsing
    │ Parser │ (Regex + Rules)
    └────────┬────────┘
    │
    ▼
    ┌─────────────────┐
    │ Abnormality │ ← Reference Range Check
    │ Detection │
    └────────┬────────┘
    │
    ▼
    ┌─────────────────┐
    │ TinyLLaMA │ ← LoRA Fine-tuned (r=16, α=32)
    │ + LoRA (1.1B) │ Domain-Adapted Generation
    └────────┬────────┘
    │
    ▼
    ┌─────────────────┐
    │ Patient-Friendly│
    │ Report │
    └─────────────────┘

### Hybrid Design Philosophy
- **Deterministic Component**: Laboratory value extraction (100% accuracy)
- **Generative Component**: Natural language explanation (controlled by structured input)
- **Result**: Best of both worlds - factual accuracy + human readability

---

## 🚀 Tech Stack

### Backend
- **Model**: TinyLLaMA (1.1B parameters)
- **Fine-tuning**: LoRA (Low-Rank Adaptation) - r=16, α=32
- **Framework**: PyTorch, Hugging Face Transformers, PEFT
- **API**: FastAPI
- **Deployment**: Hugging Face Spaces

### Frontend
- **Framework**: React + TypeScript
- **Styling**: Modern responsive design
- **Hosting**: Netlify CDN
- **Features**: Multi-file upload, session management

### Training Infrastructure
- **Dataset**: 850 manually curated samples (680 train / 85 val / 85 test)
- **Validation**: Inter-rater agreement κ=0.83 (3 medical professionals)
- **Hardware**: NVIDIA GPU (12GB VRAM)
- **Training Time**: ~8 hours

---

## 📂 Project Structure
    DAFT-BloodTestReport-Interpretation/
    ├── backend/
    │ ├── main.py # FastAPI server
    │ ├── model.py # LoRA model loading
    │ ├── lab_parser.py # Deterministic value extraction
    │ ├── interpretation.py # LLM interpretation logic
    │ ├── ocr.py # OCR processing
    │ ├── schemas.py # API schemas
    │ └── requirements.txt
    │
    ├── frontend/
    │ ├── src/
    │ │ ├── App.js # Main React component
    │ │ ├── App.css # Styling
    │ │ └── index.js
    │ ├── public/
    │ └── package.json

---

## 🔬 Research Contributions

### 1. Domain-Adaptive Fine-Tuning Framework
- Applied LoRA to TinyLLaMA for medical laboratory interpretation
- Achieved 97.9% accuracy with minimal computational overhead

### 2. Comprehensive Ablation Studies
- **LoRA Rank**: Optimal at r=16 (vs. r=4,8,32,64)
- **Training Data**: Performance plateau at 500+ samples
- **Base Model**: TinyLLaMA offers best cost-performance trade-off

### 3. Rigorous Evaluation
- Triple-blind protocol with 5 medical expert evaluators
- Statistical validation: Bonferroni-corrected t-tests, Cohen's d effect sizes
- Robustness testing: Cross-lab formats (87.5-100% accuracy), OCR errors (94.7% at 5% error)

### 4. Medical Baseline Comparisons
First study to demonstrate that **task-specific architecture** outperforms general medical pre-training:
- vs. BioBERT: 2.1% vs. 9.4% hallucination
- vs. ClinicalBERT: 2.1% vs. 11.8% hallucination
- vs. BioGPT: 2.1% vs. 7.1% hallucination

---

## 📖 Usage

### Live Demo
Visit **[healthexplain.netlify.app](https://healthexplain.netlify.app/)** to try the system:
1. Upload a blood test report (PDF or image)
2. Wait 2-3 seconds for processing
3. Receive a patient-friendly interpretation

### Local Setup

#### Backend

    cd backend
    pip install -r requirements.txt
    python [main.py](http://_vscodecontentref_/3)

# Frontend - Blood Test Report Interpretation UI

## 📁 Project Structure
    frontend/
    ├── public/
    │ ├── index.html # HTML entry point
    │ ├── manifest.json # PWA manifest
    │ ├── favicon.ico # App icon
    │ └── robots.txt # SEO configuration
    ├── src/
    │ ├── App.js # Main React component
    │ ├── App.css # Application styles
    │ ├── index.js # React DOM entry point
    │ ├── index.css # Global styles
    │ └── reportWebVitals.js # Performance monitoring
    ├── package.json # Dependencies and scripts

---

## 🎨 Tech Stack

- **Framework**: React 18.2.0
- **Build Tool**: Create React App (react-scripts 5.0.1)
- **Styling**: CSS3 (custom styles)
- **State Management**: React Hooks (useState, useRef, useEffect)

---

## 📦 Dependencies

    {
      "dependencies": {
      "react": "^18.2.0",
      "react-dom": "^18.2.0",
      "react-scripts": "5.0.1"
      }
    }

### 🚀 Quick Start
Installation
      
      cd frontend
      npm install
      
Development Server

    npm start

### 🙏 Acknowledgments
- TinyLLaMA team for the base model
- Hugging Face for infrastructure and PEFT library
- Medical professionals who contributed to dataset validation
- Open-source community for tools and frameworks

### ⚠️ Disclaimer
This system is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult qualified healthcare providers for medical decisions. The system is designed as an educational assistive tool to improve health literacy.

### 👥 Authors
- G. Jahnavi Durga - Research Scholar
- B. Phani Shankar - Research Scholar
- Abdul Ahad - Research Scholar
- A. Siddarth Chowdary - Research Scholar
- K. Nandini - Professor, Department of CSE
- Seshadri Rao Gudlavalleru Engineering College, Andhra Pradesh, India

🙋‍♀️Author--> Jahnavi Durga Ganapathi, Feel free to connect or contribute!
