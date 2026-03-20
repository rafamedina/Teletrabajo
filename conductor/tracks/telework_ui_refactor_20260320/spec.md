# Specification: Independent Telework Calendar Refactor

## Overview

Refactor the telework calendar from the Odoo Time Off (`hr.leave`) module into a fully independent model (`hr.telework.request`). This track focuses on replicating the core functionality of the standard Odoo calendar view while isolating it for telework management.

## Track ID

`telework_ui_refactor_20260320`

## Functional Requirements

### 1. Independent Calendar View

- Create a dedicated calendar view for the `hr.telework.request` model.
- **Features**:
  - **Quick Create**: Allow users to create requests directly on the calendar grid.
  - **Event Popups**: Clicking an event opens a popup with the request details.
  - **State Filters**: Filter events by their status (Draft, Validated, Refused).
  - **Employee Avatars**: Display the employee's avatar on the calendar entries.

### 2. Request Details

- **Attachments**: Add a binary field to allow users to attach files to their telework requests.
- **Reasoning**: Add a text field for users to provide a description/reason for their request.

### 3. Visual Styling (CSS)

- Integrate the existing green theme from `telework_timeoff.css`.
- **Styling Rules**:
  - **Draft/Pending**: Green background with diagonal stripes.
  - **Validated**: Solid green background.
  - **Refused**: Strikethrough or distinct visual marker (following `telework_timeoff.css`).

### 4. Access Control

- The calendar is exclusively accessible via the **Smart Button** on the `hr.employee` form.
- The view is automatically filtered for the specific employee when accessed from their profile.

## Technical Constraints

- **Odoo 18 UI Patterns**: Follow the latest XML and JS patterns for Odoo 18 Calendar and Form views.
- **Model Isolation**: Zero functional dependency on the `hr.holidays` (Time Off) module for this calendar's operation.

## Acceptance Criteria

- [ ] A dedicated "Telework" Smart Button on the employee profile opens a fully functional calendar view.
- [ ] Users can create telework requests via "Quick Create" on the calendar.
- [ ] Telework requests include fields for attachments and a text description.
- [ ] Entries are styled as green/striped when draft and solid green when validated.
- [ ] The calendar provides state-based filtering (Draft, Validated, Refused).
- [ ] No traces of the standard Time Off module are present in this specific view.
