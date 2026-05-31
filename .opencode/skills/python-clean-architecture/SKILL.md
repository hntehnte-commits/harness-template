---
name: python-clean-architecture
description: Enforce SOLID principles and clean architecture boundaries (Entities, Use Cases, Interfaces) in Python projects, preventing coupling between business logic and framework-specific databases or web routers.
---

# Skill: Python Clean Architecture

## Purpose
Enforce SOLID principles and clean architecture boundaries (Entities, Use Cases, Interfaces) in Python projects, preventing coupling between business logic and framework-specific databases or web routers.

---

## 1. Layer Separation and Core Boundaries
1. **Entities (Domain Logic)**: Declare high-level business rules inside plain Python classes or `@dataclass`. Entities must never import external libraries, frameworks (e.g., FastAPI, Django), or database engines (e.g., SQLAlchemy, Pydantic models).
2. **Use Cases (Interactors)**: Implement application-specific workflows. Use Cases coordinate the flow of data to and from Entities, and must interface with external adapters exclusively via abstract base classes (interfaces).
3. **Interface Adapters**: Declare concrete implementations of repositories, controllers, and presenters. They must inherit from domain interfaces to ensure the Dependency Inversion Principle is preserved:
   * *Correct*: Use Case imports `AbstractUserRepository` (Interface). Concrete `SQLAlchemyUserRepository` inherits from `AbstractUserRepository`.

---

## 2. Dependency Injection Protocol
1. **Explicit Injection**: Inject all repository, client, or utility dependencies through `__init__` constructors. Avoid hardcoding instantiation within methods:
   ```python
   # Correct
   class RegisterUserUseCase:
       def __init__(self, user_repo: AbstractUserRepository):
           self.user_repo = user_repo
   ```
2. **Abstract Contracts**: Leverage Python's `abc` module to define strict boundaries:
   ```python
   from abc import ABC, abstractmethod

   class AbstractUserRepository(ABC):
       @abstractmethod
       def save(self, user: User) -> None:
           pass
   ```

---

## 3. Boundary Type Safety & Validation
1. **Strict Typing (PEP 484)**: All architectural boundaries must define explicit type hints for both parameters and return types. Use `typing.Protocol` or abstract classes for interfaces.
2. **Boundary Validation**: Validate incoming request objects at the outermost adapter layer (using Pydantic or native dataclasses with custom init validation) before transferring pure domain models into the Use Cases.
