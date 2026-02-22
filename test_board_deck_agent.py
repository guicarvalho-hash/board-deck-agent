"""
Tests for Board Deck Agent
"""

import unittest
from datetime import datetime
from board_deck_agent import BoardDeckAgent, BoardDeckContent


class TestBoardDeckAgent(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = BoardDeckAgent()
    
    def test_create_deck_outline(self):
        """Test creating a deck outline."""
        deck = self.agent.create_deck_outline("January", 2026)
        
        self.assertEqual(deck.month, "January")
        self.assertEqual(deck.year, 2026)
        self.assertIsInstance(deck.sections, list)
        self.assertGreater(len(deck.sections), 0)
        
        # Check that default sections exist
        section_titles = [s['title'] for s in deck.sections]
        self.assertIn("Executive Summary", section_titles)
        self.assertIn("Financial Performance", section_titles)
        self.assertIn("Key Metrics", section_titles)
    
    def test_create_monthly_deck_with_highlights(self):
        """Test creating a monthly deck with highlights."""
        highlights = [
            "Revenue up 20%",
            "New customer acquisition"
        ]
        
        deck = self.agent.create_monthly_deck(
            month="February",
            year=2026,
            highlights=highlights
        )
        
        self.assertEqual(deck.month, "February")
        self.assertEqual(deck.year, 2026)
        self.assertEqual(deck.highlights, highlights)
    
    def test_format_deck_as_markdown(self):
        """Test formatting a deck as markdown."""
        deck = BoardDeckContent(
            month="March",
            year=2026,
            sections=[
                {"title": "Test Section", "content": "Test content"}
            ],
            highlights=["Highlight 1", "Highlight 2"]
        )
        
        markdown = self.agent.format_deck_as_markdown(deck)
        
        self.assertIn("# Board Deck - March 2026", markdown)
        self.assertIn("## Key Highlights", markdown)
        self.assertIn("Highlight 1", markdown)
        self.assertIn("## Test Section", markdown)
        self.assertIn("Test content", markdown)
    
    def test_generate_section_content_without_api_key(self):
        """Test content generation without API key returns placeholder."""
        agent = BoardDeckAgent(api_key=None)
        agent.client = None
        
        content = agent.generate_section_content(
            section_title="Financial Performance",
            context="Test company",
            data="Revenue: $1M"
        )
        
        self.assertIn("Placeholder", content)
        self.assertIn("Financial Performance", content)


if __name__ == "__main__":
    unittest.main()
