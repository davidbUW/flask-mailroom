from math import floor
import peewee as pw
from loguru import logger
from model import Donor, Donation, db


def check_donor(donor, donation):
    """
    Function to check if donor exists
    :param donor: from create form
    :param donation: from create form
    :return: add donor if donor does not exist
    :return: add donation if donor does exist using unique donor id
    """
    try:
        donor_id = Donor.get(Donor.name == donor)
    except Donor.DoesNotExist as error:
        logger.error(f'No donor found')
        logger.info(error)
        return add_donor(donor, donation)
    return add_donation(donor_id.id, donation)


def add_donor(donor, donation):
    """
    Function to add new donor
    :param donor: from create form
    :param donation: from create form
    :return: call to add donation function
    """
    try:
        with db.transaction():
            new_donor = Donor.create(name=donor)
            new_donor.save()
    except pw.IntegrityError as error:
        logger.error(f'Error creating new donor')
        logger.info(error)
        return False
    return check_donor(donor, donation)


def add_donation(donor, donation):
    """
    Function to add donation
    :param donor: from unique id
    :param donation: from create form
    :return: False if Error or True if successfully added
    """
    try:
        with db.transaction():

            new_donation = Donation.create(donor=donor,
                                           value=floor(float(donation)))
            new_donation.save()
    except pw.IntegrityError as error:
        logger.error(f'Error creating new donation')
        logger.info(error)
        return False
    return True


def view_donations(donor):
    """
    Function to view all of a donors donations
    :param donor: from single donor form
    :return: False users does not exist
    :return: donations peewee.Model.Select object if user exists
    """
    try:
        donor_id = Donor.get(Donor.name == donor)
        donations = Donation.select().where(Donation.donor[donor_id])
    except Donor.DoesNotExist as error:
        logger.error(f'No donor found')
        logger.info(error)
        return False
    return donations
