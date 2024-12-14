# Print-On-Demand E-commerce Project

This is a Django-based e-commerce application for a Print-On-Demand platform. The platform allows sellers to register, log in, and upload their products, while customers can browse, register, and purchase items.

---

## Directory Structure

### Root Directory
- **env/**: Contains the virtual environment (not included in the repository as per `.gitignore`).
- **db.sqlite3**: The SQLite database file for local development.
- **manage.py**: The main Django management script for running the project.
- **requirements.txt**: Contains the Python dependencies for the project.
- **.gitignore**: Specifies files and folders to exclude from version control.

### `PrintOnDemand/` (Main Project Directory)
- **`__init__.py`**: Marks this directory as a Python package.
- **asgi.py**: ASGI configuration for the project.
- **settings.py**: Django settings for the project, including installed apps, database configuration, and middleware.
- **urls.py**: Root URL configuration for the project.
- **wsgi.py**: WSGI configuration for the project.

### `e_commerce/` (Main App Directory)
- **`__init__.py`**: Marks this directory as a Python package.
- **admin.py**: Admin site configurations for the app.
- **apps.py**: App configuration for `e_commerce`.
- **forms.py**: Contains Django forms used for user registration and product handling.
- **models.py**: Defines the database models for categories, products, and users.
- **tests.py**: Placeholder for app-specific tests.
- **urls.py**: URL patterns for the `e_commerce` app.
- **views.py**: Contains the view functions and logic for the application.

#### Subdirectories:
- **migrations/**: Contains database migration files.
- **templates/**: Contains HTML templates for the application.
- **static/**: Contains static files like CSS, JavaScript, and images.

---

## Features

### Seller
- Register as a seller.
- Log in as a seller.
- Add, update, or remove products.
- Manage inventory and track product details.

### Customer
- Browse available products.
- Register and log in as a customer.
- Add products to the cart and checkout.

---

## Installation and Setup

### Prerequisites
- Python 3.8 or above
- Django 4.x
- SQLite (default database)
- Virtual environment setup (recommended)

### Installation Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Print-On-Demand
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use env\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the application in your browser:
   ```text
   http://127.0.0.1:8000/
   ```

---

## Usage

1. **Sellers:**
   - Use the seller-specific pages to register and log in.
   - Navigate to the "Add Product" page to upload your products.

2. **Customers:**
   - Use the customer registration page to create an account.
   - Browse products and add them to your cart.

---

## Contributing

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Added new feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).