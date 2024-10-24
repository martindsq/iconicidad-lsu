from django.core.management.base import BaseCommand
import logging
import csv
from iconicities.models import Stimulus

logger = logging.getLogger(__name__)

# python manage.py seed --mode=refresh

""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    logger.info("Delete all stimuli instances")
    Stimulus.objects.all().delete()


def create_stimulus(term, filename):
    """Creates an address object combining different elements from the list"""
    logger.info("Creating stimulus")
    stimulus = Stimulus(term=term, file_name=filename)
    stimulus.save()
    logger.info("{} stimulus created.".format(stimulus))

def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    # Creating stimuli
    import os
    module_dir = os.path.dirname(__file__)  # get current directory
    path = os.path.join(module_dir, 'seed.csv')
    with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            create_stimulus(row[0], row[1])
