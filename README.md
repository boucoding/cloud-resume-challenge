# AWS Cloud Resume Challenge — Production Serverless Architecture (2026 Edition)

**Candidate:** Abdelrahman Ahmed  
**Role:** AI & Agent Engineer — Agent Orchestration, Evals, RAG Systems  
**Connect:** [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/aadiab) · [![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/boucoding) · [![Email](https://img.shields.io/badge/Email-D14836?style=flat&logo=gmail&logoColor=white)](mailto:bouprogramming@gmail.com)  
**Live Resume Website:** [https://d1v34jwaipditu.cloudfront.net](https://d1v34jwaipditu.cloudfront.net)  
**Live Visitor Counter API:** [https://zegbzy1j8g.execute-api.eu-north-1.amazonaws.com/visitors](https://zegbzy1j8g.execute-api.eu-north-1.amazonaws.com/visitors)  
**GitHub Repository:** [boucoding/cloud-resume-challenge](https://github.com/boucoding/cloud-resume-challenge)

---

## Architecture Overview

```
[ Visitor Browser ] 
        │
        ▼ (HTTPS)
[ CloudFront Distribution ] ──(Origin Access Control / OAC)──► [ S3 Static Website Bucket ]
        │                                                     (Private, block public access)
        │ (Custom domain / Route 53 / ACM optional toggle)
        │
        ▼ (Fetch /visitors)
[ API Gateway HTTP API (v2) ] (CORS enabled)
        │
        ▼ (AWS Lambda Proxy)
[ Python 3.12 Lambda Function ] (Atomic counter logic + Pytest suite)
        │
        ▼ (IAM Least Privilege)
[ DynamoDB Table ] (PK: id="visitors", count attribute)

──────────────────────────────────────────────────────────────────────────────────────────
DevOps & CI/CD:
GitHub Repo ──► GitHub Actions (OIDC auth via AWS IAM Role)
  ├── terraform.yml (fmt, tflint, checkov, plan on PR, apply on main)
  ├── backend.yml   (pytest, build zip, deploy lambda)
  └── frontend.yml  (inject API URL, sync S3, invalidate CloudFront)
```

---

## 1. What Was Built

A full-stack, serverless, production-grade cloud resume platform with an automated CI/CD engine built declaratively with Terraform.

- **Frontend**: Responsive, modern tech resume showcasing AI & Agent Engineering experience, with a real-time visitor counter that deduplicates rapid page refreshes using `sessionStorage`.
- **CDN & Edge Security**: AWS CloudFront serving the static site over TLS 1.2+ with Origin Access Control (OAC), custom response security headers (HSTS, X-Content-Type-Options, X-Frame-Options), and optional Route 53 + ACM custom domain routing.
- **Serverless API**: API Gateway HTTP API (v2) routing requests to an AWS Lambda function running Python 3.12.
- **Database**: Amazon DynamoDB storing the visitor count, updated atomically using `ADD` expressions to eliminate concurrency race conditions.
- **Infrastructure as Code (IaC)**: 100% codified in Terraform with S3 remote state and DynamoDB state locking.
- **Continuous Integration / Continuous Deployment (CI/CD)**: GitHub Actions federated with AWS via **OpenID Connect (OIDC)**, eliminating long-lived credentials.

---

## 2. Architectural Decisions & Justifications

### Why CloudFront + Origin Access Control (OAC) instead of direct S3 website hosting?
Direct S3 static website hosting requires bucket objects to be publicly readable and does not natively support HTTPS with custom certificates or caching at the edge. By placing CloudFront in front with **Origin Access Control (OAC)**, the S3 bucket is completely private (`BlockPublicAcls = true`, `BlockPublicPolicy = true`). OAC signs requests with AWS SigV4, ensuring traffic can only originate through CloudFront with TLS encryption and low latency.

### Why API Gateway HTTP API (v2) instead of REST API (v1)?
HTTP APIs (v2) are designed specifically for serverless workloads:
1. **~70% cheaper** than REST APIs ($1.00 per million requests vs $3.50).
2. **Lower latency** because they omit legacy WS-Security and mapping template bloat.
3. Native CORS configuration directly at the gateway layer.

### Why DynamoDB with atomic counter expressions?
For a visitor counter, relational databases like RDS/Postgres introduce unnecessary costs ($15+/mo), connection pooling issues with Lambda, and maintenance overhead. DynamoDB is serverless, charges only per request (`PAY_PER_REQUEST`), and supports atomic update expressions:
```python
UpdateExpression="ADD #count :incr"
```
This guarantees race-condition-free counting under concurrent traffic without manual transactions or pessimistic locking.

### Why GitHub Actions with OIDC instead of long-lived AWS Access Keys?
Storing static `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in GitHub secrets creates a persistent attack surface. With **OIDC Federation**, GitHub Actions requests a short-lived token from AWS STS via `sts:AssumeRoleWithWebIdentity`, bound strictly to repository claims (`repo:boucoding/cloud-resume-challenge:*`). The credentials expire automatically after each workflow step.

---

## 3. Repository Structure

```
├── .github/
│   └── workflows/
│       ├── terraform.yml       # Formatting, TFLint, Checkov scan, plan & apply
│       ├── backend.yml         # Pytest + Moto tests, packaging, Lambda update
│       └── frontend.yml        # Inject API Gateway URL, S3 sync, CloudFront invalidation
├── bootstrap/                  # One-time automated state & OIDC setup
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── setup-bootstrap.ps1
├── terraform/                  # Main declarative infrastructure
│   ├── backend.tf              # S3 remote state + DynamoDB lock config
│   ├── providers.tf            # AWS providers
│   ├── variables.tf            # Region, custom domain toggles
│   ├── s3.tf                   # Private S3 static site bucket + OAC policy
│   ├── cloudfront.tf           # CloudFront CDN + security headers policy
│   ├── dns.tf                  # Conditional Route 53 + ACM SSL records
│   ├── dynamodb.tf             # Table with atomic counter item
│   ├── lambda.tf               # Python 3.12 Lambda, IAM least-privilege role
│   ├── api_gateway.tf          # HTTP API v2 + CORS + CloudWatch logging
│   ├── monitoring.tf           # CloudWatch Alarm on Lambda Errors
│   └── outputs.tf              # CloudFront URL, API URL, S3 bucket names
├── backend/
│   ├── lambda_function.py      # Python 3.12 handler (atomic ADD / read-only)
│   ├── requirements.txt
│   ├── requirements-dev.txt    # pytest, moto
│   └── tests/
│       └── test_lambda.py      # Unit tests (increment, get, CORS)
├── frontend/
│   ├── index.html              # Modern, responsive resume for Abdelrahman Ahmed
│   ├── css/
│   │   └── style.css           # Modern dark-mode styling with ambient glow
│   └── js/
│       └── counter.js          # Client counter with sessionStorage deduplication
└── README.md                   # Engineering documentation
```

---

## 4. Setup & Deployment Guide

### Prerequisites
- AWS CLI configured (`aws configure`) with administrative credentials.
- Terraform `>= 1.5.0` installed.
- Python `>= 3.10` installed.

### Step 1: Run One-Time Bootstrap
From the project root:
```powershell
.\bootstrap\setup-bootstrap.ps1 -GithubRepo "boucoding/cloud-resume-challenge"
```
This script creates:
1. S3 bucket for Terraform remote state.
2. DynamoDB lock table (`cloud-resume-tf-locks`).
3. GitHub OIDC Provider & IAM Role (`cloud-resume-github-actions-role`).
4. Automatically updates `terraform/backend.tf` with the state bucket name.

### Step 2: Configure GitHub Repository Secrets / Variables
In your GitHub repository (`Settings -> Secrets and variables -> Actions`):
- **`AWS_ROLE_TO_ASSUME`**: The IAM Role ARN output by the bootstrap script.
- **`AWS_REGION`**: `us-east-1` (or your chosen AWS region).

### Step 3: Initialize and Deploy Infrastructure Locally (or via Git Push)
To deploy locally:
```bash
cd terraform
terraform init
terraform plan
terraform apply
```
Or simply push to `main` branch to trigger GitHub Actions!

---

## 5. Testing & Validation

### Backend Unit Tests
Run local unit tests with `pytest` and `moto` (no AWS account required):
```bash
pip install -r backend/requirements-dev.txt
pytest -v backend/tests/
```

### Security Scanning
Scan Terraform code for security vulnerabilities and compliance:
```bash
checkov -d terraform/
```
