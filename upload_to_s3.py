"""Upload race data to AWS S3."""
import boto3
import os
from pathlib import Path

# AWS Configuration
# You'll need to set these environment variables or replace with your values:
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY
# AWS_REGION (e.g., 'us-east-1')
# S3_BUCKET_NAME (e.g., 'apex-racing-data')

def upload_directory_to_s3(local_directory, bucket_name, s3_prefix=''):
    """Upload a directory to S3.
    
    Args:
        local_directory: Path to local directory to upload
        bucket_name: Name of S3 bucket
        s3_prefix: Prefix for S3 keys (e.g., 'data')
        
    Returns:
        Tuple of (success_count, error_count)
    """
    s3_client = boto3.client('s3')
    
    local_path = Path(local_directory)
    success_count = 0
    error_count = 0
    errors = []
    
    for file_path in local_path.rglob('*'):
        if file_path.is_file():
            # Calculate S3 key preserving directory structure
            relative_path = file_path.relative_to(local_path)
            s3_key = f"{s3_prefix}/{relative_path}".replace('\\', '/')
            
            print(f"📤 Uploading {relative_path}...")
            
            try:
                s3_client.upload_file(
                    str(file_path),
                    bucket_name,
                    s3_key,
                    ExtraArgs={'ACL': 'public-read'}  # Make files publicly readable
                )
                print(f"✅ Uploaded {s3_key}")
                success_count += 1
            except Exception as e:
                print(f"❌ Failed to upload {relative_path}: {e}")
                errors.append((str(relative_path), str(e)))
                error_count += 1
    
    return success_count, error_count, errors

def main():
    """Main upload function with error handling."""
    
    # Get configuration from environment or prompt
    bucket_name = os.getenv('S3_BUCKET_NAME')
    
    if not bucket_name:
        print("⚠️  AWS S3 Configuration Required")
        print("\nYou need to:")
        print("1. Create an S3 bucket on AWS")
        print("2. Set environment variables:")
        print("   - AWS_ACCESS_KEY_ID")
        print("   - AWS_SECRET_ACCESS_KEY")
        print("   - AWS_REGION")
        print("   - S3_BUCKET_NAME")
        print("\nOr run with: python upload_to_s3.py")
        
        bucket_name = input("\nEnter S3 bucket name: ")
    
    # Verify AWS credentials are available
    if not os.getenv('AWS_ACCESS_KEY_ID') or not os.getenv('AWS_SECRET_ACCESS_KEY'):
        print("\n❌ Error: AWS credentials not found!")
        print("Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.")
        return
    
    # Check if data directory exists
    if not Path("data").exists():
        print("\n❌ Error: 'data' directory not found!")
        print("Please ensure race data is extracted to the 'data' directory.")
        return
    
    print(f"\n📦 Uploading data to S3 bucket: {bucket_name}")
    print("This may take 10-15 minutes for all data...\n")
    
    try:
        # Upload data directory
        success_count, error_count, errors = upload_directory_to_s3("data", bucket_name, "data")
        
        print("\n" + "="*60)
        print("📊 Upload Summary")
        print("="*60)
        print(f"✅ Successfully uploaded: {success_count} files")
        print(f"❌ Failed uploads: {error_count} files")
        
        if errors:
            print("\n⚠️  Errors encountered:")
            for file_path, error in errors[:10]:  # Show first 10 errors
                print(f"  - {file_path}: {error}")
            if len(errors) > 10:
                print(f"  ... and {len(errors) - 10} more errors")
        
        if error_count == 0:
            print("\n✅ Upload complete!")
            print(f"\n📝 Your data is now at: https://{bucket_name}.s3.amazonaws.com/data/")
        else:
            print("\n⚠️  Upload completed with errors. Please review and retry failed files.")
            
    except Exception as e:
        print(f"\n❌ Upload failed: {e}")
        print("\nPlease check:")
        print("  - AWS credentials are valid")
        print("  - S3 bucket exists and is accessible")
        print("  - You have write permissions to the bucket")

if __name__ == "__main__":
    main()
