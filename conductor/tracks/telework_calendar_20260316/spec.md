# Specification: Telework Calendar Integration

## Overview

This track aims to integrate telework management into the `hr.employee` calendar view. Employees can request telework days directly from the calendar, which will then follow an approval workflow with specific visual indicators and automated notifications for managers.

## Track ID

`telework_calendar_20260316`

## Functional Requirements

### 1. Data Model: `telework.request`

- Create a new model `telework.request` with:
  - `employee_id`: Many2one (`hr.employee`).
  - `date`: Date of the telework.
  - `state`: Selection (`draft`, `confirm`, `validate`).
  - `manager_id`: Many2one (`res.users`, related to the employee's manager).

### 2. Calendar View Extension

- Override the calendar view accessible from the `hr.employee` buttons (Time Off/Attendance context) to display `telework.request` records.
- **Selection Logic**: When an employee selects a day, the standard Odoo calendar creation dialog should appear for `telework.request`.

### 3. Visual States (CSS)

- Style calendar events based on their `state`:
  - **Draft/Confirm**: Yellow background with diagonal stripes (`striped` effect).
  - **Validated**: Solid yellow background.

### 4. Approval Workflow & Notifications

- **Creation**: Upon creating/confirming a request, an **Odoo Activity** is automatically created for the manager.
- **Validation**: Only the assigned manager can validate the request.

## Technical Constraints

- **Puzzle Architecture**: All changes must reside within the `Teletrabajo` module. No modifications to core `hr` modules.
- **Odoo 18 Compatibility**: Use standard Odoo 18 calendar view features and CSS/OWL patterns.

## Acceptance Criteria

- [ ] Employees can see/select telework days in the calendar.
- [ ] Selecting a day opens the standard creation popup.
- [ ] Draft/Confirm requests appear as yellow striped events.
- [ ] Validated requests appear as solid yellow events.
- [ ] An Odoo Activity is created for the manager on confirmation.
- [ ] Only the manager can validate.
