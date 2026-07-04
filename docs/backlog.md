# BACKLOG

> Last Updated: July 4, 2026

## Up Next

- Full manual pass through testing_checklist.md
- Presentation materials

## Known Technical Debt

- Status values enforced in app code only, not at the database level
- No authentication
- No real-time updates
- Cascade behavior on foreign key deletes not defined
- Department names are free text with no validation
- Dashboard computes per-request assignment counts with one query per row, not a single join
