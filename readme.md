# Sholix Payment System (SPS)

**A Kenya-first payment management platform designed to simplify business payment collection and transaction monitoring.**

Sholix Payment System (SPS) is a web-based platform under development, with a React and TypeScript frontend and a Django REST Framework backend. Its initial focus is helping businesses manage payment orders and build toward automated M-Pesa payment collection.

The project is being developed incrementally, starting with the core dashboard and backend APIs before integrating payment providers.

## Project Status

**Current stage:** Core application development

Implemented foundations:
- React and TypeScript dashboard using Vite.
- Django REST Framework backend.
- Django administrative interface.
- Business, payment order, payment transaction, and audit log data models.
- Dashboard summary API.
- Initial API authentication and access controls.
- SQLite database for local development.

Planned capabilities:
- Safaricom Daraja sandbox integration.
- M-Pesa STK Push payment requests.
- Paybill and Till payment recording through C2B callbacks.
- Transaction status monitoring and reconciliation.
- Business-specific dashboards and access permissions.
- Additional payment channels, subject to provider support and applicable requirements.
- Secure, authorized payouts, subject to provider approval and applicable regulatory requirements.

**Important:** M-Pesa payments are not yet connected to Safaricom. The current application does not independently process, receive, store, or transfer real funds.

## Technology Stack

### Frontend
- React
- TypeScript
- Vite
- CSS

### Backend
- Python
- Django
- Django REST Framework
- SQLite for local development

### Planned Payment Integration
- Safaricom Daraja API
- M-Pesa STK Push
- M-Pesa C2B integration for Paybill and Till payments

## Project Structure

```text
sholix_payment_system/
├── backend/
│   ├── config/
│   │   ├── settings.py
│   │   └── urls.py
│   ├── payments/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── App.css
│   │   └── services/
│   │       └── api.ts
│   ├── package.json
│   └── vite.config.ts
├── .gitignore
└── README.md
```

*The structure above describes the intended layout. Some files may differ depending on the current development state.*

## Getting Started

### Prerequisites

Install:
- Python compatible with the project's Django dependencies.
- Node.js and npm.
- Git.

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd sholix_payment_system
```

Replace `YOUR_REPOSITORY_URL` with the actual GitHub repository URL.

### 2. Set up the backend

In PowerShell:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If the dependency file is missing or incomplete, install the project's required packages before continuing.

Configure environment variables for local development. Never commit real secret keys or payment-provider credentials.

Apply database migrations:

```powershell
python manage.py migrate
```

Create an administrator account if one does not already exist:

```powershell
python manage.py createsuperuser
```

Start the backend:

```powershell
python manage.py runserver
```

Backend URLs:

- API root: http://127.0.0.1:8000/
- Health check: http://127.0.0.1:8000/api/health/
- Dashboard API: http://127.0.0.1:8000/api/dashboard/
- Django admin: http://127.0.0.1:8000/admin/

The dashboard API requires appropriate authentication and permissions.

### 3. Set up the frontend

Open a second PowerShell terminal:

```powershell
cd C:\Users\alexbahati\sholix_payment_system\frontend
npm install
npm run dev
```

Open the frontend at:

http://localhost:5173/

The Vite development server should proxy API requests to the Django backend according to `vite.config.ts`. Start both servers when running the complete application locally.

## Core Data Models

The current backend includes:

- **Business:** business identity and basic configuration.
- **PaymentOrder:** collection or payout order details, amount, channel, reference, and status.
- **PaymentTransaction:** transaction records associated with payment orders.
- **AuditLog:** records of application actions for auditing.

The existence of these models does not mean every payment workflow is fully implemented.

## Security Principles

SPS is being designed around the following principles:

- Keep credentials and environment secrets out of source control.
- Require authentication and authorization for sensitive APIs.
- Validate payment amounts and transaction data.
- Verify provider callbacks before marking payments successful.
- Use idempotency and reconciliation to reduce duplicate processing.
- Maintain auditable records of important actions.
- Restrict access to business data by tenant and user permissions as the application evolves.

Development settings are not suitable for production without a security review.

## Development Roadmap

1. Complete the dashboard and API integration.
2. Build business management and payment order interfaces.
3. Integrate M-Pesa STK Push in the Daraja sandbox.
4. Implement verified Paybill and Till C2B callbacks.
5. Add transaction monitoring and reconciliation.
6. Strengthen business-specific permissions and audit trails.
7. Prepare for production after provider approval, security testing, and any applicable compliance requirements.

## Contributing

The project is under active development. Changes should be tested locally, and existing functionality should be preserved when extending the application.

## License

No open-source license has been declared yet. All rights are reserved by the project owner unless a license is added.
