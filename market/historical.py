from __future__ import annotations

import os
import time
import pickle
from decimal import Decimal
from typing import Any
import requests

from app.logger import logger
from models.market import Candle


BINANCE_REST_URL = "https://fapi.binance.com/fapi/v1/klines"
CACHE_DIR = "dataset/cache"


class BinanceHistoricalData:

    BASE_URL = BINANCE_REST_URL
    MAX_LIMIT = 1000

    INTERVAL_MS = {
        "1m": 60_000,
        "3m": 180_000,
        "5m": 300_000,
        "15m": 900_000,
        "30m": 1_800_000,
        "1h": 3_600_000,
        "2h": 7_200_000,
        "4h": 14_400_000,
        "6h": 21_600_000,
        "8h": 28_800_000,
        "12h": 43_200_000,
        "1d": 86_400_000,
    }

    def __init__(
        self,
        timeout: int = 30,
        cache_dir: str = CACHE_DIR,
        cache_ttl_seconds: int = 300,
    ):
        self.url = self.BASE_URL
        self.timeout = timeout
        self.cache_dir = cache_dir
        self.cache_ttl_seconds = int(cache_ttl_seconds)
        os.makedirs(self.cache_dir, exist_ok=True)

    def _cache_path(
        self,
        symbol: str,
        interval: str,
        limit: int,
    ) -> str:
        return os.path.join(
            self.cache_dir,
            f"{symbol.upper()}_{interval}_{limit}.pkl",
        )

    def _cache_valid(
        self,
        rows: list,
        symbol: str,
        interval: str,
        limit: int,
    ) -> bool:
        if len(rows) < limit:
            return False

        if not rows:
            return False

        now_ms = int(time.time() * 1000)
        interval_ms = self.INTERVAL_MS.get(interval)

        if interval_ms is None:
            return False

        latest_open = int(rows[-1][0])

        # Historical cache must contain a recent enough candle.
        # Allow one interval of lag.
        if now_ms - latest_open > interval_ms * 2:
            return False

        # Validate chronological ordering.
        previous = -1

        for row in rows:
            if not row:
                return False

            current = int(row[0])

            if current <= previous:
                return False

            previous = current

        return True

    def _load_cache(
        self,
        cache_file: str,
        symbol: str,
        interval: str,
        limit: int,
    ) -> list[Candle] | None:
        try:
            with open(cache_file, "rb") as f:
                payload = pickle.load(f)

            # New cache format.
            if isinstance(payload, dict):
                rows = payload.get("rows", [])
            else:
                # Backward compatibility.
                rows = payload

            if not isinstance(rows, list):
                return None

            if not self._cache_valid(
                rows,
                symbol,
                interval,
                limit,
            ):
                return None

            rows = rows[-limit:]

            candles = [
                self._convert(
                    symbol,
                    interval,
                    row,
                )
                for row in rows
            ]

            logger.success(
                f"[CACHE HIT] {symbol} {interval} "
                f"{len(candles):,} candles restored."
            )

            return candles

        except Exception as exc:
            print(
                f"[CACHE WARNING] Invalid cache "
                f"{cache_file}: {exc}"
            )
            return None

    def fetch_klines(
        self,
        symbol: str,
        interval: str = "5m",
        limit: int = 150,
        use_cache: bool = True,
    ) -> list[Candle]:

        if limit <= 0:
            return []

        symbol = symbol.upper()

        if interval not in self.INTERVAL_MS:
            raise ValueError(
                f"Unsupported Binance interval: {interval}"
            )

        cache_file = self._cache_path(
            symbol,
            interval,
            limit,
        )

        # ====================================================
        # CACHE
        # ====================================================

        if use_cache and os.path.exists(cache_file):
            print(
                f"[CACHE] Checking: {cache_file}"
            )

            cached = self._load_cache(
                cache_file,
                symbol,
                interval,
                limit,
            )

            if cached is not None:
                return cached

            print(
                "[CACHE] Cache stale/incomplete. "
                "Refreshing from Binance."
            )

        # ====================================================
        # API DOWNLOAD
        # ====================================================

        results: list[list] = []
        end_time: int | None = None
        total_batches = (
            limit + self.MAX_LIMIT - 1
        ) // self.MAX_LIMIT
        batch_num = 0
        start_time = time.perf_counter()

        print()
        print(
            f"[HISTORICAL] {symbol} {interval}"
        )
        print(
            f"[HISTORICAL] Target: "
            f"{limit:,} candles"
        )

        while len(results) < limit:
            batch_num += 1
            batch_limit = min(
                self.MAX_LIMIT,
                limit - len(results),
            )

            params: dict[str, Any] = {
                "symbol": symbol,
                "interval": interval,
                "limit": batch_limit,
            }

            if end_time is not None:
                params["endTime"] = end_time

            batch = None

            for attempt in range(1, 6):
                try:
                    response = requests.get(
                        self.url,
                        params=params,
                        timeout=self.timeout,
                    )
                    response.raise_for_status()

                    payload = response.json()

                    if not isinstance(
                        payload,
                        list,
                    ):
                        raise RuntimeError(
                            f"Unexpected Binance response: "
                            f"{payload}"
                        )

                    batch = payload
                    break

                except Exception as exc:
                    wait_sec = attempt * 2
                    print(
                        f"[HISTORICAL RETRY] "
                        f"Batch {batch_num}/{total_batches} "
                        f"attempt {attempt}/5: {exc}"
                    )
                    time.sleep(wait_sec)

            if batch is None:
                raise RuntimeError(
                    f"Failed to fetch "
                    f"{symbol} {interval} "
                    f"batch {batch_num}."
                )

            if not batch:
                break

            results.extend(batch)

            oldest_open_time = int(
                batch[0][0]
            )
            end_time = (
                oldest_open_time - 1
            )

            elapsed = (
                time.perf_counter() - start_time
            )
            rate = (
                len(results) / max(elapsed, 1e-6)
            )
            remaining = max(
                0,
                limit - len(results),
            )
            eta = (
                remaining / max(rate, 1e-6)
            )
            pct = min(
                100.0,
                len(results) / limit * 100.0,
            )

            print(
                f"  |- Batch "
                f"{batch_num:>4}/{total_batches} | "
                f"{len(results):>8,}/{limit:,} "
                f"({pct:5.1f}%) | "
                f"ETA {eta:5.1f}s"
            )

            if len(batch) < batch_limit:
                break

            time.sleep(0.05)

        # ====================================================
        # SORT + DEDUP
        # ====================================================

        results.sort(
            key=lambda row: int(row[0])
        )

        deduplicated = []
        seen: set[int] = set()

        for row in results:
            open_time = int(row[0])
            if open_time in seen:
                continue
            seen.add(open_time)
            deduplicated.append(row)

        final_rows = deduplicated[-limit:]

        if len(final_rows) < limit:
            raise RuntimeError(
                f"Historical data incomplete: "
                f"requested={limit}, "
                f"received={len(final_rows)} "
                f"for {symbol} {interval}"
            )

        # ====================================================
        # CACHE
        # ====================================================

        try:
            with open(
                cache_file,
                "wb",
            ) as f:
                pickle.dump(
                    {
                        "version": 2,
                        "symbol": symbol,
                        "interval": interval,
                        "limit": limit,
                        "fetched_at": int(
                            time.time()
                        ),
                        "rows": final_rows,
                    },
                    f,
                    protocol=pickle.HIGHEST_PROTOCOL,
                )
            print(
                f"[CACHE] Saved "
                f"{len(final_rows):,} candles"
            )
        except Exception as exc:
            print(
                f"[CACHE WARNING] "
                f"Write failed: {exc}"
            )

        # ====================================================
        # CONVERSION
        # ====================================================

        candles = [
            self._convert(
                symbol,
                interval,
                row,
            )
            for row in final_rows
        ]

        total_elapsed = time.perf_counter() - start_time
        logger.success(
            f"[HISTORICAL COMPLETE] "
            f"{symbol} {interval} "
            f"{len(candles):,} candles in {total_elapsed:.1f}s"
        )

        return candles

    @staticmethod
    def _convert(
        symbol: str,
        interval: str,
        row: list,
    ) -> Candle:

        close_time = (
            int(row[6])
            if len(row) > 6
            else int(row[0])
            + BinanceHistoricalData.INTERVAL_MS.get(
                interval,
                300_000,
            )
            - 1
        )

        candle = Candle(
            symbol=symbol.upper(),
            interval=interval,
            open_time=int(row[0]),
            close_time=close_time,
            open=Decimal(str(row[1])),
            high=Decimal(str(row[2])),
            low=Decimal(str(row[3])),
            close=Decimal(str(row[4])),
            volume=Decimal(str(row[5])),
            trades=int(row[8]) if len(row) > 8 else 0,
            closed=True,
        )

        # Binance Futures kline:
        # row[9] = taker buy base asset volume
        # row[10] = taker buy quote asset volume
        try:
            setattr(
                candle,
                "taker_buy_volume",
                Decimal(str(row[9]))
                if len(row) > 9
                else Decimal("0"),
            )
            setattr(
                candle,
                "taker_buy_quote_volume",
                Decimal(str(row[10]))
                if len(row) > 10
                else Decimal("0"),
            )
            setattr(
                candle,
                "quote_volume",
                Decimal(str(row[7]))
                if len(row) > 7
                else Decimal("0"),
            )
        except Exception:
            pass

        return candle
