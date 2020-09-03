"""test_features"""

# noinspection PyPackageRequirements
from pytest_bdd import scenarios

scenarios('../features', example_converters=dict(number_commits=int, number_ahead=int, number_behind=int))
