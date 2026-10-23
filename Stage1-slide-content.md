# VyapaarSaathi — slide-by-slide content for the team

## 1. Title
VyapaarSaathi: a synthetic operations teammate for small electronics merchants. Paytm Build for India AI Hackathon, Track 3. Add team member names supplied by the team.

## 2. Problem
A customer says they paid, but the order is pending; the merchant must reconcile payment attempts, order status and available stock before taking action. Refund initiation does not itself prove customer credit. The frequency and time cost for the target merchant segment remain unmeasured.

## 3. Solution
A single case view with predefined synthetic scenarios and a connected walkthrough: record requirements, create and approve a quote, create an order, simulate payment and delivery, request warranty service, schedule a technician and close service. Payment cases demonstrate pending, late success, duplicate attempts, timeout, stock conflict and missing evidence. Refunds require simulated merchant approval. The public demo is scripted browser logic, not an AI model or a Paytm integration.

## 4. Tech Stack
Public demo: HTML, CSS, JavaScript, browser local storage and scripted decision rules. Local experiment: Python, SQLite and an optional OpenRouter model adapter; no key is needed for the public demo. Data, technician availability and payment events are synthetic. No real payment or messages are sent.

## 5. USP hypothesis
Explore a case view across payment, order and stock, linked to the after-sales journey for small electronics merchants. Existing tools already handle parts of this, and the proposed difference and merchant demand are not yet validated. Avoid claiming this is unique or that competitors lack safeguards.

## 6. Impact
Measured: seven of seven hand-authored decision labels matched the rules, versus one of seven for a simple illustrative baseline. These scenarios were designed with the rules and are not an independent accuracy estimate. No merchant impact or revenue recovered has been measured. Proposed pilot metrics: time to verified resolution, duplicate actions, escalation rate and confirmed outcomes.

## 7. Business Model
Hypothesis: B2B subscription per store, potentially with a platform integration fee. Pricing, willingness to pay, costs and distribution need validation. No Paytm partnership is claimed.

## Demo story
1. Open the public demo, select Late payment success and run the teammate; explain that the fetching delay and varied wording are scripted.
2. In the connected journey, record requirements, create and approve the quote, simulate payment, confirm, simulate delivery, request warranty service, select a technician and close the service. Open the timeline.
3. Show Two successful payments and simulated approval. Explain that initiated refund and confirmed customer credit are separate states.

## Sources and competitive context
- Paytm callbacks and webhooks: https://business.paytm.com/docs/callback-and-webhook/
- Cashfree reconciliation: https://www.cashfree.com/blog/ecommerce-payment-reconciliation/
- Razorpay late authorization: https://razorpay.com/docs/payments/payments/late-authorisation/
- Zoho FSM service appointments: https://www.zoho.com/fsm/service-appointments.html
- Closest identified public comparator: https://github.com/hrishabh1915/paytm-ai-customer-resolution-teammate/blob/main/docs/JUDGE_QA.md

Links: https://vyapaar-saathi-demo-1023.kapri14312025.chatgpt.site/ and https://github.com/sahilsaeidkhan/vyapaar-saathi-ai .
