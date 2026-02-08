# 🔍 AI-Based Code Similarity & Plagiarism Detection System

Hybrid plagiarism detection system using **Lexical + AST (Global & Subtree) + Stylistic Features**.  
Built with **Python** and deployed using **Streamlit**.

---

## 🚀 Live Demo  
👉 https://ai-code-plagiarism-detector-gd7yinnbfzrd7up6cw4h93.streamlit.app/

---

## 🧠 Features
- Pairwise code similarity comparison  
- Multi-file plagiarism detection  
- Similarity matrix with heatmap visualization  
- Clustering of similar (potentially plagiarized) submissions  
- ROC Curve & AUC-based evaluation  

---

## 📁 Project Structure

```bash
analysis/    # Evaluation, clustering, ROC  
model/       # Similarity model  
lexical/     # Lexical feature extraction  
syntactic/   # AST-based analysis  
stylistic/   # Coding style features  
app.py       # Streamlit web app  

```
🛠 Tech Stack

Python
Streamlit
NumPy, Pandas
Scikit-learn

▶️ How to Run Locally

# Clone the repo
git clone https://github.com/Surya12-04/ai-code-plagiarism-detector.git

# Go inside project folder
cd ai-code-plagiarism-detector

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py

👤 Author

Surya Prakash Singh
B.Tech Student | AI / ML Enthusiast
GitHub: https://github.com/Surya12-04

