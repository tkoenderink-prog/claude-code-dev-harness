# Deployment Instructions for Claude Code Development Harness

This directory contains the complete Claude Code Development Harness v2.1.0 ready for deployment to GitHub.

## Quick Deploy (Automated)

The easiest way to deploy is using the automated script:

```bash
cd harness-dist
bash DEPLOY.sh
```

The script will:
1. Clone your `claude-code-dev-harness` repository
2. Copy all harness files
3. Verify file structure
4. Set correct permissions
5. Create commit and v2.1.0 tag
6. Push to GitHub (after confirmation)

## Manual Deploy

If you prefer manual deployment:

### Step 1: Clone the Target Repository

```bash
git clone https://github.com/tkoenderink-prog/claude-code-dev-harness.git /tmp/harness-deploy
cd /tmp/harness-deploy
```

### Step 2: Copy Harness Files

From this directory:

```bash
# Copy all files except .git and deployment scripts
rsync -av --exclude='.git' --exclude='DEPLOY.sh' --exclude='DEPLOYMENT-INSTRUCTIONS.md' \
  /path/to/Claude-code-app/harness-dist/ /tmp/harness-deploy/
```

Or manually copy:
- `.claude/` directory (entire structure)
- `VERSION`
- `README.md`
- `CHANGELOG.md`
- `LICENSE`
- `CLAUDE.md`
- `.gitignore`

### Step 3: Verify Structure

Ensure these critical files exist:
- `VERSION` (should contain "2.1.0")
- `README.md` (>100 lines)
- `CHANGELOG.md` (v2.1.0 entry)
- `CLAUDE.md` (with HARNESS-CORE markers)
- `.claude/agents/` (5 files)
- `.claude/skills/` (100+ files)
- `.claude/commands/` (4 files)
- `.claude/hooks/` (3 files)

### Step 4: Set Permissions

```bash
chmod +x .claude/hooks/*
```

### Step 5: Commit and Tag

```bash
cd /tmp/harness-deploy
git add .
git commit -m "Initial release: Claude Code Development Harness v2.1.0"
git tag -a v2.1.0 -m "Version 2.1.0 - Cross-Project Harness with Version Management"
```

### Step 6: Push to GitHub

```bash
git push -u origin main
git push origin v2.1.0
```

## Verification

After deployment, verify at:
https://github.com/tkoenderink-prog/claude-code-dev-harness

Should see:
- ✅ README.md with installation instructions
- ✅ All 118+ files organized correctly
- ✅ Tag v2.1.0 visible in releases
- ✅ LICENSE file (MIT)

## What Gets Deployed

### Core Components

**Agents** (5 files):
- `orchestrator.md` - Chief of Staff, coordinates all work
- `architect.md` - Technical design and architecture
- `engineer.md` - Code implementation
- `tester.md` - Quality assurance and testing
- `reviewer.md` - Code review and standards

**Skills** (100+ files across 10 categories):
- `api/` - API design and integration (10 skills)
- `architecture/` - System design patterns (10 skills)
- `database/` - Data modeling and optimization (10 skills)
- `debugging/` - Issue resolution (10 skills)
- `deployment/` - CI/CD and DevOps (10 skills)
- `development/` - Core coding patterns (10 skills)
- `documentation/` - Technical writing (10 skills)
- `refactoring/` - Code improvement (10 skills)
- `security/` - Security best practices (10 skills)
- `testing/` - Test strategies (10 skills)

**Commands** (4 files):
- `harness-install.md` - Installation wizard (251 lines)
- `harness-pull.md` - Update from central (428 lines)
- `harness-push.md` - Contribute improvements (351 lines)
- `harness-fix-after-update.md` - Troubleshooting (452 lines)

**Hooks** (3 files):
- `session-start` - Session initialization with version check
- `user-prompt-submit` - Prompt processing
- `stop` - Session cleanup

**Documentation**:
- `README.md` - Complete usage guide
- `CHANGELOG.md` - Version history
- `LICENSE` - MIT License
- `CLAUDE.md` - Full specification
- `VERSION` - Current version (2.1.0)

### Features Included

✅ **Version Management System**
- `.claude/VERSION.lock` for tracking
- CLAUDE.md marker system
- Automatic update checking

✅ **Harness Management Commands**
- Install harness in new projects
- Pull updates safely with backups
- Push improvements back
- Fix issues after updates

✅ **Enhanced Session Hook**
- Version checking (6-hour cache)
- Fast git ls-remote
- Offline support
- 5-second timeout

✅ **Safe Update System**
- Automatic backups before updates
- PROJ- prefix preservation
- PROJECT-SPECIFIC section protection
- Conflict resolution with .CONFLICT files

## After Deployment

### Test the Installation

1. Create a test project:
   ```bash
   mkdir /tmp/test-project
   cd /tmp/test-project
   ```

2. Open in Claude Code and run:
   ```
   /harness-install
   ```

3. Answer the prompts:
   - GitHub username: `tkoenderink-prog`
   - Version: `latest`
   - Examples: `no`

4. Verify installation:
   ```bash
   ls -la .claude/
   cat .claude/VERSION.lock
   ```

### Use in Your Projects

In any project with Claude Code:

```
/harness-install
```

This will:
- Clone the harness from GitHub
- Create `.claude/` directory structure
- Set up `CLAUDE.md` with markers
- Create `VERSION.lock` for tracking
- Initialize state directory
- Update `.gitignore`

## Troubleshooting

### Issue: Git authentication required

**Solution**: Set up SSH keys or use GitHub's authentication helper:
```bash
git config --global credential.helper cache
```

### Issue: Permission denied on hooks

**Solution**: Make hooks executable:
```bash
chmod +x .claude/hooks/*
```

### Issue: rsync not found

**Solution**: Use cp instead:
```bash
cp -r harness-dist/* /tmp/harness-deploy/
```

### Issue: Tag already exists

**Solution**: Delete and recreate:
```bash
git tag -d v2.1.0
git push origin :refs/tags/v2.1.0
git tag -a v2.1.0 -m "Version 2.1.0"
git push origin v2.1.0
```

## File Statistics

- **Total Files**: 118
- **Total Lines**: ~12,000 lines of code and documentation
- **Size**: ~1 MB
- **Languages**: Markdown (documentation), Python (hooks)

## Repository Information

- **Repository**: https://github.com/tkoenderink-prog/claude-code-dev-harness
- **Version**: 2.1.0
- **Release Date**: 2025-11-09
- **License**: MIT
- **Minimum Requirements**: Claude Code, Git

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review `README.md` in the deployed repository
3. Run `/harness-fix-after-update` for diagnostics
4. Create an issue on GitHub

## Next Steps

After successful deployment:

1. ✅ Visit the GitHub repository and verify files
2. ✅ Test installation in a new project
3. ✅ Update `README.md` if needed (project-specific info)
4. ✅ Share the repository URL with team members
5. ✅ Consider creating a GitHub release from the v2.1.0 tag

---

**Deployment Location**: This directory (`harness-dist/`) can be removed after successful deployment.

**Central Repository**: All future updates should be made to the deployed GitHub repository, not this distribution directory.
