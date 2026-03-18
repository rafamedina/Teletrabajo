# Implementation Plan: Telework Calendar Integration

## Phase 1: Scaffolding & Data Model [checkpoint: c6db4d5]

- [x] Task: Define `telework.request` model with fields (`employee_id`, `date`, `state`, `manager_id`) 82e34ab
  - [x] Write tests for model structure and default values
  - [x] Implement `telework.request` model in `models/telework_request.py`
- [x] Task: Set up Access Rights and Rules 82e34ab
  - [x] Define `ir.model.access.csv` for the new model
  - [x] Task: Create Record Rules for employees (own requests) and managers (department requests) 49ce872
- [x] Task: Conductor - User Manual Verification 'Phase 1: Scaffolding & Data Model' (Protocol in workflow.md)

## Phase 2: Calendar View Integration

- [ ] Task: Inherit and Extend `hr.employee` Calendar View
  - [ ] Write tests to verify the calendar view is inherited and uses `telework.request`
  - [ ] Create `views/telework_request_views.xml` with calendar definition
  - [ ] Extend the employee's existing calendar action to point to this new model context
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Calendar View Integration' (Protocol in workflow.md)

## Phase 3: Visual Indicators (CSS)

- [ ] Task: Implement CSS styles for Telework States
  - [ ] Create `static/src/css/telework_calendar.css`
  - [ ] Define styles for `.o_telework_draft` (yellow striped) and `.o_telework_validated` (solid yellow)
- [ ] Task: Map states to CSS classes in the Calendar View
  - [ ] Update calendar view XML to use the `color` and `filters` to apply the CSS classes
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Visual Indicators (CSS)' (Protocol in workflow.md)

## Phase 4: Approval Logic & Notifications

- [ ] Task: Automated Manager Notifications (Odoo Activity)
  - [ ] Write tests for activity creation upon request confirmation
  - [ ] Implement `create_activity_for_manager` method in `telework.request` model
- [ ] Task: Validation Access Logic
  - [ ] Write tests ensuring only the manager can call the `action_validate` method
  - [ ] Implement `action_validate` with manager verification logic
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Approval Logic & Notifications' (Protocol in workflow.md)

## Phase 5: Final Integration & Polish

- [ ] Task: Final System Verification and End-to-End Tests
  - [ ] Write E2E tests for the full flow: create, notify, validate, view
  - [ ] Perform manual smoke test in Odoo 18 interface
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Final Integration & Polish' (Protocol in workflow.md)
