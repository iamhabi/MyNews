"""Django's command-line utility for administrative tasks."""
import os
import sys

import news_scraper


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    try:
        subcommand = sys.argv[1]

        if subcommand == "runserver":
            news_scraper.scraping()
    except IndexError:
        subcommand = "help"

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
