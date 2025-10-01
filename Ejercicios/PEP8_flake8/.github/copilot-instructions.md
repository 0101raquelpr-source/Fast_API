# Python Exercise Project AI Assistant Guide

## Project Overview
This project uses Python as the primary programming language and Django for web development. The codebase follows PEP8 style guidelines and uses flake8 for linting.

## Technology Stack
- **Primary Language**: Python 3.x
- **Web Framework**: Django
- **Testing**: Python unittest framework
- **Code Quality**: flake8 for linting, PEP8 for style guidelines

## Project Structure
```
PEP8_flake8/
├── juego.py          # Rock Paper Scissors game implementation
├── test_juego.py     # Unit tests for the game
├── pares.py          # Even numbers exercise
└── test_pares.py     # Unit tests for even numbers
```

## Key Patterns and Conventions

### Code Style and Best Practices
- Follow PEP8 guidelines strictly
- Use docstrings for modules and functions (see `juego.py` for examples)
- Include type hints and annotations for all functions and classes
- Apply SOLID principles:
  - Single Responsibility: Each class/function does one thing well
  - Open/Closed: Open for extension, closed for modification
  - Liskov Substitution: Subtypes must be substitutable for base types
  - Interface Segregation: Keep interfaces small and focused
  - Dependency Inversion: Depend on abstractions, not concretions
- Use dataclasses for data containers
- Implement exception handling with custom exceptions when appropriate
- Use enums for predefined choices
- Prefer composition over inheritance
- Keep functions small and focused (max 20 lines recommended)
- Use meaningful variable and function names in English
- Apply early returns to reduce nesting
- Use constants for magic numbers and strings

### Refactoring Guidelines
- Regularly review and refactor code
- Extract repeated code into functions
- Use design patterns when appropriate:
  - Factory pattern for object creation
  - Strategy pattern for interchangeable algorithms
  - Observer pattern for event handling
  - Repository pattern for data access
- Convert complex conditionals to guard clauses
- Extract configuration to settings files
- Move utility functions to separate modules
- Use dependency injection for better testing
- Consider performance implications during refactoring

### Testing Strategy
- Use Python's unittest framework as primary testing tool
- Follow Test-Driven Development (TDD) principles:
  1. Write failing test first
  2. Write minimum code to pass test
  3. Refactor while keeping tests green
- Test files are prefixed with `test_`
- Group related test cases in classes inheriting from `unittest.TestCase`
- Write descriptive docstrings for test methods explaining test scenarios

### Test Coverage Requirements
- Minimum 90% code coverage required
- Test all edge cases and error conditions
- Include unit tests for all public methods
- Add integration tests for complex workflows
- Use mocking for external dependencies
- Test both success and failure scenarios
- Include performance tests for critical paths
- Test security-sensitive functionality thoroughly

### Test Structure Pattern
1. Arrange: Set up test data and conditions
2. Act: Execute the code being tested
3. Assert: Verify the results

Example from `test_juego.py`:
```python
def test_empates(self):
    """Prueba todos los casos de empate."""
    # Arrange - implícito en este caso simple
    # Act & Assert para cada caso de prueba
    self.assertEqual(determinar_ganador("piedra", "piedra"), "Empate!")
    self.assertEqual(determinar_ganador("papel", "papel"), "Empate!")
    self.assertEqual(determinar_ganador("tijera", "tijera"), "Empate!")
```

### Development Workflow
1. Write function implementation with proper docstrings
2. Create corresponding test file
3. Implement test cases for all scenarios
4. Run tests using the unittest framework

### Running Tests
- Use VS Code's built-in test runner or
- Run from terminal: `python -m unittest -v`
- Tests are configured in `.vscode/settings.json` to run all files matching `*test*.py`

### Common Operations
- Test individual file: `python -m unittest test_file.py -v`
- Run all tests: `python -m unittest discover -v`
- Check code style: `flake8 filename.py`
- Run Django development server: `python manage.py runserver`
- Create Django migrations: `python manage.py makemigrations`
- Apply migrations: `python manage.py migrate`
- Create Django app: `python manage.py startapp app_name`

### Django Development Guidelines
- Follow Django's MTV (Model-Template-View) architecture
- Place business logic in models and views
- Use Django's built-in admin interface when possible
- Implement class-based views for common CRUD operations
- Use Django Forms for data validation
- Keep settings modular (separate dev/prod configurations)

## Project-Specific Notes
- All user-facing strings are in Spanish
- Game functions return Spanish response strings
- Test assertions expect Spanish response strings