# Contributing to Travel Planner

Thank you for your interest in contributing to Travel Planner! We welcome contributions from the community.

## 🎯 Ways to Contribute

- 🐛 **Bug Reports**: Found a bug? Let us know!
- 💡 **Feature Requests**: Have an idea? We'd love to hear it!
- 🔧 **Code Contributions**: Help us build and improve
- 📖 **Documentation**: Help improve our docs
- 🧪 **Testing**: Help us test new features

## 🚀 Getting Started

### Prerequisites
- Node.js 16+ and npm
- Python 3.9+ and pip
- Git knowledge

### Setup Development Environment

1. **Fork the Repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/travel-planner.git
   cd travel-planner
   ```

2. **Set Up Backend**
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Set up environment
   cp .env.example .env
   # Edit .env with your settings
   
   # Test backend
   cd backend
   python test_backend.py
   ```

3. **Set Up Frontend**
   ```bash
   # Install Node dependencies
   npm install
   
   # Start development server
   npm run dev
   ```

4. **Verify Setup**
   ```bash
   # Backend should be running on http://localhost:8000
   # Frontend should be running on http://localhost:5173
   # API docs at http://localhost:8000/docs
   ```

## 📝 Development Workflow

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-description
```

### 2. Make Changes
- Write clean, readable code
- Follow existing code style
- Add tests for new features
- Update documentation as needed

### 3. Test Your Changes
```bash
# Backend tests
cd backend
python test_backend.py
pytest

# Frontend tests
npm test
npm run lint
```

### 4. Commit Changes
```bash
git add .
git commit -m "feat: add new booking feature"

# Use conventional commits:
# feat: new feature
# fix: bug fix
# docs: documentation changes
# style: formatting changes
# refactor: code refactoring
# test: adding tests
# chore: maintenance tasks
```

### 5. Push and Create PR
```bash
git push origin feature/your-feature-name
# Then create a Pull Request on GitHub
```

## 🎨 Code Style Guidelines

### Python (Backend)
- Follow **PEP 8** style guide
- Use **Black** for code formatting
- Add type hints where possible
- Write docstrings for functions and classes
- Maximum line length: 88 characters

```python
# Example
def search_flights(
    origin: str, 
    destination: str, 
    date: date,
    passengers: int = 1
) -> List[FlightOption]:
    """Search for available flights.
    
    Args:
        origin: Origin airport code (IATA)
        destination: Destination airport code (IATA)
        date: Departure date
        passengers: Number of passengers
        
    Returns:
        List of available flight options
    """
    pass
```

### TypeScript (Frontend)
- Use **TypeScript** for all new code
- Follow **ESLint** configuration
- Use **Prettier** for formatting
- Prefer **functional components** with hooks
- Use **descriptive variable names**

```typescript
// Example
interface FlightSearchProps {
  onSearch: (params: SearchParams) => void;
  loading?: boolean;
}

const FlightSearch: React.FC<FlightSearchProps> = ({ 
  onSearch, 
  loading = false 
}) => {
  // Component implementation
};
```

## 🧪 Testing Guidelines

### Backend Testing
- Write unit tests for new functions
- Test API endpoints with different scenarios
- Mock external API calls
- Aim for >80% code coverage

```python
# Example test
def test_flight_search():
    """Test flight search functionality."""
    search_params = FlightSearchRequest(
        origin="NYC",
        destination="LAX",
        departure_date="2024-06-01",
        passengers=2
    )
    
    results = search_flights(search_params)
    assert len(results) > 0
    assert all(flight.price > 0 for flight in results)
```

### Frontend Testing
- Write component tests
- Test user interactions
- Test API integration
- Use React Testing Library

```typescript
// Example test
test('should search flights when form is submitted', async () => {
  render(<FlightSearch onSearch={mockOnSearch} />);
  
  fireEvent.change(screen.getByLabelText('Origin'), {
    target: { value: 'NYC' }
  });
  
  fireEvent.click(screen.getByText('Search'));
  
  expect(mockOnSearch).toHaveBeenCalledWith({
    origin: 'NYC',
    // ... other params
  });
});
```

## 📋 Pull Request Guidelines

### Before Submitting
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] No console errors or warnings
- [ ] Changes are tested manually

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing completed
- [ ] All tests pass

## Screenshots (if applicable)
Add screenshots for UI changes

## Additional Notes
Any additional information
```

## 🐛 Bug Reports

Use the issue template:

```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What should happen

**Screenshots**
Add screenshots if applicable

**Environment**
- OS: [e.g. Windows 10]
- Browser: [e.g. Chrome 91]
- Version: [e.g. 1.0.0]
```

## 💡 Feature Requests

Use the feature request template:

```markdown
**Feature Description**
Clear description of the feature

**Problem Statement**
What problem does this solve?

**Proposed Solution**
How should this work?

**Alternatives Considered**
Other solutions you considered

**Additional Context**
Any additional information
```

## 📖 Documentation

- Keep README.md up to date
- Document API changes
- Add inline code comments
- Update type definitions
- Include examples for new features

## 🎉 Recognition

Contributors will be:
- Added to the CONTRIBUTORS.md file
- Mentioned in release notes
- Given credit in documentation

## 📞 Getting Help

- 💬 **GitHub Discussions**: Ask questions
- 📧 **Email**: dev@travelplanner.com
- 🐛 **Issues**: Report bugs or request features

## 📜 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Focus on the project goals

Thank you for contributing to Travel Planner! 🙏