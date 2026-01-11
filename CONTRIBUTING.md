# Contributing to Wikipedia Quiz App

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - System information (OS, browser, etc.)

### Suggesting Features

1. Check if the feature has been suggested
2. Create an issue describing:
   - Use case and benefits
   - Proposed implementation
   - Potential challenges

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

## Development Guidelines

### Code Style

**Python (Backend):**
- Follow PEP 8
- Use type hints
- Add docstrings
- Maximum line length: 100 characters

**JavaScript (Frontend):**
- Use ES6+ features
- Use functional components
- Follow React best practices
- Use meaningful variable names

### Testing

Before submitting:
- Test all features manually
- Verify backend API endpoints
- Check frontend UI/UX
- Test error handling
- Verify database operations

### Commit Messages

Format: `type: description`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Testing
- `chore`: Maintenance

Examples:
- `feat: add quiz export functionality`
- `fix: resolve database connection issue`
- `docs: update deployment guide`

## Project Structure

```
Wiki Quiz App/
├── backend/              # FastAPI backend
│   ├── main.py          # Main application
│   ├── models.py        # Database models
│   ├── schemas.py       # Pydantic schemas
│   ├── scraper.py       # Wikipedia scraper
│   └── quiz_generator.py # LLM integration
├── frontend/            # React frontend
│   └── src/
│       ├── components/  # React components
│       ├── services/    # API services
│       └── App.jsx      # Main app
├── sample_data/         # Sample outputs
└── screenshots/         # UI screenshots
```

## Areas for Contribution

### High Priority
- [ ] Unit tests for backend
- [ ] Integration tests
- [ ] Performance optimization
- [ ] Enhanced error handling
- [ ] Accessibility improvements

### Medium Priority
- [ ] Additional LLM providers (OpenAI, Claude, etc.)
- [ ] Quiz export (PDF, CSV)
- [ ] User authentication
- [ ] Quiz sharing functionality
- [ ] Multi-language support

### Low Priority
- [ ] Dark mode
- [ ] Custom themes
- [ ] Quiz templates
- [ ] Analytics dashboard
- [ ] Social media integration

## Questions?

Feel free to open an issue for any questions or concerns.

Thank you for contributing! 🚀
