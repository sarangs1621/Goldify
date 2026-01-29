# 💎 Jewellery ERP System  
### Enterprise-Grade Inventory, Billing & Gold Ledger Platform

![Build](https://img.shields.io/badge/build-stable-brightgreen)
![Version](https://img.shields.io/badge/version-1.0-blue)
![Backend](https://img.shields.io/badge/backend-FastAPI-green)
![Frontend](https://img.shields.io/badge/frontend-React%20%2B%20Tailwind-blue)
![Database](https://img.shields.io/badge/database-MongoDB-brightgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## 🏪 Designed for Jewellery Businesses

This ERP system is purpose-built for **gold & jewellery showrooms**, workshops, and wholesalers.  
It handles **gold weight tracking, customer/vendor balances, job cards, invoices, returns, and financial reports** — all in one secure platform.

✔ Ideal for single-store & multi-branch operations  
✔ Accurate gold weight reconciliation  
✔ Audit-safe billing & returns  
✔ Ready for production deployment  

---

## 🎯 Business Problems Solved

- ❌ Manual gold stock mismatches  
- ❌ Billing errors due to rate/weight confusion  
- ❌ No visibility into party gold balance  
- ❌ Difficult return reconciliation  
- ❌ No audit trail  

✅ **This system fixes all of them**

---

## ✨ Core Modules

### 🪙 Gold Ledger System
- Party-wise gold balance
- Automatic gold settlement
- Combined gold + money view

### 📦 Inventory Management
- Category-wise gold stock
- Stock IN / OUT movements
- Auto deduction on invoice finalization

### 🛠️ Job Cards
- Workshop job cards
- Gold rate locking
- Direct invoice generation

### 🧾 Billing & Invoicing
- Draft & final invoices
- Discount handling
- Gold exchange payment mode

### 🔄 Returns
- Return drafts
- Partial & full returns
- Inventory reconciliation

---

## 🖼️ Screenshots (Demo)

> _Replace with actual screenshots_

- Login Screen  
- Dashboard Overview  
- Inventory Management  
- Job Card Creation  
- Invoice Preview  
- Gold Ledger Report  

📸 `/docs/screenshots/`

---

## 🧩 System Architecture

> High-level flow diagram

```
[ React Frontend ]
        |
        v
[ FastAPI Backend ]
        |
        v
[ MongoDB Database ]
```

- Frontend communicates via REST APIs
- Backend enforces business rules
- Database maintains full audit trail

---

## 🏗️ Technology Stack

### Frontend
- React.js
- Tailwind CSS
- Axios

### Backend
- FastAPI (Python)
- JWT Authentication
- REST APIs

### Database
- MongoDB

### Infrastructure
- Supervisor (auto-restart)
- Health check scripts
- Kubernetes-ready routing

---

## ⚙️ Environment Configuration

### Frontend
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

### Backend
```env
MONGO_URL=<mongo-connection-string>
DB_NAME=gold_shop_erp
JWT_SECRET=<secure-secret>
```

---

## 🚀 Getting Started (Demo Mode)

### Backend
```bash
cd backend
python -m venv venv
pip install -r requirements.txt
python server.py
```

### Frontend
```bash
cd frontend
yarn install
yarn start
```

➡ Open browser: **http://localhost:3000**

---

## 🧪 Testing & Reliability

- Manual UI testing
- API testing via Postman
- Edge case testing:
  - Zero-stock invoices
  - Partial returns
  - Draft vs final billing

---

## 🩺 Health & Monitoring

```bash
bash scripts/startup_check.sh
sudo supervisorctl status
sudo supervisorctl restart all
```

Logs:
- Backend: `/var/log/supervisor/backend.err.log`
- Frontend: `/var/log/supervisor/frontend.err.log`

---

## 🔐 Security & Audit

- JWT-based authentication
- Role-ready architecture
- Full audit logs
- Safe draft workflows

---

## 📄 License
MIT License

---

## 📌 Project Status

- Version: 1.0  
- Deployment: Production Ready  
- Client Demo: Ready ✅  
