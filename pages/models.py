from django.db import models


class Page(models.Model):
    """
    One editable page (About Us, Sustainability, Press & Media, DMC/Corporate,
    Home hero, etc). The frontend fetches by `slug` and matches it to the
    section it's rendering, so slugs must line up with what each React page
    requests - e.g. 'about-us', 'sustainability', 'press-media',
    'dmc-corporate', 'home'.
    """

    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    hero_image = models.ImageField(upload_to="pages/", blank=True, null=True)
    body = models.TextField(
        blank=True, help_text="Main page copy. Plain text or HTML, rendered as-is by the frontend.",
    )
    sections = models.JSONField(
        default=list, blank=True,
        help_text=(
            "Optional structured extra content for pages with repeating blocks "
            "(e.g. team members, press mentions). Free-form list of objects."
        ),
    )
    is_published = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class FAQ(models.Model):
    """Question/answer pairs shown on the Contact page."""

    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question
