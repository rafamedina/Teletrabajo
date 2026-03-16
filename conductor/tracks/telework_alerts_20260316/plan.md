# Implementation Plan: Telework Change Alerts for Managers

## Phase 1: Logic Implementation
- [ ] Task: Create a new method `_create_telework_activity` in `models/hr_employee.py` to handle the activity creation.
- [ ] Task: Integrate `_create_telework_activity` into the `write` method of `hr.employee`.
- [ ] Task: Add logic to detect changes specifically in the daily telework location fields.
- [ ] Task: Ensure the activity is assigned to the `user_id` linked to the employee's `parent_id`.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Logic Implementation' (Protocol in workflow.md)

## Phase 2: Testing and Refinement
- [ ] Task: Test the activity creation by changing a telework day as an employee.
- [ ] Task: Verify that the manager receives the correct activity with the employee's name.
- [ ] Task: Confirm that the `telework_state` still resets to `draft` correctly.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Testing and Refinement' (Protocol in workflow.md)
