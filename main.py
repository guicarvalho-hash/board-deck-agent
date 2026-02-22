"""
Main application for the Board Deck Agent.
"""
import os
import time
import argparse
from datetime import datetime
from dotenv import load_dotenv

from email_monitor import EmailMonitor
from insight_analyzer import InsightAnalyzer
from insight_store import InsightStore


class BoardDeckAgent:
    """Main agent for processing meeting minutes and compiling board insights."""
    
    def __init__(self):
        """Initialize the board deck agent."""
        # Load environment variables
        load_dotenv()
        
        # Initialize components
        self.email_monitor = EmailMonitor()
        self.insight_analyzer = InsightAnalyzer(
            api_key=os.getenv('OPENAI_API_KEY')
        )
        self.insight_store = InsightStore(
            data_file=os.getenv('DATA_FILE', 'board_insights.json')
        )
        
        self.user_email = os.getenv('USER_EMAIL')
        self.check_interval = int(os.getenv('CHECK_INTERVAL_MINUTES', '15'))
        
    def process_new_meetings(self) -> int:
        """
        Check for new meeting minutes and process them.
        
        Returns:
            Number of new meetings processed
        """
        print("\n" + "="*70)
        print(f"Checking for new meeting minutes... ({datetime.now()})")
        print("="*70)
        
        # Fetch new meeting minutes
        meeting_minutes = self.email_monitor.fetch_new_meeting_minutes()
        
        if not meeting_minutes:
            print("No new meeting minutes found.")
            return 0
            
        print(f"\nFound {len(meeting_minutes)} meeting(s) to process.")
        
        # Process each meeting
        processed_count = 0
        for meeting in meeting_minutes:
            print(f"\nProcessing: {meeting['subject']}")
            
            # Analyze meeting minutes
            insights = self.insight_analyzer.analyze_meeting_minutes(
                meeting['subject'],
                meeting['body']
            )
            
            # Add insights to store
            if self.insight_store.add_insights(meeting['subject'], insights):
                processed_count += 1
                print(f"✓ Successfully processed: {meeting['subject']}")
            else:
                print(f"✗ Failed to process: {meeting['subject']}")
        
        return processed_count
        
    def send_update_notification(self) -> bool:
        """
        Send an email notification with the updated insights.
        
        Returns:
            True if notification sent successfully
        """
        if not self.user_email:
            print("USER_EMAIL not configured, skipping email notification.")
            return False
            
        print("\nSending update notification...")
        
        # Get formatted insights
        insights_text = self.insight_store.export_to_text()
        
        # Get summary stats
        stats = self.insight_store.get_summary_stats()
        
        # Compose email
        subject = f"Board Deck Update - {stats['total_insights']} Insights from {stats['total_meetings_processed']} Meetings"
        
        body = f"""
Your Board Deck insights have been updated!

{insights_text}

---
This is an automated message from your Board Deck Agent.
To stop receiving these notifications, update your .env configuration.
"""
        
        # Send email
        success = self.email_monitor.send_email(
            to=self.user_email,
            subject=subject,
            body=body
        )
        
        return success
        
    def run_once(self) -> None:
        """Run the agent once (check emails, process, and notify)."""
        try:
            # Authenticate with Gmail
            print("Authenticating with Gmail...")
            self.email_monitor.authenticate()
            print("✓ Authentication successful")
            
            # Process new meetings
            processed = self.process_new_meetings()
            
            # Send notification if there were updates
            if processed > 0:
                print(f"\n✓ Processed {processed} new meeting(s)")
                self.send_update_notification()
            else:
                print("\nNo new meetings to process.")
                
            # Display summary
            print("\n" + "="*70)
            print("CURRENT INSIGHTS SUMMARY")
            print("="*70)
            stats = self.insight_store.get_summary_stats()
            print(f"Total Insights: {stats['total_insights']}")
            print(f"  - What Went Well: {stats['what_went_well_count']}")
            print(f"  - What Went Wrong: {stats['what_went_wrong_count']}")
            print(f"  - What's Next: {stats['whats_next_count']}")
            print(f"Total Meetings Processed: {stats['total_meetings_processed']}")
            print(f"Last Updated: {stats['last_updated']}")
            print("="*70)
            
        except Exception as e:
            print(f"Error running agent: {e}")
            raise
            
    def run_continuous(self) -> None:
        """Run the agent continuously, checking at regular intervals."""
        print(f"Starting Board Deck Agent in continuous mode...")
        print(f"Will check for new meetings every {self.check_interval} minutes.")
        print("Press Ctrl+C to stop.\n")
        
        try:
            while True:
                self.run_once()
                print(f"\nWaiting {self.check_interval} minutes until next check...")
                time.sleep(self.check_interval * 60)
                
        except KeyboardInterrupt:
            print("\n\nAgent stopped by user.")
        except Exception as e:
            print(f"\nAgent stopped due to error: {e}")
            raise


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Board Deck Agent - Automatically compile meeting insights for board presentations'
    )
    parser.add_argument(
        '--mode',
        choices=['once', 'continuous'],
        default='once',
        help='Run mode: once (single check) or continuous (keep monitoring)'
    )
    parser.add_argument(
        '--clear',
        action='store_true',
        help='Clear all stored insights before running'
    )
    
    args = parser.parse_args()
    
    # Initialize agent
    agent = BoardDeckAgent()
    
    # Clear insights if requested
    if args.clear:
        print("Clearing all stored insights...")
        agent.insight_store.clear_insights()
        print("Insights cleared.\n")
    
    # Run in selected mode
    if args.mode == 'continuous':
        agent.run_continuous()
    else:
        agent.run_once()


if __name__ == '__main__':
    main()
