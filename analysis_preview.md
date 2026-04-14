# Statistical Analysis Preview

## 1) Statistical question
Is the average daily Bitcoin return different on **Fear** days compared with **Greed** days?

## 2) Outcome variable
`btc_daily_return`

This is a continuous numeric variable, so it is suitable for a t-test.

## 3) Grouping variable
`sentiment_group`

This groups each day into:
- Fear
- Neutral
- Greed

For a simpler two-group test, I can filter to just Fear vs Greed.

## 4) Binary variable created
`positive_return`

This equals:
- `1` if daily return > 0
- `0` otherwise

I created this because it supports a **proportion z-test** later in Part 2.

## 5) Possible hypotheses

### Test idea 1 — two-sample t-test
- **Null hypothesis (H0):** Mean BTC daily return is the same on Fear days and Greed days.
- **Alternative hypothesis (H1):** Mean BTC daily return is different on Fear days and Greed days.

### Test idea 2 — one-sample t-test
- **Null hypothesis (H0):** Mean BTC daily return equals 0.
- **Alternative hypothesis (H1):** Mean BTC daily return is different from 0.

### Test idea 3 — proportion z-test
- **Null hypothesis (H0):** The proportion of positive-return days is the same on Fear days and Greed days.
- **Alternative hypothesis (H1):** The proportion of positive-return days is different on Fear days and Greed days.

## 6) Best-fit test
The best fit is probably the **two-sample t-test** because the dataset is designed to compare one continuous outcome (`btc_daily_return`) across two sentiment-based groups (`Fear` and `Greed`).

The proportion z-test is also a strong option because the Gold dataset includes the binary variable `positive_return`.
