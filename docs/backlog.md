# BACKLOG

> Last Updated: July 2, 2026

## Up Next

- (Potential Idea) Dashboard delayed panel, derived from time in queue
- Transporter Staff panel: show current assignment for on_job transporters
- Fill out docs/testing_checklist.md for Transport Requests and Assignments
- Fix README.md Running Locally section (missing database-creation step)
- Pin requirements.txt to known-working versions
- Presentation materials

## Known Technical Debt

- Status values enforced in app code only, not at the database level
- No authentication
- No real-time updates
- Cascade behavior on foreign key deletes not defined
- Department names are free text with no validation
- Dashboard computes per-request assignment counts with one query per row, not a single join
