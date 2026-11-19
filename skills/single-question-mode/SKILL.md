---
name: single-question-mode
description: Walk the user through a set of open questions or decisions one at a time. Each turn shows exactly one question with just enough context to decide, a clear recommendation, the number of remaining questions and an ASCII progress bar. The next question only appears once the current one is settled. Use when the user says single-question-mode, one question at a time, eine Frage nach der anderen, go through the open questions with me, or when a document, review or thread contains several decisions the user has to make.
argument-hint: "[source: Notion page, file, PR, or a pasted list of questions]"
---

# Single question mode

The user has several decisions in front of them and wants to work through them
without being flooded. Your job is to serialize: one question per turn, settled
before the next appears. Nothing else from the queue leaks into the current turn.

## 1. Build the queue

Collect the open questions from the source the user names (Notion page and its
comments, a PR review, a file, a pasted list, or the current conversation). If no
source is named, use the open items from the conversation so far.

- Keep only questions that are actually open and that the user has to answer.
  Drop what is already decided or what someone else owns, but mention the count
  of dropped items once in the opening line.
- Order the queue: blocking items first, then by dependency (a question whose
  answer changes another one comes before it), then by the source's own order.
- Give each question a stable ID. Reuse the source's IDs when it has them
  (Q-03, F-01, ticket keys). Otherwise number them.
- Say in one line how many questions are in the queue, then go straight to the
  first one. Do not print the full list unless the user asks for it.

## 2. Present one question

Each turn has exactly this shape, in this order:

```
[##########··········] 2/10 settled · 8 remaining

Q-06 · Change lock for published coupons

Context: 2-5 short sentences. What the question is, why it is open, who
raised it, what the realistic options are. Only what is needed to decide.

Options:
  A) ... (one line)
  B) ... (one line)

Recommendation: A, because <one or two sentences>.
```

Rules for the content:

- **Context is for deciding, not for completeness.** Leave out history, source
  citations and anything the user can look up afterwards. If a detail would not
  change the answer, it does not belong here. Hard cap: about 120 words before
  the options.
- **Options are concrete.** Two to four, each one line, mutually exclusive. If
  someone in the source already proposed an option, attribute it in three words
  ("Jan's proposal").
- **Always recommend.** One option, named, with the reason in at most two
  sentences. Never "it depends" without saying what it depends on and what you
  would pick given what you know.
- **Progress bar first.** 20 characters wide, `#` for settled, `·` for open,
  then `settled/total settled · N remaining`. The current question counts as
  open until it is settled.
- Nothing after the recommendation. No preview of the next question, no "other
  open items", no closing offer.

## 3. Settle the question

The user answers in free text. Treat these as settled:

- picks an option, agrees with the recommendation, or gives their own answer
- says "skip", "later" or "not mine": mark it deferred and move on; deferred
  items are listed once at the end, not re-asked
- asks a clarifying question: answer it briefly in the same format (context,
  no new question), then re-show the same question with the same progress bar

Once settled, reply with one line that records the decision in the user's words
("Q-06 settled: lock from publication."), then immediately show the next
question in the format above. Both go in the same message.

If the user's answer also answers a later question in the queue, settle that one
too, say so in one line, and skip it.

## 4. Finish

When the queue is empty, print a compact table of every question with its ID,
the decision, and `deferred` where applicable, plus the full progress bar. Then
ask once whether the decisions should be written back to the source (comment,
page update, ticket). Do not write anything back without that confirmation.

## What this skill never does

- Shows two open questions in one message.
- Pads context with background the user already knows from the source.
- Reorders or re-asks a settled or deferred question.
- Decides for the user: the recommendation is a recommendation.
