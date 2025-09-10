# PDF Upload Service

A full-stack PDF upload application with drag-and-drop functionality, built with React TypeScript frontend and Python Flask backend, featuring secure AWS S3 storage.

## Features

- 🔒 **Secure PDF Upload** - Only PDF files accepted with magic header validation
- 🎯 **Drag & Drop Interface** - Intuitive file upload experience
- 📊 **Real-time Progress** - Live upload progress tracking
- ☁️ **AWS S3 Integration** - Secure cloud storage with presigned URLs
- 🔐 **Security Features** - File size limits (50MB), CORS protection, secure filename handling
- ⚡ **Real-time Config Check** - Automatic AWS configuration validation

## Technology Stack

### Frontend
- **React 18** with TypeScript (compatible with Create React App)
- **react-dropzone** for drag-and-drop functionality
- **Axios** for API communication
- **CSS-in-JS** styling with modern gradients

### Backend
- **Python Flask** web framework
- **boto3** for AWS S3 integration
- **Flask-CORS** for cross-origin resource sharing
- **Werkzeug** for secure file handling

### Cloud Storage
- **AWS S3** for file storage
- **Presigned URLs** for secure file access

## Project Structure

```
pdf-upload-service/
├── frontend/                 # React TypeScript frontend
│   ├── src/
│   │   ├── App.tsx          # Main application component
│   │   ├── App.css          # Application styles
│   │   └── ...
│   ├── package.json         # Frontend dependencies
│   └── tsconfig.json        # TypeScript configuration
├── backend/                  # Python Flask backend
│   └── app.py               # Main Flask application
├── package.json             # Root package configuration
├── pyproject.toml           # Python dependencies
└── README.md                # This file
```

## Setup Instructions

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- AWS account with S3 access

### Environment Variables
Set up the following environment variables:
- `AWS_ACCESS_KEY_ID` - Your AWS access key
- `AWS_SECRET_ACCESS_KEY` - Your AWS secret key
- `AWS_S3_BUCKET` - Your S3 bucket name
- `AWS_REGION` - Your AWS region (e.g., us-east-1)

### Installation

1. **Install Frontend Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Install Backend Dependencies**
   ```bash
   # Using uv (recommended)
   uv pip install flask flask-cors boto3 python-multipart
   
   # Or using pip
   pip install flask flask-cors boto3 python-multipart
   ```

### Running the Application

1. **Start the Backend** (Terminal 1)
   ```bash
   cd backend
   FLASK_DEBUG=1 python app.py
   ```

2. **Start the Frontend** (Terminal 2)
   ```bash
   cd frontend
   PORT=5000 npm start
   ```
   
   *Note: Setting PORT=5000 ensures the frontend runs on port 5000 to match the workflow configuration. Without this, Create React App defaults to port 3000.*

The application will be available at `http://localhost:5000`

## Security Features

- **File Validation**: Only PDF files accepted with magic header verification
- **Size Limits**: Maximum file size of 50MB
- **Secure Filenames**: UUID-based filename generation
- **CORS Protection**: Environment-aware CORS configuration
- **Presigned URLs**: Secure file access without public S3 URLs

## API Endpoints

- `GET /api/config` - Check AWS configuration status
- `POST /api/upload` - Upload PDF file to S3

## Development

The application includes:
- TypeScript for type safety
- Hot reloading for development
- Comprehensive error handling
- Development vs production configurations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is available for educational and personal use.