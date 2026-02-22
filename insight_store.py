"""
Data manager for storing and updating board insights.
"""
import json
import os
from datetime import datetime
from typing import Dict, List


class InsightStore:
    """Manage storage and updates of board insights."""
    
    def __init__(self, data_file: str = 'board_insights.json'):
        """
        Initialize the insight store.
        
        Args:
            data_file: Path to JSON file for storing insights
        """
        self.data_file = data_file
        self.insights = self._load_insights()
        
    def _load_insights(self) -> Dict:
        """Load insights from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Error reading {self.data_file}, starting fresh.")
                
        # Default structure
        return {
            'what_went_well': [],
            'what_went_wrong': [],
            'whats_next': [],
            'metadata': {
                'last_updated': None,
                'total_meetings_processed': 0
            }
        }
        
    def _save_insights(self) -> None:
        """Save insights to JSON file."""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.insights, f, indent=2)
            print(f"Insights saved to {self.data_file}")
        except Exception as e:
            print(f"Error saving insights: {e}")
            
    def add_insights(self, meeting_subject: str, analyzed_insights: Dict[str, List[str]]) -> bool:
        """
        Add new insights from a meeting to the store.
        
        Args:
            meeting_subject: Subject/title of the meeting
            analyzed_insights: Categorized insights from the meeting
            
        Returns:
            True if insights were added successfully
        """
        try:
            timestamp = datetime.now().isoformat()
            
            # Add insights to each category
            for category in ['what_went_well', 'what_went_wrong', 'whats_next']:
                for insight in analyzed_insights.get(category, []):
                    self.insights[category].append({
                        'insight': insight,
                        'source': meeting_subject,
                        'date_added': timestamp
                    })
            
            # Update metadata
            self.insights['metadata']['last_updated'] = timestamp
            self.insights['metadata']['total_meetings_processed'] += 1
            
            self._save_insights()
            return True
            
        except Exception as e:
            print(f"Error adding insights: {e}")
            return False
            
    def get_all_insights(self) -> Dict:
        """Get all stored insights."""
        return self.insights
        
    def get_summary_stats(self) -> Dict:
        """Get summary statistics about stored insights."""
        return {
            'what_went_well_count': len(self.insights['what_went_well']),
            'what_went_wrong_count': len(self.insights['what_went_wrong']),
            'whats_next_count': len(self.insights['whats_next']),
            'total_insights': (
                len(self.insights['what_went_well']) +
                len(self.insights['what_went_wrong']) +
                len(self.insights['whats_next'])
            ),
            'last_updated': self.insights['metadata']['last_updated'],
            'total_meetings_processed': self.insights['metadata']['total_meetings_processed']
        }
        
    def clear_insights(self) -> None:
        """Clear all insights (useful for starting a new month)."""
        self.insights = {
            'what_went_well': [],
            'what_went_wrong': [],
            'whats_next': [],
            'metadata': {
                'last_updated': None,
                'total_meetings_processed': 0
            }
        }
        self._save_insights()
        print("All insights cleared.")
        
    def export_to_text(self) -> str:
        """
        Export insights in a readable text format.
        
        Returns:
            Formatted text with all insights
        """
        lines = []
        lines.append("=" * 70)
        lines.append("BOARD DECK - MONTHLY INSIGHTS")
        lines.append("=" * 70)
        lines.append("")
        
        stats = self.get_summary_stats()
        lines.append(f"Last Updated: {stats['last_updated']}")
        lines.append(f"Total Meetings Processed: {stats['total_meetings_processed']}")
        lines.append(f"Total Insights: {stats['total_insights']}")
        lines.append("")
        
        # What Went Well
        lines.append("🎉 WHAT WENT WELL")
        lines.append("-" * 70)
        if self.insights['what_went_well']:
            for item in self.insights['what_went_well']:
                lines.append(f"• {item['insight']}")
                lines.append(f"  Source: {item['source']}")
                lines.append("")
        else:
            lines.append("No items yet.")
            lines.append("")
        
        # What Went Wrong
        lines.append("⚠️  WHAT WENT WRONG")
        lines.append("-" * 70)
        if self.insights['what_went_wrong']:
            for item in self.insights['what_went_wrong']:
                lines.append(f"• {item['insight']}")
                lines.append(f"  Source: {item['source']}")
                lines.append("")
        else:
            lines.append("No items yet.")
            lines.append("")
        
        # What's Next
        lines.append("🚀 WHAT'S NEXT")
        lines.append("-" * 70)
        if self.insights['whats_next']:
            for item in self.insights['whats_next']:
                lines.append(f"• {item['insight']}")
                lines.append(f"  Source: {item['source']}")
                lines.append("")
        else:
            lines.append("No items yet.")
            lines.append("")
        
        lines.append("=" * 70)
        
        return "\n".join(lines)
