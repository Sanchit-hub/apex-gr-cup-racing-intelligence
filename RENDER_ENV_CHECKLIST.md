# ✅ Render Environment Variables Checklist

## Required Environment Variables

Your Render service needs these environment variables:

| Variable | Value | Status |
|----------|-------|--------|
| `PYTHON_VERSION` | `3.11.9` | ✅ Set in render.yaml |
| `USE_S3_DATA` | `true` | ✅ Set in render.yaml |
| `S3_BUCKET_NAME` | `apex-racing-data` | ✅ Set in render.yaml |
| `AWS_REGION` | `us-east-1` | ✅ Set in render.yaml |
| `AWS_ACCESS_KEY_ID` | `<your-key>` | ❌ **MUST ADD IN DASHBOARD** |
| `AWS_SECRET_ACCESS_KEY` | `<your-secret>` | ❌ **MUST ADD IN DASHBOARD** |

---

## Why Some Are in render.yaml and Some Aren't

### ✅ In render.yaml (Public/Safe)
These are non-sensitive values that can be committed to Git:
- `PYTHON_VERSION` - Just a version number
- `USE_S3_DATA` - Just a boolean flag
- `S3_BUCKET_NAME` - Public bucket name
- `AWS_REGION` - Public region name

### ❌ In Dashboard Only (Secret/Sensitive)
These are sensitive credentials that should NEVER be in Git:
- `AWS_ACCESS_KEY_ID` - Secret credential
- `AWS_SECRET_ACCESS_KEY` - Secret credential

**That's why you need to add them manually in the Render dashboard!**

---

## How to Add Secret Variables

1. Go to Render Dashboard
2. Select `apex-backend` service
3. Click **Environment** tab
4. Click **Add Environment Variable**
5. Add each secret variable:
   - Key: `AWS_ACCESS_KEY_ID`
   - Value: `<paste your key>`
   - Click Add
6. Repeat for `AWS_SECRET_ACCESS_KEY`
7. Click **Save Changes**

---

## Verification

After adding and Render redeploys, check:

```bash
# This should return lap data (not an error)
curl https://apex-backend-7orz.onrender.com/api/analytics/track/indianapolis/session/R1/best-lap
```

---

## Security Note

🔒 **Never commit AWS credentials to Git!**

- ✅ Use environment variables
- ✅ Add them in Render dashboard
- ❌ Don't put them in render.yaml
- ❌ Don't put them in .env files that get committed

The `sync: false` in render.yaml tells Render to expect these values from the dashboard, not from the file.

---

**Action Required**: Add the two secret variables in Render dashboard now!
