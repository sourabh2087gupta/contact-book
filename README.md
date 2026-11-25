# ⚡ Smart Contact Hub

A modern, full-featured **Personal CRM & Connection Manager** built with Python, Streamlit, and SQLite. Designed with a dark cosmic glassmorphism UI, crisp vector icons, and interactive analytics to go far beyond a standard CRUD contact book.

---

## ✨ Key Features

* **Instant QR Code vCard Generator:** Generate scannable vCard 3.0 QR codes directly from any contact card to save details to a mobile phone in seconds.

* **1-Click Smart Actions:** Launch instant WhatsApp chats (`wa.me`), open direct emails (`mailto:`), copy contact details to clipboard, and log "Last Contacted" timestamps with a single click.

* **Interactive Network Analytics:** Dedicated **Insights** tab powered by Plotly featuring dark-themed category distribution charts, cumulative network growth timelines, and an interactive hub-and-spoke connection graph.

* **Smart Fuzzy Search & Duplicate Radar:** Typo-tolerant search engine (powered by `difflib`) paired with an automated Duplicate Radar that flags identical phone numbers and near-matching names.

* **VIP Favorites & Follow-up Notes:** Pin priority contacts to the top with gold-accented VIP cards and attach custom CRM follow-up notes.

* **Validation & Export:** Built-in Regex validation for 10-digit phone numbers and emails, category filtering (`Family`, `Friends`, `College`, `Work`, `General`), and 1-click CSV export.

---
## 🛠️ Tech Stack


* **Language:** Python 3

* **Frontend & UI:** Streamlit, Custom CSS (Glassmorphism), Inline SVGs & Material Icons

* **Database:** SQLite3 (with automatic backward-compatible schema migrations)

* **Visualizations & Utilities:** Plotly, `qrcode[pil]`, `difflib`, `re`, `collections.Counter`

---

## 📁 Project Structure


```text

contact-book/

├── app.py              # Main Streamlit dashboard, tabs, and Plotly analytics

├── database.py         # SQLite connection, CRUD queries, and schema migrations

├── utils.py            # Regex validation, vCard QR generator, fuzzy search & CSV export

├── styles.css          # Cosmic glassmorphism theme, VIP cards, and responsive styling

├── requirements.txt    # Python dependencies

├── .gitignore          # Excludes local database and cache files

└── README.md           # Project documentation

```
## 🚀 Getting Started

1. **Clone the repository:**

   ```bash

   git clone https://github.com/sourabh2087gupta/contact-book.git

   cd contact-book

   ```



2. **Install dependencies:**

   ```bash

   pip install -r requirements.txt

   ```



3. **Run the application:**

   ```bash

   python -m streamlit run app.py

   ```

## 👨‍💻 Author


**Sourabh Gupta**  

*MCA (AI) Student | Python, SQL & Data Analytics*  

GitHub: [@sourabh2087gupta](https://github.com/sourabh2087gupta)