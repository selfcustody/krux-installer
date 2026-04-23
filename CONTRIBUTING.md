# Contributing to `Krux-Installer`

The development of `Krux-Installer` is a free and open-source, community-driven
effort that welcomes contributions from anyone. We are excited that you are
interested in helping us bring sovereign and private self-custody to everyone.

We welcome contributions in many forms, including bug reports, feature
requests, code contributions, and documentation improvements, from contributors
with any level of experience or expertise. We only ask that you respect others
and follow the process outlined in this document.

## Communication Channels

The primary communication channel is the
[GitHub repository](https://github.com/selfcustody/krux-installer).

## Contribution Workflow

The contribution workflow is designed to facilitate cooperation and ensure a
high level of quality in the project.

To contribute a patch, the workflow is as follows:

  1. Fork Repository
  2. Create topic branch
  3. Commit patches

### Commits

In general, commits should be atomic, and diffs should be easy to read.
For this reason, do not mix any formatting fixes or code moves with actual code
changes. Further, each commit should, where possible, compile and pass tests,
in order to ensure that git bisect and other automated tools function
properly.

When adding a new feature, ensure that it is covered by functional tests
whenever possible.

When refactoring, structure your PR so that it is easy to review, and don't
hesitate to split it into multiple small, focused PRs.

The Minimum Supported Python Version is **3.10.0** (enforced by our CI).
Commits should cover both the issue fixed and the solution's rationale.

These [guidelines](https://chris.beams.io/posts/git-commit/) should be kept in
mind. Commit messages follow the
["Conventional Commits 1.0.0"](https://www.conventionalcommits.org/en/v1.0.0/)
to make commit histories easier to read by humans and automated tools.
The types of commits we use are:

- `chore`: maintenance tasks;
- `ci`: continuous integration;
- `docs`: documentation changes;
- `feat`: new feature;
- `fix`: bug fix;
- `refactor`: code change that neither fixes a bug nor adds a feature;
- `style`: formatting, missing semicolons, etc; no code change;
- `test`: adding missing tests or correcting existing tests.

It is encouraged to
[GPG sign](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits)
your commits.

## Peer review

To make sure our code has the highest quality and is maintainable for
posterity, we have a thorough peer review process, where pull requests need
to be reviewed by at least one maintainer, and must not have any outstanding
comments from regular contributors.

### Conceptual Review

A review can be a conceptual review, where the reviewer leaves a comment:

- Concept (N)ACK: "I do (not) agree with the general goal of this pull request";
- Approach (N)ACK: Concept (N)ACK, but "I do (not) agree with the approach of
  this change";
- Untested ACK: "I didn't test, but ACK";
- Tested ACK: "I tested and ACKed".

A NACK needs to include a rationale why the change is not worthwhile.
NACKs without accompanying reasoning may be disregarded.

### Code Review

After conceptual agreement on the change, code review can be provided.
A review begins with ACK `<commit hash>`, where `<commit hash>` is the top
commit of the PR branch, followed by a description of how the reviewer did
the review. The following language is used within pull request comments:

`"I have tested the code"`, involving change-specific manual testing in
addition to running the unit, functional, or fuzz tests, and in case it is not
obvious how the manual testing was done, it should be described;
`"I have not tested the code, but I have reviewed it and it looks OK, I agree
it can be merged"`;
A `"nit"` refers to a trivial, often non-blocking issue.
Project maintainers reserve the right to weigh the opinions of peer reviewers
using common sense judgement and may also weigh based on merit. Reviewers that
have demonstrated a deeper commitment and understanding of the project over
time or who have clear domain expertise may naturally have more weight, as one
would expect in all walks of life.

## Coding Conventions

There's a few rules to make sure the code is readable and maintainable.
Most of them are checked by `poetry run poe lint` and `poetry run poe format`,
and are enforced by CI.

```python
# The MIT License (MIT)
# Copyright (c) 2021-2026 Krux contributors
# (full license header)
"""
module_name.py

Brief description of what this module does.
"""

class Foo:
    """
    Foo

    Brief description of the class.
    """

    def func(self):
        """Brief description of the method"""
        pass
```

All new features require testing. Tests should be unique and self-describing.
When it comes to error handling, we prefer exact and meaningful error handling
to deliver consumers (developers and users) an accurate error that describes
exactly what went wrong. Instead of:

```python
# bad: missing return statement, silently returns None instead of str
# A function that concatenates an int and a float into a str
def foo(
    bar: int,
    baz: float,
) -> str:
    str(bar) + str(baz)
```

prefer:

```python
# The MIT License (MIT)
# Copyright (c) 2021-2026 Krux contributors
# (full license header)
"""
foo.py

Utility functions for the project.
"""

def foo(
    bar: int,
    baz: float,
) -> str:
    """
    Concatenate an ``int`` and a ``float`` into a string.

    This function is provided as an example of the preferred style for
    function definitions and docstrings.

    Args:
    -----

        bar(int): the prepended message;

        baz(float): the appended message.

    Returns:
    --------

        str: the `int` and `float` converted to `str` and joined.
    """
    bar_str = str(bar)
    baz_str = str(baz)

    # Concatenate the string representations of the inputs.
    return bar_str + baz_str
```

## Testing

We expect to have 95% test coverage for critical parts,
and a decent level of coverage for everything. We have a
few types of tests that you can run using `poetry run poe test`:

Be aware when dealing with exceptions. We should guarantee them in many
weird cases.

- tests specific parts of the code under `src/utils`: the "backend";
- tests specific parts of the code under `src/app`: the "frontend".

## Release

Once a maintainer and the contributors decide we have a stable enough `main`
with sufficient features, we will create a new `tag`, with a `rev` message
and an assigned `v<X>.<Y>.<Z>` (see
[Semantic Versioning 2.0.0](https://semver.org)). From this point, all new
changes will go in the next release. After sufficient testing and making sure
we don't have bugs left, this `tag` will be released by one of the maintainers.

The release will have pre-built binaries available on GitHub's asset page.
They **must** be GPG signed by at least one of our main contributors,
and have a list of hashes for each asset (@odudex, @qlrd and/or @joaozinhom).

If we find bugs on a release, the fix may be backported and a new minor release
may be released. This is done by merging fixes on top of the release branch
and then performing another release on that branch.

If you have any questions related to this process or the codebase in general,
don't hesitate to reach out to us; we are happy to help newcomers on their
journey. Overall, have fun :)
