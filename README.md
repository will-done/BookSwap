# BookSwap📚 Book Exchange Application

This project is a web-based platform that allows users to exchange books with each other. Users can list their own books, browse books added by others, and send trade offers. It's designed to promote the circulation of books through a simple and user-friendly interface.

---

## ✨ Features

### 👤 User Functionality
- User registration, login, and logout
- Each user can manage their own books
- Only authenticated users can send or receive trade offers

### 📘 Book Management
- Add books with a title, description, cover image, and categories
- Rich text support for book descriptions
- Books can be marked as active/inactive and optionally shown on the homepage

### 🧩 Category System
- Books can be tagged under one or more categories
- Filter books by category via the user interface

### 🔎 Search Capability
- Users can search books by title
- A search term filters books accordingly

### 🔁 Trade System
- Users can offer their own books in exchange for others’ books
- Received offers can be accepted or rejected
- Trade status is tracked and labeled as "Pending", "Accepted", or "Rejected"

### 🛡️ Admin Panel
- Admin can approve or deactivate books
- Books appear on the homepage only if approved and marked accordingly

---

## 📸 Screenshots

### 🏠 Homepage
![Homepage](screenshots/home-page.png)

### ➕ Add a New Book
![Add Book](screenshots/add-book.png)

### 🔁 Trade Offer Page
![All Trade Offers](screenshots/all-trade-offers.png)

### 🏠 Register
![Register](screenshots/register.png)

### ➕ Login
![Login](screenshots/login.png)

### 🔁 My Trade Offer Page
![My Trade Offer](screenshots/my-trade-offer.png)

### 🏠 Book Details
![Book Details](screenshots/book-details.png)

### ➕ Book Search
![Book Search](screenshots/book-search.png)


---

## 🧱 Project Structure
bookstore/
├── book/ # App containing book and trade logic
├── bookstore/ # Project configuration and settings
├── templates/ # HTML templates
│ └── book/
├── static/ # Static files (CSS, JS, icons)
├── media/ # Uploaded book cover images
└── db.sqlite3 # SQLite database (for development)

---

## 📌 Notes

- Built with Django (backend) and Bootstrap 5 (frontend)
- Designed for personal book exchange and hobbyist use
- Uses SQLite for simplicity in development

---
