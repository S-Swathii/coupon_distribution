# coupon_distribution
Round-Robin Coupon Distribution with Admin Panel
💡 Project Overview
This web application distributes coupons to guest users in a round-robin manner while providing an admin panel for managing coupons and preventing abuse.

🌟 Features
Coupon Distribution:

Assigns coupons to users without repetition.
Ensures sequential distribution.
Guest User Access:

Users can claim coupons without logging in.
Abuse Prevention:

Tracks IP and browser sessions to prevent multiple claims.
Implements a cooldown period to avoid abuse.
Admin Panel:

Secure login for admin access.
View, add, update, and delete coupons.
Monitor user claim history and toggle coupon availability.
User Feedback:

Displays messages for successful claims or cooldown restrictions.
Live Deployment:

Hosted application with a public URL.
🛠️ Tech Stack
Frontend: React, Tailwind CSS, Axios
Backend: Django, Django REST Framework
Database: MySQL
Deployment: AWS/Heroku for Backend, Vercel/Netlify for Frontend
