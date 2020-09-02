"""New syntax test file"""

from pathlib import Path

# noinspection PyPackageRequirements
from pytest_bdd import then, parsers

from tests.functional.util import CommandResults


@then(parsers.parse("the command printed {branch_type} branches"))
def then_command_printed_branch_type(tmp_path: Path, branch_type: str) -> None:
    # FIXME: Implement
    pass


@then(parsers.parse("output matches contents of {file_name}"))
def then_output_matches_contents_of_file(tmp_path: Path, command_results: CommandResults, file_name: str) -> None:
    assert len(command_results.completed_processes) == 1
    result = command_results.completed_processes[0]
    output: str = result.stdout
    test_file = tmp_path / file_name
    test_content = test_file.read_text()
    assert output.strip() == test_content.strip()
