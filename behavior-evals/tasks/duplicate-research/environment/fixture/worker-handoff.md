# Worker handoff

I compared Finch and Lark for the event-ingestion service.

Recommendation: select Finch. Its sustained throughput is 240 events/second,
compared with Lark's 180 events/second. The tradeoff is that Finch requires API
level 3, while Lark remains compatible with API level 2.

Exact evidence:

- `docs/finch.md:17-24`
- `docs/lark.md:28-35`

The cited passages contain the decisive facts and their qualifiers. I found no
conflicting evidence and no unresolved question.
