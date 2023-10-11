"""
A collection of helper utilities to use when working with files.
"""


import csv
import os
from rest_framework import status

from config.constants import Constants, APIMessage


def read_investments_from_file(file_path):
    """Read the file at provided path and create a data dict with all the relevant information."""

    import_data = {}

    if not os.path.isfile(file_path):
        return APIMessage(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            payload=APIMessage.NO_FILE_FOUND,
        )
    try:
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            next(csv_reader)
            for row in csv_reader:
                import_data[row[2]] = {
                    "investment_type": Constants.InvestmentType.SHARES
                    if row[0] == "share"
                    else Constants.InvestmentType.CRYPTO,
                    "name": row[1],
                }
            return APIMessage(status=status.HTTP_200_OK, payload=import_data)
    except Exception as e:
        return APIMessage(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            payload=f"{APIMessage.ERROR_READING_FILE}: {e}.",
        )
