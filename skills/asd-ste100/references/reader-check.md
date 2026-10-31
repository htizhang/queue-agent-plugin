# Reader check

Use this check before you deliver a substantial model description, policy
explanation, report, or handoff to readers outside the work. It tests whether
the intended reader can understand the document alone, not whether the
document is correct. A narrow edit, such as one sentence, needs only the source
comparison. Repairs keep the requested length and format, and they assume the
audience's domain knowledge.

## Brief a fresh reader

A fresh reader took no part in drafting and does not inherit the author's
conversation or research context. Give it only these inputs:

- The document as readers will receive it, including its figures and appendices
- The audience and their task, such as "a queueing researcher who will
  reimplement this policy"
- The neutral questions below, which name topics rather than expected answers

The reader reads as that audience: someone who knows the field but not this
project. Tell it to use only the supplied document, including its figures and
appendices, and not to open other files or search elsewhere. Withhold separate
code, data, development history, the conversation, and your intended answers,
even when code or data ship alongside the document. Embedded pseudocode and
examples remain part of the document being checked.

Ask for answers in the reader's own words, each citing its supporting passage:

1. The system, and the decision or modeling purpose that the document addresses
2. The main idea and the reasons that the document gives for it
3. One small state, job, or example traced step by step, when useful
4. Which statements are results or evidence, which are intuition, and what
   limits apply
5. Passages where the reader had to guess, reread, or search for a definition
   or step

For a policy report, also ask how the policy differs from the relevant baselines and
what evidence supports the difference. For a model description, ask instead
what the model includes and omits, which assumptions matter, and what
calibration and validation support the model and its parameters. When policies
will use the model, ask when decisions occur, what the policy observes, and
which actions it can take. Ask for explanations, not
ratings. A verdict such as "clear" gives you nothing to check.

## Compare and repair

Compare each answer with the sources yourself, because the reader cannot. A
wrong answer, a guess, or a named gap calls for inspection. Check whether the
misunderstanding comes from the text or from the reader before changing it.
Find the cause, such as a term used before its definition, a missing step between two
ideas, or a mechanism without an example. Repair the explanation there. After a
material fix, ask the affected questions again, preferably of a new fresh
reader.

Repair the document, not the research. The policy, model, problem definition,
experiments, results, and claim strength stay as they are. Some gaps need facts
that the sources lack or contradict, such as an unspecified rule or a missing
comparator.
Report them to the user, and mark them as unresolved where the format allows.
The user decides whether to supply the facts or extend the work.

Stop when the answers match the sources and no misunderstanding remains that
would change how a reader uses the result. Gaps reported to the user can stay
open. If an essential clarification cannot fit the requested format, state that
conflict rather than omit the clarification silently. Matters of taste need no
further round.

## Independence and limits

Prefer a subagent as the fresh reader where the host supports delegation and
the task permits a fresh context. Otherwise, do a document-only self-review. Answer the same
questions from the document, and treat any answer that needs your memory of the
work as a gap. Label it a self-review when you mention it, because you already
know the intended meaning. The lack of a reviewer alone does not block delivery.

Neither a clean linter result nor an agent review certifies that people will
understand the document. Feedback from actual readers outranks a model reader's
answers, so address it first. The check changes the deliverable only through
repairs. It requires no review report, added figure, or checklist.
