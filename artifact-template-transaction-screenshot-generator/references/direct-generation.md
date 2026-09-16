# Direct-generation brief

Prepare this brief internally, then generate the image directly without requesting copy approval.

## Content fields

- Concise English service name and full title: `iLands Agent Commission - {Service Name}`. The same service name should appear in the primary item row.
- Gross payment amount, currency, payment status, and customer display name.
- Transaction ID: preserve a supplied identifier only when relevant; otherwise use an obviously synthetic value such as `ch_demo_...` rather than copying the reference ID.
- Recent activity: payment start and success timestamps and their short descriptions. Success must occur at or after start. Match the source state if it is not succeeded.
- Customer name, email, and location. Preserve supplied facts. For fictional scenarios, infer a coherent fictional customer and use an `example.com` email. For factual sources with missing details, use `Not provided` rather than inventing personal information.
- Item name, one or two short description lines, quantity, unit price, line amount, and total. Default to one commissioned deliverable when the source supports no additional items.
- Requirements: two to four concise English sentences describing the customer's actual request; no unrelated song-production language.
- Delivery: estimated date and current delivery state, or completed-delivery wording when supported. Do not copy the reference's dates. If no factual deadline exists, use `To be confirmed`; a clearly fictional scenario may use a plausible date after payment.
- Payment breakdown: payment amount, processing fee, and net amount. Keep short explanatory copy consistent with the actual currency and scenario. Do not assert Adaptive Pricing or a particular processor was used unless supplied or clearly part of a fictional mockup.

## Financial consistency

Calculate values before image generation using decimal arithmetic or integer minor units. For ordinary two-decimal currencies:

- Each line amount = quantity × unit price.
- Total = sum of line amounts, adjusted only by explicitly supplied tax or discount rows.
- The top amount, item total, and payment amount agree.
- Net amount = payment amount − processing fees.
- Keep currency and decimal formatting consistent across every occurrence.

Use supplied prices and fees exactly. If the request is explicitly fictional and omits price, choose a plausible illustrative price for the service. Missing fictional fees may be set to `0.00` with a generic `Processing fees` label; do not imply an invented rate is a real Stripe fee schedule. In factual scenarios, show `Not provided` for unavailable financial values and do not fabricate calculated net proceeds. Resolve conflicting source amounts by asking one concise clarification only when no authoritative value can be determined.

Use the template solely for layout. A new event must independently determine its customer, service, requirements, money, dates, and delivery language. All visible text is English. The generated screenshot is a visual artifact, not an action that charges anyone or verifies a transaction.
