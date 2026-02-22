# Quick Start Guide

Get your Board Deck Agent running in 4 simple steps.

## Prerequisites Checklist

Before starting, make sure you have:
- [ ] Python 3.8 or higher installed
- [ ] A Gmail account
- [ ] An OpenAI account (sign up at https://platform.openai.com/)
- [ ] 20 minutes to complete setup

## Step 1: Install Dependencies (2 minutes)

```bash
cd /path/to/board-deck-agent
pip install -r requirements.txt
```

## Step 2: Set Up Google Cloud & Gmail API (10 minutes)

### 2.1 Create Google Cloud Project
1. Go to https://console.cloud.google.com/
2. Click "New Project"
3. Name it "Board Deck Agent"
4. Click "Create"

### 2.2 Enable Gmail API
1. In the project, go to "APIs & Services" → "Library"
2. Search for "Gmail API"
3. Click "Enable"

### 2.3 Create OAuth Credentials
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure consent screen:
   - Choose "External"
   - Fill in required fields (app name, your email)
   - Add scope: `https://www.googleapis.com/auth/gmail.readonly`
   - Add scope: `https://www.googleapis.com/auth/gmail.send`
   - Add your email as test user
   - Save
4. Back to "Create Credentials" → "OAuth client ID"
5. Choose "Desktop app"
6. Name it "Board Deck Agent"
7. Click "Create"
8. Download the JSON file
9. Rename it to `credentials.json`
10. Move it to the project directory

## Step 3: Configure Environment (3 minutes)

### 3.1 Get OpenAI API Key
1. Go to https://platform.openai.com/
2. Sign up or log in
3. Go to "API Keys"
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)

### 3.2 Set Up Configuration
```bash
# Copy the example file
cp .env.example .env

# Edit .env file
nano .env  # or use your favorite editor
```

Update these values in `.env`:
```
OPENAI_API_KEY=sk-your-actual-key-here
USER_EMAIL=your.email@gmail.com
```

Save and close the file.

## Step 4: Run the Agent (5 minutes)

### First Time Setup
```bash
# Verify your setup
python test_setup.py

# Run the agent once
python main.py --mode once
```

On first run:
- A browser will open
- Log in to your Google account
- Grant permissions
- Close the browser

The agent is now ready!

### Test It

Send yourself a test email:
- Subject: "Team Meeting Minutes"
- Body: Copy content from SAMPLE_MEETING.md

Then run:
```bash
python main.py --mode once
```

You should see the agent:
1. Find your email
2. Analyze the content
3. Extract insights
4. Send you a summary

### Run Continuously

To monitor emails automatically:
```bash
python main.py --mode continuous
```

Press Ctrl+C to stop.

## What Happens Next?

The agent will:
1. **Check your inbox** every 15 minutes for emails with meeting minutes
2. **Analyze** the content using AI
3. **Extract** key insights into three categories
4. **Store** them in `board_insights.json`
5. **Email you** the updated compilation

## Monthly Workflow

### During the Month
- Let the agent run continuously: `python main.py --mode continuous`
- Or check periodically: `python main.py --mode once`
- Insights accumulate automatically

### End of Month
1. Copy insights to your board deck presentation
2. Clear for next month: `python main.py --clear`

## Troubleshooting

### "No module named X"
```bash
pip install -r requirements.txt
```

### "credentials.json not found"
- Download OAuth credentials from Google Cloud Console
- Rename to `credentials.json`
- Place in project directory

### "Invalid API key"
- Check your `.env` file
- Make sure OPENAI_API_KEY is correct
- No spaces or quotes around the key

### "No new messages found"
- Make sure test email is unread
- Check that subject/body contains "meeting minutes" or similar keywords
- The agent only checks emails from the last 7 days

## Advanced Usage

### Run as Background Service

**Linux/Mac:**
```bash
nohup python main.py --mode continuous > agent.log 2>&1 &
```

**Docker:**
```bash
docker-compose up -d
```

### View Current Insights

The insights are stored in `board_insights.json`. You can:
- Open it in any text editor
- Run `python main.py --mode once` to see a summary
- Check the email notifications

## Need Help?

1. Run the setup verification: `python test_setup.py`
2. Check SETUP.md for detailed instructions
3. Review error messages in console output

## Success! 🎉

You now have an automated assistant that:
- ✅ Monitors your email for meeting minutes
- ✅ Extracts key insights using AI
- ✅ Organizes them for your board presentation
- ✅ Keeps you updated automatically

Focus on your meetings, let the agent handle the compilation!
