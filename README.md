# 🔗 Flask URL Shortener

A powerful and simple URL shortener API built with Flask, featuring full CRUD operations, automatic redirection, and interactive Swagger documentation.

## ✨ Features

- **Shorten URLs**: Convert long URLs into short, shareable links
- **Smart Redirection**: Automatic redirect from short URLs to original destinations
- **Full CRUD Operations**: Create, read, update, and delete shortened URLs
- **Interactive API Documentation**: Built-in Swagger UI for easy testing
- **URL Validation**: Ensures only valid URLs are processed
- **Persistent Storage**: SQLite database for reliable data storage
- **Clean Architecture**: Modular design with separate models, services, and routes

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- pip (Python package manager)

### Installation

1. **Clone and navigate to the project**:
   ```bash
   git clone <your-repo-url>
   cd flask-url-shortener
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=sqlite:///instance/url_shortener.db
   BASE_URL=http://127.0.0.1:5000
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

The server will start at `http://127.0.0.1:5000` 🎉

## 📖 API Documentation

### Interactive Swagger UI
Visit `http://127.0.0.1:5000/apidocs` for interactive API documentation where you can test all endpoints directly in your browser.

### Core Endpoints

#### 🔗 Shorten a URL
```http
POST /shorten
Content-Type: application/json

{
  "url": "https://www.example.com/very/long/url/path"
}
```

**Response:**
```json
{
  "short_url": "http://127.0.0.1:5000/r/AbC123"
}
```

#### 🔍 Get URL Details
```http
GET /expand/AbC123
```

**Response:**
```json
{
  "original_url": "https://www.example.com/very/long/url/path",
  "created_at": "2024-03-01T12:02:00"
}
```

#### 🌐 Redirect (Use in Browser)
```http
GET /r/AbC123
```
Automatically redirects to the original URL.

#### 📝 Update URL
```http
PUT /update/AbC123
Content-Type: application/json

{
  "url": "https://www.newexample.com/updated/path"
}
```

#### 🗑️ Delete URL
```http
DELETE /delete/AbC123
```

#### 📋 List All URLs
```http
GET /urls
```

## 🧪 Testing the API

### Using curl

**Shorten a URL:**
```bash
curl -X POST http://127.0.0.1:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'
```

**Get URL details:**
```bash
curl http://127.0.0.1:5000/expand/AbC123
```

**Test redirect:**
```bash
curl -L http://127.0.0.1:5000/r/AbC123
```

### Using Python requests

```python
import requests

# Shorten URL
response = requests.post('http://127.0.0.1:5000/shorten', 
                        json={'url': 'https://www.example.com'})
short_url_data = response.json()
print(f"Short URL: {short_url_data['short_url']}")

# Get details
short_code = short_url_data['short_url'].split('/')[-1]
details = requests.get(f'http://127.0.0.1:5000/expand/{short_code}')
print(f"Original URL: {details.json()['original_url']}")
```

## 🏗️ Project Structure

```
flask-url-shortener/
├── app.py              # Main application entry point
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── swagger.yml         # API documentation schema
├── models/
│   ├── db.py          # Database initialization
│   └─ url_map.py     # URL mapping model
├── routes/
│   └── url_routes.py  # API route handlers
├── services/
│   └── shortener.py   # URL shortening logic
├── utils/
│   └── validators.py  # URL validation utilities
└── instance/
    └── url_shortener.db # SQLite database (auto-created)
```

## ⚙️ Configuration

The application uses environment variables for configuration:

- `DATABASE_URL`: Database connection string (default: SQLite)
- `BASE_URL`: Base URL for generating short links

## 🔧 Development

### Code Formatting
The project uses Black for code formatting:
```bash
black .
```

### Database Schema
The application uses a simple SQLite database with one table:

**url_map table:**
- `short_code` (Primary Key): 6-character alphanumeric code
- `original_url`: The original long URL
- `created_at`: Timestamp of creation

### Short Code Generation
- Uses 6-character alphanumeric codes (letters + digits)
- Ensures uniqueness by checking against existing codes
- Provides 62^6 = ~56 billion possible combinations

## 🚦 Error Handling

The API provides clear error responses:

- `400 Bad Request`: Invalid URL format
- `404 Not Found`: Short URL doesn't exist
- `201 Created`: URL successfully shortened
- `200 OK`: Successful retrieval/update
- `204 No Content`: Successful deletion
- `302 Found`: Successful redirect

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test them
4. Format code with Black: `black .`
5. Commit changes: `git commit -m "Add feature"`
6. Push to branch: `git push origin feature-name`
7. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).


---

**Happy URL shortening!** 🎉

For questions or issues, please open an issue in the repository.