from datetime import datetime, timedelta
from .db import db


class URLMap(db.Model):
    """
    Model of the table that will store the URL Mapping for the short URL and long URL (which is being shortened)
    """
    __tablename__ = "url_map"

    short_code = db.Column(db.String(10), primary_key=True)
    original_url = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, short_code, original_url):
        """
        Args:
            short_code (string): Random code generated to keep the url short and unique
            original_url (string): Actual URL being shortened
        Returns:
        """
        self.short_code = short_code
        self.original_url = original_url
        self.created_at = datetime.utcnow()
