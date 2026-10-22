# 💜 PocketPal — Student Expense & Saving Advice System

> **An intelligent, cyber-styled financial companion designed for university students to track daily expenditure, manage semester budgets, and receive data-driven, machine learning-powered saving recommendations.**

---

## 👤 Project & Contributor Information

- **Student Name**: Khushi Joshi
- **Project Title**: PocketPal Student Expense System
- **Assigned Module**: **Saving Advice & Financial Intelligence (`pages/Saving_Advice.py`)**
- **Theme**: **PocketPal Dark Cyber Violet Theme**
  - Background: `#07040d`
  - Cards & Containers: `#120b1f`
  - Borders: `#2e1f4d`
  - Text & Accents: Text `#f3e8ff`, Headings `#c084fc`, Primary Purple `#7c3aed`, Highlights `#a855f7` & `#e879f9`

---

## 🌟 Key Features

### 1. 🏠 Main Dashboard (`app.py`)
- **Quick Action Navigation Cards**: One-click routing to **Add Expense**, **Budget Planner**, and **Saving Advice**.
- **Financial KPIs**: Instant metrics for All-Time Spend, Monthly Average Burn Rate, and Primary Spending Drivers computed directly from `expenses.csv`.
- **Interactive Visualizations**: Monthly spending trajectory area graph and category allocation donut chart styled in dark purple theme.
- **Recent Activity Feed**: Real-time snapshot of the latest logged transactions with formatted amounts.
- **Data Management**: Pre-loaded with demo student data, with an option to upload custom CSV files.

### 2. ➕ Add Expense Module (`pages/Add_Expense.py`)
- **Intuitive Logging Form**: Record date, category, amount (₹), description, and payment method (UPI, Cash, Debit Card, etc.).
- **Data Persistence**: Automatically appends new transactions to `expenses.csv` and updates active session memory.
- **Live Summary**: Real-time category spend breakdown and transaction count updates.

### 3. 🎯 Budget Planner & Monitor (`pages/Budget.py`)
- **Configurable Budgets**: Interactive sidebar to set monthly budget limits across academic and living categories.
- **Utilization Gauges**: Color-coded progress indicators (Green = Healthy, Yellow = Warning at 80%, Red = Exceeded).
- **Side-by-Side Analytics**: Visual comparison between planned limits and actual expenditure.

### 4. 💡 Saving Advice & Financial Intelligence (`pages/Saving_Advice.py`) *(Khushi Joshi's Assigned Module)*
- **🔍 Spending Insights**:
  - Essential (Needs) vs. Discretionary (Wants) ratio analysis based on actual records.
  - Interactive Plotly donut and horizontal ranking charts in custom dark theme.
  - Weekday vs. Weekend spending distribution analysis.
  - Payment method digital footprint breakdown.
- **📅 Month-over-Month (MoM) Trend Analysis**:
  - Comparative grouped bar charts across academic months (August – November).
  - Net spending difference and percentage growth rate indicators.
  - Interactive dual-month deep-dive variance table with percentage change calculations and surge/saver detection.
- **💰 Actionable Saving Recommendations & Goal Simulator**:
  - **50/30/20 Student Rule Benchmark**: Evaluates whether discretionary expenditure is safely under 30%.
  - **Practical Student Optimization Tips**: Tailored advice for dining out, textbook borrowing, dorm OTT subscription sharing, and student transit passes.
  - **Interactive Savings Goal Simulator**: Dynamic slider (5% – 40%) calculating exact monthly and annual savings with actionable trimming plans.
- **🤖 Machine Learning: Student Spending Archetypes (K-Means Clustering)**:
  - Feature normalization with `StandardScaler` and clustering via `KMeans(n_clusters=4, random_state=42)`.
  - Classifies student profiles into: *The Frugal Saver*, *The Social Butterfly*, *The Balanced Budgeter*, and *The Academic Investor*.
  - Interactive 2D scatter plot with a **"⭐ YOU ARE HERE"** marker projecting your live profile onto the peer cluster space.

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Core programming language |
| **Web Framework** | [Streamlit](https://streamlit.io/) | Interactive multi-page web UI |
| **Data Processing** | [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/) | Data cleaning, manipulation, and statistical aggregation |
| **Machine Learning**| [Scikit-Learn](https://scikit-learn.org/) | `KMeans` unsupervised clustering, `StandardScaler` |
| **Visualization** | [Plotly Express & Graph Objects](https://plotly.com/python/) | Rich, responsive, interactive charts and cluster plots |

---

## 📂 Project Directory Structure

```text
pocketpal/
│
├── .streamlit/
│   └── config.toml          # Custom PocketPal dark theme configuration
│
├── pages/
│   ├── Add_Expense.py        # Module 1: Transaction entry and management
│   ├── Budget.py             # Module 2: Monthly target setting & monitoring
│   └── Saving_Advice.py      # Module 3: Khushi Joshi's Saving Advice & ML
│
├── app.py                    # Main application dashboard and router
├── expenses.csv              # Demo synthetic student expense dataset
├── requirements.txt          # Python library dependencies for deployment
├── .gitignore                # Git exclusions (venv, __pycache__, secrets)
└── README.md                 # Complete project documentation
```

---

## 💻 Local Installation & Execution

### Step 1: Open the Project Directory
```bash
cd pocketpal
```

### Step 2: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
streamlit run app.py
```
The app will open automatically in your browser at `http://localhost:8501`.

---

## 🚀 How to Upload to Your Personal GitHub Repository

Run these commands inside the `pocketpal/` directory:

```bash
# 1. Open your terminal in the pocketpal project folder:
cd "c:\Users\GANESH JOSHI\Desktop\khushi work\KHUSHI JOSHI\mini\pocketpal"

# 2. Initialize a local Git repository:
git init

# 3. Stage all project files:
git add .

# 4. Commit the changes:
git commit -m "Initial commit: PocketPal Saving Advice module by Khushi Joshi"

# 5. Set the default branch to main:
git branch -M main

# 6. Link to your personal GitHub repository (replace with your repo URL):
git remote add origin https://github.com/<your-username>/<your-repo-name>.git

# 7. Push the code to GitHub:
git push -u origin main
```

---

## ☁️ How to Deploy to Streamlit Community Cloud (Free)

1. Go to **[share.streamlit.io](https://share.streamlit.io/)** and sign in with GitHub.
2. Click **"New app"**.
3. Select your repository: `<your-username>/<your-repo-name>`.
4. Set **Branch** to `main`.
5. Set **Main file path** to `app.py`.
6. Click **Deploy!**. Streamlit Cloud will read `requirements.txt`, install all libraries, and launch your live application with a public URL.

---

## 🔒 Security & Privacy Compliance

- **No Private Data**: Contains only synthetic demo transactions (`expenses.csv`).
- **No Secrets**: Contains zero hardcoded API keys, passwords, or confidential team data.
- **Git Exclusions**: `.gitignore` ensures virtual environments, IDE files, and secrets are never committed.
