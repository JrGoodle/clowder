"""New syntax test file"""

from pathlib import Path

from pytest_bdd import then, parsers

import tests.functional.util as util
from tests.functional.util import CommandResults


@then(parsers.parse("the command printed {branch_type} branches"))
def then_command_printed_branch_type(tmp_path: Path, branch_type: str) -> None:
    # FIXME: Implement
    pass


@then(parsers.parse("output matches contents of {filename}"))
def then_output_matches_contents_of_file(tmp_path: Path, command_results: CommandResults, filename: str) -> None:
    assert len(command_results.completed_processes) == 1
    result = command_results.completed_processes[0]
    output: str = util.clean_escape_sequences(result.stdout)
    test_file = tmp_path / filename
    test_content = test_file.read_text()
    assert output.strip() == test_content.strip()
