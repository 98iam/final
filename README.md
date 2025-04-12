# Inventory Management System

A Django-based inventory management system that helps track products, categories, and stock levels.

## Features

- Product management with detailed information
- Category organization
- Stock level tracking with status indicators
- Admin interface for easy management
- Secure authentication system with Supabase integration
- Multi-user support with data isolation
- Dashboard analytics with interactive charts
- Dark mode support for better visibility
- Customizable reports

## Tech Stack

- Python 3.12
- Django 5.2
- PostgreSQL (Supabase)
- Bootstrap 5.3
- Font Awesome 6.0
- Chart.js for data visualization

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

## Analytics Features

The system includes comprehensive analytics capabilities:

- **Sales Trends**: Interactive charts showing sales over time (daily, weekly, monthly)
- **Inventory Value Tracking**: Monitor how your inventory value changes over time
- **Product Performance Metrics**: Identify your best and worst-selling products
- **Customizable Reports**: Create and save custom reports for your specific needs

## User Experience

- **Dark Mode**: Toggle between light and dark themes for comfortable viewing in different environments
- **Responsive Design**: Works well on desktop and mobile devices
- **User-specific Data**: Each user sees only their own inventory and analytics data

## License

[MIT](https://choosealicense.com/licenses/mit/)
