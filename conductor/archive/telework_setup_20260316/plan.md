# Implementation Plan: Telework Management Extension

## Phase 1: Model Implementation

- [x] Task: Create `models/hr_employee.py` to inherit `hr.employee`.
- [x] Task: Add `telework_state` (Selection: 'draft', 'validated') and `manager_id` (Many2one) fields.
- [x] Task: Update `__init__.py` files to import the new models.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Model Implementation' (Protocol in workflow.md)

## Phase 2: Logic Implementation

- [x] Task: Implement `action_validate_telework` method in `models/hr_employee.py`.
- [x] Task: Add logic to check if `self.env.user.employee_id == self.manager_id`.
- [x] Task: Raise `UserError` if validation fails; otherwise, update `telework_state`.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Logic Implementation' (Protocol in workflow.md)

## Phase 3: View Implementation

- [x] Task: Create `views/hr_employee_views.xml`.
- [x] Task: Inherit `hr.view_employee_form` to locate an existing page.
- [x] Task: Insert `manager_id` and `telework_state` into the existing page.
- [x] Task: Insert a button to trigger `action_validate_telework`.
- [x] Task: Add the view to `__manifest__.py`.
- [x] Task: Conductor - User Manual Verification 'Phase 3: View Implementation' (Protocol in workflow.md)

## Phase 4: Output Generation (Puzzle Pieces)

- [x] Task: Extract the code into the 3 "puzzle pieces" requested by the user.
- [x] Task: Format the output with `# PIEZA X - INICIO` and `# PIEZA X - FIN` comments as required.
- [x] Task: Conductor - User Manual Verification 'Phase 4: Output Generation' (Protocol in workflow.md)
