# 🚀 UV Commands Guide - Important for Students!

## 🎯 What is UV?

UV is a modern Python package manager that makes running Python projects easier. Think of it as a smart assistant that handles all the complex Python environment setup for you.

## ⚠️ IMPORTANT: Always Use UV Run

**Instead of typing:**
```bash
python script.py  # ❌ This might not work
```

**Always type:**
```bash
uv run python script.py  # ✅ This will work!
```

## 📋 Common Commands You'll Use

### Running Python Scripts
```bash
# ❌ OLD WAY (might cause errors)
python demo_simple.py
python scripts/test_omi_connection.py

# ✅ NEW WAY (always works)
uv run python demo_simple.py
uv run python scripts/test_omi_connection.py
```

### Running Python Modules
```bash
# ❌ OLD WAY
python -m agents.context_analysis.agent

# ✅ NEW WAY
uv run python -m agents.context_analysis.agent
```

### Installing New Packages
```bash
# ❌ OLD WAY
pip install requests

# ✅ NEW WAY
uv pip install requests
```

## 🤔 Why Do We Need UV?

1. **Automatic Environment Management**: UV automatically uses the correct Python version and installed packages
2. **No Activation Needed**: You don't need to remember `source .venv/bin/activate`
3. **Consistent Across Systems**: Works the same on Mac, Windows, and Linux
4. **Faster**: UV is much faster than traditional pip

## 🔧 UV vs Traditional Python

| Task | Traditional Way | UV Way |
|------|----------------|---------|
| Run a script | `python script.py` | `uv run python script.py` |
| Install package | `pip install package` | `uv pip install package` |
| Activate environment | `source .venv/bin/activate` | Not needed! |
| Check Python version | `python --version` | `uv run python --version` |

## 💡 Quick Tips

1. **UV Creates `.venv` (with dot)**: The virtual environment folder has a dot: `.venv` not `venv`

2. **No Activation Needed**: You never need to run `source .venv/bin/activate` when using UV

3. **Always Prefix with UV**: When in doubt, add `uv run` before any Python command

4. **Check You Have UV**: 
   ```bash
   uv --version  # Should show UV version
   ```

## 🚨 Common Errors and Fixes

### Error: "No such file or directory: venv/bin/activate"
**Why**: You're trying to use the old activation method  
**Fix**: Use `uv run python` instead

### Error: "Module not found"
**Why**: You ran `python` without `uv run`  
**Fix**: Add `uv run` prefix: `uv run python script.py`

### Error: "Command not found: uv"
**Why**: UV isn't installed yet  
**Fix**: Install UV first:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 📚 Examples for This Demo

### Starting the Demo
```bash
# Step 1: Start OMI Server (in terminal 1)
./scripts/start_omi_mcp.sh

# Step 2: Run Demo (in terminal 2)
uv run python demo_simple.py
```

### Testing Connection
```bash
uv run python scripts/test_omi_connection.py
```

### Running Individual Agents
```bash
uv run python -m agents.context_analysis.agent
uv run python -m agents.action_planning.agent
```

## 🎓 Remember This Rule

**If you see `python` in any command, add `uv run` before it!**

```bash
# See this?
python anything.py

# Change it to:
uv run python anything.py
```

---

*This guide is specifically for the OMI A2A Demo. UV makes Python development easier - embrace it!*