# Implementation Plan: Telework Integration in Time Off

## Phase 1: Configuration & Cleanup

- [~] Task: Remove obsolete `telework.request` model, views, and security
  - [ ] Delete `models/telework_request.py`
  - [ ] Delete `views/telework_request_views.xml`
  - [ ] Delete `security/telework_request_security.xml`
  - [ ] Remove from `__manifest__.py`
  - [ ] Delete tests in `tests/test_telework_request.py`
- [ ] Task: Create "Teletrabajo" Leave Type (Data)
  - [ ] Define `data/hr_leave_type_data.xml` for "Teletrabajo"
  - [ ] Ensure it doesn't require allocation and is available for all employees
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Configuration & Cleanup' (Protocol in workflow.md)

## Phase 2: Visual Styling (CSS)

- [ ] Task: Implement CSS styles for Telework Leave Type
  - [ ] Identify CSS classes used by Odoo 18 Calendar for leave types
  - [ ] Create `static/src/css/telework_timeoff.css`
  - [ ] Define styles for "Teletrabajo" based on its color/id and state (draft/approved)
- [ ] Task: Register CSS in Assets
  - [ ] Update `__manifest__.py` to include the new CSS file in `web.assets_backend`
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Visual Styling (CSS)' (Protocol in workflow.md)

## Phase 3: Final Integration & Tests

- [ ] Task: Write Tests for Telework Leave Integration
  - [ ] Create `tests/test_telework_leave.py`
  - [ ] Test the existence and configuration of the leave type
  - [ ] Verify employees can request it correctly
- [ ] Task: Final System Verification and End-to-End Tests
  - [ ] Perform manual smoke test in Odoo 18 Time Off dashboard
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Final Integration & Tests' (Protocol in workflow.md)
