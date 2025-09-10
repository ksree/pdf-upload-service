import os
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure CORS with specific origin
is_debug = os.getenv('FLASK_DEBUG', '0') == '1'
frontend_url = os.getenv('FRONTEND_URL')
allowed_origins = []
if frontend_url:
    allowed_origins.append(frontend_url)
if is_debug:
    allowed_origins.extend(['http://localhost:3000', 'http://localhost:5000'])

# In development, allow all origins if none specified
if is_debug and not allowed_origins:
    CORS(app)  # Allow all origins in debug mode
else:
    CORS(app, origins=allowed_origins)

# Configuration
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

@app.errorhandler(413)
def file_too_large(error):
    """Handle file too large error"""
    return jsonify({'error': f'File size exceeds {MAX_FILE_SIZE // (1024*1024)}MB limit'}), 413
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_pdf_file(file_obj):
    """Check if file is actually a PDF by checking magic header"""
    file_obj.seek(0)
    header = file_obj.read(4)
    file_obj.seek(0)
    return header == b'%PDF'

def get_s3_client():
    """Initialize S3 client"""
    try:
        # Extract just the region code from AWS_REGION (in case it has description)
        aws_region = os.getenv('AWS_REGION', 'us-east-1')
        # If region contains parentheses, extract just the region code (after the last space)
        if '(' in aws_region and ')' in aws_region:
            # Extract region code from format like "US East (Ohio) us-east-2"
            aws_region = aws_region.split()[-1]
        
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=aws_region
        )
        return s3_client
    except Exception as e:
        print(f"Error creating S3 client: {e}")
        return None

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Flask backend is running'})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload PDF file to S3"""
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file type
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        # Check if file is actually a PDF
        if not is_pdf_file(file):
            return jsonify({'error': 'File is not a valid PDF'}), 400
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({'error': f'File size exceeds {MAX_FILE_SIZE // (1024*1024)}MB limit'}), 400
        
        # Get S3 configuration
        bucket_name = os.getenv('AWS_S3_BUCKET')
        if not bucket_name:
            return jsonify({'error': 'S3 bucket not configured'}), 500
        
        # Initialize S3 client
        s3_client = get_s3_client()
        if not s3_client:
            return jsonify({'error': 'Failed to initialize S3 client'}), 500
        
        # Generate unique filename
        if not file.filename:
            return jsonify({'error': 'Invalid filename'}), 400
        original_filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{original_filename}"
        s3_key = f"pdfs/{unique_filename}"
        
        # Upload to S3
        try:
            s3_client.upload_fileobj(
                file,
                bucket_name,
                s3_key,
                ExtraArgs={
                    'ContentType': 'application/pdf',
                    'Metadata': {
                        'original_filename': original_filename,
                        'file_size': str(file_size)
                    }
                }
            )
            
            # Generate presigned URL for secure access
            try:
                presigned_url = s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': bucket_name, 'Key': s3_key},
                    ExpiresIn=3600  # 1 hour
                )
            except Exception as e:
                presigned_url = None
                print(f"Warning: Could not generate presigned URL: {e}")
            
            return jsonify({
                'message': 'File uploaded successfully',
                'filename': original_filename,
                's3_key': s3_key,
                'presigned_url': presigned_url,
                'file_size': file_size
            }), 200
            
        except NoCredentialsError:
            return jsonify({'error': 'AWS credentials not found'}), 500
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchBucket':
                return jsonify({'error': 'S3 bucket does not exist'}), 500
            else:
                return jsonify({'error': f'S3 error: {error_code}'}), 500
        except Exception as e:
            return jsonify({'error': f'Upload failed: {str(e)}'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get configuration status"""
    config_status = {
        'aws_access_key': bool(os.getenv('AWS_ACCESS_KEY_ID')),
        'aws_secret_key': bool(os.getenv('AWS_SECRET_ACCESS_KEY')),
        'aws_bucket': bool(os.getenv('AWS_S3_BUCKET')),
        'aws_region': os.getenv('AWS_REGION', 'us-east-1')
    }
    
    return jsonify({
        'configured': all(config_status.values()),
        'details': config_status
    })

if __name__ == '__main__':
    # Check required environment variables
    required_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_S3_BUCKET']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Warning: Missing environment variables: {', '.join(missing_vars)}")
        print("Set these variables to enable S3 functionality")
    
    app.run(host='0.0.0.0', port=8000, debug=is_debug)