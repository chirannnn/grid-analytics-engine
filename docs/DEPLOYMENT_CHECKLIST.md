# WindLens Deployment Checklist

## Pre-Deployment Verification
- [x] Backend tests pass (11/11)
- [x] Frontend production build succeeds
- [x] Docker Compose configuration valid
- [x] Local stack runs successfully
- [x] All API endpoints functional
- [x] Environment variables documented
- [x] Secrets excluded from Git (.env gitignored)
- [x] No mock data presented as real

## Frontend Deployment (Vercel)

### Prerequisites
- [ ] Vercel account created
- [ ] Git repository connected to Vercel

### Steps
1. [ ] Import repository in Vercel
2. [ ] Set Root Directory to `frontend`
3. [ ] Build Command: `npm run build` (auto-detected)
4. [ ] Output Directory: `dist` (auto-detected)
5. [ ] Add Environment Variable: `VITE_API_BASE_URL` = your Render backend URL (e.g., https://windlens-api.onrender.com)
6. [ ] Deploy
7. [ ] Test deployed frontend loads correctly
8. [ ] Verify API calls reach backend

## Backend Deployment (Render)

### Prerequisites
- [ ] Render account created
- [ ] Repository connected

### Steps
1. [ ] Create new Web Service
2. [ ] Connect Git repository
3. [ ] Root Directory: `backend`
4. [ ] Environment: `Python 3`
5. [ ] Build Command: `pip install -r requirements.txt`
6. [ ] Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
7. [ ] Add Environment Variables:
   - `DEBUG=False`
   - `CORS_ORIGINS=["https://your-vercel-app.vercel.app"]`
   - `ELEXON_BASE_URL=https://data.elexon.co.uk/bmrs/api/v1`
   - `ELEXON_API_KEY=` (leave empty if not required)
   - `DECISION_CUTOFF_HOUR=10`
   - `DECISION_CUTOFF_MINUTE=0`
   - `TIMEZONE=Europe/London`
   - `EVALUATION_YEAR=2026`
   - `EVALUATION_MONTH=1`
8. [ ] Deploy
9. [ ] Test health endpoint: `https://your-backend.onrender.com/api/health`
10. [ ] Test ready endpoint: `https://your-backend.onrender.com/api/health/ready`
11. [ ] Update Vercel env var with backend URL

## Post-Deployment
- [ ] Frontend loads without errors
- [ ] All API calls succeed
- [ ] Charts render with data
- [ ] Update README with actual URLs
- [ ] Test on production

## Notes
- Elexon API is public, no key required
- Free tier services may have cold starts
- CORS must be configured with actual Vercel URL
- Never commit secrets
