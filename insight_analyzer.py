"""
AI-powered insight analyzer for extracting and categorizing meeting insights.
"""
import os
from typing import Dict, List
from openai import OpenAI


class InsightAnalyzer:
    """Analyze meeting minutes and extract categorized insights."""
    
    def __init__(self, api_key: str):
        """
        Initialize the insight analyzer.
        
        Args:
            api_key: OpenAI API key
        """
        self.client = OpenAI(api_key=api_key)
        
    def analyze_meeting_minutes(self, subject: str, content: str) -> Dict[str, List[str]]:
        """
        Analyze meeting minutes and categorize insights.
        
        Args:
            subject: Meeting subject/title
            content: Meeting minutes content
            
        Returns:
            Dictionary with three categories: what_went_well, what_went_wrong, whats_next
        """
        prompt = f"""
You are analyzing meeting minutes to extract insights for a board of directors presentation.

Meeting Title: {subject}

Meeting Minutes:
{content}

Please analyze the meeting minutes and extract key insights in the following three categories:

1. **What Went Well**: Positive developments, achievements, successes, milestones reached
2. **What Went Wrong**: Challenges, issues, problems, setbacks, concerns raised
3. **What's Next**: Action items, future plans, upcoming initiatives, next steps

For each category, provide 2-5 concise bullet points (one sentence each). Focus on the most important and relevant items for board-level reporting. Be specific and quantifiable when possible.

Return your response in the following JSON format:
{{
  "what_went_well": [
    "bullet point 1",
    "bullet point 2"
  ],
  "what_went_wrong": [
    "bullet point 1",
    "bullet point 2"
  ],
  "whats_next": [
    "bullet point 1",
    "bullet point 2"
  ]
}}

If a category has no relevant items, return an empty array for that category.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert executive assistant who extracts key insights from meeting minutes for board presentations. You focus on strategic, high-level information."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            # Ensure all required keys exist
            insights = {
                'what_went_well': result.get('what_went_well', []),
                'what_went_wrong': result.get('what_went_wrong', []),
                'whats_next': result.get('whats_next', [])
            }
            
            print(f"Successfully analyzed meeting: {subject}")
            print(f"  - What went well: {len(insights['what_went_well'])} items")
            print(f"  - What went wrong: {len(insights['what_went_wrong'])} items")
            print(f"  - What's next: {len(insights['whats_next'])} items")
            
            return insights
            
        except Exception as e:
            print(f"Error analyzing meeting minutes: {e}")
            return {
                'what_went_well': [],
                'what_went_wrong': [],
                'whats_next': []
            }
            
    def summarize_insights(self, all_insights: Dict[str, List[Dict]]) -> str:
        """
        Create a formatted summary of all compiled insights.
        
        Args:
            all_insights: Dictionary containing all categorized insights
            
        Returns:
            Formatted text summary
        """
        summary_parts = []
        
        summary_parts.append("=" * 70)
        summary_parts.append("BOARD DECK - MONTHLY INSIGHTS COMPILATION")
        summary_parts.append("=" * 70)
        summary_parts.append("")
        
        # What Went Well
        summary_parts.append("🎉 WHAT WENT WELL")
        summary_parts.append("-" * 70)
        if all_insights.get('what_went_well'):
            for item in all_insights['what_went_well']:
                summary_parts.append(f"  • {item['insight']}")
                summary_parts.append(f"    (Source: {item['source']})")
                summary_parts.append("")
        else:
            summary_parts.append("  No items recorded yet.")
            summary_parts.append("")
        
        # What Went Wrong
        summary_parts.append("⚠️  WHAT WENT WRONG")
        summary_parts.append("-" * 70)
        if all_insights.get('what_went_wrong'):
            for item in all_insights['what_went_wrong']:
                summary_parts.append(f"  • {item['insight']}")
                summary_parts.append(f"    (Source: {item['source']})")
                summary_parts.append("")
        else:
            summary_parts.append("  No items recorded yet.")
            summary_parts.append("")
        
        # What's Next
        summary_parts.append("🚀 WHAT'S NEXT")
        summary_parts.append("-" * 70)
        if all_insights.get('whats_next'):
            for item in all_insights['whats_next']:
                summary_parts.append(f"  • {item['insight']}")
                summary_parts.append(f"    (Source: {item['source']})")
                summary_parts.append("")
        else:
            summary_parts.append("  No items recorded yet.")
            summary_parts.append("")
        
        summary_parts.append("=" * 70)
        
        return "\n".join(summary_parts)
