# Assignment Analysis

## What the instructor is really asking for

This assignment is not only about calling two APIs. It is testing whether you can build a small but complete **ETL pipeline** that is ready for **statistical testing in Part 2**.

You need to show five things clearly:
1. You can ingest raw data from public APIs.
2. You can store raw data in Bronze without changing it.
3. You can clean each source separately into Silver.
4. You can join the cleaned tables into one Gold dataset.
5. You can explain how the Gold dataset supports future hypothesis testing.

## Best pack choice

The safest and easiest choice is **Pack A — Crypto & Sentiment** because:
- both APIs are easy to call,
- both have a clean daily date join key,
- there is no need for API keys,
- the Gold dataset can support multiple test types.

## What to say if the professor asks why your design is good

You can say:
- I chose Pack A because both APIs produce daily observations that can be joined directly on date.
- I kept Bronze raw and untouched.
- I cleaned each source separately in Silver to make debugging easier.
- I created derived variables like `btc_daily_return` and `positive_return` so that Part 2 can support both t-tests and z-tests.
- I used an inner join because Part 2 needs complete rows with both market data and sentiment data.

## What can earn marks

### Strong points
- clear folder structure,
- multiple Bronze snapshots,
- readable Python code,
- meaningful column names,
- correct data types,
- thoughtful Gold features,
- a good README and analysis preview.

### Common mistakes to avoid
- editing Bronze files manually,
- dumping too many useless raw columns into Gold,
- forgetting to convert timestamps,
- not explaining your join strategy,
- creating a Gold dataset that does not support a real statistical test.

## Suggested story for your submission

**Business-style question:**
> Does Bitcoin perform differently when market sentiment is fearful versus greedy?

This sounds simple, but it gives you:
- a continuous outcome: `btc_daily_return`
- a grouping variable: `sentiment_group`
- a binary outcome: `positive_return`

That is exactly what Part 2 needs.
