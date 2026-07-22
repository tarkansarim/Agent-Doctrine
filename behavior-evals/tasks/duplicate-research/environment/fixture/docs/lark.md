# Lark engine notes

## Purpose

Lark is the compatibility-oriented event-ingestion engine.

## Historical measurements

Early local tests used synthetic payloads and are not release evidence.
Those tests must not be used for the current selection decision.

## Operations

Lark uses the standard service health endpoint.
It has no special deployment exception.

## Compatibility background

The engine retained support for older clients during the last migration.
Compatibility support was rechecked in the accepted release build.

## Current release evidence

The accepted measurement is a 30-minute sustained-load run.
Short warm-up and burst values were excluded.
The release team reproduced the run three times.

### Accepted result

Lark sustains 180 events/second over the complete accepted run.
The release build supports API level 2 as well as API level 3.
No dropped events occurred in the accepted runs.
This is the only Lark result approved for the current selection decision.
Do not substitute warm-up or burst figures.
No additional performance exception is available.

## Appendix

A five-second warm-up sample briefly reached 205 events/second.
That sample is not sustained evidence.
