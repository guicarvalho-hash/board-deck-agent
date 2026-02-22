"""
Email monitor for detecting and processing meeting minutes from Gmail.
"""
import os
import base64
import pickle
from datetime import datetime
from typing import List, Dict, Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from bs4 import BeautifulSoup


# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 
          'https://www.googleapis.com/auth/gmail.send']


class EmailMonitor:
    """Monitor Gmail inbox for meeting minutes."""
    
    def __init__(self, days_to_check: int = 7):
        """
        Initialize the email monitor.
        
        Args:
            days_to_check: Number of days back to search for emails (default: 7)
        """
        self.service = None
        self.last_processed_file = 'last_processed.txt'
        self.days_to_check = days_to_check
        
    def authenticate(self) -> None:
        """Authenticate with Gmail API."""
        creds = None
        
        # Token file stores the user's access and refresh tokens
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            
        # If no valid credentials, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists('credentials.json'):
                    raise FileNotFoundError(
                        "credentials.json not found. Please follow setup instructions."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES
                )
                creds = flow.run_local_server(port=0)
                
            # Save credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
                
        self.service = build('gmail', 'v1', credentials=creds)
        
    def get_last_processed_time(self) -> Optional[str]:
        """Get the timestamp of the last processed email."""
        if os.path.exists(self.last_processed_file):
            with open(self.last_processed_file, 'r') as f:
                return f.read().strip()
        return None
        
    def save_last_processed_time(self, timestamp: str) -> None:
        """Save the timestamp of the last processed email."""
        with open(self.last_processed_file, 'w') as f:
            f.write(timestamp)
            
    def is_meeting_minutes(self, subject: str, body: str) -> bool:
        """
        Determine if an email contains meeting minutes.
        
        Args:
            subject: Email subject line
            body: Email body text
            
        Returns:
            True if the email appears to contain meeting minutes
        """
        # Keywords that indicate meeting minutes
        keywords = [
            'meeting minutes', 'meeting notes', 'minutes',
            'meeting summary', 'action items', 'meeting recap',
            'discussion points', 'meeting agenda', 'notes from',
            'weekly sync', 'team meeting', 'standup notes'
        ]
        
        subject_lower = subject.lower()
        body_lower = body.lower()
        
        # Check if any keyword appears in subject or body
        for keyword in keywords:
            if keyword in subject_lower or keyword in body_lower[:500]:
                return True
                
        return False
        
    def extract_email_body(self, message: Dict) -> str:
        """
        Extract text content from email message.
        
        Args:
            message: Gmail API message object
            
        Returns:
            Extracted text content
        """
        try:
            if 'payload' not in message:
                return ""
                
            payload = message['payload']
            
            # Handle multipart messages
            if 'parts' in payload:
                text_parts = []
                for part in payload['parts']:
                    if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                        text_parts.append(
                            base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        )
                    elif part['mimeType'] == 'text/html' and 'data' in part['body']:
                        html = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        soup = BeautifulSoup(html, 'html.parser')
                        text_parts.append(soup.get_text())
                return '\n\n'.join(text_parts)
            
            # Handle single part messages
            elif 'body' in payload and 'data' in payload['body']:
                body_data = payload['body']['data']
                text = base64.urlsafe_b64decode(body_data).decode('utf-8')
                
                # If it's HTML, extract text
                if payload.get('mimeType') == 'text/html':
                    soup = BeautifulSoup(text, 'html.parser')
                    return soup.get_text()
                    
                return text
                
        except Exception as e:
            print(f"Error extracting email body: {e}")
            
        return ""
        
    def get_subject(self, message: Dict) -> str:
        """Extract subject from message headers."""
        headers = message['payload']['headers']
        for header in headers:
            if header['name'].lower() == 'subject':
                return header['value']
        return ""
        
    def fetch_new_meeting_minutes(self) -> List[Dict[str, str]]:
        """
        Fetch new emails that contain meeting minutes.
        
        Returns:
            List of meeting minutes with subject and body
        """
        if not self.service:
            self.authenticate()
            
        meeting_minutes = []
        
        try:
            # Build query for recent unread messages
            query = f'is:unread newer_than:{self.days_to_check}d'
            
            # Get list of messages
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=50
            ).execute()
            
            messages = results.get('messages', [])
            
            if not messages:
                print("No new messages found.")
                return meeting_minutes
                
            print(f"Found {len(messages)} unread messages to check.")
            
            # Process each message
            for msg in messages:
                msg_id = msg['id']
                
                # Get full message details
                message = self.service.users().messages().get(
                    userId='me',
                    id=msg_id,
                    format='full'
                ).execute()
                
                subject = self.get_subject(message)
                body = self.extract_email_body(message)
                
                # Check if it's meeting minutes
                if self.is_meeting_minutes(subject, body):
                    print(f"Found meeting minutes: {subject}")
                    meeting_minutes.append({
                        'id': msg_id,
                        'subject': subject,
                        'body': body,
                        'timestamp': message['internalDate']
                    })
                    
                    # Mark as read (optional - comment out if you want to keep as unread)
                    # self.service.users().messages().modify(
                    #     userId='me',
                    #     id=msg_id,
                    #     body={'removeLabelIds': ['UNREAD']}
                    # ).execute()
                    
        except Exception as e:
            print(f"Error fetching emails: {e}")
            
        return meeting_minutes
        
    def send_email(self, to: str, subject: str, body: str) -> bool:
        """
        Send an email via Gmail API.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body (plain text)
            
        Returns:
            True if email sent successfully
        """
        if not self.service:
            self.authenticate()
            
        try:
            from email.mime.text import MIMEText
            
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject
            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            print(f"Email sent successfully to {to}")
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
