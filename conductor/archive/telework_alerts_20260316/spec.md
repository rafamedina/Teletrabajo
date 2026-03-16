# Specification: Telework Change Alerts for Managers

## Overview

Implement a notification system that alerts an employee's direct manager (`parent_id`) whenever their telework schedule is modified. This ensures that managers are promptly informed and can validate the updated arrangements via Odoo Activities.

## Functional Requirements

- **Change Detection**: Monitor modifications to the telework location fields for each day of the week (e.g., `monday_location_id`, `tuesday_location_id`, etc.).
- **Alert Trigger**: Automatically generate a new Odoo **Activity** for the employee's direct manager (`parent_id`) when a change is detected.
- **Notification Message**: The activity will contain the message: "El empleado [Nombre] ha cambiado la fecha del teletrabajo, por favor entre a validar los cambios."
- **Target Audience**: Notifications must be sent **only** to the direct manager (`parent_id`) assigned to the employee record.

## Technical Requirements

- **State Transition**: Ensure the `telework_state` is set back to `draft` when a change occurs.
- **Activity Generation**: Use Odoo's `mail.activity` model to create the notification for the manager.
- **Manager Association**: Correctly resolve the `user_id` of the `parent_id` (employee's manager) to assign the activity.

## Acceptance Criteria

- [ ] Changing a telework day (e.g., Monday from Office to Home) creates a new activity for the employee's manager.
- [ ] The activity message includes the employee's name.
- [ ] No activity is created if the change is made by the manager themselves (optional, but recommended for clarity).
- [ ] The activity appears in the manager's Odoo dashboard/chatter.
