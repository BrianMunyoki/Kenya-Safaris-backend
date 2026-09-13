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
    Editable general website page.

    React controls presentation/layout. Django stores the editable content.
    External image URL fields preserve the images already used by the React site,
    while the ImageField remains available if local/cloud uploads are added later.
    """

    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)

    hero_image = models.ImageField(upload_to="pages/", blank=True, null=True)
    hero_image_url = models.URLField(max_length=1000, blank=True)
    hero_image_alt = models.CharField(max_length=255, blank=True)
    hero_tag = models.CharField(max_length=100, blank=True)

    body = ProseEditorField(
        blank=True,
        extensions=EDITOR_EXTENSIONS,
        sanitize=True,
        help_text="Main page content.",
    )

    is_published = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class PageSection(models.Model):
    """
    A named content section belonging to a Page.

    section_key is the stable identifier React can use to select the correct
    visual layout, e.g. story, team, pillars, services, press-coverage.
    """

    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name="sections",
    )

    section_key = models.SlugField(
        max_length=100,
        blank=True,
        help_text="Stable key used by React, e.g. story, team, services.",
    )
    kicker = models.CharField(max_length=160, blank=True)
    heading = models.CharField(max_length=200, blank=True)

    content = ProseEditorField(
        blank=True,
        extensions=EDITOR_EXTENSIONS,
        sanitize=True,
    )

    image = models.ImageField(upload_to="pages/sections/", blank=True, null=True)
    image_url = models.URLField(max_length=1000, blank=True)
    image_alt = models.CharField(max_length=255, blank=True)

    link_label = models.CharField(max_length=160, blank=True)
    link_url = models.CharField(max_length=500, blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.heading or self.section_key or f"Section {self.pk}"


class PageSectionItem(models.Model):
    """
    Repeatable item inside a page section.

    This replaces the need to type arrays/objects into JSON fields. It can hold
    team members, statistics, sustainability pillars, press mentions, services,
    awards, clients, certifications, and similar repeatable content.
    """

    section = models.ForeignKey(
        PageSection,
        on_delete=models.CASCADE,
        related_name="items",
    )

    title = models.CharField(max_length=250, blank=True)
    subtitle = models.CharField(max_length=300, blank=True)
    content = ProseEditorField(
        blank=True,
        extensions=EDITOR_EXTENSIONS,
        sanitize=True,
    )

    label = models.CharField(max_length=160, blank=True)
    value = models.CharField(max_length=160, blank=True)
    icon = models.CharField(max_length=40, blank=True)

    image_url = models.URLField(max_length=1000, blank=True)
    image_alt = models.CharField(max_length=255, blank=True)

    link_label = models.CharField(max_length=160, blank=True)
    link_url = models.CharField(max_length=500, blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title or self.label or f"Item {self.pk}"


class FAQ(models.Model):
    question = models.CharField(max_length=300)

    answer = ProseEditorField(
        extensions=EDITOR_EXTENSIONS,
        sanitize=True,
    )

    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question
