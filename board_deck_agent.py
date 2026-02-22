"""
Board Deck Agent

An AI agent to help prepare and manage monthly board of directors decks.
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import os
from openai import OpenAI
from dotenv import load_dotenv


@dataclass
class BoardDeckContent:
    """Represents content for a board deck."""
    month: str
    year: int
    sections: List[dict]
    key_metrics: Optional[dict] = None
    highlights: Optional[List[str]] = None


class BoardDeckAgent:
    """
    Agent for creating and managing monthly board decks.
    
    This agent helps automate the creation of board presentations by:
    - Structuring monthly updates
    - Generating content suggestions
    - Organizing key metrics and highlights
    - Formatting information for board presentations
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Board Deck Agent.
        
        Args:
            api_key: OpenAI API key. If not provided, will try to load from environment.
        """
        load_dotenv()
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    def create_deck_outline(self, month: str, year: int, context: str = "") -> BoardDeckContent:
        """
        Create an outline for a board deck.
        
        Args:
            month: Month name (e.g., "January")
            year: Year (e.g., 2026)
            context: Additional context about the company or specific topics to cover
            
        Returns:
            BoardDeckContent object with the deck structure
        """
        default_sections = [
            {"title": "Executive Summary", "content": ""},
            {"title": "Financial Performance", "content": ""},
            {"title": "Key Metrics", "content": ""},
            {"title": "Product Updates", "content": ""},
            {"title": "Customer Insights", "content": ""},
            {"title": "Team & Operations", "content": ""},
            {"title": "Strategic Initiatives", "content": ""},
            {"title": "Challenges & Risks", "content": ""},
            {"title": "Next Steps", "content": ""},
        ]
        
        return BoardDeckContent(
            month=month,
            year=year,
            sections=default_sections,
            key_metrics={},
            highlights=[]
        )
    
    def generate_section_content(self, section_title: str, context: str, data: str = "") -> str:
        """
        Generate content for a specific deck section using AI.
        
        Args:
            section_title: The title of the section
            context: Context about the company and what to include
            data: Raw data or information to incorporate
            
        Returns:
            Generated content for the section
        """
        if not self.client:
            return f"[Placeholder for {section_title} - OpenAI API key not configured]"
        
        prompt = f"""You are helping prepare a board of directors presentation.
        
Section: {section_title}
Company Context: {context}
Data: {data}

Generate concise, board-appropriate content for this section. Focus on:
- Key insights and takeaways
- Actionable information
- Clear, executive-level language
- Bullet points where appropriate

Keep it brief and impactful (2-3 paragraphs or 5-7 bullet points)."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert at creating board of directors presentations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[Error generating content: {str(e)}]"
    
    def format_deck_as_markdown(self, deck: BoardDeckContent) -> str:
        """
        Format a board deck as markdown.
        
        Args:
            deck: BoardDeckContent object
            
        Returns:
            Markdown formatted deck
        """
        markdown = f"# Board Deck - {deck.month} {deck.year}\n\n"
        markdown += f"*Generated: {datetime.now().strftime('%Y-%m-%d')}*\n\n"
        markdown += "---\n\n"
        
        if deck.highlights:
            markdown += "## Key Highlights\n\n"
            for highlight in deck.highlights:
                markdown += f"- {highlight}\n"
            markdown += "\n---\n\n"
        
        for section in deck.sections:
            markdown += f"## {section['title']}\n\n"
            if section.get('content'):
                markdown += f"{section['content']}\n\n"
            else:
                markdown += "*[Content to be added]*\n\n"
            markdown += "---\n\n"
        
        return markdown
    
    def create_monthly_deck(
        self, 
        month: str, 
        year: int, 
        context: str = "",
        metrics: Optional[dict] = None,
        highlights: Optional[List[str]] = None
    ) -> BoardDeckContent:
        """
        Create a complete monthly board deck.
        
        Args:
            month: Month name
            year: Year
            context: Company context
            metrics: Key metrics to include
            highlights: Key highlights to feature
            
        Returns:
            Complete BoardDeckContent object
        """
        deck = self.create_deck_outline(month, year, context)
        
        if metrics:
            deck.key_metrics = metrics
        
        if highlights:
            deck.highlights = highlights
        
        return deck
    
    def save_deck(self, deck: BoardDeckContent, output_path: str):
        """
        Save a board deck to a file.
        
        Args:
            deck: BoardDeckContent object
            output_path: Path where to save the deck
        """
        markdown = self.format_deck_as_markdown(deck)
        with open(output_path, 'w') as f:
            f.write(markdown)


def main():
    """Example usage of the Board Deck Agent."""
    agent = BoardDeckAgent()
    
    # Create a deck for the current month
    now = datetime.now()
    month = now.strftime("%B")
    year = now.year
    
    deck = agent.create_monthly_deck(
        month=month,
        year=year,
        context="Tech startup in the AI/ML space",
        highlights=[
            "Revenue grew 25% month-over-month",
            "Launched new product feature with 80% user adoption",
            "Secured partnership with Fortune 500 company"
        ]
    )
    
    # Save the deck
    output_file = f"board_deck_{month.lower()}_{year}.md"
    agent.save_deck(deck, output_file)
    print(f"Board deck created: {output_file}")
    
    # Print preview
    print("\nPreview:")
    print(agent.format_deck_as_markdown(deck))


if __name__ == "__main__":
    main()
