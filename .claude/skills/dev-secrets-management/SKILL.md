---
name: dev-secrets-management
description: Use when handling API keys, database credentials, tokens, certificates, or any sensitive data in applications - comprehensive guide covering storage (environment variables, vaults), rotation, encryption (AES-256, TLS 1.3), secret scanning (truffleHog, gitleaks), emergency response for leaks, and secure patterns for local development, CI/CD, and production environments
---

# Development Secrets Management

## Overview

**A single leaked secret can compromise your entire system.** API keys in GitHub, hardcoded passwords, credentials in Docker images - these aren't theoretical risks. Over 39 million API keys and credentials were exposed on GitHub in 2024 alone.

**Core principle:** Secrets are toxic - handle them like hazardous material with strict containment, rotation, and monitoring protocols.

**Critical truth:** Once a secret is committed to git, it's compromised forever. Deleting it in a new commit doesn't help - it lives in git history.

## When to Use

Use this skill BEFORE storing any sensitive data:
- API keys (AWS, Stripe, SendGrid, third-party services)
- Database credentials (connection strings, passwords)
- OAuth tokens and refresh tokens
- Private keys and certificates
- Encryption keys
- Service account credentials
- Webhook secrets
- Session secrets

**Use this ESPECIALLY when:**
- Setting up a new project (establish patterns from day 1)
- Adding third-party integrations
- Deploying to production
- Setting up CI/CD pipelines
- Working with Docker containers
- Onboarding new team members
- After a security incident

**Don't skip when:**
- "It's just a development key" (dev keys leak too)
- "The repo is private" (private repos aren't vaults)
- "I'll fix it later" (later never comes)
- Under deadline pressure (emergencies create leaks)

## The Iron Laws

```
1. NEVER commit secrets to version control
2. NEVER hardcode secrets in source code
3. ALWAYS rotate secrets after exposure
4. ALWAYS use least-privilege access
5. ALWAYS encrypt secrets at rest
```

Violating these laws is violating application security.

## Anti-Patterns - NEVER Do This

### ❌ Hardcoded Secrets
```python
# WRONG - Hardcoded in source
API_KEY = "sk_live_51H8xK2eZv..."
db_password = "MyP@ssw0rd123"

# WRONG - Hardcoded in config files
config = {
    "stripe_key": "sk_live_51H8xK2eZv...",
    "database_url": "postgresql://user:password@localhost/db"
}
```

### ❌ Secrets in Docker Images
```dockerfile
# WRONG - Baked into image
ENV DATABASE_PASSWORD=secretpass123
ENV AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/...
```

### ❌ Committing .env Files
```bash
# WRONG - .env in git
git add .env
git commit -m "Add environment config"
```

### ❌ Assuming Private Repos Are Safe
```
"It's a private repository, so API keys are fine here"
```
**Reality:** Private repos leak through:
- Accidental public toggle
- Compromised accounts
- Third-party integrations
- Former employee access
- Repository transfers

### ❌ Simple Deletion
```bash
# WRONG - Secret still in git history
# Commit 1: Add config with API key
# Commit 2: Remove API key from config
git add config.py
git commit -m "Remove API key"
```
**The key is still in commit 1's history forever.**

### ❌ Environment Variables for Docker Secrets
```yaml
# WRONG - Environment variables are insecure
environment:
  - DATABASE_PASSWORD=secretpass123
  - API_KEY=sk_live_51H8xK2eZv...
```
**Why wrong:** Environment variables persist in Docker metadata and process lists.

## Storage Strategies by Environment

### Local Development

**Use .env files with strict gitignore:**

```bash
# .env (NEVER commit this)
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
STRIPE_SECRET_KEY=sk_test_51H8xK2eZv...
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

```bash
# .gitignore (ALWAYS include)
.env
.env.local
.env.*.local
*.pem
*.key
secrets/
config/secrets.yml
credentials.json
```

```bash
# .env.example (commit this as template)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
STRIPE_SECRET_KEY=sk_test_your_key_here
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
```

**Load secrets at runtime:**

```javascript
// Node.js with dotenv
require('dotenv').config();
const stripeKey = process.env.STRIPE_SECRET_KEY;
```

```python
# Python with python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()
stripe_key = os.getenv('STRIPE_SECRET_KEY')
```

### CI/CD Pipelines

**GitHub Actions:**

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to production
        env:
          # Injected from GitHub Secrets
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          API_KEY: ${{ secrets.API_KEY }}
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: |
          # Use secrets via environment variables
          ./deploy.sh
```

**GitLab CI:**

```yaml
# .gitlab-ci.yml
deploy:
  stage: deploy
  script:
    - ./deploy.sh
  variables:
    # Injected from GitLab CI/CD Variables (masked & protected)
    DATABASE_URL: $DATABASE_URL
    API_KEY: $API_KEY
  only:
    - main
```

**CircleCI:**

```yaml
# .circleci/config.yml
version: 2.1
jobs:
  deploy:
    docker:
      - image: cimg/node:18.0
    steps:
      - checkout
      - run:
          name: Deploy
          command: ./deploy.sh
          environment:
            # Injected from CircleCI Project Settings
            DATABASE_URL: ${DATABASE_URL}
            API_KEY: ${API_KEY}
```

### Docker Containers

**Use Docker Secrets (Swarm/Compose):**

```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    image: myapp:latest
    secrets:
      - db_password
      - api_key
    environment:
      # Reference secrets by file path
      DATABASE_PASSWORD_FILE: /run/secrets/db_password
      API_KEY_FILE: /run/secrets/api_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    file: ./secrets/api_key.txt
```

**Read secrets from files in application:**

```javascript
// Node.js reading Docker secrets
const fs = require('fs');

function getSecret(secretName) {
  try {
    return fs.readFileSync(`/run/secrets/${secretName}`, 'utf8').trim();
  } catch (err) {
    // Fallback to environment variable for local dev
    return process.env[secretName.toUpperCase()];
  }
}

const dbPassword = getSecret('db_password');
const apiKey = getSecret('api_key');
```

```python
# Python reading Docker secrets
import os

def get_secret(secret_name):
    try:
        with open(f'/run/secrets/{secret_name}', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        # Fallback to environment variable for local dev
        return os.getenv(secret_name.upper())

db_password = get_secret('db_password')
api_key = get_secret('api_key')
```

### Production - Cloud Secrets Managers

**AWS Secrets Manager:**

```python
# Python with boto3
import boto3
import json

def get_secret(secret_name, region_name='us-east-1'):
    client = boto3.client('secretsmanager', region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# Usage
db_credentials = get_secret('prod/database/credentials')
db_password = db_credentials['password']
```

```javascript
// Node.js with AWS SDK
const { SecretsManagerClient, GetSecretValueCommand } = require('@aws-sdk/client-secrets-manager');

async function getSecret(secretName, region = 'us-east-1') {
  const client = new SecretsManagerClient({ region });
  const response = await client.send(
    new GetSecretValueCommand({ SecretId: secretName })
  );
  return JSON.parse(response.SecretString);
}

// Usage
const dbCredentials = await getSecret('prod/database/credentials');
const dbPassword = dbCredentials.password;
```

**Azure Key Vault:**

```python
# Python with Azure SDK
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def get_secret(vault_url, secret_name):
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    return client.get_secret(secret_name).value

# Usage
vault_url = "https://myvault.vault.azure.net/"
api_key = get_secret(vault_url, "api-key")
```

**Google Cloud Secret Manager:**

```python
# Python with Google Cloud SDK
from google.cloud import secretmanager

def get_secret(project_id, secret_id, version_id='latest'):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode('UTF-8')

# Usage
api_key = get_secret('my-project-id', 'api-key')
```

**HashiCorp Vault:**

```python
# Python with hvac
import hvac

def get_secret(vault_addr, token, path):
    client = hvac.Client(url=vault_addr, token=token)
    response = client.secrets.kv.v2.read_secret_version(path=path)
    return response['data']['data']

# Usage
vault_addr = 'https://vault.example.com:8200'
token = os.getenv('VAULT_TOKEN')  # From managed identity or environment
secrets = get_secret(vault_addr, token, 'secret/data/myapp')
api_key = secrets['api_key']
```

## Secrets Manager Comparison

| Feature | AWS Secrets Manager | Azure Key Vault | GCP Secret Manager | HashiCorp Vault |
|---------|---------------------|-----------------|-------------------|-----------------|
| **Rotation** | Automatic for RDS, Lambda-based custom | Manual or Event Grid | Manual or scripted | Advanced with templates |
| **Dynamic Secrets** | No | No | No | Yes |
| **Multi-Cloud** | AWS only | Azure-centric | GCP only | Yes |
| **Pricing** | $0.40/secret/month + API calls | Nominal (cheapest) | Per version + operations | Client-based (expensive) |
| **Ease of Use** | High (AWS native) | High (Azure native) | Medium | Low (complex setup) |
| **Best For** | AWS workloads | Azure workloads, cost-sensitive | GCP workloads | Multi-cloud, advanced needs |

## Encryption Best Practices

### Encryption at Rest

**Use AES-256-GCM for sensitive data:**

```python
# Python encryption with cryptography library
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

def encrypt_secret(plaintext: str, key: bytes) -> bytes:
    """Encrypt secret using AES-256-GCM"""
    aesgcm = AESGCM(key)  # key must be 32 bytes for AES-256
    nonce = os.urandom(12)  # 96-bit nonce
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
    return nonce + ciphertext  # Prepend nonce to ciphertext

def decrypt_secret(encrypted: bytes, key: bytes) -> str:
    """Decrypt secret using AES-256-GCM"""
    aesgcm = AESGCM(key)
    nonce = encrypted[:12]
    ciphertext = encrypted[12:]
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode()

# Usage
encryption_key = os.urandom(32)  # Store this in KMS!
encrypted = encrypt_secret("my-api-key-12345", encryption_key)
decrypted = decrypt_secret(encrypted, encryption_key)
```

**Key Management with Cloud KMS:**

```python
# AWS KMS for envelope encryption
import boto3
import base64

def encrypt_with_kms(plaintext, key_id):
    """Encrypt data using AWS KMS"""
    kms = boto3.client('kms')
    response = kms.encrypt(KeyId=key_id, Plaintext=plaintext)
    return base64.b64encode(response['CiphertextBlob'])

def decrypt_with_kms(ciphertext):
    """Decrypt data using AWS KMS"""
    kms = boto3.client('kms')
    response = kms.decrypt(CiphertextBlob=base64.b64decode(ciphertext))
    return response['Plaintext']
```

### Encryption in Transit

**Always use TLS 1.3 (or minimum TLS 1.2):**

```python
# Python requests with TLS verification
import requests

# GOOD - Verify TLS certificates
response = requests.get('https://api.example.com', verify=True)

# WRONG - Disabling verification
# response = requests.get('https://api.example.com', verify=False)
```

```javascript
// Node.js HTTPS with TLS 1.3
const https = require('https');

const options = {
  hostname: 'api.example.com',
  path: '/endpoint',
  method: 'GET',
  minVersion: 'TLSv1.3',  // Require TLS 1.3
  rejectUnauthorized: true  // Verify certificates
};

https.request(options, callback);
```

## Secret Rotation Strategies

### Rotation Frequency Guidelines

| Secret Type | Rotation Frequency | Rationale |
|-------------|-------------------|-----------|
| Database credentials | 30-90 days | Balance security vs. operational overhead |
| API keys (read/write) | 30 days | High-risk operations |
| API keys (read-only) | 90 days | Lower risk |
| OAuth tokens | Per spec (15 min - 1 hour) | Built into OAuth 2.0 |
| SSH keys | 90-180 days | Access control critical |
| Certificates | Before expiry (60 days) | Avoid service disruption |
| After employee departure | Immediately | Prevent unauthorized access |

### Zero-Downtime Rotation Pattern

```python
# Python example of zero-downtime API key rotation
import time

class DualKeyManager:
    """Manages two active keys during rotation"""

    def __init__(self):
        self.current_key = load_secret('api_key_current')
        self.previous_key = load_secret('api_key_previous')

    def rotate_key(self, new_key):
        """Rotate to new key with zero downtime"""
        # Step 1: Generate new key
        save_secret('api_key_current', new_key)

        # Step 2: Keep old key as fallback
        save_secret('api_key_previous', self.current_key)

        # Step 3: Update application config
        self.previous_key = self.current_key
        self.current_key = new_key

        # Step 4: Wait for propagation (30 seconds)
        time.sleep(30)

        # Step 5: Verify new key works
        if not self.verify_key(new_key):
            # Rollback if new key fails
            self.current_key = self.previous_key
            raise Exception("New key verification failed")

    def verify_key(self, key):
        """Test key against API"""
        # Implementation specific to your API
        pass

# Automated rotation with AWS Secrets Manager
def lambda_handler(event, context):
    """Lambda function for automatic rotation"""
    import boto3

    client = boto3.client('secretsmanager')
    secret_id = event['SecretId']
    token = event['ClientRequestToken']
    step = event['Step']

    if step == 'createSecret':
        # Generate new secret version
        new_secret = generate_new_api_key()
        client.put_secret_value(
            SecretId=secret_id,
            ClientRequestToken=token,
            SecretString=new_secret
        )

    elif step == 'setSecret':
        # Update service to use new secret
        update_service_credentials(secret_id, token)

    elif step == 'testSecret':
        # Verify new secret works
        verify_new_credentials(secret_id, token)

    elif step == 'finishSecret':
        # Mark rotation complete
        client.update_secret_version_stage(
            SecretId=secret_id,
            VersionStage='AWSCURRENT',
            MoveToVersionId=token
        )
```

## Secret Scanning Tools

### Pre-Commit Hooks (Prevention)

**Install git-secrets:**

```bash
# macOS
brew install git-secrets

# Linux
git clone https://github.com/awslabs/git-secrets
cd git-secrets
make install

# Setup for repository
cd /path/to/your/repo
git secrets --install
git secrets --register-aws  # Add AWS patterns
```

**Install detect-secrets:**

```bash
pip install detect-secrets

# Create baseline
detect-secrets scan > .secrets.baseline

# Add pre-commit hook
cat > .pre-commit-config.yaml <<EOF
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
EOF

# Install pre-commit
pip install pre-commit
pre-commit install
```

### Repository Scanning (Detection)

**TruffleHog (800+ secret types, verification):**

```bash
# Install
pip install truffleHog

# Scan entire git history
trufflehog git https://github.com/yourorg/yourrepo --only-verified

# Scan specific branch
trufflehog git file://. --since-commit HEAD~10

# Scan with JSON output
trufflehog git https://github.com/yourorg/yourrepo --json > results.json
```

**Gitleaks (fast, lightweight):**

```bash
# Install
brew install gitleaks

# Scan repository
gitleaks detect --source . --verbose

# Scan with config
gitleaks detect --config .gitleaks.toml --report-path report.json

# CI/CD integration
gitleaks detect --no-git --verbose --redact
```

**GitHub Secret Scanning (built-in):**

```bash
# Enable in repository settings
# Settings > Security > Code security and analysis > Secret scanning

# View alerts
gh api repos/{owner}/{repo}/secret-scanning/alerts
```

### CI/CD Integration

```yaml
# GitHub Actions with multiple scanners
name: Secret Scanning

on: [push, pull_request]

jobs:
  scan-secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Full history for scanning

      - name: TruffleHog scan
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD

      - name: Gitleaks scan
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Emergency Response - Leaked Secret

**If you discover a leaked secret, follow this procedure IMMEDIATELY:**

### 1. Revoke Compromised Credential (0-5 minutes)

```bash
# AWS - Deactivate access key
aws iam update-access-key --access-key-id AKIAIOSFODNN7EXAMPLE --status Inactive --user-name username

# GitHub - Revoke personal access token
gh api -X DELETE /applications/grants/{grant_id}

# Stripe - Roll API key
# Dashboard > Developers > API Keys > Roll key

# Database - Change password
psql -U postgres -c "ALTER USER myuser PASSWORD 'new_secure_password';"
```

**WARNING:** Simply deleting the secret from code is NOT enough. The leaked credential must be revoked/rotated.

### 2. Assess Blast Radius (5-15 minutes)

```bash
# Check CloudTrail for AWS key usage
aws cloudtrail lookup-events --lookup-attributes AttributeKey=AccessKeyId,AttributeValue=AKIAIOSFODNN7EXAMPLE --max-results 50

# Check application logs for unauthorized access
grep "AKIAIOSFODNN7EXAMPLE" /var/log/app/*.log

# Review service provider logs/dashboards
# Stripe Dashboard > Developers > Logs
# GitHub Settings > Security log
```

### 3. Scrub Git History (15-30 minutes)

**Using git-filter-repo (recommended):**

```bash
# Install
pip install git-filter-repo

# Create expressions file
cat > secrets-to-remove.txt <<EOF
literal:sk_live_51H8xK2eZv
regex:AKIA[0-9A-Z]{16}
literal:MyP@ssw0rd123
EOF

# Rewrite history
git filter-repo --replace-text secrets-to-remove.txt

# Force push (coordinate with team!)
git push origin --force --all
git push origin --force --tags
```

**Using BFG Repo-Cleaner:**

```bash
# Install
brew install bfg

# Clone mirror
git clone --mirror https://github.com/yourorg/yourrepo.git

# Remove secrets
bfg --replace-text secrets-to-remove.txt yourrepo.git

# Clean up
cd yourrepo.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push
git push --force
```

### 4. Generate New Credentials (30-45 minutes)

```bash
# AWS - Create new access key
aws iam create-access-key --user-name username

# Update all deployment configurations
# - CI/CD secrets
# - Environment variables
# - Secrets managers
# - Team members' local .env files
```

### 5. Post-Incident Actions (1-2 hours)

```bash
# Enable secret scanning
gh api -X PATCH repos/{owner}/{repo} -f security_and_analysis[secret_scanning][status]=enabled

# Add pre-commit hooks
git secrets --install
git secrets --register-aws

# Audit all secrets
detect-secrets scan --force-use-all-plugins > .secrets.baseline

# Team notification
# Send incident report with:
# - What leaked
# - Actions taken
# - Prevention measures
# - Required team actions
```

## Comprehensive Security Checklist

### Development Setup
- [ ] .env files in .gitignore
- [ ] .env.example committed (without real values)
- [ ] Pre-commit hooks installed (git-secrets or detect-secrets)
- [ ] Secrets loaded from environment variables only
- [ ] No hardcoded credentials in source code

### CI/CD Pipeline
- [ ] Secrets stored in CI/CD platform secrets (GitHub Secrets, GitLab Variables)
- [ ] Secrets injected at runtime, not in configuration files
- [ ] Build logs don't expose secrets (mask sensitive output)
- [ ] Secret scanning in pipeline (TruffleHog/Gitleaks)
- [ ] Failed secret scans block deployment

### Production Deployment
- [ ] Secrets in managed service (AWS Secrets Manager, Vault, etc.)
- [ ] Automatic rotation enabled for supported services
- [ ] Encryption at rest (AES-256-GCM)
- [ ] TLS 1.3 for all communications
- [ ] Least-privilege access (scope API keys, IAM roles)
- [ ] Monitoring and alerting on secret access

### Docker/Containers
- [ ] Docker secrets used instead of environment variables
- [ ] Secrets not baked into images
- [ ] Multi-stage builds to avoid secrets in layers
- [ ] Secrets loaded from files at runtime
- [ ] Image scanning for leaked credentials

### Rotation & Lifecycle
- [ ] Rotation schedule defined for each secret type
- [ ] Automated rotation where possible
- [ ] Zero-downtime rotation procedure tested
- [ ] Secrets rotated after employee departures
- [ ] Expired secrets removed (not just disabled)

### Monitoring & Response
- [ ] Secret scanning runs on every commit
- [ ] GitHub/GitLab secret scanning enabled
- [ ] Audit logs reviewed regularly
- [ ] Incident response plan documented
- [ ] Team trained on leak response procedures

## Common Mistakes and Fixes

| Mistake | Why It's Bad | Fix |
|---------|--------------|-----|
| "git add ." with .env | Captures all files including secrets | Use .gitignore, check with `git status` before commit |
| Private repo = safe | Repos leak through access changes, compromised accounts | Never commit secrets, even to private repos |
| Deleting secret in new commit | Still in git history forever | Use git-filter-repo to rewrite history AND rotate secret |
| Using environment variables in Docker | Persists in metadata, visible in `docker inspect` | Use Docker secrets with /run/secrets files |
| Relying only on code reviews | Reviews don't check full branch history | Automated secret scanning in CI/CD |
| Hard delete keys on rotation | Breaks rollback capability | Zero-downtime rotation with dual-key overlap |
| .gitignore after commit | .gitignore only prevents untracked files | Remove from git: `git rm --cached .env` then rewrite history |
| "I'll test it first" hardcoded keys | Test keys leak just like production keys | Use .env for ALL environments |

## Red Flags - STOP Immediately

If you catch yourself thinking or doing:
- "I'll commit this API key temporarily"
- "The repository is private, so it's fine"
- "I'll remove it before deploying"
- "It's just a test key"
- "Code review will catch it"
- Copying .env.example to .env and filling in real values in git
- Skipping .gitignore setup "for now"
- Using `git add .` without checking `git status` first
- Storing secrets in comments "for documentation"

**ALL of these mean: STOP. You're about to leak a secret.**

## Tools Reference

### Secret Scanners
- **TruffleHog**: https://github.com/trufflesecurity/trufflehog (800+ types, verification)
- **Gitleaks**: https://github.com/gitleaks/gitleaks (fast, lightweight)
- **detect-secrets**: https://github.com/Yelp/detect-secrets (enterprise, low false positives)
- **git-secrets**: https://github.com/awslabs/git-secrets (AWS patterns, pre-commit)

### Secrets Managers
- **AWS Secrets Manager**: https://aws.amazon.com/secrets-manager/
- **Azure Key Vault**: https://azure.microsoft.com/en-us/products/key-vault
- **GCP Secret Manager**: https://cloud.google.com/secret-manager
- **HashiCorp Vault**: https://www.vaultproject.io/

### History Rewriting
- **git-filter-repo**: https://github.com/newren/git-filter-repo (recommended)
- **BFG Repo-Cleaner**: https://rtyley.github.io/bfg-repo-cleaner/

### Encryption Libraries
- **Python cryptography**: https://cryptography.io/
- **Node.js crypto**: https://nodejs.org/api/crypto.html (built-in)
- **Go crypto**: https://pkg.go.dev/crypto (built-in)

## Real-World Impact

**2024 Incidents:**
- **39 million secrets** exposed on GitHub in 2024
- **Dropbox breach**: Compromised API keys accessed production environment
- **RabbitR1**: Hardcoded API keys in source code
- **Uber 2016**: AWS keys in GitHub led to $148M settlement

**Time costs:**
- Secret leak response: 4-8 hours emergency work
- Git history rewrite: 30-60 minutes
- Automated rotation setup: 2-4 hours once, saves 30 min/rotation
- Pre-commit hooks setup: 15 minutes once, prevents 100% of accidental commits

**The bottom line:** 30 minutes setting up proper secrets management saves hours of incident response and potentially catastrophic breaches.
