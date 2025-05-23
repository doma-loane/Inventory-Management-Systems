# 📦 Inventory Management Systems

A lightweight, scalable inventory and sales management system designed for retail operations using barcode/QR code scanning, real-time analytics, and efficient stock tracking.

---

## 🚦 Test & Coverage Status

[![Test Suite](https://github.com/doma-loane/Inventory-Management-Systems/actions/workflows/tests.yml/badge.svg)](https://github.com/doma-loane/Inventory-Management-Systems/actions/workflows/tests.yml)
[![Coverage Status](https://codecov.io/gh/doma-loane/Inventory-Management-Systems/branch/main/graph/badge.svg)](https://codecov.io/gh/doma-loane/Inventory-Management-Systems)

---

## 🛠 Features

- 📋 Product catalog and barcode/QR code scanning
- 📦 Real-time inventory tracking
- 🧮 Daily sales logging and performance reports
- 📊 Dashboard with visual analytics
- 🔐 Multi-user role-based access
- 📸 Mobile camera integration for product scanning

---

## 📂 Project Structure

```plaintext
Inventory-Management-Systems/
│
├── app/                  # Main application package
│   ├── routes/           # Flask Blueprints (e.g., inventory, sales)
│   ├── models.py         # SQLAlchemy models
│   ├── forms.py          # WTForms classes
│   └── __init__.py       # App factory
│
├── tests/                # Unit and route tests (pytest)
│   └── conftest.py       # Shared test fixtures
│
├── migrations/           # Alembic DB migrations
├── .github/workflows/    # CI/CD pipeline
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

---

## 🚀 Getting Started

### 1. Clone and create a virtual environment

```bash
git clone https://github.com/doma-loane/Inventory-Management-Systems.git
cd Inventory-Management-Systems
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up the database

```bash
flask db upgrade
```

### 4. Run the application

```bash
flask run
```

### 5. Run tests

```bash
pytest --cov=app tests/
```

---

## 📃 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
