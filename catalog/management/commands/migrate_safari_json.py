from django.core.management.base import BaseCommand
from django.db import transaction

from catalog.models import (
    SafariPackage,
    SafariHighlight,
    SafariItineraryDay,
    SafariInclude,
    SafariExclude,
    SafariRelatedLink,
)


class Command(BaseCommand):
    help = (
        "Copies SafariPackage JSON fields into the new related models. "
        "Existing JSON fields are left untouched."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be migrated, then roll back all changes.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        counts = {
            "packages": 0,
            "highlights": 0,
            "itinerary": 0,
            "includes": 0,
            "excludes": 0,
            "links": 0,
        }

        skipped = {
            "highlights": 0,
            "itinerary": 0,
            "includes": 0,
            "excludes": 0,
            "links": 0,
        }

        for package in SafariPackage.objects.all():
            counts["packages"] += 1

            if package.highlight_items.exists():
                skipped["highlights"] += 1
            else:
                for order, item in enumerate(package.highlights or []):
                    text = (
                        item.get("text", "")
                        if isinstance(item, dict)
                        else str(item)
                    ).strip()

                    if text:
                        SafariHighlight.objects.create(
                            safari_package=package,
                            text=text,
                            order=order,
                        )
                        counts["highlights"] += 1

            if package.itinerary_days.exists():
                skipped["itinerary"] += 1
            else:
                for order, item in enumerate(package.itinerary or []):
                    if not isinstance(item, dict):
                        continue

                    SafariItineraryDay.objects.create(
                        safari_package=package,
                        day=str(item.get("day", "")).strip(),
                        title=str(item.get("title", "")).strip(),
                        description=str(
                            item.get("desc")
                            or item.get("description")
                            or ""
                        ).strip(),
                        order=order,
                    )
                    counts["itinerary"] += 1

            if package.include_items.exists():
                skipped["includes"] += 1
            else:
                for order, item in enumerate(package.includes or []):
                    text = (
                        item.get("text", "")
                        if isinstance(item, dict)
                        else str(item)
                    ).strip()

                    if text:
                        SafariInclude.objects.create(
                            safari_package=package,
                            text=text,
                            order=order,
                        )
                        counts["includes"] += 1

            if package.exclude_items.exists():
                skipped["excludes"] += 1
            else:
                for order, item in enumerate(package.excludes or []):
                    text = (
                        item.get("text", "")
                        if isinstance(item, dict)
                        else str(item)
                    ).strip()

                    if text:
                        SafariExclude.objects.create(
                            safari_package=package,
                            text=text,
                            order=order,
                        )
                        counts["excludes"] += 1

            if package.related_link_items.exists():
                skipped["links"] += 1
            else:
                for order, item in enumerate(package.related_links or []):
                    if not isinstance(item, dict):
                        continue

                    label = str(item.get("label", "")).strip()
                    url = str(
                        item.get("url")
                        or item.get("to")
                        or ""
                    ).strip()

                    if label or url:
                        SafariRelatedLink.objects.create(
                            safari_package=package,
                            label=label,
                            url=url,
                            order=order,
                        )
                        counts["links"] += 1

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Safari packages checked: {counts['packages']}"
            )
        )

        self.stdout.write(f"Highlights created: {counts['highlights']}")
        self.stdout.write(f"Itinerary days created: {counts['itinerary']}")
        self.stdout.write(f"Includes created: {counts['includes']}")
        self.stdout.write(f"Excludes created: {counts['excludes']}")
        self.stdout.write(f"Related links created: {counts['links']}")

        self.stdout.write("")
        self.stdout.write(
            "Packages skipped because related data already existed:"
        )

        self.stdout.write(f"Highlights: {skipped['highlights']}")
        self.stdout.write(f"Itinerary: {skipped['itinerary']}")
        self.stdout.write(f"Includes: {skipped['includes']}")
        self.stdout.write(f"Excludes: {skipped['excludes']}")
        self.stdout.write(f"Related links: {skipped['links']}")

        if dry_run:
            transaction.set_rollback(True)

            self.stdout.write("")
            self.stdout.write(
                self.style.WARNING(
                    "Dry run only: all database changes rolled back."
                )
            )
        else:
            self.stdout.write("")
            self.stdout.write(
                self.style.SUCCESS(
                    "Safari JSON migration complete. "
                    "Original JSON fields were NOT deleted."
                )
            )