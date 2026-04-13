# Smart Property Hub — Project Explanation

## What Does This Project Do?

Imagine you want to buy a house, an apartment, or some land. You'd usually go to a real estate agent's office, look at photos, and ask lots of questions. This project does all of that — but online!

**Smart Property Hub** is like a virtual real estate office where:
- **Sellers** can put up their properties for sale (like pinning a "For Sale" sign)
- **Buyers** can browse through all available properties, search for specific ones, and book the ones they like
- An **Admin** watches over everything, making sure the platform runs smoothly

Think of it like OLX or MagicBricks, but simpler and built as a student project.

## How Does It Work? (Step by Step)

### Step 1: Creating an Account

When you visit the website, you see a login page. If you don't have an account, you click "Register" and choose whether you want to be a **Seller** (someone who lists properties) or a **Buyer** (someone who wants to buy/rent properties).

There's also a pre-made admin account (username: `admin`, password: `admin123`) that has special powers to manage the entire platform.

### Step 2: What Each Role Can Do

#### Admin (The Manager)
The admin is like the manager of the real estate office. They can:
- See how many users, properties, and bookings exist (the big picture)
- View and delete any user (if someone is misbehaving)
- View and delete any property
- See all bookings made by all buyers

#### Seller (The Property Owner)
A seller is like a landlord who wants to sell or rent out properties. They can:
- **Add a property** — Fill in a form with the property title, type (Apartment, Villa, Plot, Commercial), location, landmark, price (in Lakhs ₹), number of bedrooms/bathrooms, area in square feet, amenities (like Pool, Gym, Parking), and a description
- **View their listings** — See all properties they've added, with a count of how many people have shown interest (bookings)
- **Edit a property** — Change the price, update the description, mark it as "sold"
- **Delete a property** — Remove it from the platform entirely

#### Buyer (The Property Seeker)
A buyer is like someone house-hunting. They can:
- **Browse all properties** — See a grid of all available properties with photos, prices, and locations
- **Search & filter** — Look for properties by keyword, type (Villa, Apartment), location, price range, or minimum number of bedrooms
- **View property details** — Click on any property to see full details, seller info, and amenities
- **Book a property** — Send a booking request with an optional message (like "I'm interested, can I visit?")
- **View booking history** — See all properties they've booked

### Step 3: The Booking Flow

Here's how a booking works:
1. A buyer browses properties and finds one they like
2. They click "View" to see full details
3. They write a message and click "Book Now"
4. The property's status changes from "Available" to "Booked"
5. The seller can see the booking inquiry when they view that property
6. The admin can see all bookings from their admin panel

### Step 4: The Database

Everything is stored in a database called SQLite (a simple database that lives in a single file). It has 3 tables:

- **users** — Stores usernames, passwords (encrypted!), names, emails, phone numbers, and roles
- **properties** — Stores all property details (title, type, location, price, etc.)
- **bookings** — Stores which buyer booked which property, with a message and status

When the server starts for the first time, it automatically creates:
- 1 admin account
- 2 sample seller accounts
- 8 sample properties (2 Apartments, 2 Villas, 2 Plots, 2 Commercial)

## What Are the Key Technologies?

| Technology | What It Does |
|-----------|-------------|
| **Python** | The programming language everything is written in |
| **Flask** | A web framework that turns Python code into a website (handles pages, forms, logins) |
| **SQLite** | A lightweight database that stores all users, properties, and bookings in one file |
| **Werkzeug** | Encrypts passwords so they're not stored as plain text (security!) |
| **Bootstrap 5** | Makes the website look modern and professional with a dark amber theme |
| **Bootstrap Icons** | Provides little icons (🏠 🔍 👤) for buttons and labels |
| **HTML/CSS/JavaScript** | The basic building blocks of any website |

## What Is Role-Based Access Control (RBAC)?

RBAC means different users see different things and can do different things based on their "role."

Think of it like a school:
- **Principal (Admin)** can see everything — student records, teacher records, attendance
- **Teacher (Seller)** can see and manage their own class, but not other teachers' classes
- **Student (Buyer)** can view their own grades and attendance, but can't change anything

In our project:
- If a **buyer** tries to visit the "Add Property" page, they get kicked back with "Access denied"
- If a **seller** tries to visit the "Admin Users" page, same thing — "Access denied"
- Only the right role can access the right pages

This is implemented using Python "decorators" — special functions that check your role before letting you access a page.

## What Does Each File Do?

| File | Purpose |
|------|---------|\
| `app.py` | The main application — handles all 17 routes, database setup, authentication, and CRUD operations |
| `templates/base.html` | The overall page layout (dark theme with amber #f59e0b accents, navbar, footer) |
| `templates/login.html` | Login page with username/password form |
| `templates/register.html` | Registration page with role selector (Seller or Buyer) |
| `templates/home.html` | Dashboard that shows different content for admin, seller, and buyer |
| `templates/properties.html` | Property listing grid with search bar and filter dropdowns |
| `templates/property_detail.html` | Detailed view of one property with seller info, amenities, and booking form |
| `templates/add_property.html` | Form for sellers to add a new property |
| `templates/edit_property.html` | Form for sellers to edit their existing property |
| `templates/my_properties.html` | Table showing seller's own listed properties |
| `templates/my_bookings.html` | Cards showing buyer's booking history |
| `templates/admin_users.html` | Table of all users with delete buttons (admin only) |
| `templates/admin_bookings.html` | Table of all bookings across the platform (admin only) |
| `templates/about.html` | Information about the project, roles, and technology |
| `static/img/` | Property images and feature photos |
| `static/video/` | Homepage hero video and property showcase video |
| `Dockerfile` | Instructions to run the app in a Docker container |
| `requirements.txt` | List of Python packages needed (flask, werkzeug) |

## How to Run It Yourself

1. Install Python 3.8+
2. Run `pip install -r requirements.txt`
3. Run `python app.py` (starts the website, auto-creates the database)
4. Open http://localhost:5013 in your browser
5. Login with username: `admin`, password: `admin123`
6. Or register as a Seller or Buyer to try those roles

## Why Does This Matter?

- Real estate is one of the largest industries in the world
- Online property platforms save people time — no need to visit every property in person
- Role-based systems are used everywhere — banks, hospitals, schools, e-commerce sites
- This project teaches important concepts: user authentication, CRUD operations, database design, role-based access, search/filter functionality, and responsive web design
- The same architecture (Flask + SQLite + roles) can be adapted for many other types of management systems
