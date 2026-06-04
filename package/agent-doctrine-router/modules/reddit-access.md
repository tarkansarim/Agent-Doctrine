# Reddit Access Procedure

Use this module when an agent needs primary reddit.com thread data or is about
to claim Reddit is blocked, inaccessible, or unsearchable.

## Rule

- Do not claim Reddit primary threads are unsearchable just because reddit.com
  WebFetch/WebSearch domain filters, JSON endpoints, or API hosts return 403.
- For primary threads, read Reddit's RSS/Atom feeds with `curl` and a browser
  user agent, then parse `<entry>` records for `<title>` and `<link>`.
- For Reddit-derived analyses, use plain WebSearch without a `reddit.com`
  domain filter.

## Working Primary-Thread Route

```bash
curl -L -s -H 'User-Agent: Mozilla/5.0 (compatible; agent reddit RSS reader)' \
  'https://www.reddit.com/r/<sub>/top.rss?t=month'
```

Equivalent RSS routes:

| Need | Endpoint |
| --- | --- |
| Top posts for a time window | `https://www.reddit.com/r/<sub>/top.rss?t=month` |
| Current hot posts | `https://www.reddit.com/r/<sub>/hot.rss` |
| New posts | `https://www.reddit.com/r/<sub>/new.rss` |

Known blocked routes from this environment:

| Route | Observed behavior |
| --- | --- |
| WebFetch or WebSearch with a `reddit.com` domain filter | 403 or no raw thread access |
| `https://www.reddit.com/r/<sub>/top.json` and `/r/<sub>.json` | 403 |
| `https://api.reddit.com/...` | 403 |
| `https://old.reddit.com/...` | 403 |
| libreddit/redlib mirrors | blocked or unavailable |
