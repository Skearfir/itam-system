from app import create_app, db
from app.models import Department, User, Asset, Assignment, HistoryEvent
from datetime import date, datetime

app = create_app()

with app.app_context():
    # Clear existing data (for testing)
    print("Clearing existing data...")
    db.drop_all()
    db.create_all()

    # Create departments
    print("Creating departments...")
    it_dept = Department(
        name='IT',
        max_machines_allowed=2,
        description='Information Technology Department'
    )
    finance_dept = Department(
        name='Finance',
        max_machines_allowed=1,
        description='Finance Department'
    )
    design_dept = Department(
        name='Design',
        max_machines_allowed=2,
        description='Design Department - requires dual monitors'
    )

    db.session.add_all([it_dept, finance_dept, design_dept])
    db.session.commit()

    # Create users
    print("Creating users...")
    maria = User(
        employee_id='EMP001',
        full_name='Maria Rodriguez',
        email='maria.rodriguez@company.com',
        department_id=it_dept.id,
        date_of_hire=date(2020, 1, 15),
        employment_status='Active',
        manager='John Smith'
    )

    john = User(
        employee_id='EMP002',
        full_name='John Doe',
        email='john.doe@company.com',
        department_id=finance_dept.id,
        date_of_hire=date(2022, 3, 1),
        employment_status='Active'
    )

    db.session.add_all([maria, john])
    db.session.commit()

    # Create assets
    print("Creating assets...")
    laptop1 = Asset(
        service_tag='ABC12345',
        brand='Dell',
        model='Latitude 5420',
        asset_tag_internal='CR-2025-001',
        current_status='Permanent',  # Will be assigned to Maria
        warranty_expiry=date(2027, 1, 15),
        in_house=False
    )

    laptop2 = Asset(
        service_tag='DEF67890',
        brand='Lenovo',
        model='ThinkPad T14',
        asset_tag_internal='CR-2025-002',
        asset_tag_us='US-12345',
        current_status='Stock',
        warranty_expiry=date(2026, 6, 30),
        in_house=True,
        storage_location='Shelf A3, Box #12'
    )

    laptop3 = Asset(
        service_tag='GHI11111',
        brand='Dell',
        model='Latitude 7420',
        asset_tag_internal='CR-2025-003',
        current_status='Faulty',
        warranty_expiry=date(2027, 12, 31),
        in_house=True,
        faulty_sub_status='Awaiting DPS dispatch - won\'t boot',
        faulty_since_date=date(2025, 1, 15),
        currently_in_repair=False
    )

    db.session.add_all([laptop1, laptop2, laptop3])
    db.session.commit()

    # Create an assignment
    print("Creating assignment...")
    assignment1 = Assignment(
        service_tag='ABC12345',
        employee_id='EMP001',
        assignment_type='Permanent',
        assigned_date=date(2020, 1, 15),
        hostname='SJO-ABC12345',
        created_by='Admin'
    )

    db.session.add(assignment1)
    db.session.commit()  # Commit FIRST so relationships load

    # NOW generate AD description after commit
    assignment1.ad_description = assignment1.generate_ad_description()
    db.session.commit()  # Commit the updated description

    # Create history events
    print("Creating history events...")
    history1 = HistoryEvent(
        service_tag='ABC12345',
        employee_id='EMP001',
        event_type='Assignment',
        event_date=date(2020, 1, 15),
        technician='Admin',
        from_status='Stock',
        to_status='Permanent',
        notes='Initial assignment - original machine for new hire'
    )

    history2 = HistoryEvent(
        service_tag='GHI11111',
        event_type='Status Change',
        event_date=date(2025, 1, 15),
        technician='Maria Rodriguez',
        from_status='Permanent',
        to_status='Faulty',
        notes='Machine won\'t boot - suspected motherboard failure'
    )

    db.session.add_all([history1, history2])
    db.session.commit()

    # Print summary
    print("\n" + "=" * 60)
    print("✅ Sample data created successfully!")
    print("=" * 60)
    print(f"Departments: {Department.query.count()}")
    print(f"Users: {User.query.count()}")
    print(f"Assets: {Asset.query.count()}")
    print(f"Assignments: {Assignment.query.count()}")
    print(f"History Events: {HistoryEvent.query.count()}")

    print("\n" + "=" * 60)
    print("Sample queries:")
    print("=" * 60)

    # Test queries
    print(f"\n1. Maria's active assignments: {maria.active_assignments_count}")
    print(f"2. Laptop ABC12345 repair count: {laptop1.total_repair_count}")
    print(f"3. Assignment is original machine: {assignment1.is_original_machine}")
    print(f"4. Replacement due date: {assignment1.replacement_due_date}")
    print(f"5. Faulty machines: {Asset.query.filter_by(current_status='Faulty').count()}")
    print(f"6. Machines in stock: {Asset.query.filter_by(current_status='Stock').count()}")

    print("\n" + "=" * 60)
    print("Asset Details:")
    print("=" * 60)
    for asset in Asset.query.all():
        print(f"\n{asset.service_tag} - {asset.brand} {asset.model}")
        print(f"  Status: {asset.current_status}")
        print(f"  In House: {asset.in_house}")
        if asset.storage_location:
            print(f"  Location: {asset.storage_location}")
        if asset.current_assignment:
            print(f"  Assigned to: {asset.current_assignment.user.full_name}")

    print("\n" + "=" * 60)
    print("Ready to start building the UI! 🚀")
    print("=" * 60)