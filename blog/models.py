from django.db import models


class BlogPost(models.Model):
    """
    A single guide/blog article (Kenya Safari Cost, Masai Mara Safari Cost,
    Nairobi to Masai Mara Flights, etc). Powers the 'Guides & Blog' hub and
    each individual article page.
    """

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, help_text="Used in the URL, e.g. 'kenya-safari-cost'")
    tag = models.CharField(max_length=60, help_text="e.g. 'Budget Guide', 'Getting There', 'Destination'")
    excerpt = models.CharField(
        max_length=300, help_text="Short teaser shown on the guides hub card",
    )
    body = models.TextField(help_text="Full article content. Plain text or HTML, rendered as-is by the frontend.")
    hero_image = models.ImageField(upload_to="blog/", blank=True, null=True)
    read_time_minutes = models.PositiveIntegerField(
        default=5, help_text="Shown to readers as 'N min read' - set manually or estimate from word count",
    )
    author = models.CharField(max_length=120, blank=True)
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first on the guides hub")

    class Meta:
        ordering = ["order", "-published_at"]

    def __str__(self):
        return self.title
