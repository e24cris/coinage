import os
import csv
import uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from typing import Dict, List, Any
from datetime import datetime

class BetaTesterRecruitment:
    def __init__(
        self, 
        recruitment_dir: str = 'beta_tester_recruitment',
        email_config: Dict[str, str] = None
    ):
        """
        Initialize Beta Tester Recruitment
        
        Args:
            recruitment_dir: Directory to store recruitment data
            email_config: Email configuration dictionary
        """
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Ensure recruitment directory exists
        os.makedirs(recruitment_dir, exist_ok=True)
        self.recruitment_dir = recruitment_dir
        
        # Email configuration
        self.email_config = email_config or {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'sender_email': 'beta@coinage.com',
            'sender_password': os.environ.get('EMAIL_PASSWORD')
        }
    
    def load_potential_testers(self, csv_path: str) -> List[Dict[str, str]]:
        """
        Load potential beta testers from CSV
        
        Args:
            csv_path: Path to CSV file with tester information
        
        Returns:
            List of potential testers
        """
        potential_testers = []
        
        with open(csv_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                potential_testers.append(row)
        
        return potential_testers
    
    def generate_invitation_code(self) -> str:
        """
        Generate unique beta tester invitation code
        
        Returns:
            Unique invitation code
        """
        return str(uuid.uuid4())
    
    def send_invitation_email(
        self, 
        recipient: Dict[str, str], 
        invitation_code: str
    ) -> bool:
        """
        Send beta tester invitation email
        
        Args:
            recipient: Recipient details
            invitation_code: Unique invitation code
        
        Returns:
            Boolean indicating email sent successfully
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_config['sender_email']
            msg['To'] = recipient['email']
            msg['Subject'] = 'Exclusive Coinage Beta Tester Invitation'
            
            # Email body
            body = f"""
            Dear {recipient['name']},

            You've been selected for an exclusive beta testing opportunity with Coinage!

            Your Unique Invitation Code: {invitation_code}
            Beta Testing Portal: https://beta.coinage.com

            Join us in revolutionizing intelligent investing.

            Best regards,
            Coinage Beta Team
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP(
                self.email_config['smtp_server'], 
                self.email_config['smtp_port']
            ) as server:
                server.starttls()
                server.login(
                    self.email_config['sender_email'], 
                    self.email_config['sender_password']
                )
                server.send_message(msg)
            
            return True
        
        except Exception as e:
            self.logger.error(f"Email sending failed: {e}")
            return False
    
    def track_beta_tester_invitations(
        self, 
        potential_testers: List[Dict[str, str]]
    ) -> List[Dict[str, Any]]:
        """
        Track beta tester invitations
        
        Args:
            potential_testers: List of potential testers
        
        Returns:
            List of invitation tracking records
        """
        invitation_tracking = []
        
        for tester in potential_testers:
            invitation_code = self.generate_invitation_code()
            email_sent = self.send_invitation_email(tester, invitation_code)
            
            invitation_record = {
                'name': tester['name'],
                'email': tester['email'],
                'invitation_code': invitation_code,
                'invitation_date': datetime.now().isoformat(),
                'email_sent': email_sent,
                'status': 'invited'
            }
            
            invitation_tracking.append(invitation_record)
            
            # Save individual invitation record
            record_filename = f"{invitation_code}_invitation.json"
            record_path = os.path.join(self.recruitment_dir, record_filename)
            
            with open(record_path, 'w') as f:
                import json
                json.dump(invitation_record, f, indent=2)
        
        # Save comprehensive tracking file
        tracking_path = os.path.join(
            self.recruitment_dir, 
            f'beta_tester_invitations_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )
        
        with open(tracking_path, 'w') as f:
            import json
            json.dump(invitation_tracking, f, indent=2)
        
        return invitation_tracking

def main():
    """
    Run beta tester recruitment process
    """
    # Ensure CSV with potential testers exists
    recruitment_manager = BetaTesterRecruitment()
    
    # Load potential testers (replace with actual CSV path)
    potential_testers = recruitment_manager.load_potential_testers(
        'potential_beta_testers.csv'
    )
    
    # Track and send invitations
    invitation_results = recruitment_manager.track_beta_tester_invitations(
        potential_testers
    )
    
    print("Beta Tester Recruitment Complete")
    print(f"Total Invitations: {len(invitation_results)}")

if __name__ == '__main__':
    main()
