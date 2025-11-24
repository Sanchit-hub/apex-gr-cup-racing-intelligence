# 🚀 APEX Deployment Checklist - AWS S3 + Netlify + Render

## Current Status

✅ **AWS S3**: Data uploaded to `apex-racing-data` bucket  
✅ **Netlify**: Frontend deployed  
⚠️ **Render**: Backend deployed but NOT connected to S3  

---

## 🔧 IMMEDIATE ACTION REQUIRED

### Step 1: Add AWS Credentials to Render

**You MUST add AWS credentials to Render for S3 to work!**

1. Go to: https://dashboard.render.com
2. Select your service: `apex-backend`
3. Click **"Environment"** tab
4. Add these secret environment variables:

```
AWS_ACCESS_KEY_ID = <your-aws-access-key-id>
AWS_SECRET_ACCESS_KEY = <your-aws-secret-access-key>
```

5. Click **"Save Changes"**
6. Render will automatically redeploy (~3-5 minutes)

---

## Step 2: Verify Deployment

After Render redeploys, test these endpoints:

### Test 1: Health Check
```
https://apex-backend-7orz.onrender.com/health
```
Expected: `{"status": "healthy"}`

### Test 2: List Tracks
```
https://apex-backend-7orz.onrender.com/api/analytics/tracks
```
Expected: Array with track names

### Test 3: Get Sessions (should work now!)
```
https://apex-backend-7orz.onrender.com/api/analytics/track/indianapolis/sessions
```
Expected: `["R1", "R2"]` (without the "." entry)

### Test 4: Get Best Lap (THIS IS THE KEY TEST!)
```
https://apex-backend-7orz.onrender.com/api/analytics/track/indianapolis/session/R1/best-lap
```
Expected: JSON with lap time data (NOT "No lap time data available")

---

## Step 3: Test Frontend

1. Open: https://apex-gr-cup.netlify.app
2. Select a track from dropdown
3. Verify data loads correctly
4. Test all features work

---

## 🔍 Troubleshooting

### If Step 4 Still Returns "No lap time data available"

**Check Render Logs:**
1. Go to Render Dashboard
2. Click "Logs" tab
3. Look for errors like:
   - `NoCredentialsError`
   - `AccessDenied`
   - `NoSuchBucket`

**Common Issues:**

| Error | Solution |
|-------|----------|
| `NoCredentialsError` | AWS credentials not set in Render |
| `AccessDenied` | IAM user doesn't have S3 read permissions |
| `NoSuchBucket` | Bucket name is wrong (should be `apex-racing-data`) |
| `NoSuchKey` | File structure in S3 doesn't match code expectations |

---

## 📊 Architecture Overview

```
┌─────────────┐
│   Netlify   │  Frontend (React)
│  Frontend   │  https://apex-gr-cup.netlify.app
└──────┬──────┘
       │ API calls via proxy
       ↓
┌─────────────┐
│   Render    │  Backend (FastAPI)
│   Backend   │  https://apex-backend-7orz.onrender.com
└──────┬──────┘
       │ boto3 S3 client
       ↓
┌─────────────┐
│   AWS S3    │  Data Storage (3GB+ CSV files)
│   Bucket    │  apex-racing-data
└─────────────┘
```

---

## 🎯 Success Criteria

Your deployment is working when:

- ✅ Backend health check returns 200
- ✅ Tracks endpoint returns track list
- ✅ Sessions endpoint returns session list
- ✅ **Best lap endpoint returns actual lap data (NOT error)**
- ✅ Frontend loads and displays data
- ✅ All 7 tracks work correctly

---

## 📝 Next Steps After Deployment Works

1. **Test all 7 tracks**:
   - Barber Motorsports Park
   - Circuit of the Americas (COTA)
   - Indianapolis
   - Road America
   - Sebring
   - Sonoma
   - Virginia International Raceway (VIR)

2. **Monitor AWS costs**:
   - Go to AWS Cost Explorer
   - Check S3 storage and request costs
   - Should be < $1/month for this usage

3. **Update documentation**:
   - Add live demo links to README
   - Document any track-specific issues

---

## 🆘 If You're Stuck

**The #1 issue is missing AWS credentials in Render!**

Double-check:
1. AWS_ACCESS_KEY_ID is set in Render
2. AWS_SECRET_ACCESS_KEY is set in Render
3. The IAM user has `s3:GetObject` and `s3:ListBucket` permissions
4. The bucket name is exactly `apex-racing-data`

---

**Last Updated**: After S3 upload complete  
**Status**: Waiting for AWS credentials in Render
