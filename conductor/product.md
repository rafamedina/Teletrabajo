# Project: Teletrabajo

## Initial Concept

Create a new Odoo 18 module to handle telework management for `hr.employee`, ensuring only the assigned manager can validate days, while maintaining the `hr` module untouched (puzzle architecture).

## User Preferences

- **Development Skill**: Use the `odoo-development` skill for all coding tasks.
- **Commit Workflow**: Always ask for a commit message before committing changes.

## Vision

To provide a structured and automated way to manage telework requests in Odoo 18, ensuring a seamless experience for employees and managers alike.

## Target Audience

- **Employees**: To request and track their telework days.
- **Managers**: To validate and oversee the telework requests of their direct reports.

## Core Goals

- **Validation Workflow**: Implement a clear process for validating telework days, from draft to validation.
- **Manager-Specific Validation**: Ensure only the assigned manager for an employee can validate their telework days.
- **Notification System**: Automatically alert managers when changes are made to telework schedules.

## Functional Requirements

- **Employee Extension**: Extend the `hr.employee` model to include `telework_state` (Draft/Validated) and `manager_id`.
- **Validation Action**: Add a button to the employee form view to trigger the validation method.
- **Manager Check Logic**: Implement Python logic to verify the current user is the employee's assigned manager before allowing validation.
- **Manager Alerts**: Generate Odoo Activities for the manager whenever telework location fields are modified.

## Technical Constraints

- **Puzzle Architecture**: The solution must be implemented as a new module that extends the existing `hr` module, keeping the core code untouched.
- **Odoo 18 Support**: Full compatibility with Odoo 18.0 features and conventions.
- **Code Standards**: Adhere to the Odoo development guidelines, with clear comments and idiomatic Python/XML code.
