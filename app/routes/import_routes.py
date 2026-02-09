from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import pandas as pd
import os
import re
from werkzeug.utils import secure_filename
from app import db
from app.models import Asset, User, Department, Assignment, HistoryEvent
from datetime import datetime, date

import_bp = Blueprint('import_bp', __name__)

ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
UPLOAD_FOLDER = 'uploads'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def sanitize_column_name(col):
    """Make column name safe for HTML form fields"""
    return re.sub(r'[^a-zA-Z0-9_]', '_', str(col))


def parse_date(value):
    """Try to parse various date formats"""
    if pd.isna(value) or value == '' or value == 'N/A':
        return None
    if isinstance(value, (datetime, date)):
        return value.date() if isinstance(value, datetime) else value
    try:
        return pd.to_datetime(value).date()
    except:
        return None


def clean_value(value):
    """Clean cell values"""
    if pd.isna(value):
        return None
    if isinstance(value, str):
        value = value.strip()
        if value.upper() in ['N/A', 'NA', '', '#REF!', '#N/A']:
            return None
    return value


@import_bp.route('/import', methods=['GET'])
def import_page():
    """Show the import upload page"""
    return render_template('import.html')


@import_bp.route('/import/upload', methods=['POST'])
def upload_file():
    """Handle file upload and show column mapping"""
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('import_bp.import_page'))

    file = request.files['file']

    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('import_bp.import_page'))

    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload CSV or Excel (.xlsx, .xls)', 'error')
        return redirect(url_for('import_bp.import_page'))

    # Create uploads folder if needed
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Save file temporarily
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Read the file
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)
    except Exception as e:
        flash(f'Error reading file: {str(e)}', 'error')
        return redirect(url_for('import_bp.import_page'))

    # Store filepath in session for later
    session['import_filepath'] = filepath
    session['import_filename'] = filename

    # Get column names from uploaded file
    columns = df.columns.tolist()

    # ITAM fields that can be mapped
    itam_fields = [
        {'name': 'skip', 'label': '-- Skip this column --'},
        {'name': 'custom_field', 'label': '✨ Keep as Custom Field'},  # ✅ NEW OPTION
        {'name': 'service_tag', 'label': 'Service Tag (Required)', 'required': True},
        {'name': 'brand', 'label': 'Brand/Make'},
        {'name': 'model', 'label': 'Model'},
        {'name': 'hostname', 'label': 'Hostname'},
        {'name': 'country', 'label': 'Country'},
        {'name': 'city', 'label': 'City'},
        {'name': 'location_code', 'label': 'Location/Office Code (SJO, NYC, etc.)'},
        {'name': 'company_asset_tag', 'label': 'Primary Asset Tag (e.g., Local Tag)'},
        {'name': 'secondary_asset_tag', 'label': 'Secondary Asset Tag (e.g., International Tag)'},
        {'name': 'current_status', 'label': 'Status (Permanent/Stock/Faulty/etc.)'},
        {'name': 'warranty_expiry', 'label': 'Warranty Expiry Date'},
        {'name': 'assigned_to', 'label': 'Assigned To (Username)'},
        {'name': 'employee_id', 'label': 'Employee ID'},
        {'name': 'email', 'label': 'Email Address'},
        {'name': 'department', 'label': 'Department'},
        {'name': 'assignment_date', 'label': 'Assignment Date'},
        {'name': 'date_of_hire', 'label': 'Employee Hire Date'},
        {'name': 'ram_gb', 'label': 'RAM (GB)'},
        {'name': 'storage_info', 'label': 'Storage/HDD'},
        {'name': 'processor', 'label': 'Processor'},
        {'name': 'notes', 'label': 'Notes/Remarks'},
    ]

    # Try to auto-match columns
    auto_mapping = {}
    for col in columns:
        col_lower = col.lower().strip()
        if 'serial' in col_lower or 'service tag' in col_lower:
            auto_mapping[col] = 'service_tag'
        elif col_lower in ['make', 'brand', 'mater']:
            auto_mapping[col] = 'brand'
        elif col_lower == 'model':
            auto_mapping[col] = 'model'
        elif 'hostname' in col_lower:
            auto_mapping[col] = 'hostname'
        elif 'country' in col_lower:
            auto_mapping[col] = 'country'
        elif 'city' in col_lower:
            auto_mapping[col] = 'city'
        elif 'location' in col_lower or 'office' in col_lower:
            auto_mapping[col] = 'location_code'
        elif 'gep asset tag' in col_lower or 'asset tag' in col_lower:
            auto_mapping[col] = 'company_asset_tag'
        elif 'us gep' in col_lower or 'secondary' in col_lower:
            auto_mapping[col] = 'secondary_asset_tag'
        elif 'allotment' in col_lower or 'status' in col_lower:
            auto_mapping[col] = 'current_status'
        elif 'warranty' in col_lower:
            auto_mapping[col] = 'warranty_expiry'
        elif 'username' in col_lower or 'assigned to' in col_lower or 'user' in col_lower:
            auto_mapping[col] = 'assigned_to'
        elif 'employee id' in col_lower or 'zoho' in col_lower:
            auto_mapping[col] = 'employee_id'
        elif 'email' in col_lower or 'e-mail' in col_lower or 'mail' in col_lower:
            auto_mapping[col] = 'email'
        elif 'department' in col_lower:
            auto_mapping[col] = 'department'
        elif 'assigned date' in col_lower:
            auto_mapping[col] = 'assignment_date'
        elif 'hire' in col_lower:
            auto_mapping[col] = 'date_of_hire'
        elif col_lower == 'ram':
            auto_mapping[col] = 'ram_gb'
        elif col_lower in ['hdd', 'storage', 'ssd']:
            auto_mapping[col] = 'storage_info'
        elif 'processor' in col_lower or 'cpu' in col_lower:
            auto_mapping[col] = 'processor'
        elif 'remark' in col_lower or 'note' in col_lower or 'comment' in col_lower:
            auto_mapping[col] = 'notes'
        else:
            # ✅ CHANGED: Default unmapped columns to custom_field instead of skip
            auto_mapping[col] = 'custom_field'

    # Preview first 5 rows
    preview_data = df.head(5).fillna('').to_dict('records')

    # Create safe column mapping for form fields
    column_mapping = {col: sanitize_column_name(col) for col in columns}

    return render_template('import_mapping.html',
                           columns=columns,
                           column_mapping=column_mapping,
                           itam_fields=itam_fields,
                           auto_mapping=auto_mapping,
                           preview_data=preview_data,
                           total_rows=len(df))


@import_bp.route('/import/process', methods=['POST'])
def process_import():
    """Process the mapped import"""
    print("=== IMPORT PROCESS STARTED ===", flush=True)

    filepath = session.get('import_filepath')
    print(f"Filepath from session: {filepath}", flush=True)

    if not filepath or not os.path.exists(filepath):
        flash('Session expired. Please upload file again.', 'error')
        return redirect(url_for('import_bp.import_page'))

    # Read file again
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)

    print(f"File read successfully, {len(df)} rows", flush=True)

    # Get mapping from form (using sanitized column names)
    mapping = {}
    custom_field_columns = []  # ✅ NEW: Track columns for custom fields

    for col in df.columns:
        safe_col = sanitize_column_name(col)
        field = request.form.get(f'mapping_{safe_col}')
        if field == 'custom_field':  # ✅ NEW: Collect custom field columns
            custom_field_columns.append(col)
        elif field and field != 'skip':
            mapping[col] = field

    print(f"Standard mapping: {mapping}")
    print(f"Custom field columns: {custom_field_columns}")  # ✅ NEW

    # Check required field
    if 'service_tag' not in mapping.values():
        flash('Service Tag mapping is required!', 'error')
        return redirect(url_for('import_bp.import_page'))

    # Get import options
    duplicate_action = request.form.get('duplicate_action', 'skip')
    create_users = request.form.get('create_users') == 'on'
    create_departments = request.form.get('create_departments') == 'on'

    # Reverse mapping (itam_field -> excel_column)
    field_to_col = {v: k for k, v in mapping.items()}

    # Track results
    results = {
        'assets_created': 0,
        'assets_updated': 0,
        'assets_skipped': 0,
        'users_created': 0,
        'departments_created': 0,
        'errors': []
    }

    # Ensure "Unknown" department exists BEFORE processing
    unknown_dept = None
    if create_departments or create_users:
        unknown_dept = Department.query.filter_by(name='Unknown').first()
        if not unknown_dept:
            unknown_dept = Department(name='Unknown')
            db.session.add(unknown_dept)
            try:
                db.session.commit()
                print("Created 'Unknown' department")
            except Exception as e:
                db.session.rollback()
                flash(f'Failed to create Unknown department: {str(e)}', 'error')
                return redirect(url_for('import_bp.import_page'))

    # Process each row
    for index, row in df.iterrows():
        try:
            # Get service tag (required)
            service_tag_col = field_to_col.get('service_tag')
            service_tag = clean_value(row[service_tag_col])

            if not service_tag:
                results['errors'].append(f"Row {index + 2}: Missing service tag, skipped")
                results['assets_skipped'] += 1
                continue

            # Check if asset exists
            existing_asset = Asset.query.get(service_tag)

            if existing_asset and duplicate_action == 'skip':
                results['assets_skipped'] += 1
                continue

            # Handle department
            department = unknown_dept
            if 'department' in field_to_col:
                dept_name = clean_value(row[field_to_col['department']])
                if dept_name and create_departments:
                    department = Department.query.filter_by(name=dept_name).first()
                    if not department:
                        department = Department(name=dept_name)
                        db.session.add(department)
                        db.session.flush()
                        results['departments_created'] += 1

            # Handle user
            user = None
            if 'assigned_to' in field_to_col:
                username = clean_value(row[field_to_col['assigned_to']])

                excluded_values = [
                    'N/A', 'IT STOCK', 'STOCK', 'EWASTE', 'E-WASTE', 'SCRAP',
                    'STOLEN', 'TO BE SCRAPPED', 'TO BE SCRAP', 'FAULTY',
                    'WAREHOUSE', 'DISPOSAL', 'LOST', 'DAMAGED', 'BROKEN',
                    'RESERVE', 'RESERVED', 'UNASSIGNED', 'AVAILABLE'
                ]

                if username and username.upper() not in excluded_values:
                    if create_users:
                        employee_id_from_csv = None
                        if 'employee_id' in field_to_col:
                            employee_id_from_csv = clean_value(row[field_to_col['employee_id']])

                        hire_date = None
                        if 'date_of_hire' in field_to_col:
                            hire_date = parse_date(row[field_to_col['date_of_hire']])

                        if employee_id_from_csv:
                            user = User.query.filter_by(employee_id=employee_id_from_csv).first()

                        if not user:
                            user = User.query.filter_by(full_name=username).first()

                        if not user:
                            final_employee_id = employee_id_from_csv if employee_id_from_csv else f"IMPORT_{index}"

                            email_from_csv = None
                            if 'email' in field_to_col:
                                email_from_csv = clean_value(row[field_to_col['email']])

                            if email_from_csv:
                                email = email_from_csv.lower().strip()
                            else:
                                base_email = (employee_id_from_csv or f"import_{index}").lower().replace(' ', '_')
                                email = f"{base_email}@imported.local"

                            counter = 0
                            original_email = email
                            while User.query.filter_by(email=email).first():
                                counter += 1
                                email_parts = original_email.split('@')
                                email = f"{email_parts[0]}_{counter}@{email_parts[1]}"

                            user = User(
                                employee_id=final_employee_id,
                                full_name=username,
                                email=email,
                                department_id=department.id,
                                date_of_hire=hire_date or date.today(),
                                employment_status='Active'
                            )
                            db.session.add(user)
                            db.session.flush()
                            results['users_created'] += 1
                            print(f"Created user: {username} (ID: {final_employee_id}, Email: {email})", flush=True)

            # Map status values
            status = 'Stock'
            if 'current_status' in field_to_col:
                raw_status = clean_value(row[field_to_col['current_status']])
                if raw_status:
                    status_map = {
                        'permanent': 'Permanent',
                        'temporary': 'Temporary',
                        'stock': 'Stock',
                        'faulty': 'Faulty',
                        'stolen': 'Stolen',
                        'ewaste': 'Scrap',
                        'scrap': 'Scrap',
                        'to be scrapped': 'Scrap',
                        'box package': 'Box Package',
                        'in use': 'Permanent'
                    }
                    status = status_map.get(raw_status.lower(), raw_status)

            # ✅ NEW: Collect custom fields from row
            custom_fields_data = {}
            for col in custom_field_columns:
                value = clean_value(row[col])
                if value is not None:  # Only store non-null values
                    custom_fields_data[col] = str(value)  # Convert to string for JSON

            print(f"Row {index + 2} custom fields: {custom_fields_data}", flush=True)

            # Build asset data
            asset_data = {
                'service_tag': service_tag,
                'brand': clean_value(row[field_to_col['brand']]) if 'brand' in field_to_col else None,
                'model': clean_value(row[field_to_col['model']]) if 'model' in field_to_col else None,
                'asset_tag_internal': clean_value(
                    row[field_to_col['company_asset_tag']]) if 'company_asset_tag' in field_to_col else None,
                'asset_tag_us': clean_value(
                    row[field_to_col['secondary_asset_tag']]) if 'secondary_asset_tag' in field_to_col else None,
                'current_status': status,
                'warranty_expiry': parse_date(
                    row[field_to_col['warranty_expiry']]) if 'warranty_expiry' in field_to_col else None,
                'in_house': status in ['Stock', 'Box Package', 'Faulty'],
                'custom_fields': custom_fields_data,  # ✅ NEW: Add custom fields
            }

            if existing_asset and duplicate_action == 'update':
                # Update existing
                for key, value in asset_data.items():
                    if value is not None or key == 'custom_fields':  # Always update custom_fields even if empty
                        setattr(existing_asset, key, value)
                results['assets_updated'] += 1
            else:
                # Create new
                asset = Asset(**asset_data)
                db.session.add(asset)
                db.session.flush()
                results['assets_created'] += 1

                # Create assignment if user exists and status is Permanent/Temporary
                if user and status in ['Permanent', 'Temporary']:
                    assignment_date = None
                    if 'assignment_date' in field_to_col:
                        assignment_date = parse_date(row[field_to_col['assignment_date']])

                    assignment = Assignment(
                        service_tag=service_tag,
                        employee_id=user.employee_id,
                        assignment_type=status,
                        assigned_date=assignment_date or date.today(),
                    )
                    db.session.add(assignment)

                # Create history event
                history = HistoryEvent(
                    service_tag=service_tag,
                    event_type='Import',
                    event_date=date.today(),
                    technician='System Import',
                    notes=f"Imported from {session.get('import_filename', 'file')}"
                )
                db.session.add(history)

        except Exception as e:
            db.session.rollback()
            error_msg = f"Row {index + 2}: {str(e)}"
            results['errors'].append(error_msg)
            print(f"ERROR: {error_msg}", flush=True)
            continue

    # Commit all changes
    try:
        db.session.commit()
        print("Database commit successful!")
    except Exception as e:
        db.session.rollback()
        print(f"Database error: {str(e)}")
        flash(f'Database error: {str(e)}', 'error')
        return redirect(url_for('import_bp.import_page'))

    # Clean up temp file
    try:
        os.remove(filepath)
    except:
        pass

    # Clear session
    session.pop('import_filepath', None)
    session.pop('import_filename', None)

    print(f"=== IMPORT COMPLETE ===")
    print(
        f"Created: {results['assets_created']}, Updated: {results['assets_updated']}, Skipped: {results['assets_skipped']}, Errors: {len(results['errors'])}")

    return render_template('import_results.html', results=results)


@import_bp.route('/import/template')
def download_template():
    """Download a CSV template"""
    from flask import Response

    template_data = """Service Tag,Brand,Model,Internal Asset Tag,US Asset Tag,Status,Warranty Expiry,Assigned To,Employee ID,Department
ABC12345,Dell,Latitude 7440,1408-0001,US001,Permanent,2027-01-15,John Smith,EMP001,IT Department
XYZ67890,Lenovo,ThinkPad X1,1408-0002,,Stock,2026-08-20,,,
"""

    return Response(
        template_data,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=itam_import_template.csv'}
    )