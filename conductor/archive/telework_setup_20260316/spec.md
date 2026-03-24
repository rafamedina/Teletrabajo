# Specification: Telework Management Extension

## Objective

Extend the `hr.employee` model to manage telework requests, allowing only the assigned manager to validate the requests. This module acts as a "puzzle piece" that integrates seamlessly with the existing employee view without modifying the core files.

## Architecture

- **Model**: Inherit `hr.employee` to add `telework_state` (Selection: 'draft', 'validated') and `manager_id` (Many2one to `hr.employee`).
- **View**: Inherit the standard employee form view to inject the new fields and the "Validate" button into an **existing** page/tab (e.g., "Work Information" or the existing telework tab).
- **Logic**: A Python method `action_validate_telework` that checks if the current user is the assigned manager before changing the state.

## Detailed Requirements

### 1. Model Extension (hr.employee)

- **telework_state**:
  - Type: Selection
  - Options: `draft` (Borrador), `validated` (Validado)
  - Default: `draft`
- **manager_id**:
  - Type: Many2one
  - Model: `hr.employee`
  - String: "Manager de Teletrabajo"

### 2. View Inheritance

- **Location**: Locate the existing page within the employee form notebook (e.g., `hr_settings` or `public`).
- **Fields**: Inject `manager_id` and `telework_state` (readonly).
- **Button**: Insert a button to trigger `action_validate_telework` inside this existing page or in the header, ensuring it's only visible/clickable in the correct state.

### 3. Validation Logic

- **Method**: `action_validate_telework`
- **Check**: The `env.user.employee_id` must match the `manager_id` of the employee record being validated.
- **Action**: Update `telework_state` to `validated`.
- **Constraint**: Raise a `UserError` if the user is not the assigned manager.

## Acceptance Criteria

- [ ] The `telework_state` defaults to "Borrador".
- [ ] Fields and the validation button appear correctly within the existing employee tab.
- [ ] Clicking "Validate" works only if the current user is the assigned manager.
- [ ] The state changes to "Validado" upon successful validation.
- [ ] The code is separated into 3 commented "puzzle pieces" (Model, View, Logic).
