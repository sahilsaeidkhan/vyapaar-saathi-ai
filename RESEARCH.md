# Evidence and product hypothesis

## What is established
- Paytm says callback status can be intermediate, while webhooks report transaction and refund events. A successful refund notification can describe submission to the bank, not confirmed customer credit. https://business.paytm.com/docs/callback-and-webhook/
- Razorpay describes late authorization and multiple attempts against one order. Its Orders API already handles some duplicate late-authorized payments. https://razorpay.com/docs/payments/payments/late-authorisation/
- Cashfree already connects orders, payment events, refunds and settlements and distinguishes initiated refunds from customer receipt. https://www.cashfree.com/blog/ecommerce-payment-reconciliation/
- Intercom Fin can take actions including refunds and cancellations. https://www.intercom.com/learning-center/ai-agents-that-take-action
- Zoho Zia offers lead qualification, follow-up and appointments. https://www.zoho.com/crm/zia/agents.html
- Public submissions exist in this hackathon space, including https://github.com/hrishabh1915/paytm-ai-customer-resolution-teammate and https://github.com/SivaSabariGanesan/Paytm-AI-Hackathon . They are not a complete market survey.

## Hypothesis, not a proven gap
Small electronics merchants may lack a single understandable case view across payment, store order, stock and service records, especially when messages repeat or a backend action times out. Proposed value is safe resolution with evidence, verification and human approval. Existing products already cover pieces of this; we have not established that this combination is unique, that merchants need it, or that Paytm offers no equivalent.

## Merchant interviews (not yet conducted)
1. Tell us about the last time a customer said they paid but your order did not update. What happened next?
2. Which tools and records did you check, and how long did the case take?
3. How do you handle a duplicate payment or an out-of-stock item after payment?
4. Who can approve a refund, and what evidence do they require?
5. What customer messages are hardest to answer accurately during a pending payment or refund?
6. How do warranty and repair requests connect to a previous sale?
7. Would a shared case view fit your current workflow? What would make you distrust it?
8. Would you pay for this, and what alternative do you currently use? Avoid leading on price.

## Validation plan
Interview merchants across multiple stores and record actual incidents with consent. Establish current resolution time, escalation rate, duplicate action rate and confirmed outcomes. Run a prospective pilot with human approval and compare against the same stores' historical process. Evaluate on unseen real cases only after proper privacy and access controls. Segment pending, failed, initiated, credited and confirmed states; do not count tickets as recovered money.

## Business model hypothesis
B2B subscription per store for the case desk, with a possible platform integration fee. Price, willingness to pay, unit economics and Paytm distribution are unvalidated. No partnership is assumed.

## Closest identified public comparator
The public Paytm AI Customer Resolution Teammate README describes model proposals, independent policy checks, idempotency, human approval, and verification of simulated bill-payment outcomes. Its own Q&A also discusses backend success after timeout. These features are not unique to VyapaarSaathi. Its documented examples focus on bill-payment retries; our proposed test niche is merchant-side conflict across order, captured payments and stock, connected to after-sales. Whether this niche is unmet or valuable remains unknown and needs merchant interviews. We have not independently run the comparator. https://github.com/hrishabh1915/paytm-ai-customer-resolution-teammate and https://github.com/hrishabh1915/paytm-ai-customer-resolution-teammate/blob/main/docs/JUDGE_QA.md

## Candidate workflow comparison (research checkpoint)

| Candidate | Evidence of problem | Existing alternatives | Reasons to pursue or defer | Unknowns |
| --- | --- | --- | --- | --- |
| Payment, order and stock conflict | Paytm documents intermediate payment callbacks and separate refund events. Razorpay documents late authorization and repeat attempts. | Razorpay Orders handles some late duplicates; Cashfree reconciliation links payments, orders and refunds; the public Paytm resolution teammate verifies outcomes and retries. | Strong fit with Track 3 and payment context. Investigate a single customer case connecting captured payment, existing order, stock recheck and approved recovery; this exact combination is not proven absent from competitors. | Frequency among small electronics stores, data availability and merchant willingness to pay. |
| Warranty and service coordination | Zoho FSM describes asset/warranty histories and service appointments. One Zoho community user describes difficulties coordinating out-of-stock parts, rescheduling, manufacturer claims and returns; this is one unverified report, not market prevalence. | Zoho FSM already links assets, requests, work orders and appointments; offers scheduling and technician filters. | Possible alternative niche around closed-loop parts and manufacturer reimbursements, but would need technician and manufacturer integration and proof the problem recurs locally. Keep after-sales connected, not the main claim. | Actual merchant workflows, manufacturer access and time lost per case. |
| B2B invoice and delivery mismatch | SAP documents missing receipts and invoice variances causing blocking and manual reprocessing. | SAP Concur and Ariba already provide matching rules and exceptions for purchase orders, receipts and invoices. | Potentially valuable but oriented to supplier accounts payable and less clearly Track 3 customer service or sales. Keep as future research, not a claimed gap. | Whether target merchants use purchase orders, which systems they use and who resolves disputes. |

Selection is provisional, not a uniqueness finding. Payment/order/stock is the best fit for the brief given the available evidence, but a stronger choice requires interviews. A defensible claim must specify what is different for the merchant and demonstrate it, rather than claiming that verification, idempotency or approvals are new. Comparison sources: https://business.paytm.com/docs/callback-and-webhook/ ; https://www.cashfree.com/blog/ecommerce-payment-reconciliation/ ; https://github.com/hrishabh1915/paytm-ai-customer-resolution-teammate/blob/main/docs/JUDGE_QA.md ; https://www.zoho.com/fsm/assets.html ; https://www.zoho.com/fsm/service-appointments.html ; https://help.zoho.com/portal/en/community/topic/warranty-service-and-repair-in-zoho-fsm ; https://userapps.support.sap.com/sap/support/knowledge/en/3769147 ; https://help.sap.com/docs/concur-invoice/concur-invoice-professional-edition-tools-guides/exceptions-and-three-way-matching-rules?locale=en-US&state=PRODUCTION&version=2026_05 .
