# 🏯 Samurai Mechanic 🚗  
A GPT-Powered 3000GT Manual Assistant

**Samurai Mechanic** is a Streamlit app that lets you ask questions about your Mitsubishi 3000GT.  
It uses OpenAI’s Assistants API and your uploaded manual PDF to return accurate answers—delivered with the honor of a samurai.

---

## ⚙️ Features

- 💬 Natural language Q&A
- 📄 Uses a PDF car manual with file search
- 🧠 GPT-4o-mini assistant trained with a system prompt
- 🖥️ Streamlit front-end
- 🔄 Session tracking and cleanup

---

## 🚀 Setup Instructions

1. **Clone the repo**:
   ```bash
   git clone https://github.com/yourusername/samurai-mechanic.git
   cd samurai-mechanic
   ```

2. **Set your OpenAI API key**:
   ```bash
   export OPENAI_API_KEY=your_key
   ```

3. **Install dependencies**:
   ```bash
   pip install openai streamlit
   ```

4. **Run setup notebook** (`initial_setup.ipynb`) to:
   - Upload the `3000gt_manual.pdf`
   - Create an assistant
   - Note the `file_id` and `assistant_id`

5. **Update `app.py`**:
   Paste your `ASSISTANT_ID` and `FILE_ID` into the top of `app.py`.

6. **Launch the app**:
   ```bash
   streamlit run app.py
   ```

---

## 📂 File Overview

- `initial_setup.ipynb` — Uploads manual + creates assistant  
- `app.py` — Main Streamlit app  
- `3000gt_manual.pdf` — Referenced car manual (must be in root directory)  
- `README.md` — You're reading it

---

## 🧠 Example Q&A

**You**:  
*How do I replace the clutch?*

**Samurai**:  
*"First, warrior, remove the transmission as though drawing your blade. Then follow the torque specs as if they were sacred scrolls..."*
