from django.db import models


class LeadStatus(models.TextChoices):
    NEW = "new", "New"
    CONTACTED = "contacted", "Contacted"
    CLOSED = "closed", "Closed"


SUBJECT_CHOICES = [
    ("Safari Enquiry", "Safari Enquiry"),
    ("Quote Request", "Quote Request"),
    ("Booking Question", "Booking Question"),
    ("DMC / Corporate", "DMC / Corporate"),
    ("Press / Media", "Press / Media"),
    ("General Question", "General Question"),
]


class ContactEnquiry(models.Model):
    """Submission from the Contact page form."""

    name = models.CharField(max_length=160)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    subject = models.CharField(max_length=60, choices=SUBJECT_CHOICES)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=LeadStatus.choices, default=LeadStatus.NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Contact enquiries"

    def __str__(self):
        return f"{self.name} - {self.subject}"


class TripEnquiry(models.Model):
    """Submission from the 3-step Plan My Trip wizard."""

    name = models.CharField(max_length=160)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    preferred_dates = models.CharField(max_length=120, blank=True)
    guests = models.CharField(max_length=20, blank=True, help_text="e.g. '2', '7\u201310'")
    notes = models.TextField(blank=True)

    destinations = models.JSONField(default=list, blank=True)
    duration = models.JSONField(default=list, blank=True)
    budget = models.JSONField(default=list, blank=True)
    safari_type = models.JSONField(default=list, blank=True)

    status = models.CharField(max_length=20, choices=LeadStatus.choices, default=LeadStatus.NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Trip enquiries"

    def __str__(self):
        return f"{self.name} - {self.preferred_dates or 'no dates given'}"
