# Render Deployment Guide - APEX with AWS S3

## 🎯 Quick Deployment Checklist

- [ ] AWS S3 data uploaded (in progress)
- [ ] Render environment variables configured
- [ ] Backend deployed and verified
- [ ] Frontend connected to backend
- [ ] All 7 tracks tested

---

## 📋 Step-by-Step Deployment

### Step 1: Configure Render Environment Variables

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Select your service**: `apex-backend`
3. **Navigate to**: Environment tab
4. **Add these environment variables**:

```bash
USE_S3_DATA=true
S3_BUCKET_NAME=apex-racing-data
AWS_ACCESS_KEY_ID=<your-aws-access-key-id>
AWS_SECRET_ACCESS_KEY=<your-aws-secret-access-key>
AWS_REGION=us-east-1
```

5. **Click "Save Changes"**
6. Render will automatically trigger a redeploy

### Step 2: Verify Backend Deployment

**Wait for deployment to complete** (~5 minutes)

Then test these endpoints:

1. **Health Check**:
   ```
   https://apex-backend-7orz.onrender.com/health
   ```
   Expected: `{"status": "healthy"}`

2. **List Tracks**:
   ```
   https://apex-backend-7orz.onrender.com/api/analytics/tracks
   ```
   Expected: Array with 7 tracks

3. **Get Sessions for a Track**:
   ```
   https://apex-backend-7orz.onrender.com/api/analytics/track/barber_motorsports_park/sessions
   ```
   Expected: Array with session names (R1, R2, etc.)

### Step 3: Test Each Track

Test all 7 tracks to ensure S3 data loading works:

- [ ] **Barber Motorsports Park**
  ```
  /api/analytics/track/barber_motorsports_park/sessions
  ```

- [ ] **Circuit of the Americas (COTA)**
  ```
  /api/analytics/track/COTA/sessions
  ```

- [ ] **Indianapolis**
  ```
  /api/analytics/track/indianapolis/sessions
  ```

- [ ] **Road America**
  ```
  /api/analytics/track/road-america/sessions
  ```

- [ ] **Sebring**
  ```
  /api/analytics/track/sebring/sessions
  ```

- [ ] **Sonoma**
  ```
  /api/analytics/track/Sonoma/sessions
  ```

- [ ] **Virginia International Raceway (VIR)**
  ```
  /api/analytics/track/virginia-international-raceway/sessions
  ```

### Step 4: Verify Frontend Connection

1. **Open Frontend**: https://apex-gr-cup.netlify.app
2. **Test Track Selection**: Try selecting different tracks from dropdown
3. **Verify Data Loads**: Check that lap times and telemetry display correctly
4. **Test All Features**:
   - Lap time analysis
   - Driver performance
   - Sector analysis
   - Best lap calculations

---

## 🔍 Troubleshooting

### Backend Returns 500 Errors

**Check Render Logs**:
1. Go to Render Dashboard
2. Select `apex-backend`
3. Click "Logs" tab
4. Look for S3-related errors

**Common Issues**:
- AWS credentials incorrect → Verify environment variables
- S3 bucket not found → Check bucket name is `apex-racing-data`
- Files not uploaded → Wait for upload to complete

### Tracks Not Loading

**Verify S3 Upload**:
1. Go to AWS S3 Console
2. Open `apex-racing-data` bucket
3. Check `data/` folder contains all tracks
4. Verify CSV files are present

**Check File Names**:
- Files should follow pattern: `R1_trackname_lap_start.csv`
- Track folders should match API expectations

### Frontend Shows "No Data"

**Check CORS**:
- Backend should allow all origins (already configured)
- Verify backend URL in frontend is correct

**Check API Response**:
- Use browser DevTools → Network tab
- Verify API calls are successful (200 status)
- Check response contains data

---

## 📊 Performance Monitoring

### Expected Response Times

- `/health`: < 100ms
- `/api/analytics/tracks`: < 200ms
- `/api/analytics/track/{track}/sessions`: < 500ms
- `/api/analytics/track/{track}/session/{session}/best-lap`: < 2s

### S3 Data Loading

- Small files (< 1MB): ~100-300ms
- Large files (> 50MB): ~1-3s
- Acceptable for analytics use case

---

## 🎉 Success Criteria

Your deployment is successful when:

✅ All 7 tracks return sessions  
✅ Lap time data loads for each track  
✅ Frontend displays data correctly  
✅ No 500 errors in Render logs  
✅ Response times are acceptable  

---

## 🚀 Post-Deployment

### Monitor AWS Costs

1. **Go to AWS Cost Explorer**
2. **Check S3 usage**:
   - Storage: Should be ~3GB
   - Requests: Monitor GET requests
3. **Set up billing alerts** (optional):
   - Alert if cost > $1/month

### Update Documentation

- [ ] Update README with live demo links
- [ ] Add S3 deployment notes
- [ ] Document any track-specific quirks

### Hackathon Submission

- [ ] Verify all features work
- [ ] Take screenshots/video
- [ ] Update submission with S3 deployment info
- [ ] Highlight scalability improvements

---

## 📞 Support

If you encounter issues:

1. **Check Render Logs** first
2. **Verify S3 bucket** contents
3. **Test API endpoints** directly
4. **Review AWS_SETUP_GUIDE.md** for S3 configuration

---

**Deployment Time**: ~10 minutes (after S3 upload completes)  
**Result**: Production-ready APEX with all 7 tracks! 🏁
