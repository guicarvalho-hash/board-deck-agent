# Board Deck Agent

An AI-powered agent to help prepare monthly board of directors presentations and decks.

## Overview

This agent automates the creation and management of monthly board decks, helping you:
- Structure board presentations consistently
- Generate content suggestions using AI
- Organize key metrics and highlights
- Format information for board-appropriate presentation
- Save time on routine deck preparation

## Features

- 📊 **Standard Deck Structure**: Pre-configured sections for board presentations
- 🤖 **AI Content Generation**: Leverage OpenAI to generate section content
- 📝 **Markdown Output**: Export decks as markdown for easy conversion to slides
- 📅 **Monthly Automation**: Designed for recurring monthly board updates
- ⚙️ **Customizable**: Adapt sections and content to your needs

## Installation

1. Clone this repository:
```bash
git clone https://github.com/guicarvalho-hash/board-deck-agent.git
cd board-deck-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key (optional, for AI content generation):
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Usage

### Basic Usage

```python
from board_deck_agent import BoardDeckAgent

# Initialize the agent
agent = BoardDeckAgent()

# Create a monthly deck
deck = agent.create_monthly_deck(
    month="February",
    year=2026,
    context="Tech startup in the AI/ML space",
    highlights=[
        "Revenue grew 25% month-over-month",
        "Launched new product feature",
        "Secured key partnership"
    ]
)

# Save the deck
agent.save_deck(deck, "board_deck_feb_2026.md")
```

### Command Line Usage

Run the example:
```bash
python board_deck_agent.py
```

### Generate AI Content (requires OpenAI API key)

```python
agent = BoardDeckAgent()

# Generate content for a specific section
content = agent.generate_section_content(
    section_title="Financial Performance",
    context="SaaS company with subscription model",
    data="MRR: $250K, Growth: 15% MoM, Churn: 2.5%"
)
```

## Default Deck Structure

The agent creates decks with the following sections:
1. Executive Summary
2. Financial Performance
3. Key Metrics
4. Product Updates
5. Customer Insights
6. Team & Operations
7. Strategic Initiatives
8. Challenges & Risks
9. Next Steps

You can customize these sections based on your board's preferences.

## Configuration

- Set `OPENAI_API_KEY` in `.env` for AI content generation
- Modify the default sections in `create_deck_outline()` method
- Customize the output format in `format_deck_as_markdown()` method

## Roadmap

- [ ] Support for multiple output formats (PDF, PowerPoint)
- [ ] Integration with data sources (databases, APIs)
- [ ] Automated metric collection
- [ ] Email delivery integration
- [ ] Template customization
- [ ] Historical deck comparison

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License
