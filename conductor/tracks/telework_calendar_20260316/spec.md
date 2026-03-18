# Specification: Telework Integration in Time Off (hr.leave)

## Overview

Instead of a separate model, telework will be integrated directly into Odoo's standard **Time Off (hr.leave)** module. A dedicated **Leave Type** "Teletrabajo" will be created. Requests of this type will be visually distinguished in the existing Time Off calendar with a yellow color (striped for draft/confirmed, solid for validated).

## Track ID

`telework_calendar_20260316` (Updated Direction)

## Functional Requirements

### 1. Data Configuration: `hr.leave.type`
- Create a default Leave Type named "Teletrabajo".
- **Settings**: 
  - `allocation_type`: No allocation needed (employees can request freely).
  - `request_unit`: Day (or Half Day).
  - `color`: Purple (Index 5).
  - `requires_allocation`: No.
  - `leave_validation_type`: Single validation (hr).

### 2. Visual Differentiation (CSS)
- The Time Off calendar entries for the "Teletrabajo" type must be styled:
  - **Status: Draft/To Approve**: Purple background with diagonal stripes.
  - **Status: Approved**: Solid purple background.

### 3. Workflow
- Use the standard `hr.leave` approval workflow.
- Optionally, automate certain states if requested by the user later (e.g., auto-confirm).

## Technical Constraints

- **Extension**: Inherit `hr.leave` and `hr.leave.type` if needed for CSS targeting.
- **CSS**: Use OWL or standard backend CSS to target calendar events by type.
- **Odoo 18**: Must follow the latest Odoo 18 patterns for Calendar and Time Off.

## Acceptance Criteria

- [ ] A "Teletrabajo" leave type is available in the Time Off dashboard.
- [ ] Selecting "Teletrabajo" in the calendar opens the standard Time Off request form.
- [ ] Telework entries in the Time Off calendar are yellow and striped when not yet fully approved.
- [ ] Fully approved telework entries are solid yellow.
- [ ] No new independent menu or model is used; it's all within Time Off.
