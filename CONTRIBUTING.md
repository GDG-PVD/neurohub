# Contributing to NeuroHub

Thank you for your interest in contributing to NeuroHub! This educational project welcomes contributions from students, educators, and developers interested in multi-agent AI systems.

## 🤝 How to Contribute

### 1. Report Issues

If you find a bug or have a suggestion:
1. Check if the issue already exists
2. Create a new issue with a clear title and description
3. Include steps to reproduce (for bugs)
4. Add relevant labels

### 2. Suggest Features

We love new ideas! When suggesting features:
- Explain the use case
- Describe how it helps students learn
- Consider implementation complexity

### 3. Submit Pull Requests

#### Setup

```bash
# Fork and clone the repository
git clone git@github.com:YOUR-USERNAME/neurohub.git
cd neurohub

# Add upstream remote
git remote add upstream git@github.com:GDG-PVD/neurohub.git

# Create a new branch
git checkout -b feature/your-feature-name
```

#### Development Process

1. **Make your changes**
   - Follow existing code style
   - Add tests if applicable
   - Update documentation

2. **Test your changes**
   ```bash
   # Run the demo
   uv run python demo_simple.py
   
   # Test with Docker if modifying agents
   docker-compose up
   ```

3. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add amazing new feature"
   ```
   
   Use conventional commits:
   - `feat:` New features
   - `fix:` Bug fixes
   - `docs:` Documentation updates
   - `test:` Test additions
   - `refactor:` Code refactoring

4. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

### 4. Improve Documentation

Documentation is crucial for educational projects:
- Fix typos and clarify explanations
- Add examples and use cases
- Create tutorials or guides
- Translate to other languages

## 📝 Code Style

### Python
- Follow PEP 8
- Use type hints where helpful
- Add docstrings to functions
- Keep functions focused and small

### Documentation
- Use clear, simple language
- Include code examples
- Add visual diagrams when helpful
- Consider student perspective

## 🎓 Educational Focus

Remember this is an educational project. When contributing:
- Prioritize clarity over cleverness
- Add comments explaining complex concepts
- Create examples that teach
- Consider different learning styles

## 🧪 Testing

Before submitting:
1. Test the basic demo works
2. Verify documentation is accurate
3. Check for typos
4. Ensure new features don't break existing ones

## 📋 Pull Request Checklist

- [ ] Code follows project style
- [ ] Documentation updated if needed
- [ ] Tests pass (if applicable)
- [ ] Commit messages are clear
- [ ] PR description explains changes
- [ ] Considered educational impact

## 🌟 Recognition

Contributors will be:
- Listed in the README
- Credited in release notes
- Thanked in our community

## 💬 Questions?

- Open a discussion issue
- Join our Discord community
- Email: gdg-pvd@example.com

## 🚀 Areas Needing Help

### High Priority
- Windows installation guide improvements
- More agent examples
- Interactive tutorials

### Good First Issues
- Documentation typos
- Code comments
- Example improvements
- Error message clarity

### Advanced
- New agent implementations
- Performance optimizations
- Testing framework
- CI/CD setup

## 📜 Code of Conduct

Be respectful, inclusive, and constructive. This is a learning environment where everyone should feel welcome to contribute and ask questions.

---

Thank you for helping make NeuroHub better for students everywhere! 🎉