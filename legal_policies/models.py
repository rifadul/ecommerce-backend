# models.py
from tinymce.models import HTMLField

from common.model import BaseModel

class PrivacyPolicy(BaseModel):
    content = HTMLField()

    def __str__(self):
        return "Privacy Policy"

class TermsAndConditions(BaseModel):
    content = HTMLField()

    def __str__(self):
        return "Terms and Conditions"
