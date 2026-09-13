import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from pages.models import Page, PageSection, PageSectionItem


class Command(BaseCommand):
    help = (
        "Import the current React About, Sustainability, Press & Media, and "
        "DMC/Corporate content into Django without manual copy/paste."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            dest="file_path",
            help="Optional path to a Phase 2 seed JSON file.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be imported, then roll back the transaction.",
        )

    def handle(self, *args, **options):
        default_path = Path(settings.BASE_DIR) / "pages" / "data" / "react_pages_phase2.json"
        seed_path = Path(options.get("file_path") or default_path)

        if not seed_path.exists():
            raise CommandError(f"Seed file not found: {seed_path}")

        with seed_path.open("r", encoding="utf-8") as fh:
            payload = json.load(fh)

        pages = payload.get("pages", [])
        page_created = page_updated = 0
        section_created = section_updated = 0
        item_created = 0

        with transaction.atomic():
            for page_data in pages:
                page, created = Page.objects.update_or_create(
                    slug=page_data["slug"],
                    defaults={
                        "title": page_data.get("title", ""),
                        "subtitle": page_data.get("subtitle", ""),
                        "hero_image_url": page_data.get("hero_image_url", ""),
                        "hero_image_alt": page_data.get("hero_image_alt", ""),
                        "hero_tag": page_data.get("hero_tag", ""),
                        "body": page_data.get("body", ""),
                        "is_published": True,
                    },
                )
                if created:
                    page_created += 1
                else:
                    page_updated += 1

                for section_data in page_data.get("sections", []):
                    section, section_was_created = PageSection.objects.update_or_create(
                        page=page,
                        section_key=section_data["section_key"],
                        defaults={
                            "kicker": section_data.get("kicker", ""),
                            "heading": section_data.get("heading", ""),
                            "content": section_data.get("content", ""),
                            "image_url": section_data.get("image_url", ""),
                            "image_alt": section_data.get("image_alt", ""),
                            "link_label": section_data.get("link_label", ""),
                            "link_url": section_data.get("link_url", ""),
                            "order": section_data.get("order", 0),
                        },
                    )
                    if section_was_created:
                        section_created += 1
                    else:
                        section_updated += 1

                    # The seed is the source of truth during the migration phase.
                    # Recreate this section's items so rerunning the importer cleanly
                    # reflects changes in the React snapshot without duplicates.
                    section.items.all().delete()
                    for item_data in section_data.get("items", []):
                        PageSectionItem.objects.create(
                            section=section,
                            title=item_data.get("title", ""),
                            subtitle=item_data.get("subtitle", ""),
                            content=item_data.get("content", ""),
                            label=item_data.get("label", ""),
                            value=item_data.get("value", ""),
                            icon=item_data.get("icon", ""),
                            image_url=item_data.get("image_url", ""),
                            image_alt=item_data.get("image_alt", ""),
                            link_label=item_data.get("link_label", ""),
                            link_url=item_data.get("link_url", ""),
                            order=item_data.get("order", 0),
                        )
                        item_created += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"Pages: {page_created} created, {page_updated} updated"
                )
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Sections: {section_created} created, {section_updated} updated"
                )
            )
            self.stdout.write(
                self.style.SUCCESS(f"Section items written: {item_created}")
            )

            if options["dry_run"]:
                transaction.set_rollback(True)
                self.stdout.write(
                    self.style.WARNING("Dry run only: database changes rolled back.")
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        "Phase 2 page import complete. Do not rerun after making "
                        "editorial changes in Django Admin unless you intend to "
                        "resync these four pages from the React snapshot."
                    )
                )
