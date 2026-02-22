# Board Deck Agent

Automatically compile meeting insights for your board of directors presentations.

## What It Does

The Board Deck Agent monitors your email inbox for meeting minutes and automatically:

1. **Detects** meeting minutes emails based on subject line and content
2. **Analyzes** the content using AI (OpenAI GPT-4)
3. **Categorizes** insights into three key areas:
   - 🎉 **What Went Well** - Achievements, successes, positive developments
   - ⚠️ **What Went Wrong** - Challenges, issues, concerns
   - 🚀 **What's Next** - Action items, future plans, next steps
4. **Compiles** all insights into a structured format
5. **Notifies** you via email when new insights are added

## Why Use This?

If you send monthly board decks and participate in multiple meetings throughout the month, this agent:
- **Saves time** by automatically extracting key points from meeting minutes
- **Ensures completeness** by tracking insights from all meetings
- **Maintains structure** consistent with your board presentation format
- **Operates automatically** so you don't miss important updates

## Quick Start

See [SETUP.md](SETUP.md) for detailed setup instructions.

### Prerequisites
- Python 3.8+
- Gmail account
- OpenAI API key
- Google Cloud Project with Gmail API enabled

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys and email

# Run once
python main.py --mode once

# Or run continuously
python main.py --mode continuous
```

## How It Works

```
┌─────────────────────┐
│  Meeting Minutes    │
│  Arrive via Email   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Email Monitor      │
│  Detects & Fetches  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  AI Analyzer        │
│  Extracts Insights  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Insight Store      │
│  Updates Categories │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Email Notification │
│  Sends You Update   │
└─────────────────────┘
```

## Usage Examples

### Check for new meetings once
```bash
python main.py --mode once
```

### Run continuously (monitors every 15 minutes)
```bash
python main.py --mode continuous
```

### Clear insights at month-end
```bash
python main.py --clear
```

## What You Need to Do

To get this running immediately, you need to:

1. **Set up Google Cloud Project** (10 minutes)
   - Create project at https://console.cloud.google.com/
   - Enable Gmail API
   - Create OAuth 2.0 credentials (Desktop app)
   - Download credentials.json

2. **Get OpenAI API Key** (5 minutes)
   - Sign up at https://platform.openai.com/
   - Create API key
   - Copy the key

3. **Configure the Agent** (2 minutes)
   - Copy .env.example to .env
   - Add your OpenAI API key
   - Add your email address

4. **First Run** (2 minutes)
   - Run `python main.py --mode once`
   - Authenticate with Google (one-time)
   - Agent is now ready!

Total setup time: ~20 minutes

See [SETUP.md](SETUP.md) for detailed step-by-step instructions.

## Configuration

All configuration is in the `.env` file:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key
USER_EMAIL=your.email@example.com

# Optional
CHECK_INTERVAL_MINUTES=15  # How often to check for new emails
DATA_FILE=board_insights.json  # Where to store insights
```

## Output Format

The agent produces a structured compilation:

```
======================================================================
BOARD DECK - MONTHLY INSIGHTS
======================================================================

🎉 WHAT WENT WELL
----------------------------------------------------------------------
• Revenue increased 15% month-over-month exceeding targets
  Source: Q4 Sales Review Meeting
• New feature launch received positive customer feedback
  Source: Product Team Weekly Sync

⚠️ WHAT WENT WRONG
----------------------------------------------------------------------
• Server downtime incident affected 5% of users for 2 hours
  Source: Infrastructure Post-Mortem
• Marketing campaign underperformed by 20%
  Source: Marketing Review Meeting

🚀 WHAT'S NEXT
----------------------------------------------------------------------
• Launch mobile app beta to 1000 users by end of month
  Source: Product Roadmap Planning
• Implement new monitoring system to prevent future outages
  Source: Infrastructure Post-Mortem

======================================================================
```

## Project Structure

```
board-deck-agent/
├── main.py              # Main application entry point
├── email_monitor.py     # Gmail API integration
├── insight_analyzer.py  # OpenAI-powered analysis
├── insight_store.py     # Data storage and management
├── requirements.txt     # Python dependencies
├── .env.example        # Configuration template
├── SETUP.md            # Detailed setup guide
└── README.md           # This file
```

## Features

- ✅ Automatic email monitoring
- ✅ AI-powered insight extraction
- ✅ Three-category classification
- ✅ Persistent storage
- ✅ Email notifications
- ✅ Single-run or continuous modes
- ✅ Monthly reset capability
- ✅ Source tracking for each insight

## Requirements

- Python 3.8+
- Gmail account (for email monitoring)
- OpenAI API key (for AI analysis)
- Google Cloud Project (for Gmail API)

## License

MIT License - Feel free to use and modify for your needs.

## Support

For detailed setup instructions, see [SETUP.md](SETUP.md).
