# Design Document: AWS S3 Data Hosting

## Overview

The AWS S3 Data Hosting feature provides cloud-based storage and retrieval for APEX's race telemetry datasets. This design enables the application to serve 3GB+ of race data without bundling it with deployment artifacts, solving size limitations on platforms like Render (500MB limit) and Netlify.

The solution uses AWS S3 as the primary data store, with boto3 as the Python SDK for S3 interactions. The system maintains backward compatibility with local file storage for development environments through environment-based configuration.

## Architecture

### High-Level Architecture

```
┌─────────────────┐
│   Frontend      │
│   (Netlify)     │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│   Backend API   │
│   (Render)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│  S3DataLoader   │─────▶│   AWS S3 Bucket  │
│                 │      │  apex-racing-data│
└─────────────────┘      └──────────────────┘
         │                        │
         │                        ├─ data/
         │                        │  ├─ barber_motorsports_park/
         │                        │  ├─ circuit_of_the_americas/
         │                        │  ├─ indianapolis/
         │                        │  └─ ...
         │
         ▼
┌─────────────────┐
│  Local Files    │
│  (Development)  │
└─────────────────┘
```

### Component Interaction Flow

1. **API Request**: Frontend requests track data via REST API
2. **Data Loader Check**: Backend checks `USE_S3_DATA` environment variable
3. **S3 Retrieval**: If enabled, S3DataLoader fetches CSV from S3 bucket
4. **Parsing**: CSV content is parsed into pandas DataFrame
5. **Response**: Processed data returned to frontend as JSON

## Components and Interfaces

### 1. S3DataLoader Class

**Location**: `backend/services/s3_data_loader.py`

**Responsibilities**:
- Initialize boto3 S3 client with AWS credentials
- Download CSV files from S3 bucket
- Parse CSV content into pandas DataFrames
- Handle S3 errors gracefully
- Discover available tracks and sessions

**Interface**:

```python
class S3DataLoader:
    def __init__(self) -> None
    def _get_s3_key(self, track_name: str, filename: str) -> str
    def _download_csv_from_s3(self, s3_key: str) -> Optional[pd.DataFrame]
    def load_lap_times(self, track_name: str, session: str) -> Optional[pd.DataFrame]
    def load_telemetry(self, track_name: str, session: str) -> Optional[pd.DataFrame]
    def get_available_tracks(self) -> list[str]
    def get_available_sessions(self, track_name: str) -> list[str]
```

### 2. Upload Script

**Location**: `upload_to_s3.py`

**Responsibilities**:
- Upload local data directory to S3
- Preserve directory structure
- Set appropriate file permissions (public-read)
- Report upload progress and errors

**Interface**:

```python
def upload_directory_to_s3(local_directory: str, bucket_name: str, s3_prefix: str) -> None
def main() -> None
```

### 3. Environment Configuration

**Configuration Variables**:
- `USE_S3_DATA`: Boolean flag to enable S3 data source (default: false)
- `S3_BUCKET_NAME`: Name of the S3 bucket (default: apex-racing-data)
- `AWS_ACCESS_KEY_ID`: AWS IAM access key
- `AWS_SECRET_ACCESS_KEY`: AWS IAM secret key
- `AWS_REGION`: AWS region for S3 bucket (default: us-east-1)

## Data Models

### S3 Key Structure

```
data/{track_name}/{session}_{track_name}_{data_type}.csv
```

**Examples**:
- `data/barber_motorsports_park/practice_barber_motorsports_park_lap_start.csv`
- `data/circuit_of_the_americas/race_circuit_of_the_americas_telemetry_data.csv`

### File Naming Patterns

The system supports multiple naming patterns to handle variations:

**Lap Times**:
1. `{session}_{track_name}_lap_start.csv`
2. `{session}_{track_name_with_hyphens}_lap_start.csv`
3. `{session}_lap_start.csv`

**Telemetry**:
1. `{session}_{track_name}_telemetry_data.csv`
2. `{session}_{track_name_with_hyphens}_telemetry_data.csv`
3. `{session}_telemetry_data.csv`

### DataFrame Schema

**Lap Times DataFrame**:
- Columns: `LapNumber`, `LapTime`, `Driver`, `CarNumber`, etc.
- Index: Integer row index

**Telemetry DataFrame**:
- Columns: `Time`, `Speed`, `Throttle`, `Brake`, `Latitude`, `Longitude`, etc.
- Index: Integer row index

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Upload preserves directory structure

*For any* local directory with race data files, uploading to S3 should result in S3 keys that preserve the relative path structure with format `data/{track_name}/{filename}`

**Validates: Requirements 1.2**

### Property 2: S3 configuration determines data source

*For any* data loading request, when `USE_S3_DATA` is true, the system should use S3 as the data source, and when false or unset, the system should use local files

**Validates: Requirements 4.1, 4.2**

### Property 3: File not found returns None

*For any* S3 key that does not exist in the bucket, attempting to download should return None without raising an exception

**Validates: Requirements 2.4**

### Property 4: Multiple filename patterns are attempted

*For any* track and session combination, when the first filename pattern fails, the system should attempt alternative patterns before returning None

**Validates: Requirements 6.1, 6.2**

### Property 5: Track discovery lists all subdirectories

*For any* S3 bucket with data organized under `data/` prefix, listing available tracks should return all subdirectory names under that prefix

**Validates: Requirements 3.1**

### Property 6: Session discovery extracts from filenames

*For any* track directory in S3, listing sessions should return all unique session prefixes from files matching `{session}_lap_start.csv` pattern

**Validates: Requirements 3.2**

### Property 7: Invalid credentials produce clear errors

*For any* S3 operation with invalid AWS credentials, the system should handle the authentication error gracefully and provide a clear error message

**Validates: Requirements 1.4, 2.5**

### Property 8: Data format consistency across sources

*For any* track and session, the DataFrame returned from S3 should have the same schema and format as the DataFrame returned from local files

**Validates: Requirements 4.3**

## Error Handling

### S3 Client Errors

**Authentication Errors** (`NoCredentialsError`, `ClientError` with 403):
- Log error with message indicating credential issue
- Return None or empty list
- Do not crash the application

**Bucket Not Found** (`NoSuchBucket`):
- Log error with bucket name
- Return None or empty list
- Suggest checking bucket name and region

**File Not Found** (`NoSuchKey`):
- Log warning (not error) since this is expected for pattern matching
- Try next filename pattern
- Return None only after all patterns exhausted

**Network Errors** (`ConnectionError`, `Timeout`):
- Log error with retry suggestion
- Return None or empty list
- Consider implementing retry logic in future

### CSV Parsing Errors

**Malformed CSV**:
- Log error with filename and parsing issue
- Return None
- Do not crash the application

**Empty File**:
- Log warning
- Return empty DataFrame
- Continue processing

### Upload Script Errors

**Missing Environment Variables**:
- Prompt user for bucket name interactively
- Provide clear instructions for setting environment variables
- Exit gracefully if credentials still missing

**Upload Failures**:
- Log specific file that failed
- Continue uploading remaining files
- Report summary of successes and failures at end

## Testing Strategy

### Unit Testing

**Framework**: pytest

**Test Coverage**:

1. **S3DataLoader Tests**:
   - Test initialization with environment variables
   - Test S3 key generation for various track names
   - Test CSV parsing from S3 response
   - Test error handling for missing files
   - Test pattern matching logic

2. **Upload Script Tests**:
   - Test directory traversal
   - Test S3 key generation from file paths
   - Test error reporting

3. **Integration Tests**:
   - Test end-to-end data loading from mock S3
   - Test fallback to local files
   - Test environment variable switching

**Mocking Strategy**:
- Use `moto` library to mock AWS S3 for unit tests
- Use `unittest.mock` to mock boto3 client for error scenarios
- Create fixture CSV files for testing parsing logic

### Property-Based Testing

**Framework**: Hypothesis (Python property-based testing library)

**Configuration**: Each property test should run a minimum of 100 iterations

**Property Tests**:

1. **Property 1: Upload preserves directory structure**
   - **Feature: aws-s3-data-hosting, Property 1: Upload preserves directory structure**
   - Generate random directory structures
   - Upload to mock S3
   - Verify S3 keys match expected format

2. **Property 2: S3 configuration determines data source**
   - **Feature: aws-s3-data-hosting, Property 2: S3 configuration determines data source**
   - Generate random environment variable values
   - Verify correct data source is used

3. **Property 3: File not found returns None**
   - **Feature: aws-s3-data-hosting, Property 3: File not found returns None**
   - Generate random non-existent S3 keys
   - Verify None is returned without exceptions

4. **Property 4: Multiple filename patterns are attempted**
   - **Feature: aws-s3-data-hosting, Property 4: Multiple filename patterns are attempted**
   - Generate random track/session combinations
   - Mock S3 to fail first patterns
   - Verify all patterns are attempted

5. **Property 5: Track discovery lists all subdirectories**
   - **Feature: aws-s3-data-hosting, Property 5: Track discovery lists all subdirectories**
   - Generate random S3 bucket structures
   - Verify all track directories are discovered

6. **Property 6: Session discovery extracts from filenames**
   - **Feature: aws-s3-data-hosting, Property 6: Session discovery extracts from filenames**
   - Generate random session filenames
   - Verify correct session names are extracted

7. **Property 7: Invalid credentials produce clear errors**
   - **Feature: aws-s3-data-hosting, Property 7: Invalid credentials produce clear errors**
   - Generate invalid credential combinations
   - Verify graceful error handling

8. **Property 8: Data format consistency across sources**
   - **Feature: aws-s3-data-hosting, Property 8: Data format consistency across sources**
   - Generate random CSV data
   - Load from both S3 and local
   - Verify DataFrames are equivalent

### Manual Testing

**AWS Setup Verification**:
1. Follow AWS_SETUP_GUIDE.md step-by-step
2. Verify S3 bucket creation
3. Verify IAM user creation and permissions
4. Test upload script with real AWS credentials
5. Verify files are accessible in S3 console

**Deployment Testing**:
1. Deploy backend to Render with S3 configuration
2. Test `/api/analytics/tracks` endpoint
3. Test data loading for each track
4. Verify frontend can load all tracks
5. Monitor CloudWatch logs for S3 errors

**Performance Testing**:
1. Measure S3 download latency vs local file access
2. Test with concurrent requests
3. Monitor S3 request costs
4. Verify caching behavior (if implemented)

## Security Considerations

### IAM Permissions

**Principle of Least Privilege**:
- Create dedicated IAM user for APEX application
- Grant only S3 read permissions for production
- Grant S3 write permissions only for upload script
- Use separate IAM users for different environments

**Recommended IAM Policy**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::apex-racing-data",
        "arn:aws:s3:::apex-racing-data/*"
      ]
    }
  ]
}
```

### Credential Management

**Environment Variables**:
- Never commit AWS credentials to version control
- Use environment variables in deployment platforms
- Rotate credentials periodically
- Use AWS Secrets Manager for production (future enhancement)

**Public Access**:
- S3 bucket should allow public read for simplicity
- Alternative: Use pre-signed URLs for private buckets (future enhancement)
- Monitor S3 access logs for suspicious activity

### Data Privacy

**Race Data**:
- Telemetry data is not personally identifiable
- No sensitive information in CSV files
- Public access is acceptable for this use case

## Deployment Configuration

### Render Configuration

**Environment Variables** (set in Render dashboard):
```
USE_S3_DATA=true
S3_BUCKET_NAME=apex-racing-data
AWS_ACCESS_KEY_ID=<your-access-key>
AWS_SECRET_ACCESS_KEY=<your-secret-key>
AWS_REGION=us-east-1
```

**Build Command**: `pip install -r requirements.txt`

**Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

### Local Development

**Environment Variables** (`.env` file):
```
USE_S3_DATA=false
```

**No AWS credentials needed for local development**

## Performance Considerations

### Latency

**S3 Download Time**:
- Typical CSV file: 1-5 MB
- Expected latency: 100-500ms (depending on region)
- Acceptable for analytics use case

**Optimization Opportunities**:
- Implement caching layer (Redis/Memcached)
- Use S3 Transfer Acceleration for faster downloads
- Compress CSV files (gzip) to reduce transfer time

### Cost

**AWS Free Tier**:
- 5 GB storage (sufficient for race data)
- 20,000 GET requests per month
- 2,000 PUT requests per month

**Estimated Monthly Cost** (after free tier):
- Storage: ~$0.07 (3GB × $0.023/GB)
- Requests: ~$0.01 (assuming 10,000 requests)
- **Total**: ~$0.10/month

### Scalability

**Current Design**:
- Supports up to 100 tracks without modification
- Handles concurrent requests through boto3 connection pooling
- No server-side caching (stateless)

**Future Enhancements**:
- Add CloudFront CDN for global distribution
- Implement server-side caching
- Use S3 Select for querying CSV data without full download

## Migration Path

### Phase 1: S3 Integration (Current)
- Add boto3 dependency
- Create S3DataLoader class
- Create upload script
- Update documentation

### Phase 2: Deployment
- Create S3 bucket
- Upload data to S3
- Configure Render environment variables
- Deploy and test

### Phase 3: Optimization (Future)
- Add caching layer
- Implement CloudFront CDN
- Add monitoring and alerting
- Optimize CSV file sizes

## Documentation

### User-Facing Documentation

1. **AWS_SETUP_GUIDE.md**: Complete setup instructions for AWS S3
2. **.env.example**: Example environment configuration
3. **README.md**: Updated with S3 deployment instructions

### Developer Documentation

1. **Code Comments**: Inline documentation in S3DataLoader
2. **API Documentation**: Updated FastAPI docs with S3 configuration
3. **Architecture Diagram**: Visual representation of S3 integration

## Monitoring and Observability

### Logging

**S3 Operations**:
- Log all S3 download attempts (success/failure)
- Log filename patterns attempted
- Log authentication errors
- Use structured logging for easy parsing

**Example Log Format**:
```
INFO: Loading lap times for barber_motorsports_park/practice
INFO: Attempting pattern: practice_barber_motorsports_park_lap_start.csv
INFO: Successfully loaded from S3: data/barber_motorsports_park/practice_barber_motorsports_park_lap_start.csv
```

### Metrics

**Key Metrics to Track**:
- S3 request count
- S3 error rate
- Average download latency
- Cache hit rate (if caching implemented)

**Tools**:
- AWS CloudWatch for S3 metrics
- Render logs for application metrics
- Consider adding application-level metrics (Prometheus/Grafana)

## Rollback Plan

### If S3 Integration Fails

1. **Immediate Rollback**:
   - Set `USE_S3_DATA=false` in Render
   - Redeploy with local data (if size permits)
   - Or use mock data temporarily

2. **Troubleshooting**:
   - Check AWS credentials in Render environment
   - Verify S3 bucket name and region
   - Check S3 bucket permissions
   - Review CloudWatch logs for errors

3. **Alternative Solutions**:
   - Use different cloud storage (Google Cloud Storage, Azure Blob)
   - Implement data streaming from external API
   - Use database storage (PostgreSQL with large object support)
