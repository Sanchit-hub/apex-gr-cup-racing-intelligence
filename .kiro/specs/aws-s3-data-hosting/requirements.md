# Requirements Document

## Introduction

The AWS S3 Data Hosting feature enables APEX to host and serve large race telemetry datasets (3GB+) from cloud storage instead of bundling them with the application deployment. This solves deployment size limitations on platforms like Render and Netlify while maintaining fast data access for analytics.

## Glossary

- **APEX**: The GR Cup Analytics Platform - a web application for analyzing Toyota GR Cup race telemetry
- **S3**: Amazon Simple Storage Service - AWS cloud object storage service
- **Telemetry Data**: CSV files containing lap times, speed, throttle, brake, and GPS coordinates from race sessions
- **Track**: A racing circuit (e.g., Barber Motorsports Park, Circuit of the Americas)
- **Session**: A specific race event (e.g., practice, qualifying, race)
- **Data Loader**: Backend service responsible for loading and processing race data
- **Render**: Cloud platform hosting the APEX backend API
- **Netlify**: Cloud platform hosting the APEX frontend application

## Requirements

### Requirement 1

**User Story:** As a system administrator, I want to upload race data to AWS S3, so that the data is accessible to the deployed application without exceeding deployment size limits.

#### Acceptance Criteria

1. WHEN the administrator runs the upload script with valid AWS credentials THEN the system SHALL upload all race data files to the specified S3 bucket
2. WHEN uploading files to S3 THEN the system SHALL preserve the directory structure with format `data/{track_name}/{filename}`
3. WHEN the upload completes THEN the system SHALL report the total number of files uploaded and any errors encountered
4. WHEN AWS credentials are invalid or missing THEN the system SHALL provide a clear error message and prevent upload attempts

### Requirement 2

**User Story:** As a backend service, I want to load race data from S3, so that I can provide analytics without requiring local data storage.

#### Acceptance Criteria

1. WHEN the backend is configured to use S3 data THEN the Data Loader SHALL initialize an S3 client with the configured credentials
2. WHEN requesting lap times for a track and session THEN the system SHALL download and parse the corresponding CSV file from S3
3. WHEN requesting telemetry data for a track and session THEN the system SHALL download and parse the corresponding CSV file from S3
4. WHEN an S3 file is not found THEN the system SHALL return None and log the error without crashing
5. WHEN S3 credentials are invalid THEN the system SHALL handle the authentication error gracefully and return appropriate error responses

### Requirement 3

**User Story:** As a backend service, I want to discover available tracks and sessions from S3, so that the API can dynamically list available data without hardcoding track names.

#### Acceptance Criteria

1. WHEN listing available tracks THEN the system SHALL query S3 for all subdirectories under the `data/` prefix
2. WHEN listing sessions for a track THEN the system SHALL query S3 for all files matching the pattern `{session}_lap_start.csv` in that track's directory
3. WHEN S3 queries fail THEN the system SHALL return an empty list and log the error

### Requirement 4

**User Story:** As a developer, I want the system to support both local and S3 data sources, so that I can develop locally without requiring AWS credentials.

#### Acceptance Criteria

1. WHEN the environment variable `USE_S3_DATA` is set to `true` THEN the Data Loader SHALL use the S3 data source
2. WHEN the environment variable `USE_S3_DATA` is set to `false` or not set THEN the Data Loader SHALL use the local file system data source
3. WHEN switching between data sources THEN the system SHALL maintain the same API interface and return data in the same format

### Requirement 5

**User Story:** As a deployment engineer, I want clear documentation for AWS setup, so that I can configure S3 hosting without prior AWS experience.

#### Acceptance Criteria

1. WHEN reading the setup guide THEN the documentation SHALL provide step-by-step instructions for creating an AWS account
2. WHEN reading the setup guide THEN the documentation SHALL provide step-by-step instructions for creating an S3 bucket with appropriate permissions
3. WHEN reading the setup guide THEN the documentation SHALL provide step-by-step instructions for creating IAM credentials
4. WHEN reading the setup guide THEN the documentation SHALL provide instructions for configuring environment variables in Render
5. WHEN reading the setup guide THEN the documentation SHALL include cost estimates and troubleshooting guidance

### Requirement 6

**User Story:** As a system operator, I want the S3 integration to handle various file naming patterns, so that data from different sources can be loaded successfully.

#### Acceptance Criteria

1. WHEN loading lap times THEN the system SHALL attempt multiple filename patterns including underscores and hyphens
2. WHEN a file is not found with the first pattern THEN the system SHALL try alternative patterns before returning None
3. WHEN loading telemetry data THEN the system SHALL attempt multiple filename patterns including underscores and hyphens
