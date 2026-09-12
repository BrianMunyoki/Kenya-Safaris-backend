from django.db import models


class Destination(models.Model):
    """One entry on the Destinations hub (Tanzania, Botswana, Rwanda...)."""

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, help_text="Used in the URL, e.g. 'tanzania'")
    tag = models.CharField(max_length=80, blank=True, help_text="e.g. 'East Africa'")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="destinations/", blank=True, null=True)
    highlights = models.JSONField(
        default=list, blank=True,
        help_text="List of short tags, e.g. [\"Serengeti\", \"Ngorongoro\"]",
    )
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class SafariPackage(models.Model):
    """Safari package or safari information page."""

    title = models.CharField(max_length=160)

    slug = models.SlugField(
        max_length=180,
        unique=True,
        help_text="e.g. 'masai-mara-3day'"
    )

    destination = models.ForeignKey(
        Destination,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="packages",
    )

    subtitle = models.TextField(blank=True)

    tag = models.CharField(
        max_length=100,
        blank=True
    )

    image = models.URLField(
        max_length=500,
        blank=True
    )

    image_alt = models.CharField(
        max_length=255,
        blank=True
    )

    duration = models.CharField(
        max_length=60,
        blank=True
    )

    price_label = models.CharField(
        max_length=100,
        blank=True
    )

    group_size = models.CharField(
        max_length=100,
        blank=True
    )

    difficulty = models.CharField(
        max_length=100,
        blank=True
    )

    overview = models.TextField(
        blank=True
    )

    highlights = models.JSONField(
        default=list,
        blank=True
    )

    itinerary = models.JSONField(
        default=list,
        blank=True
    )

    includes = models.JSONField(
        default=list,
        blank=True
    )

    excludes = models.JSONField(
        default=list,
        blank=True
    )

    related_links = models.JSONField(
        default=list,
        blank=True
    )

    badge = models.CharField(
        max_length=40,
        blank=True,
        help_text="e.g. 'Best Seller', 'Seasonal', 'Premium'"
    )

    is_published = models.BooleanField(
        default=True
    )

    order = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title