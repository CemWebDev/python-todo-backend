# A RESTful API for managing todos with user authentication built with FastAPI and MongoDB.

## Features

- User registration and login with API key authentication
- Create, read, update, and delete todos
- User-specific todo management
- Secure password hashing with bcrypt
- MongoDB integration for data persistence
- RESTful API design with FastAPI

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **MongoDB**: NoSQL database for storing user and todo data
- **PyMongo**: MongoDB driver for Python
- **Pydantic**: Data validation and settings management
- **Passlib**: Password hashing library
- **Python-dotenv**: Environment variable management
- **Uvicorn**: ASGI server for running the application

## Installation

### Prerequisites

- Python 3.8+
- MongoDB (local installation or MongoDB Atlas)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/CemWebDev/python-todo-backend.git
   cd python-todo-backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with the following variables:
   ```
   MONGO_URI=mongodb://localhost:27017/todo_app
   ```

## Running the Application

Start the application with:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

- API documentation: `http://localhost:8000/docs`
- Alternative documentation: `http://localhost:8000/redoc`

## Environment Variables

- `MONGO_URI`: MongoDB connection string (default: `mongodb://localhost:27017/todo_app`)

## API Endpoints

### Authentication

- `POST /register`: Register a new user
  - Request body: `{ "email": "user@example.com", "password": "password123" }`
  - Response: User object with ID

- `POST /login`: Login and get API key
  - Request body: `{ "username": "user@example.com", "password": "password123" }`
  - Response: API key and user information

- `POST /logout`: Logout (for future token invalidation)

### Todos

All todo endpoints require an API key in the `X-API-Key` header.

- `GET /todos`: Get all todos for the authenticated user
- `POST /todos`: Create a new todo
  - Request body: `{ "title": "Task title", "description": "Task description", "completed": false }`
- `GET /todos/{todo_id}`: Get a specific todo by ID
- `PUT /todos/{todo_id}`: Update a specific todo
  - Request body: `{ "title": "Updated title", "description": "Updated description", "completed": true }`
- `DELETE /todos/{todo_id}`: Delete a specific todo

## Usage Examples

### Register a New User

```bash
curl -X 'POST' 
  'http://localhost:8000/register' 
  -H 'Content-Type: application/json' 
  -d '{
  "email": "user@example.com",
  "password": "password123"
}'
```

### Login and Get API Key

```bash
curl -X 'POST' 
  'http://localhost:8000/login' 
  -H 'Content-Type: application/x-www-form-urlencoded' 
  -d 'username=user@example.com&password=password123'
```

### Create a Todo

```bash
curl -X 'POST' 
  'http://localhost:8000/todos' 
  -H 'X-API-Key: YOUR_API_KEY' 
  -H 'Content-Type: application/json' 
  -d '{
  "title": "Complete project",
  "description": "Finish the Todo API project",
  "completed": false
}'
```

### Get All Todos

```bash
curl -X 'GET' 
  'http://localhost:8000/todos'
  -H 'X-API-Key: YOUR_API_KEY'
```

## Project Structure

```
todo-api/
├── app/
│   ├── auth/
│   │   └── auth.py         # Authentication utilities
│   ├── models/
│   │   ├── todo.py         # Todo models
│   │   └── user.py         # User models
│   ├── routes/
│   │   ├── auth.py         # Authentication routes
│   │   └── todo.py         # Todo routes
│   ├── database.py         # Database connection
│   └── main.py             # Application entry point
├── .env                    # Environment variables
├── .gitignore              # Git ignore file
├── README.md               # Project documentation
└── requirements.txt        # Project dependencies
```


## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request