# VyapaarSaathi: operations teammate prototype

A simulated electronics merchant case desk, built for the Paytm Build for India AI Hackathon, Track 3. It explores reconciliation: what should happen when payment, order, stock and customer records disagree. All records, people and amounts are fictional, and the project has no affiliation with Paytm.

## Run it

Open `index.html` in a modern browser. There are no dependencies and no credentials.

Run `node test.cjs` to check the case decisions.

## What works

Eight hand-authored cases show deterministic decision logic with explanations. Approving a simulated duplicate refund, or simulating a customer credit, updates the view. The connected walkthrough performs scripted quote, payment, order and service actions using synthetic records kept in browser storage, and its timeline persists in the same browser until Reset demo.

Be clear about what this is: a rules-based prototype. It does not call an AI model, and it does not touch any real payment, messaging, order or inventory API. A timeout scenario illustrates a backend lookup in fixture data; it does not prove production idempotency or concurrent inventory locking.

## Evaluation

`node test.cjs` compares seven hand-labelled payment scenarios against a deliberately simple baseline (promise confirmation whenever any payment is captured, otherwise ask for another payment). Prototype decisions match 7/7 expected labels; the baseline matches 1/7.

The scenarios and the decisions were designed together, so read this as a regression check, not an independent accuracy estimate, a production benchmark, or evidence of merchant impact. No recovery or revenue is claimed.

## Local agent experiment

Two optional local pieces explore what a model-driven version could look like. Neither is connected to the public static demo.

**Model-ready sandbox.** `orchestrator.py` exposes a model adapter contract: it receives the customer request, case evidence and allowed actions, and expects a structured `{action, rationale}` dictionary back. A local SQLite executor then checks payment, stock, approval and action keys independently of the model, so the model proposes and the executor enforces. Run `python -m unittest -v test_orchestrator` for the mock-model and safety checks.

`model_adapter.py` is a tool-calling adapter restricted to the free OpenRouter route. Set `MODEL_API_URL` (https://openrouter.ai/api/v1/chat/completions), `MODEL_NAME` (openrouter/free) and `MODEL_API_KEY` as environment variables, and pass `ModelAdapter()` to `orchestrate`. A live OpenRouter tool-call was verified locally on synthetic cases; availability and model responses vary. Only use a provider whose data handling is appropriate, and never put real data or exposed keys into this prototype.

**Stateful local server.** Start `python server.py` and open http://127.0.0.1:8766. The server binds only to localhost and runs against local SQLite synthetic records, with an optional configured model and an offline deterministic fallback. The browser shows a local agent panel when served by this backend. The local journey creates an enquiry and draft quote, approves it into a linked payment order, simulates payment capture, confirms the order, marks delivery, checks a synthetic warranty and schedules a technician. Replayed confirmation does not consume extra inventory, and a technician-slot uniqueness constraint blocks double booking.

Never put this server on the public internet, never feed it real records, and never treat its approval flag as authenticated approval. SQLite demo behaviour does not prove distributed consistency or safe production financial operations.

## What production would need

Authenticated provider APIs and verified webhooks, durable state, transactional inventory reservations, idempotency keys, action-status lookup, retry controls, audit trails, role-based approvals and customer consent. Provider status, bank credit and settlement must be treated as separate evidence. The experimental AI layer would need deterministic policy enforcement, human review and proper evaluation, and API permissions and merchant workflows would need validation with Paytm and real merchants before deployment. A ticket or an initiated refund is not recovered money.

## Research

See `RESEARCH.md` for sources, competing products, open questions and interview prompts.

## Submission materials

See `Stage1-slide-content.md` and `VyapaarSaathi-Stage1-Submission.pptx` for the hackathon presentation.
