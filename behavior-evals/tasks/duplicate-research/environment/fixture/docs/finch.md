# Finch engine notes

## Purpose

Finch is an event-ingestion engine used for sustained workloads.

## Development history

The prototype used API level 2, but that prototype is no longer supported.
Several experimental figures in old planning notes are not release evidence.

## Current release evidence

The following figures come from the accepted 30-minute sustained-load run.
Short burst results are intentionally excluded from the release decision.

### Accepted result

Finch sustains 240 events/second over the complete accepted run.
The release build requires API level 3 and does not support API level 2.
The result was reproduced three times without dropped events.
This is the only Finch result approved for the current selection decision.
Do not use prototype figures from earlier sections.
No additional compatibility exception is available.

## Operational notes

Finch exposes standard health and queue-depth metrics.
Deployment uses the normal service rollout path.

## Historical appendix

An early prototype reached 260 events/second for ten seconds.
That burst was never accepted as sustained evidence.
