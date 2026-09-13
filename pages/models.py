from django.db import models
from django_prose_editor.fields import ProseEditorField


EDITOR_EXTENSIONS = {
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
}


class Page(models.Model):
    """
    Editable general website page:
    About Us, Sustainability, Press & Media, DMC/Corporate, etc.
    """

    slug = models.SlugField(
        max_length=100,
        unique=True,
    )

    title = models.CharField(
        max_length=200,
    )

    subtitle = models.CharField(
        max_length=300,
        blank=True,
    )

    hero_image = models.ImageField(
        upload_to="pages/",
        blank=True,
        null=True,
    )

    body = ProseEditorField(
        blank=True,
        extensions=EDITOR_EXTENSIONS,
        sanitize=True,
        help_text="Main page content.",
    )

    is_published = models.BooleanField(
        default=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.title


class PageSection(models.Model):
    """
    A repeatable content section belonging to a Page.
    """

    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name="sections",
    )

    heading = models.CharField(
        max_length=200,
        blank=True,
    )

    content = ProseEditorField(
        blank=True,
        extensions=EDITOR_EXTENSIONS,
        sanitize=True,
    )

    image = models.ImageField(
        upload_to="pages/sections/",
        blank=True,
        null=True,
    )

    image_alt = models.CharField(
        max_length=255,
        blank=True,
    )

    order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.heading or f"Section {self.pk}"


class FAQ(models.Model):
    question = models.CharField(
        max_length=300,
    )

    answer = ProseEditorField(
        extensions=EDITOR_EXTENSIONS,
        sanitize=True,
    )

    order = models.PositiveIntegerField(
        default=0,
    )

    is_published = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["order"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question