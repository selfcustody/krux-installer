# Contributing to ``Krux-Installer``

The development of `Krux-Installer` is FOSS and community effort based and
welcomes contributions from anyone. We are excited you are interested in
helping us bringing sovereign and private self-custody to everyone.

We welcome contributions in many forms, including bug reports, feature
requests, code contributions, and documentation improvements. From any
contributors with any level of experience or expertise. We only ask that you
respect others and follow the process outlined in this document.

## Communications Channels

The primary communication channel is the [GitHub repository](https://github.com/selfcustody/krux-installer).

## Contribution Workflow

The contribution workflow is designed to facilitate cooperation and ensure a
high level of quality in the project. The process is as follows:

To contribute a patch, the workflow is as follows:

  1. Fork Repository
  2. Create topic branch
  3. Commit patches

### Commits

In general commits should be atomic and diffs should be easy to read.
For this reason do not mix any formatting fixes or code moves with actual code
changes. Further, each commit, individually, should as possible compile and
pass tests, in order to ensure git bisect and other automated tools function
properly.

When adding a new feature ensure that it is covered by functional tests where
possible.

When refactoring, structure your PR to make it easy to review and don't
hesitate to split it into multiple small, focused PRs.

The Minimum Supported Python Version is **3.12.0** (enforced by our CI).
Commits should cover both the issue fixed and the solution's rationale.

These [guidelines](https://chris.beams.io/posts/git-commit/) should be kept in
mind. Commit messages follow the
["Conventional Commits 1.0.0"](https://www.conventionalcommits.org/en/v1.0.0/)
to make commit histories easier to read by humans and automated tools.
The types of commits we use are:

- chore: maintenance tasks;
- ci: continuous integration;
- docs: documentation changes;
- feat: new feature;
- fix: bug fix;
- refactor: code change that neither fixes a bug nor adds a feature;
- style: formatting, missing semi colons, etc; no code change;
- test: adding missing tests or correcting existing tests.

It is required to
[GPG sign](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits)
your commits.

## Peer review

To make sure our code has the highest quality and is maintainable for
posterity, we have a thorough peer review process, where pull requests need
to be reviewed by at least one maintainer, and must not have any outstanding
comment from regular contributors.

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
A review begins with ACK BRANCH_COMMIT, where BRANCH_COMMIT is the top of
the PR branch, followed by a description of how the reviewer did the review.
The following language is used within pull request comments:

"I have tested the code", involving change-specific manual testing in
addition to running the unit, functional, or fuzz tests, and in case it is not
obvious how the manual testing was done, it should be described;
"I have not tested the code, but I have reviewed it and it looks OK, I agree
it can be merged";
A "nit" refers to a trivial, often non-blocking issue.
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
"""Awesome module comment"""

class Foo:
   """Some awesome comment"""

      def func(self):
            """Some awesome comment"""
            pass
```

All new features require testing. Tests should be unique and self-describing.
When it comes error handling, we prefer exact and meaningful error handling
to deliver consumers(developers and users) an accurate error that describes
exactly what happened wrong. Instead of:

```python
# A function that concatenate a int and a float into a str
def foo(
    bar: int,
    baz: float,
) -> str:
  str(bar) + str(baz)
```

prefer:

```python
"""src.utils.foo: a good description"""

# A function that concatenate a int and a float into a str and why do that
# for a good and reasonable reason that you should discuss with other developers
def foo(
    bar: int,
    baz: float,
) -> str:
  """I do that because i liked""""
  bar_str = str(bar)
  baz_str = str(baz)

  # We need to concatenate to be compliant
  return bar_str + baz_str
```

## Testing

We expect to have 100% test coverage for critical parts,
and a decent level of coverage for everything. We have a
few types of tests that you can run using `poetry run poe test`:

- tests specific parts of the code under `src/utils`: the "backend";
- tests specific parts of the code under `src/app`: the "frontend".

## Release

Once a maintainer and the contributors decide we have a stable enough `main`
with sufficient features, we will create a new branch at that point. From this
point, all new changes will go in the next release. After sufficient testing
and making sure we don't have bugs left, this branch will be released by one
of the maintainers.

The release will have pre-built binaries available on github's asset page.
They **must** be GPG signed, and have a list of hashes for each asset.

If we find bugs on a release, the fix may be backported and a new minor release
may be released. This is done by merging fixes on top of the release branch.
And then performing another release on that branch.

If you have any questions, related to this process or the codebase in general.
Don't hesitate to reach us out, we are happy to help newcomers in their amazing
journey. Overall, have fun :)
