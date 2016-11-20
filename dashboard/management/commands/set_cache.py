from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'creates cache of list of DSRs'

    def handle(self, *args, **options):
        dsrs = User.objects.filter(is_superuser=False)
        try:
            cache.set('dsrs', dsrs)
        except:
            raise CommandError('Cache could not be set for ' % dsrs)
        self.stdout.write(self.style.SUCCESS('Successfully set for "%s"' % dsrs))
        return
