# ADR-007: Adopt UV as Package Manager

**Date:** 2025-07-24

**Status:** Accepted

**Deciders:** Development Team

**Tags:** tooling, development, dependencies, ai-generated

## Context

Python package management has traditionally been slow and complex, especially for projects with many dependencies. The project initially used pip with requirements.txt, but modern Python packaging standards recommend pyproject.toml. UV, created by Astral (makers of Ruff), offers significant performance improvements and better dependency resolution.

## Decision

Adopt UV as the primary package manager while maintaining pip compatibility through pyproject.toml.

## Considered Options

1. **UV (Astral)**: Modern, fast Python package manager
   - Pros:
     - 10-100x faster than pip
     - Better dependency resolver
     - Drop-in pip replacement
     - Built in Rust for performance
     - Supports PEP 517/518/621 standards
   - Cons:
     - Relatively new tool
     - Requires separate installation
     - Team learning curve

2. **pip + pip-tools**: Traditional approach
   - Pros:
     - Universal availability
     - Well-understood
     - No extra installation
   - Cons:
     - Slow dependency resolution
     - Complex dependency management
     - Requires multiple files

3. **Poetry**: Popular alternative package manager
   - Pros:
     - All-in-one solution
     - Good dependency resolution
     - Lock file support
   - Cons:
     - Slower than UV
     - Non-standard pyproject.toml sections
     - More opinionated

## Consequences

### Positive
- Faster dependency installation (seconds vs minutes)
- Better dependency conflict resolution
- Modern Python packaging standards (PEP 621)
- Maintains pip compatibility
- Improved developer experience

### Negative
- Developers need to install UV separately
- Another tool to learn
- Potential issues if UV development stops

### Neutral
- Setup scripts auto-detect UV
- Fallback to pip ensures compatibility
- Documentation needs updating

## Implementation Notes

```toml
# pyproject.toml replaces requirements.txt
[project]
name = "omi-a2a-demo"
dependencies = [
    "fastapi>=0.104.0",
    "a2a-sdk>=1.0.0",
    # ...
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "black>=23.0.0",
    # ...
]
```

```bash
# Installation is now:
uv pip install -e ".[dev]"
# Instead of:
pip install -r requirements.txt
```

## References

- [UV Documentation](https://github.com/astral-sh/uv)
- [PEP 621 - Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
- [ADR-003: Docker Deployment](003-docker-deployment.md) - UV speeds up Docker builds

## Notes

This decision modernizes our Python tooling and aligns with current best practices. The performance improvements are particularly valuable for CI/CD pipelines and Docker builds.