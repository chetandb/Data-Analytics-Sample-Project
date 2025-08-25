# Data Analytics Sample Project

A comprehensive data analytics and user management system built with Python Flask and advanced data processing capabilities. This project demonstrates best practices in data pipeline development, user authentication, and automated testing.

## 🌟 Features

### Data Processing & Analytics
- **Advanced Data Pipeline**: Robust data cleaning, transformation, and validation pipeline
- **Batch Processing**: Efficient parallel processing for large datasets
- **Data Cleaning**: Automated handling of missing values, duplicates, and data type corrections
- **Data Transformation**: Aggregation, date parsing, and statistical operations
- **Comprehensive Logging**: Detailed logging for monitoring and debugging

### User Management System
- **User Registration & Authentication**: Secure user registration with email verification
- **Password Security**: Industry-standard password hashing and validation
- **Email Verification**: Token-based email verification system
- **Role & Permission Management**: Flexible role-based access control
- **Password Recovery**: Secure password reset functionality

### Quality Assurance
- **Comprehensive Testing**: Unit tests for all major components
- **Pytest Integration**: Modern testing framework with organized test structure
- **Code Quality**: Automated code quality checks with GitHub Actions
- **Test Coverage**: Tests for user management, data processing, and pipeline operations

## 🏗️ Project Structure

```
Data-Analytics-Sample-Project/
├── Data_Preprocessing_Cleaning/     # Data processing modules
│   ├── Data_Cleaning/              # Data cleaning utilities
│   │   ├── DataCleaner.py          # Main data cleaning class
│   │   ├── DataTypeCorrector.py    # Data type validation and correction
│   │   ├── DuplicateRemover.py     # Duplicate detection and removal
│   │   └── Test*.py                # Unit tests for cleaning modules
│   ├── Data_Transformation/        # Data transformation utilities
│   │   ├── Aggregator.py           # Data aggregation operations
│   │   ├── DateParser.py           # Date parsing and formatting
│   │   └── Test*.py                # Unit tests for transformation modules
│   ├── DataPipeline.py             # Main data pipeline orchestrator
│   └── TestDatapipeline.py         # Pipeline integration tests
├── User_Management/                 # User management system
│   ├── user_registration/          # Registration and authentication
│   │   ├── app.py                  # Flask application
│   │   ├── models.py               # Database models
│   │   ├── config.py               # Application configuration
│   │   ├── db.py                   # Database initialization
│   │   └── test_*.py               # User management tests
│   ├── templates/                  # HTML templates
│   ├── user_permission/            # Role and permission management
│   └── password_recovery/          # Password reset functionality
├── Tests/                          # Integration and system tests
├── .github/workflows/              # CI/CD pipeline
└── requirements.txt                # Python dependencies
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- SQLite (included with Python)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Data-Analytics-Sample-Project
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   cd User_Management/user_registration
   python app.py
   ```
   This will create the SQLite database with all necessary tables.

### Configuration

1. **Email Configuration** (Optional)
   Edit `User_Management/user_registration/config.py` to configure email settings:
   ```python
   MAIL_SERVER = 'your-smtp-server.com'
   MAIL_USERNAME = 'your-email@example.com'
   MAIL_PASSWORD = 'your-app-password'
   ```

2. **Database Configuration**
   The project uses SQLite by default. To use a different database, modify the `SQLALCHEMY_DATABASE_URI` in `config.py`.

## 💻 Usage

### Running the Web Application

```bash
cd User_Management/user_registration
python app.py
```

The application will be available at `http://localhost:5000`

### Using the Data Pipeline

```python
import pandas as pd
from Data_Preprocessing_Cleaning.DataPipeline import DataPipeline

# Load your data
df = pd.read_csv('your_data.csv')

# Create and run the pipeline
pipeline = DataPipeline(df)
pipeline.run_pipeline(n_chunks=4)
```

### Data Cleaning Example

```python
import pandas as pd
from Data_Preprocessing_Cleaning.Data_Cleaning.DataCleaner import DataCleaner

# Load data
df = pd.read_csv('messy_data.csv')

# Clean the data
cleaner = DataCleaner(df)
cleaned_df = cleaner.handle_missing_values(strategy='median')
```

## 🧪 Testing

The project uses pytest for comprehensive testing. Tests are organized across three main directories:

### Running All Tests

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run tests with coverage report
pytest --cov=.
```

### Running Specific Test Suites

```bash
# User management tests
pytest User_Management/

# Data processing tests
pytest Data_Preprocessing_Cleaning/

# Integration tests
pytest Tests/
```

### Test Structure

- **Unit Tests**: Test individual components and functions
- **Integration Tests**: Test component interactions
- **System Tests**: End-to-end testing of complete workflows

## 📊 Data Pipeline Features

### Data Cleaning
- **Missing Value Handling**: Multiple strategies (mean, median, mode, forward/backward fill)
- **Data Type Correction**: Automatic detection and correction of data types
- **Duplicate Removal**: Configurable duplicate detection and removal
- **Outlier Detection**: Statistical methods for identifying and handling outliers

### Data Transformation
- **Aggregation**: Flexible grouping and aggregation operations
- **Date Processing**: Robust date parsing and formatting
- **Feature Engineering**: Automated feature creation and transformation
- **Data Validation**: Schema validation and data quality checks

### Performance Optimization
- **Batch Processing**: Parallel processing for large datasets
- **Memory Management**: Efficient memory usage for large files
- **Logging**: Comprehensive logging for monitoring and debugging
- **Error Handling**: Robust error handling and recovery

## 🔐 Security Features

### User Authentication
- **Password Hashing**: PBKDF2 with SHA-256
- **Input Validation**: Comprehensive validation for usernames, emails, and passwords
- **Email Verification**: Token-based email verification system
- **Session Management**: Secure session handling

### Security Best Practices
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **XSS Protection**: Input sanitization and output encoding
- **CSRF Protection**: Cross-site request forgery protection
- **Secure Headers**: Security headers implementation

## 🔧 Development

### Code Quality

- **Linting**: Follow PEP 8 style guidelines
- **Type Hints**: Use type annotations where applicable
- **Documentation**: Comprehensive docstrings and comments
- **Testing**: Maintain high test coverage

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests before committing
pytest

# Check code style
flake8 .
```

## 📝 Dependencies

### Core Dependencies
- **Flask**: Web framework for user management system
- **Flask-SQLAlchemy**: Database ORM
- **Flask-Mail**: Email functionality
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **werkzeug**: Security utilities

### Testing Dependencies
- **pytest**: Testing framework
- **selenium**: Web application testing

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Ensure SQLite database is properly initialized
   - Check file permissions in the project directory

2. **Email Verification Not Working**
   - Verify email configuration in `config.py`
   - Check email server settings and credentials

3. **Import Errors**
   - Ensure all dependencies are installed
   - Verify Python path and virtual environment activation

4. **Test Failures**
   - Run tests individually to isolate issues
   - Check database state between tests
   - Verify test data setup

### Logging

The application generates detailed logs in:
- `data_processing.log`: Data pipeline operations
- Flask debug logs: Web application operations

## 📄 License

This project is available under the MIT License. See the LICENSE file for more details.

## 🤝 Support

For questions, issues, or contributions:
1. Check existing issues in the repository
2. Create a new issue with detailed description
3. Follow the contribution guidelines

## 🚀 Future Enhancements

- **API Development**: RESTful API for data operations
- **Dashboard**: Web-based analytics dashboard
- **Advanced Analytics**: Machine learning integration
- **Database Support**: PostgreSQL and MySQL support
- **Containerization**: Docker support for easy deployment
- **Monitoring**: Application performance monitoring

---

**Note**: This project has been optimized by removing unnecessary cache files and build artifacts while retaining all essential functionality for development and testing.
