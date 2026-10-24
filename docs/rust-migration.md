# Rust Migration

Port clowder cli from python to rust.

Goals:

- Better performance
- Better portability (single binary)
- Better multithreading (especially for parallel clowder command options)

Keep all current BDD Gherkin files. So also keep python test harness and runner if that's the easiest route. All current tests are functional tests and call the cli interface so this should be a clean layer of separation. I only care about porting the actual cli to rust.

Before porting, feel free to create more tests that capture and preserve command output formatting. Tests will need to ignore parts that predictably change between test runs, but much should be consistent between runs. Currently many tests just confirm that commands exit successfully (i.e. help commands), but don't check the actual output.

Commit and push to `rust-migration` branch as you make progress. Check CI validation status on PR.

While working on this migration, check ChatGPT usage periodically. At 10% remaining or below, use one reset without asking. Keep the second reset in reserve.
