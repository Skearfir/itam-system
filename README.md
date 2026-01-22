# ITAM - IT Asset Management System

Open source IT asset management for small IT teams.

## Why This Exists

I built this because I got tired of managing 550+ laptops in Excel.

## Philosophy

**Money shouldn't stop you** from having good tools.

## [Future] Features

- ✅ Machine inventory (Dell, Lenovo, Chromebook, etc.)
- ✅ User management (link to employees)
- ✅ Assignment tracking (who has what, when)
- ✅ Complete history (every machine, every user, every assignment)
- ✅ Document generation (government forms, receipts)
- ✅ Replacement tracking (5-year policy support)
- ✅ Technician attribution (who did what, when)
- ✅ Compliance monitoring (AD/Intune integration planned)
- ✅ Excel template auto-fill (for government forms)

## Built For

Small IT teams (1-5 people) managing:
- 10-500 machines
- Multiple locations
- Government compliance requirements (Free Zone, etc.)
- Manual processes that need automation

## Tech Stack

- Python 3.11+
- Flask (web framework)
- SQLite (database - upgradable to PostgreSQL)
- openpyxl (Excel file handling)

## Installation

```bash
# Clone the repo
git clone https://github.com/skearfir/itam-system.git
cd itam-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python database.py

# Run the app
python app.py
```

Visit: http://localhost:5000

## Current Status

🚧 **In Development** - MVP Phase

Started: December 2025  
Target: Working system by Q2 2026  

## Roadmap

**Phase 1: Core ITAM (Current)**
- [ ] Database schema
- [ ] Basic web interface
- [ ] Machine CRUD
- [ ] User CRUD
- [ ] Assignment tracking

**Phase 2: Documents & Reports**
- [ ] Excel template auto-fill
- [ ] Government form generation
- [ ] Return receipts
- [ ] Reports (stock, compliance, replacements)

**Phase 3: Integrations**
- [ ] Active Directory sync
- [ ] Intune compliance checking
- [ ] Email notifications
- [ ] Brand warranty API

**Phase 4: Advanced Features**
- [ ] Multi-tenant support
- [ ] Role-based access
- [ ] API for automation
- [ ] Mobile-responsive design

## Contributing

Not accepting contributions yet (MVP in progress).

Once stable, contributions welcome!

## License

MIT License - Free for commercial and personal use.

## Support

This is open source software. No official support, but:
- GitHub Issues for bug reports
- Discussions for questions
- Community Discord (coming soon)

## Author

Built by someone who actually does IT asset management for a living.

7+ years managing assets in Excel → Finally built the tool I wished existed.

## Philosophy

> "If someone wants to do it themselves... sure... money shouldn't stop you."

- Core software: **Free forever** (open source)
- Installation help: (coming later)
- Customization: (coming later)
- Hosting: DIY or use our hosted version (coming later)

Everyone deserves good tools. 