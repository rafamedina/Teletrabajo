# Implementation Plan: Telework Management Extension

## Phase 1: Model Implementation
- [ ] Task: Create `models/hr_employee.py` to inherit `hr.employee`.
- [ ] Task: Add `telework_state` (Selection: 'draft', 'validated') and `manager_id` (Many2one) fields.
- [ ] Task: Update `__init__.py` files to import the new models.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Model Implementation' (Protocol in workflow.md)

## Phase 2: Logic Implementation
- [ ] Task: Implement `action_validate_telework` method in `models/hr_employee.py`.
- [ ] Task: Add logic to check if `self.env.user.employee_id == self.manager_id`.
- [ ] Task: Raise `UserError` if validation fails; otherwise, update `telework_state`.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Logic Implementation' (Protocol in workflow.md)

## Phase 3: View Implementation
- [ ] Task: Create `views/hr_employee_views.xml`.
- [ ] Task: Inherit `hr.view_employee_form` to locate an existing page (e.g., `<page name="public">` or similar depending on the existing telework structure).
- [ ] Task: Insert `manager_id` and `telework_state` into the existing page.
- [ ] Task: Insert a button to trigger `action_validate_telework`.
- [ ] Task: Add the view to `__manifest__.py`.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: View Implementation' (Protocol in workflow.md)

## Phase 4: Output Generation (Puzzle Pieces)
- [ ] Task: Extract the code into the 3 "puzzle pieces" requested by the user.
- [ ] Task: Format the output with `# PIEZA X - INICIO` and `# PIEZA X - FIN` comments as required.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Output Generation' (Protocol in workflow.md)
