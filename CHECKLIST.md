# What You Need To Do - Complete Checklist

This is your action plan to get the Board Deck Agent up and running immediately.

## Time Required: ~20 Minutes

---

## Part 1: Google Cloud Setup (10 minutes)

### Step 1.1: Create Google Cloud Project (2 min)
- [ ] Go to https://console.cloud.google.com/
- [ ] Click "Select a project" dropdown at top
- [ ] Click "New Project"
- [ ] Name: "Board Deck Agent"
- [ ] Click "Create"
- [ ] Wait for project creation
- [ ] Select the new project

### Step 1.2: Enable Gmail API (1 min)
- [ ] In left menu: "APIs & Services" → "Library"
- [ ] Search: "Gmail API"
- [ ] Click on "Gmail API"
- [ ] Click "Enable" button
- [ ] Wait for activation

### Step 1.3: Configure OAuth Consent Screen (3 min)
- [ ] In left menu: "APIs & Services" → "OAuth consent screen"
- [ ] Select "External" user type
- [ ] Click "Create"
- [ ] Fill in required fields:
  - App name: "Board Deck Agent"
  - User support email: (your email)
  - Developer contact: (your email)
- [ ] Click "Save and Continue"
- [ ] Click "Add or Remove Scopes"
- [ ] Search and add these scopes:
  - `https://www.googleapis.com/auth/gmail.readonly`
  - `https://www.googleapis.com/auth/gmail.send`
- [ ] Click "Update" then "Save and Continue"
- [ ] Click "Add Users"
- [ ] Add your email address
- [ ] Click "Save and Continue"
- [ ] Review summary and click "Back to Dashboard"

### Step 1.4: Create OAuth Credentials (2 min)
- [ ] In left menu: "APIs & Services" → "Credentials"
- [ ] Click "Create Credentials" button at top
- [ ] Select "OAuth client ID"
- [ ] Application type: "Desktop app"
- [ ] Name: "Board Deck Agent Desktop"
- [ ] Click "Create"
- [ ] In popup, click "Download JSON"
- [ ] Save the file
- [ ] Rename downloaded file to: `credentials.json`
- [ ] Move `credentials.json` to your project directory

### Step 1.5: Verify Files (1 min)
- [ ] Confirm `credentials.json` is in project root
- [ ] File should be ~500-1000 bytes
- [ ] Contains: client_id, client_secret, redirect_uris

✅ **Google Cloud setup complete!**

---

## Part 2: OpenAI Setup (5 minutes)

### Step 2.1: Create OpenAI Account (2 min)
- [ ] Go to https://platform.openai.com/
- [ ] Click "Sign up" (or "Log in" if you have account)
- [ ] Complete registration

### Step 2.2: Set Up Billing (2 min)
- [ ] Go to https://platform.openai.com/account/billing
- [ ] Click "Add payment method"
- [ ] Add credit card (note: ~$1-2/month usage)
- [ ] Set usage limits if desired (recommended: $10/month)

### Step 2.3: Create API Key (1 min)
- [ ] Go to https://platform.openai.com/api-keys
- [ ] Click "Create new secret key"
- [ ] Name: "Board Deck Agent"
- [ ] Copy the key (starts with `sk-`)
- [ ] Save it somewhere temporarily (you'll need it in next step)
- [ ] ⚠️ You won't see this key again!

✅ **OpenAI setup complete!**

---

## Part 3: Project Configuration (3 minutes)

### Step 3.1: Install Dependencies (1 min)
```bash
cd /path/to/board-deck-agent
pip install -r requirements.txt
```
- [ ] Run the command above
- [ ] Wait for installation to complete
- [ ] Should see "Successfully installed" messages

### Step 3.2: Create Environment File (1 min)
```bash
cp .env.example .env
```
- [ ] Run the command above
- [ ] Verify `.env` file created

### Step 3.3: Configure Environment (1 min)
- [ ] Open `.env` in text editor
- [ ] Update `OPENAI_API_KEY=` with your key from Step 2.3
- [ ] Update `USER_EMAIL=` with your Gmail address
- [ ] Leave other settings as default
- [ ] Save and close file

Your `.env` should look like:
```
OPENAI_API_KEY=sk-proj-abc123...
USER_EMAIL=you@gmail.com
SENDER_EMAIL=you@gmail.com
DATA_FILE=board_insights.json
CHECK_INTERVAL_MINUTES=15
```

✅ **Configuration complete!**

---

## Part 4: First Run & Authentication (2 minutes)

### Step 4.1: Verify Setup (1 min)
```bash
python test_setup.py
```
- [ ] Run the command above
- [ ] All tests should pass (5/5)
- [ ] If any fail, check error messages and fix

### Step 4.2: First Authentication (1 min)
```bash
python main.py --mode once
```
- [ ] Run the command above
- [ ] Browser window will open automatically
- [ ] Log in to your Gmail account
- [ ] Click "Allow" to grant permissions
- [ ] Browser will show "Authentication successful"
- [ ] Close browser window
- [ ] Return to terminal

✅ **Authentication complete!**

---

## Part 5: Test the Agent (3 minutes)

### Step 5.1: Send Test Email (1 min)
- [ ] Open Gmail
- [ ] Compose new email
- [ ] To: (your email)
- [ ] Subject: "Test Meeting Minutes - Product Review"
- [ ] Body: (copy from SAMPLE_MEETING.md or write any meeting notes)
- [ ] Send email
- [ ] Leave email unread

### Step 5.2: Run Agent (1 min)
```bash
python main.py --mode once
```
- [ ] Run the command above
- [ ] Agent should find your test email
- [ ] Should analyze and extract insights
- [ ] Should send you a summary email
- [ ] Check output for success messages

### Step 5.3: Verify Results (1 min)
- [ ] Check your email for summary from agent
- [ ] Open `board_insights.json` to see stored data
- [ ] Verify insights are categorized correctly

✅ **Testing complete!**

---

## Part 6: Start Continuous Monitoring (1 minute)

### Option A: Run in Foreground
```bash
python main.py --mode continuous
```
- [ ] Run command above
- [ ] Keep terminal open
- [ ] Press Ctrl+C to stop

### Option B: Run in Background (Linux/Mac)
```bash
nohup python main.py --mode continuous > agent.log 2>&1 &
```
- [ ] Run command above
- [ ] Check `agent.log` for output
- [ ] Agent runs in background

### Option C: Run with Docker
```bash
docker-compose up -d
```
- [ ] Run command above
- [ ] View logs: `docker-compose logs -f`
- [ ] Stop: `docker-compose down`

✅ **Agent is now running!**

---

## Summary Checklist

- [ ] Google Cloud Project created
- [ ] Gmail API enabled
- [ ] OAuth consent configured
- [ ] OAuth credentials downloaded as `credentials.json`
- [ ] OpenAI account created
- [ ] OpenAI API key generated
- [ ] Dependencies installed
- [ ] `.env` file configured
- [ ] Setup verification passed
- [ ] First authentication completed
- [ ] Test email processed successfully
- [ ] Summary email received
- [ ] Agent running in desired mode

---

## What Happens Now?

The agent will automatically:

1. **Monitor** your Gmail inbox every 15 minutes
2. **Detect** emails with meeting minutes
3. **Analyze** the content using AI
4. **Extract** insights in three categories:
   - 🎉 What Went Well
   - ⚠️ What Went Wrong
   - 🚀 What's Next
5. **Store** insights in `board_insights.json`
6. **Email** you updated compilations

---

## Your Monthly Workflow

### During the Month
- Agent runs automatically in background
- Meeting minutes arrive in your inbox
- Agent processes them automatically
- You receive email summaries
- Insights accumulate in storage

### End of Month
1. Review compiled insights (check email or `board_insights.json`)
2. Copy insights to your board deck presentation
3. Clear insights for next month:
   ```bash
   python main.py --clear
   ```

---

## Support & Help

### If Something Goes Wrong

1. **Run diagnostics:**
   ```bash
   python test_setup.py
   ```

2. **Check detailed guides:**
   - Quick start: `QUICKSTART.md`
   - Setup guide: `SETUP.md`
   - Architecture: `ARCHITECTURE.md`

3. **Common issues:**
   - Missing credentials.json → Re-download from Google Cloud
   - Invalid API key → Check .env file
   - No emails found → Send test email with "meeting minutes" in subject
   - Permission errors → Delete token.json and re-authenticate

---

## Cost Breakdown

- **Google Cloud:** $0 (free tier)
- **OpenAI API:** ~$1-2/month (20 meetings)
- **Hosting:** $0 (local) or $5-10/month (cloud)

**Total: ~$1-12/month**

---

## Next Steps After Setup

1. **Customize keywords** (optional)
   - Edit `email_monitor.py` to add custom meeting detection keywords

2. **Adjust check interval** (optional)
   - Change `CHECK_INTERVAL_MINUTES` in `.env`

3. **Set up automatic startup** (optional)
   - Configure systemd service (Linux)
   - Set up Task Scheduler (Windows)
   - Use Docker with restart policy

4. **Integrate with calendar** (future enhancement)
   - Could auto-detect meeting times
   - Request minutes if not received

---

## Success! 🎉

You now have a fully automated assistant that:

✅ Monitors your email continuously
✅ Identifies meeting minutes automatically
✅ Extracts strategic insights using AI
✅ Organizes them for board presentations
✅ Keeps you updated in real-time

**No more manual compilation of meeting insights!**

Focus on your meetings and strategic work. Let the agent handle the administrative task of compiling insights for your board deck.

---

## Questions?

Refer to documentation:
- `README.md` - Overview
- `QUICKSTART.md` - Fast setup
- `SETUP.md` - Detailed setup
- `ARCHITECTURE.md` - How it works
- `SAMPLE_MEETING.md` - Test data

The agent is designed to be simple, reliable, and hands-off. Once set up, it just works!
