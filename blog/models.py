from django.db import models
from django_prose_editor.fields import ProseEditorField


class BlogPost(models.Model):
    title = models.CharField(max_length=200)

    slug = models.SlugField(
        max_length=220,
        unique=True,
        help_text="Used in the URL, e.g. 'kenya-safari-cost'",
    )

    tag = models.CharField(
        max_length=60,
        help_text="e.g. 'Budget Guide', 'Getting There', 'Destination'",
    )

    excerpt = models.CharField(
        max_length=300,
        help_text="Short teaser shown on the guides hub card",
    )

    body = ProseEditorField(
        extensions={
            "Bold": True,
            "Italic": True,
            "Heading": {"levels": [2, 3, 4]},
            "BulletList": True,
            "OrderedList": True,
            "ListItem": True,
            "Blockquote": True,
            "Link": {
                "protocols": ["http", "https", "mailto"],
            },
            "HorizontalRule": True,
        },
        sanitize=True,
        help_text="Write and format the full article here.",
    )

    hero_image = models.ImageField(
        upload_to="blog/",
        blank=True,
        null=True,
    )

    read_time_minutes = models.PositiveIntegerField(
        default=5,
        help_text="Shown to readers as 'N min read' - set manually or estimate from word count",
    )

    author = models.CharField(
        max_length=120,
        blank=True,
    )

    is_published = models.BooleanField(
        default=True,
    )

    published_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    order = models.PositiveIntegerField(
        default=0,
        help_text="Lower numbers show first on the guides hub",
    )

    class Meta:
        ordering = ["order", "-published_at"]

    def __str__(self):
        return self.title