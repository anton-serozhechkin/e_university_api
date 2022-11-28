from enum import Enum


'''
class ApplicationStatus(Enum):
    """Enum based class to set up Status of application status"""

    ACCEPTED = "Схвалено"
    REJECTED = "Відхилено"
    ON_REVIEW = "Розглядається"
    CANCELED = "Скасовано"
'''

ApplicationDict = {
    'Схвалено': 1,
    'Відхилено': 2,
    'Розглядається': 3,
    'Скасовано': 4
}

ApplicationStatus = Enum('ApplicationStatus', ApplicationDict)
