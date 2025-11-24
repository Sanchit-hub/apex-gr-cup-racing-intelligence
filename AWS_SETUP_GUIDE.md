# AWS S3 Setup Guide for APEX

## 🎯 Overview

This guide will help you set up AWS S3 to host all race data (3GB+) for your APEX deployment. By using S3, you can deploy the full application with all 7 tracks without hitting deployment size limits on Render or Netlify.

---

## 📋 Prerequisites

1. **AWS Account** (free tier available)
2. **AWS CLI** (optional but recommended)
3. **All race data extracted** locally in the `data/` directory

---

## 🚀 Step-by-Step Setup

### **Step 1: Create AWS Account**

1. Go to [aws.amazon.com](https://aws.amazon.com)
2. Click "Create an AWS Account"
3. Follow the signup process (requires credit card but free tier available)
4. Complete email verification

### **Step 2: Create S3 Bucket**

1. **Login to AWS Console**: [console.aws.amazon.com](https://console.aws.amazon.com)
2. **Search for "S3"** in the services search bar
3. **Click "Create bucket"**
4. **Bucket settings**:
   - **Bucket name**: `apex-racing-data` (must be globally unique - if taken, try `apex-racing-data-yourname`)
   - **AWS Region**: `us-east-1` (or closest to your target audience)
   - **Object Ownership**: ACLs enabled
   - **Block Public Access settings**: **Uncheck "Block all public access"**
     - ⚠️ Acknowledge the warning (we need public read access for the data)
   - **Bucket Versioning**: Disabled
   - **Default encryption**: Amazon S3-managed keys (SSE-S3)
5. **Click "Create bucket"**

### **Step 3: Configure Bucket Policy for Public Read**

1. **Open your bucket** in the S3 console
2. **Go to "Permissions" tab**
3. **Scroll to "Bucket policy"** and click "Edit"
4. **Paste this policy** (replace `apex-racing-data` with your bucket name):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::apex-racing-data/*"
    }
  ]
}
```

5. **Click "Save changes"**

### **Step 4: Create IAM User for Upload**

1. **Go to IAM service** in AWS Console
2. **Click "Users"** → **"Create user"**
3. **User details**:
   - **User name**: `apex-s3-uploader`
   - Click "Next"
4. **Set permissions**:
   - Select **"Attach policies directly"**
   - Search for and select: **`AmazonS3FullAccess`**
   - Click "Next"
5. **Review and create user**
6. **Create access key**:
   - Click on the newly created user
   - Go to "Security credentials" tab
   - Click "Create access key"
   - Select "Command Line Interface (CLI)"
   - Check the confirmation box
   - Click "Create access key"
7. **IMPORTANT**: Save the Access Key ID and Secret Access Key
   - Download the CSV file or copy them to a secure location
   - You won't be able to see the secret key again!

### **Step 5: Upload Data to S3**

#### **Option A: Using the Upload Script (Recommended)**

1. **Set environment variables** (Windows CMD):
   ```cmd
   set AWS_ACCESS_KEY_ID=your_access_key_here
   set AWS_SECRET_ACCESS_KEY=your_secret_key_here
   set AWS_REGION=us-east-1
   set S3_BUCKET_NAME=apex-racing-data
   ```

   Or for PowerShell:
   ```powershell
   $env:AWS_ACCESS_KEY_ID="your_access_key_here"
   $env:AWS_SECRET_ACCESS_KEY="your_secret_key_here"
   $env:AWS_REGION="us-east-1"
   $env:S3_BUCKET_NAME="apex-racing-data"
   ```

2. **Install boto3** (if not already installed):
   ```bash
   pip install boto3
   ```

3. **Run upload script**:
   ```bash
   python upload_to_s3.py
   ```

4. **Wait for upload to complete** (15-30 minutes depending on internet speed)

#### **Option B: Using AWS Console (Manual)**

1. **Go to your S3 bucket** in AWS Console
2. **Click "Upload"**
3. **Click "Add folder"** and select your `data` folder
4. **Click "Upload"** (will take 15-30 minutes)
5. **Wait for upload to complete**

### **Step 6: Verify Upload**

1. **Go to your S3 bucket** in AWS Console
2. **Navigate to `data/` folder**
3. **Verify you see all track folders**:
   - `barber_motorsports_park/`
   - `circuit_of_the_americas/`
   - `indianapolis/`
   - `road_america/`
   - `sebring/`
   - `sonoma/`
   - `virginia_international_raceway/`
4. **Click into a track folder** and verify CSV files are present

### **Step 7: Configure Render Deployment**

1. **Go to Render Dashboard**: [dashboard.render.com](https://dashboard.render.com)
2. **Find your service**: `apex-backend`
3. **Go to "Environment" tab**
4. **Add environment variables**:
   - `USE_S3_DATA` = `true`
   - `S3_BUCKET_NAME` = `apex-racing-data` (or your bucket name)
   - `AWS_ACCESS_KEY_ID` = `your_access_key`
   - `AWS_SECRET_ACCESS_KEY` = `your_secret_key`
   - `AWS_REGION` = `us-east-1`
5. **Click "Save Changes"**
6. **Render will automatically redeploy** with the new configuration

---

## ✅ Verification

### **Test S3 Access**

1. **Check bucket contents**:
   - Go to S3 console
   - Open your bucket
   - Verify `data/` folder with all tracks

2. **Test API**:
   - Visit: `https://your-backend-url.onrender.com/docs`
   - Try `/api/analytics/tracks` endpoint
   - Should return all 7 tracks

3. **Test Frontend**:
   - Visit your frontend URL
   - Select different tracks from dropdown
   - Verify data loads correctly

---

## 💰 Cost Estimate

**AWS S3 Free Tier** (first 12 months):
- ✅ 5GB storage (enough for race data)
- ✅ 20,000 GET requests per month
- ✅ 2,000 PUT requests per month

**After Free Tier** (or if exceeded):
- Storage: ~$0.023 per GB per month
- GET requests: ~$0.0004 per 1,000 requests
- PUT requests: ~$0.005 per 1,000 requests

**Estimated monthly cost for APEX**:
- Storage (3GB): ~$0.07/month
- Requests (10,000 GET): ~$0.004/month
- **Total**: ~$0.10 - $0.50/month

💡 **Tip**: The free tier is more than enough for development and moderate production use!

---

## 🔧 Troubleshooting

### **"Access Denied" Error**

**Symptoms**: API returns 403 errors when trying to load data

**Solutions**:
- ✅ Check IAM user has S3 permissions
- ✅ Verify bucket policy allows public read (see Step 3)
- ✅ Check AWS credentials in Render environment variables
- ✅ Ensure bucket name matches in environment variables

### **"Bucket Not Found" Error**

**Symptoms**: API returns "NoSuchBucket" error

**Solutions**:
- ✅ Verify bucket name is correct in environment variables
- ✅ Check AWS region matches (us-east-1)
- ✅ Ensure bucket exists and is accessible
- ✅ Try accessing bucket directly in S3 console

### **Upload Fails**

**Symptoms**: Upload script fails or times out

**Solutions**:
- ✅ Check internet connection
- ✅ Verify AWS credentials are correct
- ✅ Try uploading smaller batches
- ✅ Check AWS CLI is configured: `aws s3 ls`
- ✅ Verify IAM user has S3 write permissions

### **Data Not Loading in Frontend**

**Symptoms**: Frontend shows "No data available" or loading errors

**Solutions**:
- ✅ Check browser console for errors
- ✅ Verify backend API is returning data: `/api/analytics/tracks`
- ✅ Check Render logs for S3 errors
- ✅ Verify `USE_S3_DATA=true` in Render environment
- ✅ Test S3 URL directly: `https://apex-racing-data.s3.amazonaws.com/data/barber_motorsports_park/`

### **High AWS Costs**

**Symptoms**: Unexpected AWS charges

**Solutions**:
- ✅ Check S3 usage in AWS Cost Explorer
- ✅ Verify you're within free tier limits
- ✅ Consider adding CloudFront CDN for caching
- ✅ Review S3 access logs for unusual activity
- ✅ Set up AWS Budgets to alert on spending

---

## 🔒 Security Best Practices

### **IAM User Permissions**

- ✅ Use separate IAM users for upload vs. read-only access
- ✅ Rotate access keys periodically (every 90 days)
- ✅ Never commit AWS credentials to version control
- ✅ Use environment variables for all credentials

### **Bucket Security**

- ✅ Enable S3 access logging for audit trail
- ✅ Use bucket policies to restrict access
- ✅ Consider using AWS Secrets Manager for production
- ✅ Monitor CloudWatch for unusual access patterns

### **Data Privacy**

- ✅ Telemetry data is anonymized (no PII)
- ✅ Public read access is acceptable for this use case
- ✅ Consider private bucket + pre-signed URLs for sensitive data

---

## 🎯 Next Steps

After completing setup:

1. ✅ **Test locally** with S3 data (set `USE_S3_DATA=true` in `.env`)
2. ✅ **Deploy to Render** with S3 configuration
3. ✅ **Verify frontend** connects to all tracks
4. ✅ **Monitor AWS costs** in first month
5. ✅ **Submit to hackathon** with full data! 🏁

---

## 📚 Additional Resources

- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [AWS Free Tier Details](https://aws.amazon.com/free/)
- [boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Render Environment Variables](https://render.com/docs/environment-variables)

---

**Total setup time**: 30-45 minutes  
**Data upload time**: 15-30 minutes  
**Cost**: Free tier (or <$1/month)

**Result**: Full 7-track deployment with all data! 🏁🚀
