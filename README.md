# 🏢 Employee Management System

[![Django](https://img.shields.io/badge/Django-5.2+-green.svg)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-blue.svg)](https://getbootstrap.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)
[![Last Updated](https://img.shields.io/badge/Updated-July%202025-brightgreen.svg)]()

A modern, responsive Django web application for comprehensive employee management with advanced features and professional UI.

## 🌟 Features

### 📋 Core Functionality
- **CRUD Operations**: Complete Create, Read, Update, Delete for employee records
- **Advanced Search**: Real-time search by name or age
- **Pagination**: Efficient handling of large datasets (10 records per page)
- **Data Validation**: Comprehensive form validation and error handling
- **Responsive Design**: Mobile-first Bootstrap 5 interface

### 🎨 User Interface
- **Professional Design**: Clean, modern interface with Bootstrap 5
- **Intuitive Navigation**: Consistent breadcrumb and navigation system
- **Interactive Elements**: Modal confirmations, loading states, form validation
- **Accessibility**: ARIA labels and keyboard navigation support
- **Mobile Responsive**: Optimized for all device sizes

### ⚡ Performance & Security
- **Database Optimization**: Indexed queries and efficient data retrieval
- **Caching System**: Smart caching for frequently accessed data
- **Security**: CSRF protection, input sanitization, SQL injection prevention
- **Error Handling**: Comprehensive error logging and user-friendly messages
- **Soft Delete**: Data protection with soft delete functionality

### 🔧 Admin Features
- **Enhanced Admin Panel**: Custom admin interface with bulk operations
- **Data Export**: Easy data management and export capabilities
- **User Management**: Role-based access control ready
- **Audit Trail**: Complete logging of all operations

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/employee-management-system.git
   cd employee-management-system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main Application: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## 📱 Usage

### Employee Management
1. **View Employees**: Navigate to the main page to see all employees
2. **Add Employee**: Click "เพิ่มพนักงานใหม่" to add new employee
3. **Edit Employee**: Click the edit button (✏️) next to any employee
4. **Delete Employee**: Click the delete button (🗑️) with confirmation
5. **Search**: Use the search box to find employees by name or age

### Admin Panel
1. Access `/admin/` with superuser credentials
2. Manage employees with advanced filtering and bulk operations
3. View detailed statistics and audit logs

## 🛠️ Technology Stack

- **Backend**: Django 5.2+
- **Frontend**: Bootstrap 5.3, JavaScript (ES6+)
- **Database**: SQLite (development), PostgreSQL/MySQL ready
- **Icons**: Font Awesome 6
- **Styling**: Custom CSS with Bootstrap customization

## 📊 Project Structure

```
MainProject/
├── MainApp/                    # Main application
│   ├── models.py              # Employee model with optimizations
│   ├── views.py               # View logic with caching
│   ├── urls.py                # URL configuration
│   ├── admin.py               # Enhanced admin interface
│   ├── templates/             # HTML templates
│   │   ├── basetemplates.html # Base template
│   │   ├── person.html        # Employee list
│   │   ├── from_view.html     # Employee form
│   │   └── about.html         # About page
│   ├── static/                # Static files
│   │   ├── bootstrap/         # Bootstrap files
│   │   └── images/           # Application images
│   └── migrations/            # Database migrations
├── MainProject/               # Project settings
│   ├── settings.py           # Optimized Django settings
│   ├── urls.py               # Main URL configuration
│   └── wsgi.py               # WSGI configuration
├── requirements.txt           # Python dependencies
├── README.md                 # Project documentation
├── USAGE.md                  # Detailed usage guide
└── .gitignore               # Git ignore file
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production settings:
```
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
ALLOWED_HOSTS=your-domain.com
```

### Database Configuration
The system supports multiple databases:
- **SQLite**: Default for development
- **PostgreSQL**: Recommended for production
- **MySQL**: Supported with configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Django](https://www.djangoproject.com/) - The web framework
- [Bootstrap](https://getbootstrap.com/) - CSS framework
- [Font Awesome](https://fontawesome.com/) - Icons
- [GitHub](https://github.com/) - Version control and hosting

## 📞 Support

If you have any questions or need help, please:
1. Check the [USAGE.md](USAGE.md) for detailed documentation
2. Open an issue on GitHub
3. Contact the development team

---

**Made with ❤️ using Django and Bootstrap**
