# Contributing to SUMA LMS

Thank you for your interest in contributing to SUMA LMS! We welcome contributions from the community and are grateful for your help in making this project better.

## 🤝 How to Contribute

### Reporting Issues

If you find a bug or have a feature request, please:

1. Check if the issue already exists in the [Issues](https://github.com/your-username/suma-lms/issues) page
2. Create a new issue with:
   - Clear, descriptive title
   - Detailed description of the problem or feature request
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Screenshots (if applicable)

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed
4. **Test your changes**
   ```bash
   python test_api_complete.py
   python test_ollama.py
   ```
5. **Commit your changes**
   ```bash
   git commit -m "Add: your feature description"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request**

## 📋 Development Setup

### Prerequisites

- Python 3.8+
- Git
- [Ollama](https://ollama.ai) (for AI features)

### Setup Development Environment

1. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/suma-lms.git
   cd suma-lms
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment**
   ```bash
   cp env.example .env
   # Edit .env with your settings
   ```

5. **Setup Ollama (for AI features)**
   ```bash
   ollama serve
   ollama pull llama3.1:8b
   ```

6. **Initialize database**
   ```bash
   python init_db.py
   ```

7. **Start development server**
   ```bash
   python -m app.main
   ```

## 🎯 Areas for Contribution

### High Priority
- **Frontend Development**: Next.js + TailwindCSS interface
- **Mobile App**: React Native or Flutter app
- **Real-time Features**: WebSocket integration for notifications
- **Advanced AI Features**: More sophisticated AI capabilities

### Medium Priority
- **Testing**: More comprehensive test coverage
- **Documentation**: API documentation improvements
- **Performance**: Database optimization, caching
- **Security**: Enhanced security features

### Low Priority
- **Internationalization**: Multi-language support
- **Themes**: Customizable UI themes
- **Plugins**: Plugin system for extensions
- **Analytics**: Usage analytics and reporting

## 📝 Code Style Guidelines

### Python Code
- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions small and focused
- Use meaningful variable and function names

### API Design
- Follow RESTful conventions
- Use appropriate HTTP status codes
- Include proper error handling
- Document all endpoints
- Use consistent naming conventions

### Database
- Use descriptive table and column names
- Add proper indexes for performance
- Include foreign key constraints
- Write migration scripts for schema changes

## 🧪 Testing Guidelines

### Running Tests
```bash
# Run all tests
python test_api_complete.py

# Test specific functionality
python test_ollama.py
python test_api.py

# Test with coverage
pip install coverage
coverage run test_api_complete.py
coverage report
```

### Writing Tests
- Write tests for new features
- Test both success and error cases
- Use descriptive test names
- Mock external dependencies
- Aim for high test coverage

## 📚 Documentation

### Code Documentation
- Write clear docstrings
- Include type hints
- Add inline comments for complex logic
- Update README.md for new features

### API Documentation
- Document all endpoints
- Include request/response examples
- Add error code documentation
- Keep documentation up to date

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment Information**
   - Python version
   - Operating system
   - Ollama version (if applicable)

2. **Steps to Reproduce**
   - Clear, numbered steps
   - Expected behavior
   - Actual behavior

3. **Additional Context**
   - Screenshots or error messages
   - Log files
   - Related issues

## 💡 Feature Requests

When requesting features, please include:

1. **Problem Description**
   - What problem does this solve?
   - Who would benefit from this feature?

2. **Proposed Solution**
   - How should this feature work?
   - Any design considerations?

3. **Alternatives Considered**
   - Other ways to solve the problem
   - Why this approach is preferred

## 🔄 Pull Request Process

1. **Before Submitting**
   - Ensure all tests pass
   - Update documentation
   - Follow code style guidelines
   - Write clear commit messages

2. **Pull Request Template**
   - Describe what changes were made
   - Link to related issues
   - Include screenshots (if applicable)
   - List any breaking changes

3. **Review Process**
   - Address reviewer feedback
   - Keep PRs focused and small
   - Respond to comments promptly
   - Update PR as needed

## 🏷️ Commit Message Convention

Use the following format for commit messages:

```
type: short description

Longer description if needed

- Bullet points for multiple changes
- Reference issues with #123
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Maintenance tasks

Examples:
```
feat: add AI-powered task analysis

- Integrate Ollama for file analysis
- Add new API endpoint /ai/task-analysis
- Support multiple file formats

Closes #45
```

## 📞 Getting Help

If you need help:

1. Check the [Issues](https://github.com/your-username/suma-lms/issues) page
2. Read the [Documentation](README.md)
3. Join our [Discussions](https://github.com/your-username/suma-lms/discussions)
4. Create a new issue for questions

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to SUMA LMS! 🎉
