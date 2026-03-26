const GREETINGS = [
  "It looks like you've modified some files",
  "that we can't accept as contributions.",
  "The complete list of files we can't accept are:"
].join(" ");

const WARNING = [
  "You'll need to revert and edit or rebase your changes.",
  "Once you get those files reverted, we can continue with",
  "review procedures. :octocat:"
].join(" ");

const ERROR = [
  "We failed in something, it's not your fault, but you",
  "will need to retrigger with \`git commit --amend --no-edit\` and",
  "\`git push --force-with-lease\`."
].join(" ");

/**
 * Build the rejection comment for unauthorized file changes.
 *
 * @param {string} actor - GitHub username of the PR author
 * @param {string} badFiles - Newline-bullet-separated file list
 * @returns {string} Formatted rejection comment body
 *
 * @example
 * const msg = get_not_allowed("some-user", "LICENSE\n- AGENT.md");
 * console.assert(msg.includes("Hey there some-user"));
 * console.assert(msg.includes("- LICENSE"));
 * console.assert(msg.includes("- AGENT.md"));
 */
function get_not_allowed(actor, badFiles)
{
  return (`👋 Hey there ${actor}.

${GREETINGS}

- ${badFiles}

${WARNING}`
  );
}

/**
 * Append a comment link to the failure message.
 *
 * @param {string} msg - Base failure message
 * @param {object} createdComment - GitHub API comment response
 * @param {string} createdComment.data.html_url - Comment URL
 * @returns {string} Failure message with comment link appended
 *
 * @example
 * const comment = {
 *   data: { html_url: "https://github.com/org/repo/pull/1#issuecomment-123" }
 * };
 * const result = get_failed_msg("Something failed.", comment);
 * console.assert(result.includes("Something failed."));
 * console.assert(result.includes("Please see https://github.com"));
 */
function get_failed_msg(msg, createdComment)
{
  return (`${msg}

Please see ${createdComment.data.html_url} for details.`
  );
}

/**
 * Check if PR author has permissions to edit protected files.
 *
 * @param {object} context - GitHub Actions context object
 * @param {object} context.payload.pull_request
 * @param {string} context.payload.pull_request.author_association
 * @returns {boolean} `true` if COLLABORATOR, MEMBER, or OWNER
 *
 * @example
 * const ctx_member = {
 *   payload: { pull_request: { author_association: "MEMBER" } }
 * };
 * console.assert(is_valid_author(ctx_member) === true);
 *
 * @example
 * const ctx_none = {
 *   payload: { pull_request: { author_association: "NONE" } }
 * };
 * console.assert(is_valid_author(ctx_none) === false);
 *
 * @example
 * const ctx_missing = { payload: {} };
 * console.assert(is_valid_author(ctx_missing) === false);
 */
function is_valid_author(context)
{
  const allowedAssociations = ['COLLABORATOR', 'MEMBER', 'OWNER'];
  const authorAssociation = context.payload.pull_request
    && context.payload.pull_request.author_association;

  return allowedAssociations.includes(authorAssociation);
}

/**
 * Post an error comment when the workflow fails internally.
 *
 * @param {object} github - GitHub API client
 * @param {object} context - GitHub Actions context object
 * @param {object} context.repo - Repository owner and name
 * @param {number} context.payload.number - PR number
 * @param {Error} err - The caught error
 * @returns {Promise<object>} GitHub API comment response
 *
 * @example
 * const err = new Error("JSON.parse failed");
 * // const comment = await on_error(github, context, err);
 * // console.assert(comment.data.html_url.includes("github.com"));
 */
async function on_error(github, context, err)
{
  const reviewMessage = `${ERROR}

${err.toString()}`;

  return await github.rest.issues.createComment({
    owner: context.repo.owner,
    repo: context.repo.repo,
    issue_number: context.payload.number,
    body: reviewMessage,
  });
}

/**
 * Filter author permissions on protected file changes.
 *
 * Posts a rejection comment and fails the workflow if an
 * unauthorized contributor modifies protected files.
 * Permitted authors (COLLABORATOR, MEMBER, OWNER) pass
 * through silently.
 *
 * Requires `CHANGE_FILES` environment variable set via
 * `env:` in the workflow YAML as a JSON array of changed
 * file paths.
 *
 * @param {object} params - Destructured github-script params
 * @param {object} params.github - GitHub API client
 * @param {object} params.context - GitHub Actions context
 * @param {string} params.context.actor - PR author username
 * @param {object} params.context.payload - Webhook payload
 * @param {object} params.context.repo - Repository info
 * @param {object} params.core - Actions core utilities
 *
 * @example
 * // Unauthorized contributor:
 * process.env.CHANGE_FILES = '["LICENSE", "AGENT.md"]';
 * const context = {
 *   actor: "external-user",
 *   payload: {
 *     pull_request: { author_association: "NONE" },
 *     number: 42
 *   },
 *   repo: { owner: "selfcustody", repo: "krux-installer" }
 * };
 * // await script({github, context, core});
 * // -> posts rejection comment, calls core.setFailed()
 *
 * @example
 * // Permitted maintainer:
 * const context_member = {
 *   actor: "maintainer",
 *   payload: {
 *     pull_request: { author_association: "MEMBER" },
 *     number: 42
 *   },
 *   repo: { owner: "selfcustody", repo: "krux-installer" }
 * };
 * // await script({github, context: context_member, core});
 * // -> returns silently, no comment, no failure
 */
module.exports = async ({github, context, core}) =>
{
  try
  {
    if (is_valid_author(context))
      return;

    const badFiles = JSON.parse(process.env.CHANGE_FILES).join("\n- ");
    const reviewMessage = get_not_allowed(context.actor, badFiles);
    const createdComment = await github.rest.issues.createComment({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: context.payload.number,
      body: reviewMessage,
    });

    const msg = get_failed_msg(WARNING, createdComment);
    core.setFailed(msg);
  } catch(err) {
    const createdComment = await on_error(github, context, err);
    const msg = get_failed_msg(ERROR, createdComment);
    core.setFailed(msg);
  }
}
