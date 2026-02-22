# Architecture Overview

This document explains how the Board Deck Agent works internally.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          User's Gmail                            │
│                    (Meeting Minutes Arrive)                      │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               │ Gmail API
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Email Monitor Module                         │
│  • Authenticates with Gmail OAuth 2.0                            │
│  • Fetches unread emails from last 7 days                        │
│  • Identifies meeting minutes by keywords                        │
│  • Extracts email subject and body content                       │
│  • Sends notification emails                                     │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               │ Meeting data
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Insight Analyzer Module                        │
│  • Receives meeting subject and content                          │
│  • Sends to OpenAI GPT-4 for analysis                           │
│  • Uses structured prompts for categorization                    │
│  • Extracts insights in three categories                         │
│  • Returns structured JSON data                                  │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               │ Categorized insights
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Insight Store Module                          │
│  • Loads existing insights from JSON file                        │
│  • Adds new insights with metadata                               │
│  • Tracks source and timestamp                                   │
│  • Updates statistics                                            │
│  • Persists to disk                                              │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               │ Formatted summary
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Notification Email                           │
│  • Formatted text summary                                        │
│  • All three categories with insights                            │
│  • Source attribution                                            │
│  • Statistics                                                    │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### 1. Main Application (`main.py`)

**Purpose:** Orchestrates the entire workflow and provides CLI interface.

**Key Classes:**
- `BoardDeckAgent`: Main controller class

**Key Methods:**
- `process_new_meetings()`: Checks for and processes new meeting minutes
- `send_update_notification()`: Sends email with compiled insights
- `run_once()`: Single execution cycle
- `run_continuous()`: Continuous monitoring loop

**Flow:**
1. Load environment variables
2. Initialize all modules
3. Authenticate with Gmail
4. Fetch new meeting minutes
5. Analyze each meeting
6. Store insights
7. Send notification
8. Wait or exit based on mode

### 2. Email Monitor (`email_monitor.py`)

**Purpose:** Interface with Gmail API for reading and sending emails.

**Key Classes:**
- `EmailMonitor`: Manages Gmail API interactions

**Key Methods:**
- `authenticate()`: OAuth 2.0 authentication flow
- `fetch_new_meeting_minutes()`: Retrieves unread emails with meeting content
- `is_meeting_minutes()`: Determines if email contains meeting minutes
- `extract_email_body()`: Parses email content (handles HTML and plain text)
- `send_email()`: Sends formatted notifications

**Gmail API Usage:**
- Scopes: `gmail.readonly`, `gmail.send`
- Authentication: OAuth 2.0 with refresh token
- Queries: Searches unread emails from last 7 days
- Rate Limits: Well within free tier limits (1B quota units/day)

**Meeting Detection Keywords:**
```python
keywords = [
    'meeting minutes', 'meeting notes', 'minutes',
    'meeting summary', 'action items', 'meeting recap',
    'discussion points', 'meeting agenda', 'notes from',
    'weekly sync', 'team meeting', 'standup notes'
]
```

### 3. Insight Analyzer (`insight_analyzer.py`)

**Purpose:** AI-powered extraction and categorization of insights.

**Key Classes:**
- `InsightAnalyzer`: Analyzes meeting content using OpenAI

**Key Methods:**
- `analyze_meeting_minutes()`: Main analysis function
- `summarize_insights()`: Formats insights for display

**AI Model:**
- Model: GPT-4
- Temperature: 0.3 (balanced creativity/consistency)
- Response Format: JSON
- System Prompt: Executive assistant persona

**Analysis Prompt Structure:**
```
Input:
- Meeting title/subject
- Full meeting content

Process:
- Extract strategic insights
- Focus on board-level information
- Quantify when possible
- Be concise (one sentence per bullet)

Output Categories:
1. What Went Well (successes, achievements)
2. What Went Wrong (challenges, issues)
3. What's Next (action items, plans)
```

**Error Handling:**
- Returns empty arrays if analysis fails
- Logs errors but continues processing
- Validates JSON structure

### 4. Insight Store (`insight_store.py`)

**Purpose:** Persist and manage insights data.

**Key Classes:**
- `InsightStore`: Manages JSON-based data storage

**Key Methods:**
- `add_insights()`: Adds new categorized insights
- `get_all_insights()`: Retrieves all stored data
- `get_summary_stats()`: Calculates statistics
- `export_to_text()`: Formats for display/email
- `clear_insights()`: Resets for new month

**Data Structure:**
```json
{
  "what_went_well": [
    {
      "insight": "Revenue increased 15%",
      "source": "Sales Meeting",
      "date_added": "2024-01-15T10:30:00"
    }
  ],
  "what_went_wrong": [...],
  "whats_next": [...],
  "metadata": {
    "last_updated": "2024-01-15T10:30:00",
    "total_meetings_processed": 5
  }
}
```

## Data Flow

### Single Execution Cycle

```
1. START
   ↓
2. Load Configuration (.env)
   ↓
3. Initialize Modules
   ↓
4. Authenticate Gmail (OAuth)
   ↓
5. Fetch Unread Emails
   ↓
6. For Each Email:
   ├─ Check if Meeting Minutes
   ├─ Extract Content
   ├─ Analyze with AI
   ├─ Store Insights
   └─ Continue
   ↓
7. If New Insights:
   ├─ Format Summary
   ├─ Send Email Notification
   └─ Log Success
   ↓
8. Display Statistics
   ↓
9. END (or wait if continuous)
```

## Security Considerations

### Authentication & Authorization
- OAuth 2.0 for Gmail (no password storage)
- API keys in environment variables (not in code)
- Token refresh automatic
- Minimal Gmail scopes requested

### Data Privacy
- Processes emails locally
- Only sends data to OpenAI API (for analysis)
- No third-party data sharing
- Insights stored locally in JSON

### Secrets Management
- `.env` file for configuration (gitignored)
- `credentials.json` gitignored
- `token.json` gitignored
- No hardcoded secrets

## Configuration

### Environment Variables
```
OPENAI_API_KEY       # Required: OpenAI API key
USER_EMAIL           # Required: Email for notifications
SENDER_EMAIL         # Optional: Defaults to USER_EMAIL
DATA_FILE            # Optional: Default board_insights.json
CHECK_INTERVAL_MINUTES # Optional: Default 15
```

### Files
- `credentials.json`: Google OAuth client credentials
- `token.json`: OAuth refresh token (generated)
- `board_insights.json`: Persistent data store
- `.env`: Environment configuration

## Error Handling

### Gmail API Errors
- Retry with exponential backoff
- Refresh token if expired
- Graceful degradation if API unavailable

### OpenAI API Errors
- Returns empty insights on failure
- Logs error but continues
- Can retry on next cycle

### Storage Errors
- Creates new file if missing
- Validates JSON on load
- Atomic writes to prevent corruption

## Performance

### Email Checking
- Only checks unread emails (efficient)
- Limited to last 7 days
- Batch processing (up to 50 at once)

### AI Analysis
- Processes sequentially (controlled costs)
- Uses GPT-4 (high quality)
- Structured JSON responses (reliable)

### Storage
- JSON file (simple, portable)
- In-memory operations
- Single write per update cycle

## Scalability

### Current Design
- Handles dozens of meetings per month
- Lightweight (minimal resources)
- Can run on modest hardware

### Limitations
- Sequential processing (not parallel)
- Single user (not multi-tenant)
- Local storage (not distributed)

### Future Enhancements
- Database backend (PostgreSQL/MongoDB)
- Multi-user support
- Parallel processing
- Web dashboard
- API endpoints

## Testing

### Setup Verification (`test_setup.py`)
- Checks dependencies installed
- Validates environment variables
- Tests API connections
- Verifies file permissions

### Manual Testing
- Use SAMPLE_MEETING.md for testing
- Send test email to yourself
- Run with `--mode once`
- Verify output in board_insights.json

## Deployment Options

### 1. Local Development
```bash
python main.py --mode continuous
```

### 2. Background Process (Linux/Mac)
```bash
nohup python main.py --mode continuous > agent.log 2>&1 &
```

### 3. Systemd Service (Linux)
```ini
[Unit]
Description=Board Deck Agent

[Service]
ExecStart=/usr/bin/python3 /path/to/main.py --mode continuous
Restart=always

[Install]
WantedBy=multi-user.target
```

### 4. Docker Container
```bash
docker-compose up -d
```

### 5. Cloud Deployment
- AWS EC2 / Lightsail
- Google Cloud Compute Engine
- DigitalOcean Droplet
- Heroku (with persistent storage)

## Monitoring

### Logs
- Console output (stdout/stderr)
- Can redirect to file
- Includes timestamps
- Error details

### Metrics to Track
- Meetings processed per cycle
- Insights added per meeting
- API call success rates
- Email send success rates

### Health Checks
- Run `test_setup.py` periodically
- Monitor log files
- Check notification emails received
- Verify board_insights.json updated

## Cost Estimate

### OpenAI API
- Model: GPT-4
- ~1000 tokens per meeting
- Cost: ~$0.03 per meeting
- Monthly (20 meetings): ~$0.60

### Gmail API
- Free tier: 1B quota units/day
- Usage: ~100 units per check
- Well within limits: $0

### Infrastructure
- Local: $0
- Cloud (minimal): $5-10/month

**Total Monthly Cost: ~$1-11**

## Maintenance

### Regular Tasks
- Monitor for API changes
- Update dependencies (`pip install -U`)
- Clear insights monthly
- Review OAuth token expiry

### Updates
- Pull latest code: `git pull`
- Update dependencies: `pip install -r requirements.txt`
- Restart service

### Backup
- Backup `board_insights.json` regularly
- Export insights before clearing
- Keep `credentials.json` secure

## Troubleshooting

See SETUP.md and QUICKSTART.md for detailed troubleshooting steps.

## Future Enhancements

### Planned
- [ ] Web dashboard for viewing insights
- [ ] More sophisticated meeting detection
- [ ] Custom categorization rules
- [ ] Integration with Slack/Teams
- [ ] Calendar integration
- [ ] Multiple board deck templates

### Ideas
- Export to PowerPoint directly
- Mobile app notifications
- Multi-language support
- Team collaboration features
- Analytics and trends
