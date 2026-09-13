import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from catalog.models import SafariPackage
from pages.models import FAQ


class Command(BaseCommand):
    help = (
        "Import the current React safari detail content and Contact FAQ content "
        "into Django without manual copy/paste. Safe to run more than once."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            dest="file_path",
            help="Optional path to a seed JSON file.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be imported, then roll back the transaction.",
        )

    def handle(self, *args, **options):
        default_path = Path(settings.BASE_DIR) / "catalog" / "data" / "react_seed_phase1.json"
        seed_path = Path(options.get("file_path") or default_path)

        if not seed_path.exists():
            raise CommandError(f"Seed file not found: {seed_path}")

        with seed_path.open("r", encoding="utf-8") as fh:
            payload = json.load(fh)

        packages = payload.get("packages", [])
        faqs = payload.get("faqs", [])

        package_created = 0
        package_updated = 0
        faq_created = 0
        faq_updated = 0

        with transaction.atomic():
            for item in packages:
                defaults = {
                    "title": item.get("title", ""),
                    "subtitle": item.get("subtitle", ""),
                    "tag": item.get("tag", ""),
                    "image": item.get("image", ""),
                    "image_alt": item.get("image_alt", ""),
                    "duration": item.get("duration", ""),
                    "price_label": item.get("price_label", ""),
                    "group_size": item.get("group_size", ""),
                    "difficulty": item.get("difficulty", ""),
                    "overview": item.get("overview", ""),
                    "highlights": item.get("highlights", []),
                    "itinerary": item.get("itinerary", []),
                    "includes": item.get("includes", []),
                    "excludes": item.get("excludes", []),
                    "related_links": item.get("related_links", []),
                    "badge": item.get("badge", ""),
                    "is_published": True,
                }

                _, created = SafariPackage.objects.update_or_create(
                    slug=item["slug"],
                    defaults=defaults,
                )
                if created:
                    package_created += 1
                else:
                    package_updated += 1

            for item in faqs:
                _, created = FAQ.objects.update_or_create(
                    question=item["question"],
                    defaults={
                        "answer": item.get("answer", ""),
                        "order": item.get("order", 0),
                        "is_published": True,
                    },
                )
                if created:
                    faq_created += 1
                else:
                    faq_updated += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"Safari packages: {package_created} created, {package_updated} updated"
                )
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"FAQs: {faq_created} created, {faq_updated} updated"
                )
            )

            if options["dry_run"]:
                transaction.set_rollback(True)
                self.stdout.write(self.style.WARNING("Dry run only: database changes rolled back."))
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        "Phase 1 import complete. The command is idempotent and can be run again."
                    )
                )
