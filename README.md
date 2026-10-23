# VyapaarSaathi: operations teammate prototype

A simulated electronics merchant case desk for the Paytm Build for India AI Hackathon, Track 3. It explores reconciliation when payment, order, stock and customer records disagree. All records, people and amounts are fictional.

## Run
Open `index.html` in a modern browser. Run `node test.cjs` to check the case decisions. There are no dependencies or credentials.

## What works
Eight hand-authored cases show deterministic decision logic and explanations. Approving a simulated duplicate refund and simulating customer credit update the view. Enquiry, quote, inventory, message and service details are linked synthetic fixtures; service booking and order confirmation are narrative outcomes, not persisted backend transactions. This is a rules-based prototype; it does not call an AI model or actual payment, messaging, order or inventory APIs. Refresh resets the demo. A timeout scenario illustrates a backend lookup in fixture data; it does not prove production idempotency or concurrent inventory locking.

## Synthetic evaluation
`node test.cjs` compares seven hand-labelled payment scenarios with a deliberately simple baseline: promise confirmation whenever any payment is captured, otherwise ask for another payment. This baseline is illustrative, not a competitor. Prototype decisions match 7/7 expected labels and baseline matches 1/7. The scenarios and decisions were designed together, so this is a regression check, not an independent accuracy estimate, production benchmark or evidence of merchant impact. No recovery or revenue is claimed.

## Production work required
Use authenticated provider APIs and verified webhooks, durable state, transactional inventory reservations, idempotency keys, action-status lookup, retry controls, audit trails, role-based approvals and customer consent. Treat provider status, bank credit and settlement as separate evidence. Add a tested AI layer for language understanding with deterministic policy enforcement, evaluation and human review. Validate API permissions and merchant workflows with Paytm and real merchants before deployment. A ticket or initiated refund is not recovered money.

## Research
See `RESEARCH.md` for sources, competing products, open questions and interview prompts. This prototype has no affiliation with Paytm.

## Model-ready sandbox
`orchestrator.py` exposes a model adapter contract receiving the customer request, case evidence and allowed actions; it expects a structured `{action, rationale}` dictionary. A local SQLite executor checks payment, stock, approval and action keys independently of the model. Run `python -m unittest -v test_orchestrator` for the mock-model and safety checks. This is a separate backend experiment, not connected to the browser demo. No model adapter, provider credential, real structured tool-calling API or authentication is included. An actual AI teammate requires a configured model, provider-specific adapter, evaluation, authenticated human approvals and integration with real systems. SQLite demo behavior does not prove distributed consistency or safe production financial operations.

`model_adapter.py` provides an optional OpenAI-compatible chat-completions adapter. Configure `MODEL_API_URL` (HTTPS endpoint), `MODEL_NAME` and `MODEL_API_KEY` as environment variables and pass `ModelAdapter()` to `orchestrate`. Only use a provider whose data handling is appropriate. No live provider call has been tested and compatibility varies. The model proposes JSON; the executor enforces its own rules. Do not expose keys or use real data in this prototype.

