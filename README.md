# Coffee Shop API
A REST API for a coffee shop built with FastAPI and SQLite. Supports user registration, login, menu browsing, order creation, and admin routes.

## Features
- User registration and login with bcrypt.
- Menu browsing and order creation.
- View order history (/my_orders).
- Admin route for all orders (/admin/orders).
- Tested via Swagger UI.

## Installation
1. Clone: `git clone https://github.com/your_username/coffee-shop.git && cd coffee-shop`
2. Virtual env: `python -m venv venv && source venv/bin/activate` (Windows: `venv\Scripts\activate`)
3. Install: `pip install -r requirements.txt`
4. Create a `.env` file in the project root with: SECRET_KEY=your_secret_key_here
5. Run: `uvicorn main:app --reload`
6. Open: `http://127.0.0.1:8000/docs`

## Tech Stack
- FastAPI
- SQLite
- SQLAlchemy
- bcrypt
- JWT

## Future Plans
- Optimize SQL queries.
- Add order cancellation.
- Build frontend.

## License
MIT License
