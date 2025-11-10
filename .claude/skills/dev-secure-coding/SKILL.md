---
name: dev-secure-coding
description: Use when implementing security-sensitive features, handling user input, database queries, file operations, or authentication - comprehensive guide covering XSS, SQL injection, CSRF, command injection, path traversal, insecure deserialization, and race conditions with prevention strategies and code examples
---

# Secure Coding Practices

## Overview

**Core Principle:** Security vulnerabilities aren't just theoretical - they're actively exploited daily. Writing secure code isn't optional; it's fundamental.

Based on the **2024 CWE Top 25 Most Dangerous Software Weaknesses** and **OWASP Secure Coding Practices**, this skill provides actionable guidance for preventing the most critical vulnerabilities.

**Violations covered:** XSS (#1), SQL Injection (#3), CSRF (#4), Path Traversal (#5), Command Injection (#11)

## When to Use

**ALWAYS use when:**
- Accepting user input (forms, APIs, uploads)
- Building database queries
- Executing system commands
- Handling file paths or uploads
- Implementing authentication/authorization
- Deserializing data (JSON, YAML, XML, pickle)
- Managing session state or cookies
- Writing code that will process untrusted data

**During code review:**
- Any data crosses trust boundaries
- String concatenation with user input
- File system operations
- Database interactions
- Shell/subprocess execution

## 1. Cross-Site Scripting (XSS)

### What It Is

XSS allows attackers to inject malicious JavaScript into web pages viewed by other users. Ranked **#1** in 2024 CWE Top 25.

**Types:**
- **Reflected XSS**: Immediate reflection of user input (search results, error messages)
- **Stored XSS**: Persistent injection (comments, profile data)
- **DOM-based XSS**: Client-side JavaScript manipulation

### Vulnerable Code (BAD)

```javascript
// JavaScript - Directly inserting user input
const username = request.query.name;
document.getElementById('welcome').innerHTML = `Hello ${username}!`;

// Python Flask - No escaping
@app.route('/search')
def search():
    query = request.args.get('q', '')
    return f'<h1>Results for: {query}</h1>'

// React - Dangerous HTML injection
function UserComment({ comment }) {
  return <div dangerouslySetInnerHTML={{ __html: comment }} />;
}
```

### Secure Code (GOOD)

```javascript
// JavaScript - Use textContent instead of innerHTML
const username = request.query.name;
document.getElementById('welcome').textContent = `Hello ${username}!`;

// Python Flask - Auto-escaping with templates
@app.route('/search')
def search():
    query = request.args.get('q', '')
    return render_template('search.html', query=query)
# In template: <h1>Results for: {{ query }}</h1>

// React - Automatic escaping by default
function UserComment({ comment }) {
  return <div>{comment}</div>;
}
```

### Prevention Strategies

1. **Use Framework Security Features**: Modern frameworks (React, Angular, Flask, Django) escape output by default
2. **Output Encoding**: Encode data based on context (HTML, JavaScript, URL, CSS)
3. **Content Security Policy (CSP)**: Strict CSP with nonces/hashes prevents inline script execution
4. **Input Validation**: Whitelist expected input patterns, reject everything else
5. **Avoid Dangerous APIs**: Never use `innerHTML`, `eval()`, `dangerouslySetInnerHTML` with user data

**CSP Header Example:**
```http
Content-Security-Policy: default-src 'self'; script-src 'nonce-{random}'; object-src 'none'
```

## 2. SQL Injection

### What It Is

SQL Injection allows attackers to manipulate database queries through user input. Ranked **#3** in 2024 CWE Top 25.

### Vulnerable Code (BAD)

```python
# Python - String concatenation
username = request.form['username']
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)
# Attack: username = "admin' OR '1'='1"

# JavaScript/Node - Template string injection
const userId = req.params.id;
const query = `SELECT * FROM orders WHERE user_id = ${userId}`;
db.query(query);

# Java - Concatenated SQL
String email = request.getParameter("email");
String query = "SELECT * FROM users WHERE email = '" + email + "'";
Statement stmt = connection.createStatement();
ResultSet rs = stmt.executeQuery(query);
```

### Secure Code (GOOD)

```python
# Python - Parameterized query
username = request.form['username']
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))

# JavaScript/Node - Parameterized with pg
const userId = req.params.id;
const query = 'SELECT * FROM orders WHERE user_id = $1';
await db.query(query, [userId]);

# Java - PreparedStatement
String email = request.getParameter("email");
String query = "SELECT * FROM users WHERE email = ?";
PreparedStatement pstmt = connection.prepareStatement(query);
pstmt.setString(1, email);
ResultSet rs = pstmt.executeQuery();
```

### Prevention Strategies

1. **Always Use Parameterized Queries**: Prepared statements separate SQL code from data
2. **Use ORM Frameworks**: SQLAlchemy, Hibernate, Sequelize handle parameterization automatically
3. **Never Build SQL with String Concatenation**: Even with validation, don't concatenate
4. **Least Privilege**: Database accounts should have minimal necessary permissions
5. **Input Validation**: Whitelist expected formats (numbers, emails, etc.)

**Why Parameterization Works:** The database receives query structure and data separately, preventing data from being interpreted as SQL commands.

## 3. Cross-Site Request Forgery (CSRF)

### What It Is

CSRF tricks authenticated users into performing unwanted actions. Attacker crafts malicious requests that leverage victim's active session. Ranked **#4** in 2024 CWE Top 25.

### Vulnerable Code (BAD)

```python
# Flask - No CSRF protection
@app.route('/transfer', methods=['POST'])
def transfer_money():
    amount = request.form['amount']
    to_account = request.form['to']
    # Execute transfer using session cookie for auth
    process_transfer(session['user_id'], to_account, amount)
    return 'Transfer complete'

# Express - Missing CSRF middleware
app.post('/delete-account', (req, res) => {
    const userId = req.session.userId;
    deleteUser(userId);
    res.send('Account deleted');
});
```

### Secure Code (GOOD)

```python
# Flask - CSRF protection with Flask-WTF
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

@app.route('/transfer', methods=['POST'])
def transfer_money():
    # Token automatically validated by CSRFProtect
    amount = request.form['amount']
    to_account = request.form['to']
    process_transfer(session['user_id'], to_account, amount)
    return 'Transfer complete'

# Express - csurf middleware
const csrf = require('csurf');
const csrfProtection = csrf({ cookie: true });

app.post('/delete-account', csrfProtection, (req, res) => {
    const userId = req.session.userId;
    deleteUser(userId);
    res.send('Account deleted');
});
```

### Prevention Strategies

1. **CSRF Tokens**: Include unpredictable token in forms, validate on server
2. **SameSite Cookies**: Set `SameSite=Strict` or `SameSite=Lax` on session cookies
3. **Double-Submit Cookies**: Send token in both cookie and request parameter
4. **Verify Origin/Referer Headers**: Check requests originate from your domain
5. **Require Re-authentication**: For sensitive actions, ask for password confirmation

**SameSite Cookie Example:**
```python
response.set_cookie('session', value, samesite='Strict', secure=True, httponly=True)
```

**Important:** SameSite cookies provide dev-defense-in-depth but don't replace CSRF tokens.

## 4. Command Injection

### What It Is

Command injection allows attackers to execute arbitrary shell commands through user input. Escalated to **#11** in 2024 (jumped 12 positions).

### Vulnerable Code (BAD)

```python
# Python - shell=True with user input
import subprocess
filename = request.form['filename']
subprocess.run(f'ls -l {filename}', shell=True)
# Attack: filename = "; rm -rf /"

# Node.js - exec with user input
const { exec } = require('child_process');
const branch = req.query.branch;
exec(`git checkout ${branch}`, (error, stdout) => {
    res.send(stdout);
});

# PHP - system() with user input
$file = $_GET['file'];
system("cat " . $file);
```

### Secure Code (GOOD)

```python
# Python - Use list arguments, shell=False
import subprocess
filename = request.form['filename']
subprocess.run(['ls', '-l', filename], shell=False)

# Python - Better: Use Path API, avoid shell entirely
from pathlib import Path
filename = request.form['filename']
file_path = Path('/safe/directory') / filename
if file_path.exists():
    print(file_path.stat())

# Node.js - execFile with argument array
const { execFile } = require('child_process');
const branch = req.query.branch;
execFile('git', ['checkout', branch], (error, stdout) => {
    res.send(stdout);
});
```

### Prevention Strategies

1. **Avoid Shell Invocation**: Use language APIs instead of shell commands
2. **Never Use `shell=True`**: In Python subprocess, `shell=False` is critical
3. **Use Argument Lists**: Pass commands as arrays, not concatenated strings
4. **Input Validation**: Whitelist allowed characters (alphanumeric, dash, underscore)
5. **Escape When Necessary**: Use `shlex.quote()` (Python) if shell is unavoidable

## 5. Path Traversal

### What It Is

Path traversal exploits allow attackers to access files outside intended directories using `../` sequences. Ranked **#5** in 2024 CWE Top 25. Increased 85% in closed-source projects (2023-2024).

### Vulnerable Code (BAD)

```python
# Python - Direct file access with user input
import os
filename = request.args.get('file')
with open(f'/app/uploads/{filename}', 'r') as f:
    return f.read()
# Attack: file = "../../../etc/passwd"

# Node.js - Path concatenation
const express = require('express');
app.get('/download', (req, res) => {
    const file = req.query.filename;
    res.sendFile('/var/www/files/' + file);
});

# Java - File access without validation
String fileName = request.getParameter("file");
File file = new File("/app/data/" + fileName);
FileInputStream fis = new FileInputStream(file);
```

### Secure Code (GOOD)

```python
# Python - Path validation with pathlib
from pathlib import Path

BASE_DIR = Path('/app/uploads')
filename = request.args.get('file')

# Resolve to absolute path and verify it's within BASE_DIR
file_path = (BASE_DIR / filename).resolve()
if not file_path.is_relative_to(BASE_DIR):
    abort(403, "Access denied")

with open(file_path, 'r') as f:
    return f.read()

# Node.js - Path resolution and validation
const path = require('path');
const baseDir = '/var/www/files';

app.get('/download', (req, res) => {
    const filename = req.query.filename;
    const filePath = path.resolve(baseDir, filename);

    if (!filePath.startsWith(baseDir)) {
        return res.status(403).send('Access denied');
    }
    res.sendFile(filePath);
});
```

### Prevention Strategies

1. **Never Use User Input Directly in Paths**: Map file IDs to paths server-side
2. **Validate Against Base Directory**: Resolve path, verify it starts with expected base
3. **Whitelist Validation**: Only allow alphanumeric filenames, reject `../`, `./`, `\`
4. **Use Path Canonicalization**: `Path.resolve()` removes symlinks and traversal sequences
5. **Restrict File System Access**: Run application with minimal file permissions

## 6. Insecure Deserialization

### What It Is

Deserializing untrusted data can lead to remote code execution, particularly with formats like Python pickle, YAML, or Java serialization.

### Vulnerable Code (BAD)

```python
# Python - Pickle from untrusted source
import pickle
user_data = request.get_data()
obj = pickle.loads(user_data)  # RCE possible!

# Python - Unsafe YAML loading
import yaml
config = request.form['config']
data = yaml.load(config)  # Executes Python code!

# Java - Unsafe deserialization
ObjectInputStream ois = new ObjectInputStream(request.getInputStream());
Object obj = ois.readObject();  // RCE possible
```

### Secure Code (GOOD)

```python
# Python - Use JSON instead of pickle
import json
user_data = request.get_json()
obj = json.loads(user_data)  # Safe - no code execution

# Python - Safe YAML loading
import yaml
config = request.form['config']
data = yaml.safe_load(config)  # Restricted to basic types

# Java - Validate before deserialization
ObjectInputStream ois = new ValidatingObjectInputStream(
    request.getInputStream(),
    Arrays.asList("com.example.SafeClass")
);
Object obj = ois.readObject();
```

### Prevention Strategies

1. **Avoid Deserializing Untrusted Data**: Never deserialize user-provided data if possible
2. **Use Safe Formats**: Prefer JSON over pickle/YAML/Java serialization
3. **Use Safe Methods**: `yaml.safe_load()` instead of `yaml.load()`
4. **Validate Integrity**: Use digital signatures/HMAC to verify data hasn't been tampered
5. **Restrict Types**: Whitelist allowed classes for deserialization

## 7. Race Conditions (TOCTOU)

### What It Is

Time-of-Check to Time-of-Use (TOCTOU) vulnerabilities occur when state changes between checking a condition and using the resource. Critical in multi-threaded/multi-process applications.

### Vulnerable Code (BAD)

```python
# Python - Check then use (TOCTOU)
import os
filename = '/tmp/user_upload.txt'

if os.path.exists(filename):
    # Attacker can replace file here via symlink!
    with open(filename, 'r') as f:
        content = f.read()

# Node.js - Non-atomic file operations
const fs = require('fs');
if (fs.existsSync(lockfile)) {
    // Gap: another process could delete lock
    fs.unlinkSync(lockfile);
}

# Java - Check-then-act
File file = new File("/tmp/data.txt");
if (!file.exists()) {
    // File could be created here by attacker
    file.createNewFile();
}
```

### Secure Code (GOOD)

```python
# Python - Atomic operation, handle exception
import os
filename = '/tmp/user_upload.txt'

try:
    # Atomic: open only if exists, fail otherwise
    fd = os.open(filename, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'r') as f:
        content = f.read()
except FileNotFoundError:
    handle_missing_file()

# Node.js - Atomic file operations
const fs = require('fs').promises;
try {
    await fs.unlink(lockfile);  // Atomic operation
} catch (err) {
    if (err.code !== 'ENOENT') throw err;
}

# Java - Atomic file creation
File file = new File("/tmp/data.txt");
try {
    file.createNewFile();  // Returns false if exists, atomic
} catch (IOException e) {
    handle_error(e);
}
```

### Prevention Strategies

1. **Use Atomic Operations**: Single indivisible operations eliminate TOCTOU gap
2. **Open with Flags**: Use `O_CREAT | O_EXCL` to atomically create-if-not-exists
3. **File Locking**: Use proper file locks (`fcntl.flock()`) for concurrent access
4. **Avoid Check-Then-Use**: Operate directly, handle exceptions instead of pre-checking
5. **Use File Descriptors**: Keep descriptor open between check and use

## Language-Specific Security Notes

### Python
- **Always**: `shell=False` in subprocess
- **Use**: `secrets` module for tokens, not `random`
- **Avoid**: `pickle`, `eval()`, `exec()` with untrusted data
- **Database**: Use SQLAlchemy ORM or parameterized queries

### JavaScript/Node.js
- **Always**: `helmet` middleware for security headers
- **Use**: `validator` library for input sanitization
- **Avoid**: `eval()`, `Function()`, `innerHTML` with user data
- **Database**: Use query builders (Knex) or ORMs (Sequelize)

### Java
- **Always**: PreparedStatement for SQL, never Statement
- **Use**: OWASP Java Encoder for output encoding
- **Avoid**: Runtime.exec() with user input
- **Frameworks**: Spring Security provides comprehensive protection

### PHP
- **Always**: PDO with prepared statements, never mysqli concat
- **Use**: `filter_input()` for validation
- **Avoid**: `eval()`, `system()`, `exec()` with user data
- **Enable**: `display_errors=Off` in production

## Code Review Security Checklist

**Input Handling:**
- [ ] All user input validated against whitelist
- [ ] Input validation on server-side (never trust client)
- [ ] Length limits enforced on all string inputs
- [ ] File uploads restricted by type, size, and scanned

**Output Encoding:**
- [ ] Context-aware output encoding (HTML, JS, URL, CSS)
- [ ] Framework auto-escaping enabled
- [ ] CSP headers configured with nonces
- [ ] No `innerHTML`, `dangerouslySetInnerHTML` with user data

**Database Security:**
- [ ] Parameterized queries or ORM used exclusively
- [ ] No string concatenation in SQL
- [ ] Database errors don't expose schema details
- [ ] Least privilege principle for database accounts

**Authentication & Sessions:**
- [ ] Passwords hashed with bcrypt/scrypt/Argon2
- [ ] CSRF tokens on state-changing requests
- [ ] Session cookies: `HttpOnly`, `Secure`, `SameSite=Strict`
- [ ] Account lockout after failed login attempts

**File & System Operations:**
- [ ] No user input in file paths without validation
- [ ] File paths canonicalized and validated
- [ ] No `shell=True` or command concatenation
- [ ] Subprocess uses argument lists, not strings

**Secrets Management:**
- [ ] No hardcoded credentials in code
- [ ] Environment variables or secret managers used
- [ ] API keys rotated regularly
- [ ] `.env` files in `.gitignore`

## Testing for Vulnerabilities

### Manual Testing Techniques

**XSS Testing:**
```
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
javascript:alert('XSS')
```

**SQL Injection Testing:**
```
' OR '1'='1
admin'--
1' UNION SELECT NULL--
```

**Path Traversal Testing:**
```
../../../etc/passwd
..\..\..\..\windows\win.ini
....//....//etc/passwd
```

**Command Injection Testing:**
```
; ls -la
| cat /etc/passwd
`whoami`
$(whoami)
```

### Automated Security Tools

**Static Analysis (SAST):**
- **Semgrep**: Pattern-based security scanning (free, fast)
- **Bandit**: Python security linter
- **ESLint security plugins**: JavaScript/Node.js
- **SonarQube**: Multi-language code quality and security

**Dynamic Analysis (DAST):**
- **OWASP ZAP**: Web application security scanner
- **Burp Suite**: Comprehensive web security testing
- **sqlmap**: Automated SQL injection detection

**Dependency Scanning (SCA):**
- **Snyk**: Vulnerability scanning for dependencies
- **npm audit**: Node.js dependency vulnerabilities
- **pip-audit**: Python dependency vulnerabilities
- **OWASP Dependency-Check**: Multi-language SCA

**Secrets Scanning:**
- **TruffleHog**: Find secrets in git history
- **git-secrets**: Prevent committing secrets
- **detect-secrets**: Baseline secrets management

## Integration with Development Workflow

1. **Pre-commit Hooks**: Run `bandit`, `eslint-plugin-security`, or `semgrep`
2. **CI/CD Pipeline**: SAST in build, DAST in staging, SCA on dependencies
3. **Security Training**: Regular OWASP Top 10 workshops for developers
4. **Threat Modeling**: Identify security requirements during design
5. **Penetration Testing**: Annual third-party security audits

## References

**Official Resources:**
- OWASP Secure Coding Practices: https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/
- CWE Top 25 (2024): https://cwe.mitre.org/top25/archive/2024/2024_cwe_top25.html
- OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/

**CWE References:**
- CWE-79: Cross-Site Scripting
- CWE-89: SQL Injection
- CWE-352: CSRF
- CWE-78: OS Command Injection
- CWE-22: Path Traversal
- CWE-502: Deserialization of Untrusted Data
- CWE-367: TOCTOU Race Condition

## The Bottom Line

**Security is not optional.** Every vulnerability in this skill is actively exploited. The 2024 CWE Top 25 isn't theoretical - it represents real attacks causing real damage.

**Defense in depth:** Use multiple layers (input validation + parameterized queries + CSP + CSRF tokens). If one layer fails, others protect you.

**Fail secure:** When in doubt about security, reject the request. Better to inconvenience a user than expose the system.

**Learn from others' mistakes:** The CWE Top 25 shows where developers fail most often. Don't become another statistic.
