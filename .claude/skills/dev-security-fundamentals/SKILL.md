---
name: dev-security-fundamentals
description: Use when implementing authentication, handling user input, deploying applications, or reviewing code for security issues - comprehensive guide covering OWASP Top 10, auth/authz patterns, input validation, security headers, and common vulnerabilities with actionable mitigations
---

# Development Security Fundamentals

## Overview

**Security is not a feature you add later - it's a foundation you build from the start.**

Most security breaches result from well-known, preventable vulnerabilities. This skill provides actionable guidance for avoiding them.

**Core principle:** Defense in depth - multiple layers of security, assuming each layer can fail.

**Violating these fundamentals doesn't just risk your application - it risks your users' data, privacy, and trust.**

## When to Use

Use this skill when:
- **Implementing authentication or authorization** - Before writing login, session, or permission code
- **Handling any user input** - Forms, APIs, file uploads, search queries
- **Deploying applications** - Configuring servers, containers, cloud services
- **Code review** - Evaluating security posture of changes
- **Investigating security issues** - Understanding vulnerabilities and proper mitigations
- **API design** - Exposing endpoints that accept or return data
- **Database operations** - Constructing queries, storing sensitive data
- **Third-party integrations** - Adding dependencies or external services

**Don't skip this for:**
- "Simple" internal tools (insiders are threats too)
- Prototypes (prototypes become production)
- "Low-value" targets (all data has value to someone)

## Core Security Principles

### Defense in Depth
**Never rely on a single security control.** Layer multiple independent defenses.

```javascript
// ❌ BAD: Single layer - if validation fails, you're exposed
app.post('/transfer', (req, res) => {
  const amount = req.body.amount;
  transferMoney(req.user.id, amount);
});

// ✅ GOOD: Multiple layers
app.post('/transfer',
  requireAuthentication,        // Layer 1: Must be logged in
  requireCSRFToken,              // Layer 2: Valid CSRF token
  rateLimitByUser(10, '1h'),    // Layer 3: Rate limiting
  (req, res) => {
    // Layer 4: Input validation
    const amount = validatePositiveNumber(req.body.amount, { max: 10000 });

    // Layer 5: Authorization check
    if (!canTransfer(req.user.id, amount)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }

    // Layer 6: Transaction integrity
    transferMoney(req.user.id, amount);
  }
);
```

### Least Privilege
**Grant minimum permissions necessary.** Users, processes, and services should only access what they need.

```python
# ❌ BAD: Database user has full admin rights
DATABASE_URL = "postgresql://admin:password@localhost/myapp"

# ✅ GOOD: Different users for different operations
READ_ONLY_DB = "postgresql://app_reader:pass@localhost/myapp"
WRITE_DB = "postgresql://app_writer:pass@localhost/myapp"
MIGRATION_DB = "postgresql://app_migrator:pass@localhost/myapp"

# Application uses read-only by default
# Only specific operations use write connection
```

### Secure by Default
**The safe path should be the easy path.** Make insecure options require explicit opt-in.

```javascript
// ❌ BAD: Insecure by default
function createSession(userId, options = {}) {
  const secure = options.secure || false;  // Defaults to insecure!
  // ...
}

// ✅ GOOD: Secure by default
function createSession(userId, options = {}) {
  const secure = options.insecure ? false : true;  // Opt-in to insecurity
  const httpOnly = options.allowJavaScriptAccess ? false : true;
  const sameSite = options.sameSite || 'strict';
  // ...
}
```

### Fail Securely
**When something goes wrong, fail closed, not open.**

```python
# ❌ BAD: Error grants access
def check_permission(user_id, resource_id):
    try:
        perms = database.get_permissions(user_id, resource_id)
        return 'write' in perms
    except Exception:
        return True  # ERROR: Failure grants access!

# ✅ GOOD: Error denies access
def check_permission(user_id, resource_id):
    try:
        perms = database.get_permissions(user_id, resource_id)
        return 'write' in perms
    except Exception as e:
        logger.error(f"Permission check failed: {e}")
        return False  # Fail securely - deny access
```

## OWASP Top 10 (2021 - Current as of 2024)

### A01: Broken Access Control
**Risk:** Users accessing resources they shouldn't (other users' data, admin functions).

**Prevention:**
```javascript
// ❌ BAD: Using user-supplied ID without authorization check
app.get('/api/profile/:userId', async (req, res) => {
  const profile = await getProfile(req.params.userId);
  res.json(profile);  // ANYONE can access ANY profile!
});

// ✅ GOOD: Verify authorization
app.get('/api/profile/:userId', requireAuth, async (req, res) => {
  const requestedUserId = req.params.userId;

  // Check if user can access this profile
  if (req.user.id !== requestedUserId && !req.user.isAdmin) {
    return res.status(403).json({ error: 'Access denied' });
  }

  const profile = await getProfile(requestedUserId);
  res.json(profile);
});

// ✅ BETTER: Use session user ID, never trust client
app.get('/api/profile', requireAuth, async (req, res) => {
  // Only allow users to access their own profile
  const profile = await getProfile(req.user.id);
  res.json(profile);
});
```

**Key Rules:**
- Default deny - require explicit grants
- Check authorization on every request (don't cache inappropriately)
- Use indirect object references (map IDs, don't expose internal IDs)
- Log access control failures

### A02: Cryptographic Failures
**Risk:** Exposing sensitive data through weak or missing encryption.

**Prevention:**
```python
# ❌ BAD: Storing passwords in plaintext
user.password = request.form['password']
db.save(user)

# ❌ BAD: Using weak hashing
user.password = md5(request.form['password'])  # MD5 is broken!

# ✅ GOOD: Use bcrypt/argon2 for passwords
import bcrypt

# Hashing password on registration
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
user.password_hash = hashed

# Verifying password on login
if bcrypt.checkpw(password.encode('utf-8'), user.password_hash):
    # Password correct
    pass
```

**Data Classification:**
```python
# Classify your data and protect accordingly
SENSITIVITY_LEVELS = {
    'public': {
        'encryption_at_rest': False,
        'encryption_in_transit': True,  # Always use HTTPS
    },
    'internal': {
        'encryption_at_rest': True,
        'encryption_in_transit': True,
        'access_logging': True,
    },
    'confidential': {
        'encryption_at_rest': True,
        'encryption_in_transit': True,
        'access_logging': True,
        'data_masking': True,
        'requires_mfa': True,
    },
    'restricted': {
        'encryption_at_rest': True,
        'encryption_in_transit': True,
        'access_logging': True,
        'data_masking': True,
        'requires_mfa': True,
        'audit_trail': True,
        'data_retention_days': 90,
    }
}
```

### A03: Injection
**Risk:** Attackers executing malicious code via unsanitized input (SQL, OS commands, LDAP).

**Prevention:**
```javascript
// ❌ BAD: String concatenation creates SQL injection
const userId = req.query.id;
const query = `SELECT * FROM users WHERE id = ${userId}`;
// Attacker sends: ?id=1 OR 1=1 (returns all users!)

// ✅ GOOD: Parameterized queries (prepared statements)
const userId = req.query.id;
const query = 'SELECT * FROM users WHERE id = ?';
const user = await db.query(query, [userId]);
// Input is treated as data, never executed as code
```

```python
# ❌ BAD: Command injection vulnerability
import os
filename = request.form['filename']
os.system(f'cat {filename}')  # Attacker sends: "file.txt; rm -rf /"

# ✅ GOOD: Use safe APIs, validate input
import subprocess
from pathlib import Path

filename = request.form['filename']

# Validate: only alphanumeric and specific characters
if not re.match(r'^[\w\-. ]+$', filename):
    raise ValueError('Invalid filename')

# Use safe subprocess with list arguments (no shell)
result = subprocess.run(
    ['cat', filename],
    capture_output=True,
    shell=False,  # Critical: don't use shell
    timeout=5
)
```

**NoSQL Injection:**
```javascript
// ❌ BAD: MongoDB injection
const username = req.body.username;  // Attacker sends: {$gt: ""}
db.users.find({ username: username });  // Returns all users!

// ✅ GOOD: Validate types and use proper query builders
const username = String(req.body.username);  // Force to string
if (typeof username !== 'string') {
    throw new Error('Invalid username type');
}
db.users.find({ username: username });
```

### A04: Insecure Design
**Risk:** Architectural flaws that can't be fixed with patches.

**Prevention Patterns:**
- **Threat modeling** - Identify attack vectors in design phase
- **Secure design patterns** - Use proven architectural patterns
- **Limit blast radius** - Compartmentalize systems

```javascript
// ❌ BAD: No rate limiting on password reset
app.post('/reset-password', async (req, res) => {
  await sendResetEmail(req.body.email);
  res.json({ success: true });
});
// Attacker can enumerate users, DoS email system

// ✅ GOOD: Rate limiting + consistent timing
const rateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 3,  // 3 attempts per window
  skipSuccessfulRequests: false,
});

app.post('/reset-password', rateLimiter, async (req, res) => {
  const email = req.body.email;
  const userExists = await checkUserExists(email);

  if (userExists) {
    await sendResetEmail(email);
  }

  // ALWAYS return same response (timing and message)
  // Don't leak whether email exists
  await sleep(randomBetween(100, 300));  // Prevent timing attacks
  res.json({ message: 'If that email exists, reset link sent' });
});
```

### A05: Security Misconfiguration
**Risk:** Default configs, unnecessary features, verbose errors exposing internals.

**Prevention:**
```javascript
// ❌ BAD: Detailed errors in production
app.use((err, req, res, next) => {
  res.status(500).json({
    error: err.message,
    stack: err.stack,  // NEVER expose stack traces in production!
    query: req.query,  // May contain sensitive data
  });
});

// ✅ GOOD: Generic errors in production, detailed in logs
app.use((err, req, res, next) => {
  // Log full details server-side
  logger.error('Request failed', {
    error: err.message,
    stack: err.stack,
    user: req.user?.id,
    path: req.path,
    method: req.method,
  });

  // Generic message to client
  const message = process.env.NODE_ENV === 'production'
    ? 'Internal server error'
    : err.message;

  res.status(500).json({ error: message });
});
```

**Security Headers Configuration:**
```javascript
const helmet = require('helmet');

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'"],  // Prefer nonces over unsafe-inline
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'"],
      fontSrc: ["'self'"],
      objectSrc: ["'none'"],
      mediaSrc: ["'self'"],
      frameSrc: ["'none'"],
    },
  },
  hsts: {
    maxAge: 31536000,  // 1 year
    includeSubDomains: true,
    preload: true,
  },
}));
```

### A06: Vulnerable and Outdated Components
**Risk:** Using libraries with known vulnerabilities.

**Prevention:**
```bash
# Regular dependency audits
npm audit
npm audit fix

# Or use automated tools
npm install -g npm-check-updates
ncu -u

# Pin versions, but keep updated
# package.json - use exact versions for critical deps
{
  "dependencies": {
    "express": "4.18.2",  // Exact version, not ^4.18.2
    "bcrypt": "5.1.0"
  }
}

# Use Dependabot, Renovate, or Snyk for automated updates
```

**Component Selection Criteria:**
- Is it actively maintained? (Check last commit date)
- Does it have known vulnerabilities? (Check npm audit, Snyk)
- How many dependencies does it have? (Prefer minimal)
- What's its security track record?

### A07: Identification and Authentication Failures
**Risk:** Broken login, session management, credential storage.

**Prevention:**
```javascript
// ✅ GOOD: Secure session configuration
const session = require('express-session');

app.use(session({
  secret: process.env.SESSION_SECRET,  // Strong random secret
  name: 'sessionId',  // Don't use default name
  cookie: {
    secure: true,        // HTTPS only
    httpOnly: true,      // No JavaScript access
    sameSite: 'strict',  // CSRF protection
    maxAge: 3600000,     // 1 hour
  },
  resave: false,
  saveUninitialized: false,
  rolling: true,  // Reset expiration on activity
}));
```

**Multi-Factor Authentication:**
```python
# Implement MFA for sensitive operations
from pyotp import TOTP

def verify_login(username, password, mfa_token):
    user = authenticate(username, password)
    if not user:
        return False

    # Verify MFA token
    totp = TOTP(user.mfa_secret)
    if not totp.verify(mfa_token, valid_window=1):
        logger.warning(f'Invalid MFA for user {user.id}')
        return False

    return user
```

### A08: Software and Data Integrity Failures
**Risk:** Insecure CI/CD, unsigned updates, untrusted deserialization.

**Prevention:**
```javascript
// ❌ BAD: Deserializing untrusted data
const userData = JSON.parse(req.body.data);
eval(userData.code);  // NEVER EVER use eval() on user input!

// ✅ GOOD: Validate structure and use safe parsers
const Ajv = require('ajv');
const ajv = new Ajv();

const schema = {
  type: 'object',
  properties: {
    name: { type: 'string', maxLength: 100 },
    age: { type: 'integer', minimum: 0, maximum: 150 },
  },
  required: ['name', 'age'],
  additionalProperties: false,  // Reject unknown fields
};

const validate = ajv.compile(schema);
const data = JSON.parse(req.body.data);

if (!validate(data)) {
  return res.status(400).json({ errors: validate.errors });
}
```

**Verify Integrity:**
```bash
# Use SRI (Subresource Integrity) for CDN resources
<script
  src="https://cdn.example.com/library.js"
  integrity="sha384-oqVuAfXRKap7fdgcCY5uykM6+R9GqQ8K/ux..."
  crossorigin="anonymous">
</script>

# Verify package checksums
npm ci --ignore-scripts  # Don't run install scripts
```

### A09: Security Logging and Monitoring Failures
**Risk:** Can't detect or respond to breaches.

**What to Log:**
```javascript
// Security event logging
const securityLog = require('winston');

// Log authentication events
function loginAttempt(username, success, ipAddress) {
  securityLog.info('Login attempt', {
    event: 'auth.login',
    username: username,  // Log username, NOT password
    success: success,
    ip: ipAddress,
    timestamp: new Date().toISOString(),
  });

  if (!success) {
    // Additional monitoring for failed logins
    failedLoginCounter.inc({ username });
  }
}

// Log access control failures
function accessDenied(userId, resource, action) {
  securityLog.warn('Access denied', {
    event: 'authz.denied',
    userId: userId,
    resource: resource,
    action: action,
    timestamp: new Date().toISOString(),
  });
}

// Log high-value transactions
function transferMoney(fromUser, toUser, amount) {
  securityLog.info('Money transfer', {
    event: 'transaction.transfer',
    from: fromUser,
    to: toUser,
    amount: amount,
    timestamp: new Date().toISOString(),
  });
}
```

**What NOT to Log:**
- Passwords or password hashes
- Session tokens or API keys
- Credit card numbers or CVV
- Personal identifiable information (PII) without justification
- Full request bodies (may contain sensitive data)

### A10: Server-Side Request Forgery (SSRF)
**Risk:** Attacker tricks server into making requests to internal resources.

**Prevention:**
```python
# ❌ BAD: Fetching arbitrary URLs
url = request.form['url']
response = requests.get(url)  # Attacker sends: http://localhost:9200

# ✅ GOOD: Validate and restrict URLs
from urllib.parse import urlparse
import ipaddress

ALLOWED_DOMAINS = ['api.example.com', 'cdn.example.com']

def is_safe_url(url):
    parsed = urlparse(url)

    # Must be HTTPS
    if parsed.scheme != 'https':
        return False

    # Must be in allowed domains
    if parsed.hostname not in ALLOWED_DOMAINS:
        return False

    # Resolve hostname and check it's not internal
    try:
        ip = ipaddress.ip_address(socket.gethostbyname(parsed.hostname))
        # Reject private/internal IPs
        if ip.is_private or ip.is_loopback:
            return False
    except:
        return False

    return True

url = request.form['url']
if is_safe_url(url):
    response = requests.get(url, timeout=5)
else:
    raise ValueError('Invalid URL')
```

## Authentication & Authorization Patterns

### OAuth2 Best Practices
```javascript
// OAuth2 Authorization Code Flow (most secure for web apps)
app.get('/auth/callback', async (req, res) => {
  const { code, state } = req.query;

  // Verify state parameter (CSRF protection)
  if (state !== req.session.oauth_state) {
    return res.status(403).send('Invalid state parameter');
  }

  // Exchange code for token
  const tokenResponse = await fetch('https://oauth.provider.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      grant_type: 'authorization_code',
      code: code,
      redirect_uri: process.env.OAUTH_REDIRECT_URI,
      client_id: process.env.OAUTH_CLIENT_ID,
      client_secret: process.env.OAUTH_CLIENT_SECRET,
    }),
  });

  const { access_token, refresh_token } = await tokenResponse.json();

  // Store tokens securely (encrypted, httpOnly cookie or server-side session)
  req.session.access_token = access_token;
  req.session.refresh_token = refresh_token;

  res.redirect('/dashboard');
});
```

### JWT Security
```python
import jwt
from datetime import datetime, timedelta

# ✅ GOOD: Secure JWT configuration
def create_jwt(user_id, roles):
    # Use strong algorithm
    payload = {
        'sub': user_id,  # Subject (user ID)
        'iat': datetime.utcnow(),  # Issued at
        'exp': datetime.utcnow() + timedelta(minutes=15),  # Short expiry
        'roles': roles,
    }

    token = jwt.encode(
        payload,
        key=os.environ['JWT_SECRET'],  # Strong secret, never in code
        algorithm='HS256'  # Or RS256 for asymmetric
    )

    return token

def verify_jwt(token):
    try:
        payload = jwt.decode(
            token,
            key=os.environ['JWT_SECRET'],
            algorithms=['HS256'],  # Explicitly specify allowed algorithms
            options={
                'verify_exp': True,  # Verify expiration
                'require': ['sub', 'exp', 'iat'],  # Required claims
            }
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthError('Token expired')
    except jwt.InvalidTokenError:
        raise AuthError('Invalid token')
```

**JWT Storage:**
- ❌ DON'T store in localStorage (vulnerable to XSS)
- ❌ DON'T store in sessionStorage (vulnerable to XSS)
- ✅ DO store in httpOnly cookies (immune to XSS)
- ✅ DO use short expiration times (15-30 minutes)
- ✅ DO implement refresh token rotation

## Input Validation & Sanitization

### Whitelisting Over Blacklisting
```javascript
// ❌ BAD: Blacklist approach (always incomplete)
function sanitizeUsername(username) {
  return username
    .replace(/script/gi, '')
    .replace(/alert/gi, '')
    .replace(/onerror/gi, '');
  // Attacker uses: "scr<script>ipt" or variations
}

// ✅ GOOD: Whitelist approach
function sanitizeUsername(username) {
  // Only allow alphanumeric, dash, underscore
  if (!/^[a-zA-Z0-9_-]{3,20}$/.test(username)) {
    throw new Error('Invalid username format');
  }
  return username;
}
```

### Context-Specific Encoding
```javascript
const escapeHTML = (str) => str
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;')
  .replace(/'/g, '&#x27;');

const escapeSQL = (str) => str.replace(/'/g, "''");  // Better: use parameterized queries

const escapeURL = (str) => encodeURIComponent(str);

const escapeJS = (str) => JSON.stringify(str).slice(1, -1);
```

## Security Checklist for Developers

### Before Every Commit
- [ ] No secrets in code (API keys, passwords, tokens)
- [ ] All user input validated
- [ ] Parameterized queries used (no string concatenation)
- [ ] Authorization checks on all protected routes
- [ ] Error messages don't leak sensitive information
- [ ] HTTPS enforced
- [ ] Security headers configured

### Before Every Deployment
- [ ] Dependencies audited (`npm audit`, `pip check`)
- [ ] Security tests passing
- [ ] Logging configured for security events
- [ ] Rate limiting enabled on APIs
- [ ] CSRF protection enabled
- [ ] Session configuration secure
- [ ] Database credentials rotated
- [ ] TLS certificates valid

### Monthly Reviews
- [ ] Review access control lists
- [ ] Audit user permissions
- [ ] Review security logs for anomalies
- [ ] Update dependencies
- [ ] Review and rotate secrets/API keys

## Common Pitfalls

### "Security Through Obscurity"
```javascript
// ❌ BAD: Hiding API endpoint names
app.post('/a8f3k2j9x', handleAdminAction);  // Attacker will find it

// ✅ GOOD: Proper authorization
app.post('/admin/action', requireAuth, requireRole('admin'), handleAdminAction);
```

### Client-Side Security Checks
```javascript
// ❌ BAD: Only validating on client
<button onclick="if(user.isAdmin) deleteUser()">Delete</button>

// ✅ GOOD: Validate on server
app.delete('/users/:id', requireAuth, requireAdmin, deleteUser);
```

### Trusting User Input
```javascript
// ❌ BAD: Using user input directly
const limit = req.query.limit;  // Attacker sends: 999999999
const users = await db.users.find().limit(limit);  // DoS!

// ✅ GOOD: Validate and cap
const limit = Math.min(parseInt(req.query.limit) || 10, 100);
const users = await db.users.find().limit(limit);
```

## Tools & Resources

### Static Analysis
- **ESLint with security plugins**: `eslint-plugin-security`
- **Bandit** (Python): Detects common security issues
- **SonarQube**: Multi-language security scanning
- **Semgrep**: Pattern-based code analysis

### Dependency Scanning
- **npm audit** / **yarn audit**: Node.js
- **pip-audit**: Python
- **Snyk**: Multi-language, automated PR updates
- **Dependabot**: GitHub native dependency updates

### Dynamic Testing
- **OWASP ZAP**: Web application security scanner
- **Burp Suite**: HTTP proxy for testing
- **sqlmap**: SQL injection testing
- **testssl.sh**: TLS/SSL configuration testing

### Learning Resources
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **OWASP Cheat Sheet Series**: https://cheatsheetseries.owasp.org/
- **PortSwigger Web Security Academy**: Free hands-on labs
- **NIST Cybersecurity Framework**: https://www.nist.gov/cyberframework
- **CWE Top 25**: Most dangerous software weaknesses

## Integration with Other Skills

**Use alongside:**
- **dev-systematic-debugging** - When investigating security vulnerabilities
- **dev-test-driven-development** - Write security tests first
- **api-design** - Secure API design patterns
- **code-organization** - Separate security concerns

**This skill complements:**
- Database design (encryption, access patterns)
- Deployment (secure configurations)
- Error handling (fail securely)

## Real-World Impact

**Security done right:**
- Prevents 95%+ of common attacks
- Builds user trust
- Avoids breach costs ($4.45M average in 2023)
- Enables compliance (GDPR, HIPAA, SOC 2)

**Security done wrong:**
- Data breaches
- Regulatory fines
- Reputation damage
- Loss of user trust

**The cost of security is always less than the cost of a breach.**
