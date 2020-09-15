"""test_features"""

from pytest_bdd import scenarios

# scenarios('../features', example_converters=dict(number_commits=int, number_ahead=int, number_behind=int))
scenarios('../features/base.feature')
scenarios('../features/branch.feature')
scenarios('../features/checkout.feature')
scenarios('../features/clean.feature')
scenarios('../features/config.feature')
scenarios('../features/diff.feature')
scenarios('../features/forall.feature')
scenarios('../features/herd.feature')
scenarios('../features/init.feature')
scenarios('../features/link.feature')
scenarios('../features/prune.feature')
scenarios('../features/repo.feature')
scenarios('../features/reset.feature')
scenarios('../features/save.feature')
scenarios('../features/start.feature')
scenarios('../features/stash.feature')
scenarios('../features/status.feature')
scenarios('../features/yaml.feature')
