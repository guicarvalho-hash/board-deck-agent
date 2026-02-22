# Board Deck Agent Setup Guide

This guide will help you get the Board Deck Agent up and running to automatically process your meeting minutes and compile insights for your board presentations.

## Overview

The Board Deck Agent automatically:
1. Monitors your Gmail inbox for meeting minutes
2. Extracts key insights using AI (OpenAI GPT-4)
3. Categorizes insights into: What Went Well, What Went Wrong, What's Next
4. Stores and updates a compilation of all insights
5. Emails you the updated compilation after processing new meetings

## Prerequisites

- Python 3.8 or higher
- Gmail account
- OpenAI API account
- Google Cloud Project (for Gmail API access)

## Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Set Up Google Cloud Project and Gmail API

### 2.1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Create Project" or select an existing project
3. Give it a name like "Board Deck Agent"

### 2.2: Enable Gmail API

1. In your Google Cloud Console, go to "APIs & Services" > "Library"
2. Search for "Gmail API"
3. Click on it and press "Enable"

### 2.3: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - User Type: External (or Internal if you have Google Workspace)
   - App name: Board Deck Agent
   - User support email: Your email
   - Developer contact: Your email
   - Scopes: Add the Gmail API scopes (gmail.readonly, gmail.send)
   - Test users: Add your email address
4. Back to "Create Credentials" > "OAuth client ID"
5. Application type: "Desktop app"
6. Name: "Board Deck Agent Desktop"
7. Click "Create"
8. Download the JSON file
9. Rename it to `credentials.json` and place it in the project root directory

## Step 3: Get OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Go to API Keys section
4. Create a new API key
5. Copy the key (you won't be able to see it again)

## Step 4: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your information:
   ```
   OPENAI_API_KEY=sk-your-actual-openai-api-key-here
   USER_EMAIL=your.email@example.com
   SENDER_EMAIL=your.email@example.com
   DATA_FILE=board_insights.json
   CHECK_INTERVAL_MINUTES=15
   ```

## Step 5: First Run and Authentication

Run the agent for the first time:

```bash
python main.py --mode once
```

On the first run:
1. A browser window will open asking you to log in to your Google account
2. Grant the requested permissions (read and send emails)
3. The agent will save the authentication token for future use

## Step 6: Test the Setup

### Option A: Test with Existing Emails

If you have recent emails with meeting minutes:
```bash
python main.py --mode once
```

### Option B: Test with a Sample Meeting Minutes Email

Send yourself a test email with "Meeting Minutes" in the subject and some content about a meeting. Then run:
```bash
python main.py --mode once
```

## Step 7: Run in Continuous Mode

Once everything is working, you can run the agent in continuous mode:

```bash
python main.py --mode continuous
```

This will:
- Check for new meeting minutes every 15 minutes (configurable in .env)
- Process any new meetings automatically
- Send you email updates when new insights are compiled
- Keep running until you stop it (Ctrl+C)

## Usage Modes

### Single Check Mode
Run once and exit:
```bash
python main.py --mode once
```

### Continuous Monitoring Mode
Keep monitoring for new meetings:
```bash
python main.py --mode continuous
```

### Clear All Insights
Start fresh (useful at the beginning of each month):
```bash
python main.py --clear
```

## File Structure

After setup, your directory will look like:
```
board-deck-agent/
├── main.py                 # Main application
├── email_monitor.py        # Gmail integration
├── insight_analyzer.py     # AI analysis
├── insight_store.py        # Data storage
├── requirements.txt        # Dependencies
├── .env                    # Your configuration (not committed)
├── .env.example           # Configuration template
├── credentials.json       # Google OAuth credentials (not committed)
├── token.json            # Gmail auth token (generated, not committed)
├── board_insights.json   # Stored insights (generated)
└── README.md             # This file
```

## Running as a Background Service

### On Linux/Mac (using systemd)

Create a service file `/etc/systemd/system/board-deck-agent.service`:

```ini
[Unit]
Description=Board Deck Agent
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/board-deck-agent
ExecStart=/usr/bin/python3 /path/to/board-deck-agent/main.py --mode continuous
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable board-deck-agent
sudo systemctl start board-deck-agent
```

### On Windows (using Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Name: "Board Deck Agent"
4. Trigger: At startup
5. Action: Start a program
6. Program: `python`
7. Arguments: `C:\path\to\board-deck-agent\main.py --mode continuous`
8. Start in: `C:\path\to\board-deck-agent`

### Using Docker (Recommended for Production)

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py", "--mode", "continuous"]
```

Build and run:
```bash
docker build -t board-deck-agent .
docker run -d --name board-deck-agent \
  -v $(pwd)/credentials.json:/app/credentials.json \
  -v $(pwd)/token.json:/app/token.json \
  -v $(pwd)/.env:/app/.env \
  -v $(pwd)/board_insights.json:/app/board_insights.json \
  board-deck-agent
```

## Troubleshooting

### "credentials.json not found"
- Make sure you've downloaded the OAuth credentials from Google Cloud Console
- Rename the file to exactly `credentials.json`
- Place it in the project root directory

### "OPENAI_API_KEY not set"
- Check your `.env` file
- Make sure the key starts with `sk-`
- Ensure there are no extra spaces or quotes

### "No new messages found"
- The agent only checks unread emails from the last 7 days
- Make sure your test email contains keywords like "meeting minutes" in the subject or body
- Check that the email is unread

### "Permission denied" errors
- Re-run the authentication: delete `token.json` and run the agent again
- Make sure you granted all requested permissions during OAuth flow

### Gmail API quota exceeded
- The free tier allows 1 billion quota units per day
- Each API call uses a small amount
- For normal use (checking every 15 minutes), you'll be well within limits

## Monthly Workflow

At the end of each month:

1. Review your compiled insights:
   ```bash
   python main.py --mode once
   ```

2. Copy the insights to your board deck presentation

3. Clear the insights for the new month:
   ```bash
   python main.py --clear
   ```

## Security Notes

- Never commit `credentials.json`, `token.json`, or `.env` to version control
- Keep your OpenAI API key secure
- Regularly review OAuth permissions in your Google Account settings
- The agent only reads emails and sends to your configured email address

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the error messages in the console output
3. Ensure all prerequisites are met
4. Verify your configuration in `.env`

## What's Next?

Once set up, the agent will:
- Automatically monitor your inbox
- Process new meeting minutes as they arrive
- Keep your board deck insights up to date
- Email you when new insights are added

Simply forward meeting minutes to your email or ensure they're sent to your configured email address, and the agent will handle the rest!
