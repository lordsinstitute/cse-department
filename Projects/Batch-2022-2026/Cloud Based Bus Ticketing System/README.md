# B8 — Cloud-Based Comprehensive Bus Ticketing and Reservation System

## Project Structure

```
code/
├── app.py                          # Main Flask application (346 lines)
├── bus_ticketing.db                # SQLite database (auto-created on first run)
├── Dockerfile                      # Docker container configuration
├── .dockerignore                   # Docker ignore file
├── static/                         # Static assets
└── templates/
    ├── base.html                   # Base layout (navbar, Bootstrap 5, flash messages)
    ├── home.html                   # Dynamic home page (Guest / User / Admin views)
    ├── login.html                  # Login page
    ├── register.html               # Registration page
    ├── search.html                 # Bus search with route dropdowns
    ├── book.html                   # Ticket booking form
    ├── my_bookings.html            # User booking history with cancel option
    ├── admin_dashboard.html        # Admin dashboard with stats
    ├── admin_buses.html            # Admin bus fleet management
    ├── admin_bookings.html         # Admin view all bookings
    └── add_bus.html                # Admin add new bus form
```

## Features

- **User Module:** Register, login, search buses, book tickets, view bookings, cancel bookings
- **Admin Module:** Dashboard with stats, manage buses, add buses, view all bookings
- **Route Dropdowns:** Source and destination populated from database
- **Payment Options:** Online (UPI/Card), Net Banking, Digital Wallet, Cash
- **Real-time Seats:** Available seats update instantly after booking/cancellation
- **SQLite Database:** Zero setup, auto-created on first run, persists across restarts
- **10 Pre-loaded Routes:** Hyderabad to Bangalore, Chennai, Mumbai, Goa, Pune, Delhi, etc.
- **Dynamic Home Page:** Different views for Guest, Logged-in User, and Admin

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation Steps (Windows)

**Step 1:** Open Command Prompt and navigate to project

```bash
cd code
```

**Step 2:** Install required packages

```bash
pip install flask
```

**Step 3:** Run the application

```bash
python app.py
```

**Step 4:** Open in browser

```
http://127.0.0.1:5000
```

The SQLite database (`bus_ticketing.db`) is auto-created on first run with an admin user and 10 sample bus routes.

---

## Docker Setup (Windows)

### Prerequisites

- Install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
- Make sure Docker Desktop is running

### Build and Run

**Step 1:** Open Command Prompt and navigate to project

```bash
cd code
```

**Step 2:** Build the Docker image

```bash
docker build -t bus-ticketing .
```

**Step 3:** Run the container

```bash
docker run -d -p 5000:5000 --name bus-app bus-ticketing
```

**Step 4:** Open in browser

```
http://localhost:5000
```

### Docker Management Commands

```bash
# Stop the container
docker stop bus-app

# Start the container again
docker start bus-app

# Remove the container
docker rm -f bus-app

# View logs
docker logs bus-app

# Rebuild after code changes
docker rm -f bus-app
docker build -t bus-ticketing .
docker run -d -p 5000:5000 --name bus-app bus-ticketing
```

---

## Accounts

| Role | Username | Password | Access |
|---|---|---|---|
| Admin | `admin` | `admin123` | Dashboard, Manage Buses, Add Bus, All Bookings |
| User | (register) | (register) | Search, Book, My Bookings, Cancel |

## Pages Overview

| Page | URL | Access | Description |
|---|---|---|---|
| Home | `/` | All | Dynamic home (Guest / User / Admin) |
| Register | `/register` | Guest | Create a new account |
| Login | `/login` | Guest | Login with credentials |
| Search | `/search` | User | Search buses with route dropdowns |
| Book | `/book/<id>` | User | Book tickets for a bus |
| My Bookings | `/my-bookings` | User | View and cancel bookings |
| Admin Dashboard | `/admin` | Admin | Stats and recent bookings |
| Manage Buses | `/admin/buses` | Admin | View all buses |
| Add Bus | `/admin/add-bus` | Admin | Add a new bus route |
| All Bookings | `/admin/bookings` | Admin | View all user bookings |

---

## Quick Start

1. Open browser: `http://127.0.0.1:5000`
2. Click "Register" → Name: `John`, Username: `john`, Password: `pass123`
3. Login with same credentials
4. Search buses: From `Hyderabad` → To `Bangalore`
5. Click **Book Now** → fill details → **Confirm Booking**

---

## Test Cases

### Test Case 1: User Registration and Login

1. Open http://127.0.0.1:5000
2. Click **Register**
3. Fill: Name: `Mohammed`, Username: `mohammed`, Password: `test123`, Email: `mohammed@test.com`, Phone: `9876543210`
4. Click **Register** → redirects to Login
5. Enter `mohammed` / `test123` → Click **Login**

**Expected:** Redirects to Search page. Home page shows personalized welcome.

---

### Test Case 2: Search and Book a Ticket

1. Login as `mohammed` / `test123`
2. Click **Search** in navbar
3. Select From: `Hyderabad`, To: `Bangalore`
4. Click **Search** → "Express Liner" should appear (AC Sleeper, Rs. 850.00)
5. Click **Book Now**
6. Fill: Passenger Name: `Mohammed Ahmed`, Age: `22`, Gender: `Male`, Seats: `2`, Travel Date: any future date, Payment: `Online Payment`
7. Click **Confirm Booking**

**Expected:** "Booking confirmed! 2 seat(s) booked. Total: Rs. 1700.00". Available seats reduced by 2.

---

### Test Case 3: View and Cancel Booking

1. After booking, click **My Bookings** in navbar
2. You should see the booking with all details
3. Click **Cancel** → confirm the cancellation

**Expected:** Status changes to "Cancelled", payment shows "Refunded", seats restored on the bus.

---

### Test Case 4: Admin Dashboard

1. Logout → Login as `admin` / `admin123`
2. Home page shows Admin Control Panel with stats
3. Click **Dashboard** → detailed analytics with recent bookings table
4. Click **Buses** → list of all 10 buses with seat counts
5. Click **All Bookings** → see all user bookings

**Expected:** Stats reflect real data (bookings, revenue, users).

---

### Test Case 5: Admin Add New Bus

1. Login as `admin` / `admin123`
2. Click **Buses** → Click **+ Add Bus**
3. Fill: Bus Number: `TS-11-5555`, Bus Name: `Deccan Queen`, Type: `Volvo AC`, Source: `Hyderabad`, Destination: `Kolkata`, Departure: `15:00`, Arrival: `12:00`, Seats: `40`, Fare: `2200`
4. Click **Add Bus**

**Expected:** "Bus added successfully!" New bus appears in the bus list and in user search results.

---

### Test Case 6: Book Multiple Routes

1. Login as any user
2. Search `Hyderabad` → `Mumbai` → Book 1 seat on "Night Rider" (Rs. 1450)
3. Search `Hyderabad` → `Goa` → Book 3 seats on "Luxury Coach" (Rs. 5400 total)
4. Check **My Bookings** → both bookings visible
5. Login as `admin` → Check **Dashboard** → revenue and booking count updated

**Expected:** Both bookings appear. Admin sees updated stats.

---

### Test Case 7: Guest Home Page

1. Logout or open in incognito browser
2. Visit http://127.0.0.1:5000

**Expected:** Landing page with hero section, live stats, "Why Choose BusBook?" features, "How It Works" 4-step flow, Register/Login buttons.

---

## Pre-loaded Bus Routes

| Bus Number | Bus Name | Type | Route | Time | Seats | Fare |
|---|---|---|---|---|---|---|
| AP-01-1234 | Express Liner | AC Sleeper | Hyderabad → Bangalore | 22:00-06:00 | 40 | Rs. 850 |
| AP-02-5678 | Royal Travels | AC Seater | Hyderabad → Chennai | 20:00-07:00 | 50 | Rs. 950 |
| AP-03-9012 | City Connect | Non-AC Seater | Hyderabad → Vijayawada | 06:00-12:00 | 55 | Rs. 350 |
| AP-04-3456 | Night Rider | AC Sleeper | Hyderabad → Mumbai | 18:00-08:00 | 36 | Rs. 1450 |
| AP-05-7890 | Metro Express | AC Seater | Hyderabad → Pune | 21:00-09:00 | 45 | Rs. 1100 |
| AP-06-2345 | South Star | Non-AC Sleeper | Hyderabad → Tirupati | 22:30-06:30 | 40 | Rs. 550 |
| AP-07-6789 | Green Line | AC Seater | Hyderabad → Warangal | 07:00-11:00 | 50 | Rs. 250 |
| AP-08-0123 | Luxury Coach | Volvo AC | Hyderabad → Goa | 17:00-07:00 | 42 | Rs. 1800 |
| TS-09-4567 | Quick Ride | Non-AC Seater | Hyderabad → Karimnagar | 08:00-12:00 | 55 | Rs. 200 |
| TS-10-8901 | Premium Bus | Volvo AC | Hyderabad → Delhi | 16:00-18:00 | 40 | Rs. 2500 |

## Notes

- SQLite database (`bus_ticketing.db`) is auto-created on first run — no setup needed
- Admin account (`admin`/`admin123`) is seeded automatically
- All 10 bus routes are seeded on first run
- Data persists across server restarts (stored in `.db` file)
- To reset data, simply delete `bus_ticketing.db` and restart the app
