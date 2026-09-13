# LedgerLens v5

**Financial Intelligence System** — Detect anomalies, rank risk, explain findings, and provide a human review workflow.

## Mission

Answer the question: **"What happened in my financial data that I need to know about right now?"**

## Core Architecture

```
CSV / QuickBooks / Xero
        ↓
   Normalize
        ↓
  Intelligence Engine (Deterministic Signals)
        ↓
    Risk Engine
        ↓
   Finding
        ↓
  Human Review Workflow
        ↓
  Audit Trail
```

## Key Principles

- **AI never creates findings** — only explains them
- **Deterministic detection** — signals are reproducible, not magical
- **Multi-tenant by default** — organization_id on every query
- **Audit everything** — every decision is recorded
- **Workflow-first UI** — focus on review and resolution, not dashboards

## Project Structure

```
ledgerlens-v5/
├── apps/
│   ├── api/              # FastAPI backend
│   │   ├── app/
│   │   │   ├── api/      # Endpoints
│   │   │   ├── models/   # SQLAlchemy ORM
│   │   │   ├── schemas/  # Pydantic validation
│   │   │   ├── services/ # Business logic
│   │   │   ├── core/     # Config, security
│   │   │   └── db/       # Database setup
│   │   ├── migrations/   # Alembic
│   │   ├── tests/
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   │
│   └── web/              # React + Vite frontend
│       ├── src/
│       │   ├── pages/
│       │   ├── components/
│       │   ├── api/
│       │   ├── hooks/
│       │   └── types/
│       ├── package.json
│       └── Dockerfile
│
├── docker-compose.yml
├── .env.example
└── README.md
```

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+ (for local web development)
- Python 3.11+ (for local API development)

### Run with Docker

```bash
# 1. Clone the repository
git clone https://github.com/kbmu2304/ledgerlens-v5.git
cd ledgerlens-v5

# 2. Set up environment
cp .env.example .env

# 3. Start all services
docker-compose up --build

# Services will be available at:
# API: http://localhost:8000
# Frontend: http://localhost:5173
# Docs: http://localhost:8000/docs
# Database: localhost:5432
```

### Run Locally (Development)

#### Backend

```bash
cd apps/api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create database
export DATABASE_URL=postgresql://ledgerlens:ledgerlens_dev_password@localhost:5432/ledgerlens

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd apps/web

# Install dependencies
npm install

# Start dev server
npm run dev
```

## API Endpoints

### Findings Workflow

```
GET    /api/v1/findings              # List all findings
GET    /api/v1/findings/{id}         # Get finding detail
POST   /api/v1/findings/{id}/open    # Mark as open
POST   /api/v1/findings/{id}/review  # Start review
POST   /api/v1/findings/{id}/confirm # Confirm issue
POST   /api/v1/findings/{id}/false-positive  # Mark false positive
POST   /api/v1/findings/{id}/resolve # Mark resolved
GET    /api/v1/findings/{id}/audit   # Get audit trail
```

### Data Ingestion

```
POST   /api/v1/imports/csv           # Upload CSV
GET    /api/v1/imports/{id}          # Check import status
```

### Transactions

```
GET    /api/v1/transactions          # List transactions
GET    /api/v1/transactions/{id}     # Get transaction detail
```

### Vendors

```
GET    /api/v1/vendors               # List vendors
GET    /api/v1/vendors/{id}          # Get vendor detail
```

### Audit

```
GET    /api/v1/audit-events          # List all audit events
```

## Database Schema

### Core Tables

- **organizations** — Tenant isolation root
- **users** — Team members per organization
- **transactions** — Normalized financial transactions
- **accounts** — Chart of accounts / bank accounts
- **vendors** — Counterparties / suppliers
- **findings** — Detected anomalies
- **finding_signals** — Evidence supporting a finding
- **reviews** — Human review of findings
- **decisions** — Resolution decision (confirm/false-positive)
- **audit_events** — Immutable audit trail
- **integrations** — Connected data sources (CSV, QB, Xero)

### Finding State Machine

```
DETECTED
   ↓
OPEN
   ↓
UNDER_REVIEW
   ↓
  ┌──────────────┐
  ↓              ↓
CONFIRMED  FALSE_POSITIVE
  ↓              ↓
  └──────┬───────┘
         ↓
     RESOLVED
```

## Intelligence Engine

### Signal Types

1. **Amount Anomaly** — Transaction amount outside historical range
2. **Frequency Anomaly** — Unusual payment frequency to vendor
3. **Vendor Anomaly** — New counterparty or unusual vendor behavior
4. **Timing Anomaly** — Payment outside normal business hours/patterns
5. **Duplicate Anomaly** — Likely duplicate transaction
6. **Account Anomaly** — Unexpected account usage
7. **Historical Anomaly** — Deviation from account trends
8. **Policy Violation** — Explicit policy rule breach

### Risk Scoring

```
risk_score = sum([
    amount_score (0-15),
    frequency_score (0-15),
    vendor_score (0-15),
    timing_score (0-15),
    duplicate_score (0-15),
    account_score (0-15),
    historical_score (0-10),
    policy_score (0-10)
])

Normalized to 0-100:
0-29   → LOW
30-59  → MEDIUM
60-79  → HIGH
80-100 → CRITICAL
```

## Development Workflow

### Add a New Feature

1. **Create a branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Backend changes:**
   - Add models in `apps/api/app/models/`
   - Add API endpoints in `apps/api/app/api/`
   - Add services in `apps/api/app/services/`
   - Write tests in `apps/api/tests/`

3. **Frontend changes:**
   - Add pages in `apps/web/src/pages/`
   - Add components in `apps/web/src/components/`
   - Use hooks from `apps/web/src/hooks/`

4. **Database changes:**
   - Modify SQLAlchemy models
   - Create Alembic migration: `alembic revision --autogenerate -m "description"`
   - Apply migration: `alembic upgrade head`

5. **Commit and push:**
   ```bash
   git add .
   git commit -m "feat: your feature description"
   git push origin feature/your-feature-name
   ```

## Testing

### Backend Tests

```bash
cd apps/api
pytest tests/
```

### Frontend Tests

```bash
cd apps/web
npm run test
```

## Deployment

### Docker Build

```bash
docker build -t ledgerlens-api:latest ./apps/api
docker build -t ledgerlens-web:latest ./apps/web
```

### Production Checklist

- [ ] Set strong `JWT_SECRET`
- [ ] Configure `OPENAI_API_KEY`
- [ ] Use production PostgreSQL (not Docker)
- [ ] Enable HTTPS/TLS
- [ ] Configure CORS properly
- [ ] Set up monitoring/logging
- [ ] Enable Row Level Security in PostgreSQL
- [ ] Backup database regularly

## First Vertical Slice (Definition of Done)

A user should be able to:

1. ✅ Create/select an organization
2. ✅ Import demo CSV
3. ✅ Get normalized transactions
4. ✅ Run deterministic analysis
5. ✅ Generate findings
6. ✅ Open a finding
7. ✅ See evidence/signals
8. ✅ Start a review
9. ✅ Confirm or mark false positive
10. ✅ Resolve finding
11. ✅ See complete audit history
12. ✅ Refresh browser → same state persisted
13. ✅ Never see another organization's data

## Roadmap

### v5.1 (Current)
- [x] Database schema
- [x] SQLAlchemy models
- [x] Finding state machine
- [x] FastAPI endpoints
- [x] React pages
- [x] CSV ingestion
- [x] Deterministic signals
- [x] Risk scoring
- [x] Audit trail

### v5.2
- [ ] QuickBooks integration
- [ ] Xero integration
- [ ] Better signal algorithms
- [ ] AI explanation layer
- [ ] Dashboard with metrics

### v5.3
- [ ] Custom controls/rules
- [ ] Bulk actions
- [ ] Report generation
- [ ] Team collaboration features
- [ ] Mobile app

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request

## License

Proprietary — LedgerLens Inc.

## Support

For issues, questions, or feature requests, open an issue on GitHub.

---

**Building LedgerLens like a real startup.**
