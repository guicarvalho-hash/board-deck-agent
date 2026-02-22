#!/usr/bin/env python3
"""
Example usage of the Board Deck Agent
"""

from board_deck_agent import BoardDeckAgent
from datetime import datetime


def example_basic_deck():
    """Create a basic board deck."""
    print("Creating a basic board deck...\n")
    
    agent = BoardDeckAgent()
    
    # Get current month/year
    now = datetime.now()
    month = now.strftime("%B")
    year = now.year
    
    # Create deck
    deck = agent.create_monthly_deck(
        month=month,
        year=year,
        context="Technology startup in AI/ML space",
        highlights=[
            "Revenue grew 25% month-over-month",
            "Launched new product feature with 80% user adoption",
            "Secured partnership with Fortune 500 company",
            "Team expanded to 25 employees"
        ]
    )
    
    # Save to file
    output_file = f"example_deck_{month.lower()}_{year}.md"
    agent.save_deck(deck, output_file)
    
    print(f"✓ Deck saved to: {output_file}\n")
    print("Preview:")
    print("-" * 60)
    print(agent.format_deck_as_markdown(deck))


def example_custom_sections():
    """Create a deck with custom content."""
    print("\nCreating a deck with custom sections...\n")
    
    agent = BoardDeckAgent()
    
    # Create outline
    deck = agent.create_deck_outline("January", 2026, "SaaS Company")
    
    # Add custom content to sections
    deck.sections[0]['content'] = """
**Summary**: Strong growth across all metrics with significant product momentum.

**Key Highlights**:
- ARR reached $5M milestone
- Customer count: 150 (+30 this month)
- Net Revenue Retention: 120%
"""
    
    deck.sections[1]['content'] = """
**Monthly Recurring Revenue**: $250,000 (+15% MoM)
**Burn Rate**: $180,000/month
**Runway**: 18 months
**Cash Position**: $3.2M
"""
    
    # Print formatted output
    print(agent.format_deck_as_markdown(deck))


if __name__ == "__main__":
    print("=" * 60)
    print("Board Deck Agent - Examples")
    print("=" * 60)
    print()
    
    example_basic_deck()
    example_custom_sections()
