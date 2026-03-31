# Smart Property Hub

A Flask web application for real estate property management with three user roles — Admin, Seller, and Buyer. Sellers can list properties, buyers can browse and book, and admins manage the entire platform.

## Features

- **3 User Roles:** Admin (platform management), Seller (list/manage properties), Buyer (browse/book properties)
- Property listing with details (type, location, price, bedrooms, bathrooms, area, amenities)
- Advanced search with filters (keyword, type, location, price range, bedrooms)
- Property booking system with status tracking (pending, confirmed, cancelled)
- Role-based dashboards with real-time statistics
- User management for administrators
- Responsive dark-themed UI with Bootstrap 5

## Property Types

- Apartment, Villa, Plot, Commercial

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation (Windows)

1. **Clone the repository:**
```bash
git clone <repository-url>
cd code
```

2. **Create a virtual environment (recommended):**
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the application:**
```bash
python app.py
```
Open http://localhost:5013 in your browser.

5. **Login:**
- Admin: `admin` / `admin123`
- Seller: `seller1` / `seller123` or `seller2` / `seller123`
- Or register a new account as Seller or Buyer

## Docker Deployment

```bash
docker build -t smart-property-hub .
docker run -p 5013:5013 smart-property-hub
```

## Project Structure

```
code/
├── app.py                     # Flask app with all routes, DB init, auth, CRUD
├── static/
│   ├── img/                   # Property and feature images
│   │   ├── pic01.jpg, pic02.jpg, pic03.jpg
│   │   ├── cm1.jpg, cm2.jpg, cm3.jpg, cm4.jpg
│   │   ├── cta01.jpg, forestbridge.jpg, bg.jpg
│   └── video/
│       ├── banner.mp4         # Homepage hero video
│       └── props.mp4          # Property showcase video
├── templates/
│   ├── base.html              # Dark theme layout (amber accent)
│   ├── login.html             # Login page
│   ├── register.html          # Register with role selector
│   ├── home.html              # Role-based dashboard
│   ├── properties.html        # Property listing with search/filter
│   ├── property_detail.html   # Single property view + booking
│   ├── add_property.html      # Seller: add property form
│   ├── edit_property.html     # Seller: edit property form
│   ├── my_properties.html     # Seller: own listings
│   ├── my_bookings.html       # Buyer: booking history
│   ├── admin_users.html       # Admin: user management
│   ├── admin_bookings.html    # Admin: all bookings
│   └── about.html             # About the platform
├── Dockerfile
├── requirements.txt
└── .gitignore
```

## User Roles

| Role | Capabilities |
|------|-------------|
| **Admin** | View platform stats, manage all users, manage all properties, view all bookings |
| **Seller** | Add/edit/delete own properties, view booking inquiries on own properties |
| **Buyer** | Browse properties, search with filters, book properties, view booking history |

## Test Cases

1. Register as buyer → redirect to login with success message
2. Register as seller → redirect to login with success message
3. Login as admin/admin123 → admin dashboard with stats (users, properties, bookings)
4. Login as seller → seller dashboard with own properties and booking count
5. Login as buyer → buyer dashboard with available properties and featured listings
6. Seller adds property → appears in listings
7. Seller edits own property → changes saved
8. Seller deletes own property → removed from system
9. Buyer browses properties → grid with search/filter
10. Buyer books available property → booking saved, property status changes to "booked"
11. Buyer views booking history → past bookings shown with details
12. Admin views all users → sellers and buyers listed with role badges
13. Admin deletes a user → user and their data removed
14. Admin views all bookings → all bookings with buyer/seller info
15. Access /add-property as buyer → "Access denied" redirect
16. Access /admin/users as seller → "Access denied" redirect

## Technology Stack

- **Backend:** Python, Flask
- **Database:** SQLite
- **Frontend:** Bootstrap 5, Bootstrap Icons
- **Authentication:** Session-based (Werkzeug password hashing)
