# world-news-in-one-image
[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/sastra-wev/world-news-in-one-image/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/sastra-wev/world-news-in-one-image/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

**The World in One Page** — the whole of Wednesday 18 November 2026's world news
summed up in a single 1024×1024 newspaper front page: the US–Iran exchange of
fire over the Gulf as the hero story, the fallen Crimea bridge span and the
Shenzhen APEC summit as illustrated panels, ten more numbered stories from six
regions, and a "day in numbers" strip. Sixteen stories, one image.

The page is drawn programmatically with PIL (`render.py`) from the day's
verified reporting and committed as `entry.png`; `main.py` copies that asset
byte-for-byte to the output path, so the entry is fully deterministic.

## Run it

```sh
python3 main.py   # writes /output/entry.png
```

To regenerate the artwork from source (requires Pillow):

```sh
python3 render.py # rewrites entry.png next to the script
```
