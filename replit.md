# PDF Upload Service

## Overview

This is a production-ready PDF file upload service that allows users to securely upload PDF documents to AWS S3 storage. The application consists of a React TypeScript frontend with drag-and-drop functionality and a Python Flask backend that handles file validation, processing, and S3 integration. The system includes comprehensive error handling, file type validation, security features, and configuration status monitoring.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

**September 10, 2025**
- Implemented complete PDF upload application with React frontend and Flask backend
- Added AWS S3 integration with presigned URLs for secure file access
- Implemented security features: CORS restrictions, PDF magic header validation, file size limits
- Added production-ready configurations with debug mode controls
- Configured proxy routing for frontend-backend communication

## System Architecture

### Frontend Architecture
- **Framework**: React 19.1.1 with TypeScript for type safety and modern development
- **UI Components**: Custom drag-and-drop interface using react-dropzone for intuitive file uploads
- **State Management**: React hooks (useState, useCallback, useEffect) for local component state
- **HTTP Client**: Axios for API communication with the backend
- **Styling**: CSS-in-JS approach with gradient backgrounds and modern UI design
- **Development Setup**: Create React App with proxy configuration for local development

### Backend Architecture
- **Framework**: Flask (Python) as a lightweight web server for handling file uploads
- **CORS Configuration**: Environment-aware CORS settings that adapt between development and production
- **File Validation**: Multi-layered validation including file extension checking and PDF magic header verification
- **Error Handling**: Comprehensive error handling with custom error handlers for file size limits and validation failures
- **Security**: Secure filename handling using werkzeug utilities and file type validation

### File Processing Pipeline
- **Upload Validation**: Files are validated for PDF format, size limits (50MB max), and proper file headers
- **Secure Processing**: Filenames are sanitized and unique identifiers are generated using UUID
- **Storage Strategy**: Direct upload to S3 with optional presigned URL generation for secure access

### Configuration Management
- **Environment Variables**: AWS credentials, bucket configuration, and CORS settings managed through environment variables
- **Runtime Configuration**: Dynamic configuration checking with status endpoint for monitoring AWS setup
- **Development vs Production**: Separate configurations for local development and production deployment

## External Dependencies

### Cloud Storage
- **AWS S3**: Primary storage solution for uploaded PDF files
- **AWS SDK (boto3)**: Python SDK for S3 integration and file operations
- **Required Credentials**: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME, AWS_REGION

### Core Technologies
- **React Ecosystem**: React DOM, React Scripts for frontend development and build process
- **TypeScript**: Type definitions for React, Node.js, and react-dropzone for enhanced developer experience
- **Testing Framework**: Testing Library suite with Jest DOM for comprehensive frontend testing
- **Python Web Stack**: Flask with Flask-CORS for cross-origin resource sharing

### Development Tools
- **Build System**: Create React App for frontend bundling and development server
- **Package Management**: npm/Node.js for frontend dependencies, pip for Python backend dependencies
- **Development Proxy**: Frontend proxy configuration to backend during local development