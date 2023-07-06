"""New syntax test file"""

from pathlib import Path

from pytest_bdd import then, parsers

from clowder.util.format import Format

from tests.functional.util import CommandResults


@then(parsers.parse("the command printed {branch_type} branches"))
def then_command_printed_branch_type(tmp_path: Path, branch_type: str) -> None:
    # FIXME: Implement
    pass


@then(parsers.parse("output matches contents of {filename} test file"))
def then_output_matches_contents_of_file(shared_datadir: Path, tmp_path: Path,
                                         command_results: CommandResults, filename: str) -> None:
    assert len(command_results.completed_processes) == 1
    result = command_results.completed_processes[0]
    output: str = Format.clean_escape_sequences(result.stdout)
    test_file = shared_datadir / "yaml" / "command_output" / filename
    test_content = test_file.read_text()
    assert output.strip() == test_content.strip()


@then(parsers.parse("file {output_file} matches contents of {test_file} test file"))
def then_output_file_matches_contents_of_file(shared_datadir: Path, tmp_path: Path, command_results: CommandResults,
                                              output_file: str, test_file: str) -> None:
    output_file = tmp_path / output_file
    output_contents = output_file.read_text()
    output = Format.clean_escape_sequences(output_contents)
    test_file = shared_datadir / "yaml" / "command_output" / test_file
    test_content = test_file.read_text()
    assert output.strip() == test_content.strip()
