# 💰 Secure Wallet API

![Python](https://img.shields.io/badge/python-3.12-blue?logo=python&style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white&style=flat-square)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?logo=postgresql&logoColor=white&style=flat-square)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-3676AB?logo=sqlalchemy&logoColor=white&style=flat-square)
![License](https://img.shields.io/github/license/hasansharif819/secure-wallet?style=flat-square)

---

## ✨ Project Overview

**Secure Wallet API** is a modern, secure wallet management backend built with FastAPI, allowing users to:

- Register and login with JWT authentication 🔐
- Top-up and withdraw funds from their wallet 💳
- View real-time wallet balance and transaction history 📊
- Built on async SQLAlchemy ORM with PostgreSQL for scalability ⚡

---

## 🚀 Quick Start Guide

Follow the steps below to get the project up and running on your local machine.

---

### 1️⃣ Clone the repository

```bash
git clone https://github.com/hasansharif819/secure-wallet.git
cd secure-wallet
```

### 2️⃣ Create & activate Python virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate     # Windows
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure PostgreSQL Database
Make sure PostgreSQL is installed and running.

Create the database for the app:

```bash
sudo -i -u postgres psql
CREATE DATABASE wallet_db;
GRANT ALL PRIVILEGES ON DATABASE wallet_db TO database_user_name
\q
```

### 5️⃣ Setup environment variables
Update alembic.ini file (line 87) with the following content:
```bash
sqlalchemy.url = postgresql+asyncpg://sharif:password@localhost:5432/wallet_db
Replace sharif with <your_database_user> and password <your_database_password>
```

Also Update the database/db_url.py file

```bash
SQLALCHEMY_DATABASE_URL="postgresql+asyncpg://sharif:password@localhost:5432/wallet_db"
Replace sharif with <your_database_user> and password <your_database_password>
```

### 6️⃣ Run database migrations (Optional)
As you cloning may be its not needed. You can skip this. If you use this please see the alembic/versions/"your migration name file" then update that upgrade and downgrade
Alembic for migrations, run:

```bash
alembic revision --autogenerate -m "initial migration"
alembic upgrade head
If you are not using migrations and rely on SQLAlchemy to create tables automatically, skip this step.
```

### 7️⃣ Start the FastAPI server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
Open your browser at http://localhost:5000/docs to access the API.
```

### View on Swagger
```bash
https://youtu.be/Fz-8cs8Gc8s
```

### 📂 Project Structure

* secure-wallet/
* │
* ├── app/
* │   ├── api/              # API routes and endpoints
* │   ├── core/             # Security
* │   ├── database/         # DB session & base class
* │   ├── models/           # SQLAlchemy ORM models
* │   ├── schemas/          # Pydantic data models (validation)
* │   ├── services/         # Business logic & utilities
* │   └── main.py           # FastAPI app entrypoint
* │
* ├── tests/                # Async test suites with pytest
* ├── alembic/              # Alembic migrations (if used)
* ├── requirements.txt      # Python dependencies
* └── README.md             # Project documentation

### 🔥 API Endpoints Summary
Method	Endpoint	Description	Auth Required
POST	/auth/register	Register new user	No
POST	/auth/login	Obtain JWT access token	No
GET	/wallet/balance	Get current wallet balance	Yes
POST	/wallet/top-up	Add funds to wallet	Yes
POST	/wallet/withdraw	Withdraw funds from wallet	Yes


### 👨‍💻 Author
* Sharif Hasan
* ✉️ hs.sharif819@gmail.com
* 📞 +8801640911511
* 🌐 [GitHub](https://github.com/hasansharif819)
