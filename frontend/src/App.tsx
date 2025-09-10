import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import './App.css';

interface UploadResponse {
  message: string;
  filename: string;
  s3_key: string;
  presigned_url: string | null;
  file_size: number;
}

interface ConfigResponse {
  configured: boolean;
  details: {
    aws_access_key: boolean;
    aws_secret_key: boolean;
    aws_bucket: boolean;
    aws_region: string;
  };
}

function App() {
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadResult, setUploadResult] = useState<UploadResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [configStatus, setConfigStatus] = useState<ConfigResponse | null>(null);

  const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 
    (window.location.hostname === 'localhost' ? '/api' : '/api');

  // Check configuration status
  React.useEffect(() => {
    checkConfig();
  }, []);

  const checkConfig = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/config`);
      setConfigStatus(response.data);
    } catch (err) {
      console.error('Failed to check config:', err);
    }
  };

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    // Validate file type
    if (file.type !== 'application/pdf') {
      setError('Only PDF files are allowed');
      return;
    }

    // Validate file size (50MB limit)
    if (file.size > 50 * 1024 * 1024) {
      setError('File size must be less than 50MB');
      return;
    }

    setError(null);
    setUploadResult(null);
    setUploading(true);
    setUploadProgress(0);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            setUploadProgress(progress);
          }
        },
      });

      setUploadResult(response.data);
    } catch (err: any) {
      if (err.response?.data?.error) {
        setError(err.response.data.error);
      } else {
        setError('Upload failed. Please try again.');
      }
    } finally {
      setUploading(false);
      setUploadProgress(0);
    }
  }, [API_BASE_URL]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    multiple: false,
    disabled: uploading,
    noClick: false,
    noKeyboard: false
  });

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="App">
      <div className="container">
        <h1>PDF Upload to S3</h1>
        
        {/* Configuration Status */}
        {configStatus && (
          <div className={`config-status ${configStatus.configured ? 'configured' : 'not-configured'}`}>
            <h3>Configuration Status</h3>
            {configStatus.configured ? (
              <p className="success">✅ AWS S3 is properly configured</p>
            ) : (
              <div className="error">
                <p>❌ AWS S3 configuration incomplete:</p>
                <ul>
                  <li>Access Key: {configStatus.details.aws_access_key ? '✅' : '❌'}</li>
                  <li>Secret Key: {configStatus.details.aws_secret_key ? '✅' : '❌'}</li>
                  <li>S3 Bucket: {configStatus.details.aws_bucket ? '✅' : '❌'}</li>
                  <li>Region: {configStatus.details.aws_region}</li>
                </ul>
                <p>Please set the required environment variables to enable uploads.</p>
              </div>
            )}
          </div>
        )}

        {/* Upload Area */}
        <div 
          {...getRootProps()} 
          className={`dropzone ${isDragActive ? 'active' : ''} ${uploading ? 'uploading' : ''}`}
        >
          <input {...getInputProps()} />
          {uploading ? (
            <div className="upload-progress">
              <div className="spinner"></div>
              <p>Uploading... {uploadProgress}%</p>
              <div className="progress-bar">
                <div 
                  className="progress-fill" 
                  style={{ width: `${uploadProgress}%` }}
                ></div>
              </div>
            </div>
          ) : isDragActive ? (
            <p>Drop the PDF file here...</p>
          ) : (
            <div className="upload-instructions">
              <div className="upload-icon">📄</div>
              <p>Drag and drop a PDF file here, or click to select</p>
              <p className="upload-hint">Maximum file size: 50MB</p>
            </div>
          )}
        </div>

        {/* Error Display */}
        {error && (
          <div className="error-message">
            <p>❌ {error}</p>
          </div>
        )}

        {/* Success Display */}
        {uploadResult && (
          <div className="success-message">
            <h3>✅ Upload Successful!</h3>
            <div className="upload-details">
              <p><strong>Filename:</strong> {uploadResult.filename}</p>
              <p><strong>File Size:</strong> {formatFileSize(uploadResult.file_size)}</p>
              <p><strong>S3 Key:</strong> {uploadResult.s3_key}</p>
              {uploadResult.presigned_url && (
                <p><strong>Download Link:</strong> 
                  <a href={uploadResult.presigned_url} target="_blank" rel="noopener noreferrer">
                    View/Download PDF
                  </a>
                  <span className="url-note"> (Link expires in 1 hour)</span>
                </p>
              )}
            </div>
          </div>
        )}

        {/* Refresh Config Button */}
        <button 
          onClick={checkConfig} 
          className="refresh-button"
          disabled={uploading}
        >
          🔄 Refresh Configuration
        </button>
      </div>
    </div>
  );
}

export default App;