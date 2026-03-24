# Technology Stack: Teletrabajo

## Core Framework

- **Odoo 18.0 Community Edition**: The foundational ERP framework used for the project, providing the ORM, UI components, and the HR module infrastructure.

## Deployment and Infrastructure

- **Docker Compose**: The project is containerized using Docker Compose for local development and potential deployment, ensuring consistency across environments.
- **PostgreSQL 15+**: The underlying database management system used by Odoo to store and query all application data.

## Languages and Runtimes

- **Python 3.10+**: The backend programming language for all business logic, ORM models, and server actions.

## Module Architecture

- **Puzzle (Modular) Extension**: A design pattern where the solution is developed as an independent Odoo module (`teletrabajo`) that inherits and extends the core `hr` module's models and views without modifying them directly.
