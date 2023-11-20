from .base import Base
from django.db import models

# Create Model Upload
class UploadedFile(Base):
    file = models.FileField()
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.uploaded_on.date()