# Implementation Plan

- [x] 1. Add AWS dependencies and environment configuration


  - Add boto3 to requirements.txt
  - Create .env.example with S3 configuration variables
  - Update render.yaml with S3 environment variables
  - _Requirements: 4.1, 4.2_



- [ ] 2. Implement S3DataLoader service
- [ ] 2.1 Create S3DataLoader class with initialization
  - Implement __init__ method to initialize boto3 S3 client
  - Read S3_BUCKET_NAME from environment variables
  - Read AWS credentials from environment
  - _Requirements: 2.1_

- [x]* 2.2 Write property test for S3 client initialization

  - **Property 2: S3 configuration determines data source**
  - **Validates: Requirements 4.1, 4.2**

- [ ] 2.3 Implement S3 key generation method
  - Create _get_s3_key method to format S3 keys
  - Ensure format follows `data/{track_name}/{filename}` pattern
  - _Requirements: 1.2_


- [ ]* 2.4 Write property test for S3 key format
  - **Property 1: Upload preserves directory structure**
  - **Validates: Requirements 1.2**

- [ ] 2.5 Implement CSV download from S3
  - Create _download_csv_from_s3 method
  - Use boto3 to get object from S3
  - Parse CSV content into pandas DataFrame
  - Handle S3 errors gracefully (return None)
  - _Requirements: 2.2, 2.3, 2.4_


- [ ]* 2.6 Write property test for file not found handling
  - **Property 3: File not found returns None**
  - **Validates: Requirements 2.4**

- [ ] 2.7 Implement lap times loading with pattern matching
  - Create load_lap_times method
  - Try multiple filename patterns (underscores, hyphens)
  - Return DataFrame if any pattern succeeds

  - _Requirements: 2.2, 6.1, 6.2_

- [ ]* 2.8 Write property test for pattern matching
  - **Property 4: Multiple filename patterns are attempted**
  - **Validates: Requirements 6.1, 6.2**


- [ ] 2.9 Implement telemetry loading with pattern matching
  - Create load_telemetry method
  - Try multiple filename patterns
  - Return DataFrame if any pattern succeeds
  - _Requirements: 2.3, 6.3_

- [ ] 2.10 Implement track discovery
  - Create get_available_tracks method
  - List S3 objects with prefix 'data/'

  - Extract track names from subdirectories
  - Handle S3 errors gracefully (return empty list)
  - _Requirements: 3.1, 3.3_

- [ ]* 2.11 Write property test for track discovery
  - **Property 5: Track discovery lists all subdirectories**
  - **Validates: Requirements 3.1**

- [ ] 2.12 Implement session discovery
  - Create get_available_sessions method
  - List S3 objects in track directory
  - Extract session names from filenames matching pattern
  - Handle S3 errors gracefully (return empty list)
  - _Requirements: 3.2, 3.3_



- [ ]* 2.13 Write property test for session discovery
  - **Property 6: Session discovery extracts from filenames**
  - **Validates: Requirements 3.2**

- [x]* 2.14 Write property test for invalid credentials handling


  - **Property 7: Invalid credentials produce clear errors**
  - **Validates: Requirements 2.5**

- [ ] 3. Create S3 upload script
- [ ] 3.1 Implement upload_directory_to_s3 function
  - Traverse local directory recursively
  - Generate S3 keys preserving directory structure
  - Upload files with public-read ACL
  - Log upload progress and errors
  - _Requirements: 1.1, 1.2, 1.3_

- [ ] 3.2 Implement main function with error handling
  - Read S3_BUCKET_NAME from environment or prompt user
  - Provide clear error messages for missing credentials
  - Call upload_directory_to_s3 for data directory
  - Report upload summary


  - _Requirements: 1.3, 1.4_

- [ ]* 3.3 Write property test for upload error handling
  - **Property 7: Invalid credentials produce clear errors**
  - **Validates: Requirements 1.4**

- [ ]* 3.4 Write unit tests for upload script
  - Test directory traversal
  - Test S3 key generation from file paths
  - Test error reporting with mock S3
  - _Requirements: 1.1, 1.2, 1.3_

- [ ] 4. Integrate S3DataLoader with existing services
- [ ] 4.1 Update analytics routers to support S3 data source
  - Check USE_S3_DATA environment variable


  - Initialize S3DataLoader when enabled
  - Maintain backward compatibility with local files
  - _Requirements: 4.1, 4.2, 4.3_

- [ ]* 4.2 Write property test for data format consistency
  - **Property 8: Data format consistency across sources**
  - **Validates: Requirements 4.3**



- [ ]* 4.3 Write integration tests for S3 data loading
  - Test end-to-end data loading from mock S3
  - Test fallback to local files
  - Test environment variable switching
  - _Requirements: 4.1, 4.2, 4.3_

- [ ] 5. Create AWS setup documentation
- [ ] 5.1 Write AWS_SETUP_GUIDE.md
  - Include AWS account creation steps
  - Include S3 bucket creation with permissions
  - Include IAM user creation and credentials
  - Include Render environment variable configuration
  - Include cost estimates
  - Include troubleshooting section
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ] 5.2 Update README.md with S3 deployment instructions

  - Add S3 deployment section
  - Link to AWS_SETUP_GUIDE.md
  - Update deployment steps
  - _Requirements: 5.1_

- [ ] 6. Checkpoint - Ensure all tests pass
  - Run all unit tests
  - Run all property tests
  - Verify S3 integration works with mock data
  - Ask the user if questions arise

- [ ] 7. Deploy and verify
- [ ] 7.1 Create S3 bucket in AWS
  - Follow AWS_SETUP_GUIDE.md steps
  - Create bucket with appropriate permissions
  - Create IAM user with S3 access
  - _Requirements: 5.2, 5.3_

- [ ] 7.2 Upload data to S3
  - Set AWS environment variables locally
  - Run upload_to_s3.py script
  - Verify all files uploaded successfully
  - _Requirements: 1.1, 1.2, 1.3_

- [ ] 7.3 Configure Render deployment
  - Add S3 environment variables to Render
  - Set USE_S3_DATA=true
  - Redeploy backend service
  - _Requirements: 5.4_

- [ ] 7.4 Verify deployment
  - Test /api/analytics/tracks endpoint
  - Test data loading for each track
  - Verify frontend can load all tracks
  - Monitor logs for S3 errors
  - _Requirements: 2.2, 2.3, 3.1, 3.2_

- [ ] 8. Final checkpoint - Production verification
  - Ensure all tests pass
  - Verify all 7 tracks load correctly
  - Check AWS costs and usage
  - Ask the user if questions arise
