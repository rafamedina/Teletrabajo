# Product Guidelines: Teletrabajo

## Coding Style

- **Odoo Conventions**: Strictly follow the Odoo 18 framework's Python ORM and XML standards for all development.
- **Modern Python Syntax**: Utilize modern Python features (3.10+) where they enhance clarity and performance.
- **Puzzle Block Comments**: All code blocks must be enclosed in clear start/end comments (e.g., `# PIEZA X - INICIO` / `# PIEZA X - FIN`) to facilitate the "puzzle" architecture.

## Documentation and Documentation Skill

- **Documentation Expert**: Utilize the `documentation-writer` skill to generate high-quality technical documentation for the project.
- **Technical Context**: All Python methods and complex XML inheritance structures must be documented to explain the rationale behind the implementation.

## Naming Conventions

- **Field Prefixes**: All custom fields added to existing models must use clear, technical prefixes (e.g., `telework_state`, `telework_manager_id`) to avoid name collisions.
- **Odoo Standards**: Adhere to the standard `underscore_case` for all technical names and the `module_name.view_id` pattern for XML records.

## UX and UI Principles

- **Native Odoo Layouts**: Prioritize using the standard Odoo notebook and group elements to ensure the UI feels native and integrated.
- **Dynamic Feedback**: Leverage field attributes (e.g., `invisible`, `readonly`) to provide immediate feedback based on the employee's state and current user.
