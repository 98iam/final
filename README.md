# Inventory Management System

A Django-based inventory management system that helps track products, categories, and stock levels with advanced analytics, customizable dashboards, and AI-powered assistance.

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
- Export functionality (CSV, Excel, PDF)
- Dashboard widget customization
- AI Assistant for natural language inventory queries

## Tech Stack

- Python 3.12
- Django 5.2
- PostgreSQL (Supabase)
- Bootstrap 5.3
- Font Awesome 6.0
- Chart.js for data visualization
- Google Gemini API for AI assistance

## Installation

1. Clone the repository:
```bash
git clone https://github.com/98iam/final.git
cd final
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

4. Create a `.env` file in the project root and add your API keys:
```
GOOGLE_GEMINI_API_KEY=your_gemini_api_key_here
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
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
- **Data Export**: Export data in various formats (CSV, Excel, PDF)

## User Experience

- **Dark Mode**: Toggle between light and dark themes for comfortable viewing in different environments
- **Responsive Design**: Works well on desktop and mobile devices
- **User-specific Data**: Each user sees only their own inventory and analytics data
- **Dashboard Customization**: Drag-and-drop interface to reorder and toggle dashboard widgets
- **Personalized Settings**: User preferences are saved and applied across sessions
- **User Profile Management**: Update personal information, profile picture, and account preferences
- **Notification Preferences**: Configure email notifications for low stock alerts and order updates
- **Security Settings**: Change password and manage account security

## AI Assistant

- **Natural Language Queries**: Ask questions about your inventory in plain English
- **Inventory Insights**: Get quick answers about stock levels, sales, and product information
- **Accessible Interface**: Available from any page via a convenient sidebar
- **Powered by Google Gemini**: Utilizes Google's advanced AI model for accurate responses

## License

[MIT](https://choosealicense.com/licenses/mit/)
