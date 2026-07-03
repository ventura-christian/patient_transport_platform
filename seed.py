"""
One-time script to load sample data for demos and grading.

Run this after `alembic upgrade head` and before starting the server:

    python seed.py

Safe to run more than once. The script checks for existing rows first,
so it won't create duplicates on a second run.
"""

from app.database.session import SessionLocal
from app.models.transporter import Transporter
from app.models.transport_request import TransportRequest

SAMPLE_TRANSPORTERS = [
    'Tessa Etzioni',
    'Christian Ventura',
    'Zack De La Rocha',
    'Les Claypool',
    'Andrew Reynolds',
    'Jeff Grosso',
    'Steve Jobs',
    'Guido Van Rossum',
    'Oliver Tree',
    'Darrell Abbott',
    'Alfred Ventura',
    'Linus Torvalds',
    'Tony Alva',
    'Jay Adams',
]

SAMPLE_REQUESTS = [
    {
        'patient_name': 'Patient A',
        'origin_department': 'ICU',
        'origin_room': '4',
        'destination_department': 'Radiology',
        'equipment_needed': 'Wheelchair',
        'biohazard': False,
        'transporters_required': 1,
    },
    {
        'patient_name': 'Patient B',
        'origin_department': 'ER',
        'origin_room': '2',
        'destination_department': 'Surgery',
        'equipment_needed': 'Stretcher',
        'biohazard': True,
        'transporters_required': 1,
    },
    {
        'patient_name': 'Patient C',
        'origin_department': 'Cardiology',
        'origin_room': '7',
        'destination_department': 'ICU',
        'equipment_needed': None,
        'biohazard': False,
        'transporters_required': 1,
    },
]


def run():
    db = SessionLocal()
    try:
        if db.query(Transporter).count() == 0:
            for name in SAMPLE_TRANSPORTERS:
                db.add(Transporter(name=name))
            print(f'Added {len(SAMPLE_TRANSPORTERS)} transporters.')
        else:
            print('Transporters already exist, skipping.')

        if db.query(TransportRequest).count() == 0:
            for data in SAMPLE_REQUESTS:
                db.add(TransportRequest(**data))
            print(f'Added {len(SAMPLE_REQUESTS)} transport requests.')
        else:
            print('Transport requests already exist, skipping.')

        db.commit()
    finally:
        db.close()


if __name__ == '__main__':
    run()
