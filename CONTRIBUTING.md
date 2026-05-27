# Contributing Guidelines

Thank you for contributing to the WhatsApp Agent Template Platform! Please adhere to the following standards.

## Development Rules

### Branch Naming
Create feature branches named after the module or feature:
```text
feature/module-name
```
*Example*: `feature/rag`, `feature/whatsapp`

### Commit Message Format
Commit messages must follow the Conventional Commits style:
```text
type(scope): summary

[optional body describing What, Why, and Impact]
```
*Allowed Types*:
* `feat`: A new feature
* `fix`: A bug fix
* `docs`: Documentation changes
* `style`: Code style modifications (formatting, white-space)
* `refactor`: Code changes that neither fix a bug nor add a feature
* `perf`: Performance improvements
* `test`: Adding or correcting tests
* `chore`: Build process or auxiliary tool changes

*Example*:
```text
feat(agent): add execution runtime
```

## Architectural Guidelines (Modular Monolith)

* **No Circular Imports**: Enforced via import checkers.
* **No Business Logic in Routes**: Put all logic in core services.
* **No Global State**: Ensure services are stateless and rely on dependency injection.
* **Dependency Flow**: Apps can import Core/Shared. Core can import Shared. Shared cannot import anything. Customers can import Core. Nothing can import Customers.

## Coding Style
* **Python**: PEP 8 compliance, formatted using Black, checked using flake8/ruff.
* **JavaScript/TypeScript**: Prettier for formatting, ESLint for lint rules.
