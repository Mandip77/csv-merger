# Contributing to CSV Merger

Thank you for your interest in contributing! We welcome all contributions, from bug reports to feature ideas to code improvements.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/csv-merger
   cd csv-merger
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Set up development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Development Workflow

### Running the App
```bash
cd practise/csvmerger
python mergecsvfiles_advanced.py
```

### Code Style
- Use **PEP 8** conventions
- Aim for **clear, readable code** with descriptive variable names
- Add **docstrings** to functions and classes
- Keep **line length** under 100 characters

### Testing
For UI testing, manually exercise features in the app. For data functions, consider adding unit tests:
```bash
# Example: create tests/test_merge.py and run with pytest
pytest tests/
```

## Reporting Issues

### Bug Reports
Please include:
- **What you did** — Steps to reproduce
- **What happened** — Actual behavior
- **What you expected** — Expected behavior
- **Environment** — OS, Python version, how you installed the app
- **Screenshot/log** — Error message or log output if applicable

### Feature Requests
Describe:
- **Use case** — Why this feature would be useful
- **Example** — How you'd use it
- **Alternatives** — Any workarounds you've found

## Submitting Pull Requests

1. **Keep commits clean** — One feature or fix per commit with clear messages
2. **Test locally** — Run the app and verify your changes work
3. **Update docs** — If you change behavior, update README or help text
4. **Create PR** — Push your branch and open a pull request with:
   - Clear title and description
   - Reference any related issues (#123)
   - Screenshots for UI changes

### PR Review Process
- Project maintainers will review your PR
- We may request changes or have questions
- Once approved, your PR will be merged!

## Setting Up a Development Environment on Different Platforms

### Windows (PowerShell)
```powershell
cd practise\csvmerger
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python mergecsvfiles_advanced.py
```

### macOS / Linux (Bash)
```bash
cd practise/csvmerger
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python mergecsvfiles_advanced.py
```

## Project Areas

### High Priority (Good for Contributions)
- **Bug fixes** — Any reported issues
- **Documentation** — Improve README, docstrings, help text
- **Testing** — Add unit or integration tests
- **UX improvements** — Better error messages, tooltips, workflows

### Medium Priority
- **Performance** — Optimize large file handling
- **Theme improvements** — Better dark mode, color choices
- **Localization** — Translate UI to other languages

### Lower Priority (Requires Discussion)
- Major architecture changes
- Breaking API changes
- New dependencies (discuss first to avoid bloat)

## Code of Conduct

Be respectful, inclusive, and constructive. We're building this together!

## Questions?

- Open an issue with your question
- Start a discussion on GitHub Discussions
- Email the maintainers

---

**Thank you for contributing!** 🙏
