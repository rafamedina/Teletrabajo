# Implementation Plan: Independent Telework Calendar Refactor

## Phase 1: Model & Backend Logic

Refine the `hr.telework.request` model to include the necessary fields for attachments and reasoning, ensuring the backend supports the new UI requirements.

- [x] **Task: Update Model Fields (TDD)**
  - [x] Write tests to verify the existence and behavior of `attachment_ids` (Many2many to `ir.attachment`) and `reason` (Text).
  - [x] Implement the fields in `models/telework_request.py`.
- [x] **Task: Security & ACLs**
  - [x] Verify that the `ir.model.access.csv` and record rules allow users to manage their own attachments.
- [x] **Task: Conductor - User Manual Verification 'Phase 1: Model & Backend Logic' (Protocol in workflow.md)**

## Phase 2: Calendar UI Implementation

Develop the dedicated calendar view with advanced Odoo 18 features (Quick Create, Popups, etc.).

- [~] **Task: Define Calendar View (TDD)**
  - [x] Write tests (Tours or Python) to verify the presence of the new calendar view definition.
  - [ ] Implement the `<calendar>` view in `views/telework_request_views.xml` with `quick_create="1"`, `event_open_popup="1"`, and employee avatars.
- [~] **Task: Implement Search & Filters**
  - [ ] Add state-based filters (Draft, Validated, Refused) to the search view.
- [ ] **Task: Form View Enhancement**
  - [ ] Update the form view to include the attachment and reason fields in a user-friendly layout.
- [ ] **Task: Conductor - User Manual Verification 'Phase 2: Calendar UI Implementation' (Protocol in workflow.md)**

## Phase 3: Visual Styling & Integration

Apply the green visual theme and finalize the Smart Button connection.

- [ ] **Task: CSS Theme Refinement (TDD)**
  - [ ] Write tests to verify that the `is_hatched` field correctly drives the CSS classes in the UI.
  - [ ] Refine `static/src/css/telework_timeoff.css` to ensure perfect compatibility with the Odoo 18 calendar renderer.
- [ ] **Task: Smart Button & Action Logic**
  - [ ] Verify that the Smart Button on `hr.employee` opens the new calendar view with the correct context and domain.
- [ ] **Task: Clean Up Redundancies**
  - [ ] Remove any remaining references to the old `hr.leave` based implementation in the Teletrabajo module.
- [ ] **Task: Conductor - User Manual Verification 'Phase 3: Visual Styling & Integration' (Protocol in workflow.md)**
