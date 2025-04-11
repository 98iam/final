# Inventory Management System

A Django-based inventory management system that helps track products, categories, and stock levels.

## Features

- Product management with detailed information
- Category organization
- Stock level tracking with status indicators
- Admin interface for easy management
- Secure authentication system with Supabase integration
- Multi-user support with data isolation

## Tech Stack

- Python 3.12
- Django 5.2
- PostgreSQL (Supabase)
- Bootstrap 5.3
- Font Awesome 6.0

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Usage

1. Access the admin interface at `http://localhost:8000/admin`
2. Log in with your credentials
3. Start managing your inventory!

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
