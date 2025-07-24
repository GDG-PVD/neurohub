# 📋 Repository Migration Checklist

## Files to Copy to NeuroHub Repository

### ✅ Core Files
- [ ] `README-neurohub.md` → Rename to `README.md`
- [ ] `LICENSE`
- [ ] `CONTRIBUTING.md`
- [ ] `.gitignore`
- [ ] `.env.example`
- [ ] `pyproject.toml`
- [ ] `setup.sh`

### ✅ Documentation
- [ ] `STUDENT_GUIDE.md`
- [ ] `INSTRUCTOR_PRESENTATION.md`
- [ ] `STUDENT_QUICK_REFERENCE.md`
- [ ] `UV_COMMANDS_GUIDE.md`
- [ ] `WORKING_DEMO_SUMMARY.md`
- [ ] `OMI_MCP_OFFICIAL_REFERENCE.md`
- [ ] `MCP_VS_A2A_EXPLANATION.md`

### ✅ Documentation Folders
- [ ] `docs/classroom/`
  - [ ] `DEMO_BACKUP_PLAN.md`
  - [ ] `EXPECTED_OUTPUTS.md`

### ✅ Code Files
- [ ] `demo_simple.py`
- [ ] `a2a_sdk.py`
- [ ] `agents/` directory (all agent implementations)
- [ ] `core/` directory
- [ ] `config/` directory
- [ ] `scripts/` directory
- [ ] `integrations/` directory (if exists)

### ✅ Scripts
- [ ] `scripts/start_omi_mcp.sh`
- [ ] `scripts/stop_omi_mcp.sh`
- [ ] `scripts/test_omi_connection.py`

## ❌ Files NOT to Copy
- `.env.local` (contains secrets)
- Any `.env` files with actual keys
- `__pycache__/` directories
- `.venv/` or `venv/` directories
- `.git/` directory
- Any log files
- Any database files

## 📝 Before Pushing

1. **Remove any API keys or secrets** from all files
2. **Update the main README**: Use `README-neurohub.md` as the new `README.md`
3. **Verify .gitignore** is properly configured
4. **Test the setup** with a fresh clone

## 🚀 Git Commands

```bash
# Initialize new repo
cd /path/to/new/neurohub
git init
git remote add origin git@github.com:GDG-PVD/neurohub.git

# Add files
git add .
git commit -m "Initial commit: NeuroHub educational multi-agent AI demo"

# Push to GitHub
git push -u origin main
```

## 📋 Post-Migration

1. **Update GitHub Settings**:
   - Add description: "Educational demonstration of multi-agent AI systems using OMI wearable"
   - Add topics: `ai`, `education`, `multi-agent`, `omi`, `mcp`, `python`
   - Set up GitHub Pages if needed

2. **Create Initial Release**:
   - Tag: `v0.1.0`
   - Title: "Initial Educational Release"
   - Description: Include setup instructions

3. **Add Protection Rules**:
   - Protect main branch
   - Require PR reviews

4. **Documentation**:
   - Add link to live demo (if available)
   - Include screenshots in README

## ✅ Final Checks

- [ ] No sensitive data in any file
- [ ] All documentation references correct repo URL
- [ ] Setup instructions work with fresh clone
- [ ] Demo runs successfully
- [ ] All links in documentation work