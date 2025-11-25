# Contributing to APEX

Thank you for your interest in contributing to APEX! We welcome contributions from the motorsports and developer communities.

## 🎯 Ways to Contribute

### 1. Report Bugs
Found a bug? Please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Your environment (OS, browser, Python version)

### 2. Suggest Features
Have an idea? Open an issue with:
- Feature description
- Use case / problem it solves
- Proposed implementation (optional)
- Examples from other tools (optional)

### 3. Improve Documentation
- Fix typos or unclear explanations
- Add examples or tutorials
- Translate documentation
- Create video tutorials

### 4. Submit Code
- Fix bugs
- Implement new features
- Improve performance
- Add tests
- Refactor code

## 🚀 Getting Started

### Prerequisites
```bash
python 3.11+
node 18+
git
```

### Setup Development Environment

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/apex-gr-cup-racing-intelligence.git
   cd apex-gr-cup-racing-intelligence
   ```

3. **Install dependencies**
   ```bash
   # Backend
   pip install -r requirements.txt
   
   # Frontend
   cd frontend
   npm install
   ```

4. **Extract race data**
   ```bash
   python scripts/extract_data.py
   ```

5. **Run development servers**
   ```bash
   # Terminal 1: Backend
   python -m uvicorn backend.main:app --reload
   
   # Terminal 2: Frontend
   cd frontend
   npm run dev
   ```

## 📝 Development Guidelines

### Code Style

**Python**:
- Follow PEP 8
- Use type hints
- Write docstrings for functions
- Keep functions focused and small

**TypeScript/React**:
- Use functional components
- Follow React hooks best practices
- Use TypeScript types (no `any`)
- Keep components small and reusable

### Commit Messages
Follow conventional commits:
```
feat: add tire degradation model
fix: correct lap time calculation
docs: update API documentation
refactor: simplify data loading logic
test: add unit tests for lap analyzer
```

### Branch Naming
```
feature/tire-degradation
fix/lap-time-bug
docs/api-reference
refactor/data-loader
```

## 🧪 Testing

### Run Tests
```bash
# Backend tests
pytest

# Frontend tests
cd frontend
npm test
```

### Add Tests
- Write tests for new features
- Ensure existing tests pass
- Aim for >80% code coverage

## 📋 Pull Request Process

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, documented code
   - Add tests if applicable
   - Update documentation

3. **Test your changes**
   ```bash
   # Run tests
   pytest
   cd frontend && npm test
   
   # Check code style
   flake8 backend/
   cd frontend && npm run lint
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template
   - Wait for review

### PR Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] All tests pass
- [ ] No merge conflicts
- [ ] Descriptive commit messages

## 🎨 Design Principles

### 1. **Simplicity**
- Keep it simple and intuitive
- Avoid over-engineering
- Clear is better than clever

### 2. **Performance**
- Sub-100ms API responses
- Efficient data processing
- Minimize bundle size

### 3. **Reliability**
- Graceful error handling
- Comprehensive logging
- Defensive programming

### 4. **Accessibility**
- Free and open source
- Well-documented
- Easy to deploy

## 🏗️ Architecture

### Backend Structure
```
backend/
├── main.py              # FastAPI app
├── routers/             # API endpoints
├── services/            # Business logic
│   ├── lap_analyzer.py
│   └── s3_data_loader.py
└── config/              # Configuration
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/      # React components
│   ├── App.tsx          # Main app
│   └── main.tsx         # Entry point
└── public/              # Static assets
```

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

## 🤝 Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inclusive environment for all contributors.

### Our Standards
- Be respectful and constructive
- Welcome newcomers
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior
- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information

## 💬 Communication

- **Issues**: For bugs and feature requests
- **Discussions**: For questions and ideas
- **Pull Requests**: For code contributions

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

## 📧 Questions?

Open an issue or reach out to the maintainers!

---

**Thank you for contributing to APEX!** 🏁

Together, we're making professional racing analytics accessible to everyone.
