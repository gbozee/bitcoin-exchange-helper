import asyncio
from binance.client import Client
try:
    from greenletio import async_
except Exception as e:
    pass

def sync_call(future):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(future)

async def loop_helper(callback):
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, callback)
    return await future


class AsyncClient:
    def __init__(self, api_key=None, api_secret=None):
        self.api_key = api_key
        self.api_secret = api_secret

    @property
    def client(self):
        return Client(api_key=self.api_key, api_secret=self.api_secret)

    def sync_client(self):
        return self.client

    async def get_client(self) -> Client:
        return await loop_helper(lambda: self.client)

    async def client_helper(self, function_name, *args, **kwargs):
        client = await self.get_client()
        return await loop_helper(
            lambda: getattr(client, function_name)(*args, **kwargs)
        )

    async def client_helper2(self, function_name, *args, **kwargs):
        func = getattr(self.client, function_name)
        return await async_(func)(*args, **kwargs)

    # Exchange Endpoints
    async def get_products(self):
        """Return list of products currently listed on Binance

        Use get_exchange_info() call instead

        :returns: list - List of product dictionaries

        :raises: BinanceRequestException, BinanceAPIException

        """

        return await self.client_helper("get_products")

    async def get_exchange_info(self):
        """Return rate limits and list of symbols

        :returns: list - List of product dictionaries

        .. code-block:: python

            {
                "timezone": "UTC",
                "serverTime": 1508631584636,
                "rateLimits": [
                    {
                        "rateLimitType": "REQUESTS",
                        "interval": "MINUTE",
                        "limit": 1200
                    },
                    {
                        "rateLimitType": "ORDERS",
                        "interval": "SECOND",
                        "limit": 10
                    },
                    {
                        "rateLimitType": "ORDERS",
                        "interval": "DAY",
                        "limit": 100000
                    }
                ],
                "exchangeFilters": [],
                "symbols": [
                    {
                        "symbol": "ETHBTC",
                        "status": "TRADING",
                        "baseAsset": "ETH",
                        "baseAssetPrecision": 8,
                        "quoteAsset": "BTC",
                        "quotePrecision": 8,
                        "orderTypes": ["LIMIT", "MARKET"],
                        "icebergAllowed": false,
                        "filters": [
                            {
                                "filterType": "PRICE_FILTER",
                                "minPrice": "0.00000100",
                                "maxPrice": "100000.00000000",
                                "tickSize": "0.00000100"
                            }, {
                                "filterType": "LOT_SIZE",
                                "minQty": "0.00100000",
                                "maxQty": "100000.00000000",
                                "stepSize": "0.00100000"
                            }, {
                                "filterType": "MIN_NOTIONAL",
                                "minNotional": "0.00100000"
                            }
                        ]
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """

        return await self.client_helper("get_exchange_info")

    async def get_symbol_info(self, symbol):
        """Return information about a symbol

        :param symbol: required e.g BNBBTC
        :type symbol: str

        :returns: Dict if found, None if not

        .. code-block:: python

            {
                "symbol": "ETHBTC",
                "status": "TRADING",
                "baseAsset": "ETH",
                "baseAssetPrecision": 8,
                "quoteAsset": "BTC",
                "quotePrecision": 8,
                "orderTypes": ["LIMIT", "MARKET"],
                "icebergAllowed": false,
                "filters": [
                    {
                        "filterType": "PRICE_FILTER",
                        "minPrice": "0.00000100",
                        "maxPrice": "100000.00000000",
                        "tickSize": "0.00000100"
                    }, {
                        "filterType": "LOT_SIZE",
                        "minQty": "0.00100000",
                        "maxQty": "100000.00000000",
                        "stepSize": "0.00100000"
                    }, {
                        "filterType": "MIN_NOTIONAL",
                        "minNotional": "0.00100000"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """

        return await self.client_helper("get_symbol_info", symbol)

    async def get_server_time(self):
        """Test connectivity to the Rest API and get the current server time.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#check-server-time

        :returns: Current server time

        .. code-block:: python

            {
                "serverTime": 1499827319559
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_server_time")

    # Market Data Endpoints

    async def get_all_tickers(self):
        """Latest price for all symbols.

        https://www.binance.com/restapipub.html#symbols-price-ticker

        :returns: List of market tickers

        .. code-block:: python

            [
                {
                    "symbol": "LTCBTC",
                    "price": "4.00000200"
                },
                {
                    "symbol": "ETHBTC",
                    "price": "0.07946600"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_all_tickers")

    async def get_orderbook_tickers(self):
        """Best price/qty on the order book for all symbols.

        https://www.binance.com/restapipub.html#symbols-order-book-ticker

        :returns: List of order book market entries

        .. code-block:: python

            [
                {
                    "symbol": "LTCBTC",
                    "bidPrice": "4.00000000",
                    "bidQty": "431.00000000",
                    "askPrice": "4.00000200",
                    "askQty": "9.00000000"
                },
                {
                    "symbol": "ETHBTC",
                    "bidPrice": "0.07946700",
                    "bidQty": "9.00000000",
                    "askPrice": "100000.00000000",
                    "askQty": "1000.00000000"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_orderbook_tickers")

    async def get_order_book(self, **params):
        """Get the Order Book for the market

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#order-book

        :param symbol: required
        :type symbol: str
        :param limit:  Default 100; max 1000
        :type limit: int

        :returns: API response

        .. code-block:: python

            {
                "lastUpdateId": 1027024,
                "bids": [
                    [
                        "4.00000000",     # PRICE
                        "431.00000000",   # QTY
                        []                # Can be ignored
                    ]
                ],
                "asks": [
                    [
                        "4.00000200",
                        "12.00000000",
                        []
                    ]
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_order_book", **params)

    async def get_recent_trades(self, **params):
        """Get recent trades (up to last 500).

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#recent-trades-list

        :param symbol: required
        :type symbol: str
        :param limit:  Default 500; max 500.
        :type limit: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "id": 28457,
                    "price": "4.00000100",
                    "qty": "12.00000000",
                    "time": 1499865549590,
                    "isBuyerMaker": true,
                    "isBestMatch": true
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_recent_trades", **params)

    async def get_historical_trades(self, **params):
        """Get older trades.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#recent-trades-list

        :param symbol: required
        :type symbol: str
        :param limit:  Default 500; max 500.
        :type limit: int
        :param fromId:  TradeId to fetch from. Default gets most recent trades.
        :type fromId: str

        :returns: API response

        .. code-block:: python

            [
                {
                    "id": 28457,
                    "price": "4.00000100",
                    "qty": "12.00000000",
                    "time": 1499865549590,
                    "isBuyerMaker": true,
                    "isBestMatch": true
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_historical_trades", **params)

    async def get_aggregate_trades(self, **params):
        """Get compressed, aggregate trades. Trades that fill at the time,
        from the same order, with the same price will have the quantity aggregated.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#compressedaggregate-trades-list

        :param symbol: required
        :type symbol: str
        :param fromId:  ID to get aggregate trades from INCLUSIVE.
        :type fromId: str
        :param startTime: Timestamp in ms to get aggregate trades from INCLUSIVE.
        :type startTime: int
        :param endTime: Timestamp in ms to get aggregate trades until INCLUSIVE.
        :type endTime: int
        :param limit:  Default 500; max 500.
        :type limit: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "a": 26129,         # Aggregate tradeId
                    "p": "0.01633102",  # Price
                    "q": "4.70443515",  # Quantity
                    "f": 27781,         # First tradeId
                    "l": 27781,         # Last tradeId
                    "T": 1498793709153, # Timestamp
                    "m": true,          # Was the buyer the maker?
                    "M": true           # Was the trade the best price match?
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_aggregate_trades", **params)

    async def get_historical_klines(self, *args, **kwargs):
        """Get Historical Klines from Binance

        See dateparser docs for valid start and end string formats http://dateparser.readthedocs.io/en/latest/

        If using offset strings for dates add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

        :param symbol: Name of symbol pair e.g BNBBTC
        :type symbol: str
        :param interval: Binance Kline interval
        :type interval: str
        :param start_str: Start date string in UTC format or timestamp in milliseconds
        :type start_str: str|int
        :param end_str: optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
        :type end_str: str|int
        :param limit: Default 500; max 1000.
        :type limit: int

        :return: list of OHLCV values

        """
        return await self.client_helper("get_historical_klines", *args, **kwargs)

    async def get_avg_price(self, **params):
        """Current average price for a symbol.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#current-average-price

        :param symbol:
        :type symbol: str

        :returns: API response

        .. code-block:: python

            {
                "mins": 5,
                "price": "9.35751834"
            }
"""
        return await self.client_helper("get_avg_price", **params)

    async def get_ticker(self, **params):
        """24 hour price change statistics.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#24hr-ticker-price-change-statistics

        :param symbol:
        :type symbol: str

        :returns: API response

        .. code-block:: python

            {
                "priceChange": "-94.99999800",
                "priceChangePercent": "-95.960",
                "weightedAvgPrice": "0.29628482",
                "prevClosePrice": "0.10002000",
                "lastPrice": "4.00000200",
                "bidPrice": "4.00000000",
                "askPrice": "4.00000200",
                "openPrice": "99.00000000",
                "highPrice": "100.00000000",
                "lowPrice": "0.10000000",
                "volume": "8913.30000000",
                "openTime": 1499783499040,
                "closeTime": 1499869899040,
                "fristId": 28385,   # First tradeId
                "lastId": 28460,    # Last tradeId
                "count": 76         # Trade count
            }

        OR

        .. code-block:: python

            [
                {
                    "priceChange": "-94.99999800",
                    "priceChangePercent": "-95.960",
                    "weightedAvgPrice": "0.29628482",
                    "prevClosePrice": "0.10002000",
                    "lastPrice": "4.00000200",
                    "bidPrice": "4.00000000",
                    "askPrice": "4.00000200",
                    "openPrice": "99.00000000",
                    "highPrice": "100.00000000",
                    "lowPrice": "0.10000000",
                    "volume": "8913.30000000",
                    "openTime": 1499783499040,
                    "closeTime": 1499869899040,
                    "fristId": 28385,   # First tradeId
                    "lastId": 28460,    # Last tradeId
                    "count": 76         # Trade count
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_ticker", **params)

    async def get_symbol_ticker(self, **params):
        """Latest price for a symbol or symbols.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#24hr-ticker-price-change-statistics

        :param symbol:
        :type symbol: str

        :returns: API response

        .. code-block:: python

            {
                "symbol": "LTCBTC",
                "price": "4.00000200"
            }

        OR

        .. code-block:: python

            [
                {
                    "symbol": "LTCBTC",
                    "price": "4.00000200"
                },
                {
                    "symbol": "ETHBTC",
                    "price": "0.07946600"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_symbol_ticker", **params)

    async def get_orderbook_ticker(self, **params):
        """Latest price for a symbol or symbols.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#symbol-order-book-ticker

        :param symbol:
        :type symbol: str

        :returns: API response

        .. code-block:: python

            {
                "symbol": "LTCBTC",
                "bidPrice": "4.00000000",
                "bidQty": "431.00000000",
                "askPrice": "4.00000200",
                "askQty": "9.00000000"
            }

        OR

        .. code-block:: python

            [
                {
                    "symbol": "LTCBTC",
                    "bidPrice": "4.00000000",
                    "bidQty": "431.00000000",
                    "askPrice": "4.00000200",
                    "askQty": "9.00000000"
                },
                {
                    "symbol": "ETHBTC",
                    "bidPrice": "0.07946700",
                    "bidQty": "9.00000000",
                    "askPrice": "100000.00000000",
                    "askQty": "1000.00000000"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_orderbook_ticker", **params)

    # Account Endpoints

    async def create_order(self, **params):
        """Send in a new order

        Any order with an icebergQty MUST have timeInForce set to GTC.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#new-order--trade

        :param symbol: required
        :type symbol: str
        :param side: required
        :type side: str
        :param type: required
        :type type: str
        :param timeInForce: required if limit order
        :type timeInForce: str
        :param quantity: required
        :type quantity: decimal
        :param quoteOrderQty: amount the user wants to spend (when buying) or receive (when selling)
            of the quote asset, applicable to MARKET orders
        :type quoteOrderQty: decimal
        :param price: required
        :type price: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param icebergQty: Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.
        :type icebergQty: decimal
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        Response ACK:

        .. code-block:: python

            {
                "symbol":"LTCBTC",
                "orderId": 1,
                "clientOrderId": "myOrder1" # Will be newClientOrderId
                "transactTime": 1499827319559
            }

        Response RESULT:

        .. code-block:: python

            {
                "symbol": "BTCUSDT",
                "orderId": 28,
                "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
                "transactTime": 1507725176595,
                "price": "0.00000000",
                "origQty": "10.00000000",
                "executedQty": "10.00000000",
                "status": "FILLED",
                "timeInForce": "GTC",
                "type": "MARKET",
                "side": "SELL"
            }

        Response FULL:

        .. code-block:: python

            {
                "symbol": "BTCUSDT",
                "orderId": 28,
                "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
                "transactTime": 1507725176595,
                "price": "0.00000000",
                "origQty": "10.00000000",
                "executedQty": "10.00000000",
                "status": "FILLED",
                "timeInForce": "GTC",
                "type": "MARKET",
                "side": "SELL",
                "fills": [
                    {
                        "price": "4000.00000000",
                        "qty": "1.00000000",
                        "commission": "4.00000000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3999.00000000",
                        "qty": "5.00000000",
                        "commission": "19.99500000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3998.00000000",
                        "qty": "2.00000000",
                        "commission": "7.99600000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3997.00000000",
                        "qty": "1.00000000",
                        "commission": "3.99700000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3995.00000000",
                        "qty": "1.00000000",
                        "commission": "3.99500000",
                        "commissionAsset": "USDT"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        return await self.client_helper("create_order", **params)

    async def order_limit(self, **params):
        """Send in a new limit order

        Any order with an icebergQty MUST have timeInForce set to GTC.

        :param symbol: required
        :type symbol: str
        :param side: required
        :type side: str
        :param quantity: required
        :type quantity: decimal
        :param price: required
        :type price: str
        :param timeInForce: default Good till cancelled
        :type timeInForce: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param icebergQty: Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.
        :type icebergQty: decimal
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        See order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        return await self.client_helper("order_limit", **params)

    async def order_limit_buy(self, **params):
        """Send in a new limit buy order

        Any order with an icebergQty MUST have timeInForce set to GTC.

        :param symbol: required
        :type symbol: str
        :param quantity: required
        :type quantity: decimal
        :param price: required
        :type price: str
        :param timeInForce: default Good till cancelled
        :type timeInForce: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param stopPrice: Used with stop orders
        :type stopPrice: decimal
        :param icebergQty: Used with iceberg orders
        :type icebergQty: decimal
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        See order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        return await self.client_helper("order_limit_buy", **params)

    async def order_limit_sell(self, **params):
        """Send in a new limit sell order

        :param symbol: required
        :type symbol: str
        :param quantity: required
        :type quantity: decimal
        :param price: required
        :type price: str
        :param timeInForce: default Good till cancelled
        :type timeInForce: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param stopPrice: Used with stop orders
        :type stopPrice: decimal
        :param icebergQty: Used with iceberg orders
        :type icebergQty: decimal
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        See order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        return await self.client_helper("order_limit_sell", **params)

    async def order_market(self, **params):
        """Send in a new market order

        :param symbol: required
        :type symbol: str
        :param side: required
        :type side: str
        :param quantity: required
        :type quantity: decimal
        :param quoteOrderQty: amount the user wants to spend (when buying) or receive (when selling)
            of the quote asset
        :type quoteOrderQty: decimal
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        See order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        return await self.client_helper("order_market", **params)

    async def order_market_buy(self, **params):
        """Send in a new market buy order

        :param symbol: required
        :type symbol: str
        :param quantity: required
        :type quantity: decimal
        :param quoteOrderQty: the amount the user wants to spend of the quote asset
        :type quoteOrderQty: decimal
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        See order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        return await self.client_helper("order_market_buy", **params)

    async def order_market_sell(self, **params):
        """Send in a new market sell order

        :param symbol: required
        :type symbol: str
        :param quantity: required
        :type quantity: decimal
        :param quoteOrderQty: the amount the user wants to receive of the quote asset
        :type quoteOrderQty: decimal
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        See order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        return await self.client_helper("order_market_sell", **params)

    async def create_oco_order(self, **params):
        """Send in a new OCO order

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#new-oco-trade

        :param symbol: required
        :type symbol: str
        :param listClientOrderId: A unique id for the list order. Automatically generated if not sent.
        :type listClientOrderId: str
        :param side: required
        :type side: str
        :param quantity: required
        :type quantity: decimal
        :param limitClientOrderId: A unique id for the limit order. Automatically generated if not sent.
        :type limitClientOrderId: str
        :param price: required
        :type price: str
        :param limitIcebergQty: Used to make the LIMIT_MAKER leg an iceberg order.
        :type limitIcebergQty: decimal
        :param stopClientOrderId: A unique id for the stop order. Automatically generated if not sent.
        :type stopClientOrderId: str
        :param stopPrice: required
        :type stopPrice: str
        :param stopLimitPrice: If provided, stopLimitTimeInForce is required.
        :type stopLimitPrice: str
        :param stopIcebergQty: Used with STOP_LOSS_LIMIT leg to make an iceberg order.
        :type stopIcebergQty: decimal
        :param stopLimitTimeInForce: Valid values are GTC/FOK/IOC.
        :type stopLimitTimeInForce: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        Response ACK:

        .. code-block:: python

            {
            }

        Response RESULT:

        .. code-block:: python

            {
            }

        Response FULL:

        .. code-block:: python

            {
            }

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        return await self.client_helper("create_oco_order", **params)

    async def order_oco_buy(self, **params):
        """Send in a new OCO buy order

        :param symbol: required
        :type symbol: str
        :param listClientOrderId: A unique id for the list order. Automatically generated if not sent.
        :type listClientOrderId: str
        :param quantity: required
        :type quantity: decimal
        :param limitClientOrderId: A unique id for the limit order. Automatically generated if not sent.
        :type limitClientOrderId: str
        :param price: required
        :type price: str
        :param limitIcebergQty: Used to make the LIMIT_MAKER leg an iceberg order.
        :type limitIcebergQty: decimal
        :param stopClientOrderId: A unique id for the stop order. Automatically generated if not sent.
        :type stopClientOrderId: str
        :param stopPrice: required
        :type stopPrice: str
        :param stopLimitPrice: If provided, stopLimitTimeInForce is required.
        :type stopLimitPrice: str
        :param stopIcebergQty: Used with STOP_LOSS_LIMIT leg to make an iceberg order.
        :type stopIcebergQty: decimal
        :param stopLimitTimeInForce: Valid values are GTC/FOK/IOC.
        :type stopLimitTimeInForce: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        See OCO order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        return await self.client_helper("order_oco_buy", **params)

    async def order_oco_sell(self, **params):
        """Send in a new OCO sell order

        :param symbol: required
        :type symbol: str
        :param listClientOrderId: A unique id for the list order. Automatically generated if not sent.
        :type listClientOrderId: str
        :param quantity: required
        :type quantity: decimal
        :param limitClientOrderId: A unique id for the limit order. Automatically generated if not sent.
        :type limitClientOrderId: str
        :param price: required
        :type price: str
        :param limitIcebergQty: Used to make the LIMIT_MAKER leg an iceberg order.
        :type limitIcebergQty: decimal
        :param stopClientOrderId: A unique id for the stop order. Automatically generated if not sent.
        :type stopClientOrderId: str
        :param stopPrice: required
        :type stopPrice: str
        :param stopLimitPrice: If provided, stopLimitTimeInForce is required.
        :type stopLimitPrice: str
        :param stopIcebergQty: Used with STOP_LOSS_LIMIT leg to make an iceberg order.
        :type stopIcebergQty: decimal
        :param stopLimitTimeInForce: Valid values are GTC/FOK/IOC.
        :type stopLimitTimeInForce: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        See OCO order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        return await self.client_helper("order_oco_sell", **params)

    async def create_test_order(self, **params):
        """Test new order creation and signature/recvWindow long. Creates and validates a new order but does not send it into the matching engine.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#test-new-order-trade

        :param symbol: required
        :type symbol: str
        :param side: required
        :type side: str
        :param type: required
        :type type: str
        :param timeInForce: required if limit order
        :type timeInForce: str
        :param quantity: required
        :type quantity: decimal
        :param price: required
        :type price: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param icebergQty: Used with iceberg orders
        :type icebergQty: decimal
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: The number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException


        """
        return await self.client_helper("create_test_order", **params)

    async def get_order(self, **params):
        """Check an order's status. Either orderId or origClientOrderId must be sent.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#query-order-user_data

        :param symbol: required
        :type symbol: str
        :param orderId: The unique order id
        :type orderId: int
        :param origClientOrderId: optional
        :type origClientOrderId: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "symbol": "LTCBTC",
                "orderId": 1,
                "clientOrderId": "myOrder1",
                "price": "0.1",
                "origQty": "1.0",
                "executedQty": "0.0",
                "status": "NEW",
                "timeInForce": "GTC",
                "type": "LIMIT",
                "side": "BUY",
                "stopPrice": "0.0",
                "icebergQty": "0.0",
                "time": 1499827319559
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_order", **params)

    async def get_all_orders(self, **params):
        """Get all account orders; active, canceled, or filled.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#all-orders-user_data

        :param symbol: required
        :type symbol: str
        :param orderId: The unique order id
        :type orderId: int
        :param limit: Default 500; max 500.
        :type limit: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "symbol": "LTCBTC",
                    "orderId": 1,
                    "clientOrderId": "myOrder1",
                    "price": "0.1",
                    "origQty": "1.0",
                    "executedQty": "0.0",
                    "status": "NEW",
                    "timeInForce": "GTC",
                    "type": "LIMIT",
                    "side": "BUY",
                    "stopPrice": "0.0",
                    "icebergQty": "0.0",
                    "time": 1499827319559
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_all_orders", **params)

    async def cancel_order(self, **params):
        """Cancel an active order. Either orderId or origClientOrderId must be sent.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#cancel-order-trade

        :param symbol: required
        :type symbol: str
        :param orderId: The unique order id
        :type orderId: int
        :param origClientOrderId: optional
        :type origClientOrderId: str
        :param newClientOrderId: Used to uniquely identify this cancel. Automatically generated by default.
        :type newClientOrderId: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "symbol": "LTCBTC",
                "origClientOrderId": "myOrder1",
                "orderId": 1,
                "clientOrderId": "cancelMyOrder1"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("cancel_order", **params)

    async def get_open_orders(self, **params):
        """Get all open orders on a symbol.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#current-open-orders-user_data

        :param symbol: optional
        :type symbol: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "symbol": "LTCBTC",
                    "orderId": 1,
                    "clientOrderId": "myOrder1",
                    "price": "0.1",
                    "origQty": "1.0",
                    "executedQty": "0.0",
                    "status": "NEW",
                    "timeInForce": "GTC",
                    "type": "LIMIT",
                    "side": "BUY",
                    "stopPrice": "0.0",
                    "icebergQty": "0.0",
                    "time": 1499827319559
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_open_orders", **params)

    # User Stream Endpoints
    async def get_account(self, **params):
        """Get current account information.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#account-information-user_data

        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "makerCommission": 15,
                "takerCommission": 15,
                "buyerCommission": 0,
                "sellerCommission": 0,
                "canTrade": true,
                "canWithdraw": true,
                "canDeposit": true,
                "balances": [
                    {
                        "asset": "BTC",
                        "free": "4723846.89208129",
                        "locked": "0.00000000"
                    },
                    {
                        "asset": "LTC",
                        "free": "4763368.68006011",
                        "locked": "0.00000000"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_account", **params)

    async def get_asset_balance(self, asset, **params):
        """Get current asset balance.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#account-information-user_data

        :param asset: required
        :type asset: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: dictionary or None if not found

        .. code-block:: python

            {
                "asset": "BTC",
                "free": "4723846.89208129",
                "locked": "0.00000000"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_asset_balance", asset, **params)

    async def get_my_trades(self, **params):
        """Get trades for a specific symbol.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#account-trade-list-user_data

        :param symbol: required
        :type symbol: str
        :param limit: Default 500; max 500.
        :type limit: int
        :param fromId: TradeId to fetch from. Default gets most recent trades.
        :type fromId: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "id": 28457,
                    "price": "4.00000100",
                    "qty": "12.00000000",
                    "commission": "10.10000000",
                    "commissionAsset": "BNB",
                    "time": 1499865549590,
                    "isBuyer": true,
                    "isMaker": false,
                    "isBestMatch": true
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_my_trades", **params)

    async def get_system_status(self):
        """Get system status detail.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/wapi-api.md#system-status-system

        :returns: API response

        .. code-block:: python

            {
                "status": 0,        # 0: normal，1：system maintenance
                "msg": "normal"     # normal or System maintenance.
            }

        :raises: BinanceAPIException

        """
        return await self.client_helper("get_system_status")

    async def get_account_status(self, **params):
        """Get account status detail.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/wapi-api.md#account-status-user_data

        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "msg": "Order failed:Low Order fill rate! Will be reactivated after 5 minutes.",
                "success": true,
                "objs": [
                    "5"
                ]
            }

        :raises: BinanceWithdrawException

        """
        return await self.client_helper("get_account_status", **params)

    async def get_dust_log(self, **params):
        """Get log of small amounts exchanged for BNB.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/wapi-api.md#dustlog-user_data

        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "success": true,
                "results": {
                    "total": 2,   //Total counts of exchange
                    "rows": [
                        {
                            "transfered_total": "0.00132256", # Total transfered BNB amount for this exchange.
                            "service_charge_total": "0.00002699",   # Total service charge amount for this exchange.
                            "tran_id": 4359321,
                            "logs": [           # Details of  this exchange.
                                {
                                    "tranId": 4359321,
                                    "serviceChargeAmount": "0.000009",
                                    "uid": "10000015",
                                    "amount": "0.0009",
                                    "operateTime": "2018-05-03 17:07:04",
                                    "transferedAmount": "0.000441",
                                    "fromAsset": "USDT"
                                },
                                {
                                    "tranId": 4359321,
                                    "serviceChargeAmount": "0.00001799",
                                    "uid": "10000015",
                                    "amount": "0.0009",
                                    "operateTime": "2018-05-03 17:07:04",
                                    "transferedAmount": "0.00088156",
                                    "fromAsset": "ETH"
                                }
                            ],
                            "operate_time": "2018-05-03 17:07:04" //The time of this exchange.
                        },
                        {
                            "transfered_total": "0.00058795",
                            "service_charge_total": "0.000012",
                            "tran_id": 4357015,
                            "logs": [       // Details of  this exchange.
                                {
                                    "tranId": 4357015,
                                    "serviceChargeAmount": "0.00001",
                                    "uid": "10000015",
                                    "amount": "0.001",
                                    "operateTime": "2018-05-02 13:52:24",
                                    "transferedAmount": "0.00049",
                                    "fromAsset": "USDT"
                                },
                                {
                                    "tranId": 4357015,
                                    "serviceChargeAmount": "0.000002",
                                    "uid": "10000015",
                                    "amount": "0.0001",
                                    "operateTime": "2018-05-02 13:51:11",
                                    "transferedAmount": "0.00009795",
                                    "fromAsset": "ETH"
                                }
                            ],
                            "operate_time": "2018-05-02 13:51:11"
                        }
                    ]
                }
            }

        :raises: BinanceWithdrawException

        """
        return await self.client_helper("get_dust_log", **params)

    async def transfer_dust(self, **params):
        """Convert dust assets to BNB.

        https://github.com/binance-exchange/binance-official-api-docs/blob/9dbe0e961b80557bb19708a707c7fad08842b28e/wapi-api.md#dust-transfer-user_data

        :param asset: The asset being converted. e.g: 'ONE'
        :type asset: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code:: python

            result = client.transfer_dust(asset='ONE')

        :returns: API response

        .. code-block:: python

            {
                "totalServiceCharge":"0.02102542",
                "totalTransfered":"1.05127099",
                "transferResult":[
                    {
                        "amount":"0.03000000",
                        "fromAsset":"ETH",
                        "operateTime":1563368549307,
                        "serviceChargeAmount":"0.00500000",
                        "tranId":2970932918,
                        "transferedAmount":"0.25000000"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("transfer_dust", **params)

    async def get_asset_dividend_history(self, **params):
        """Query asset dividend record.

        https://github.com/binance-exchange/binance-official-api-docs/blob/9dbe0e961b80557bb19708a707c7fad08842b28e/wapi-api.md#asset-dividend-record-user_data

        :param asset: optional
        :type asset: str
        :param startTime: optional
        :type startTime: long
        :param endTime: optional
        :type endTime: long
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code:: python

            result = client.get_asset_dividend_history()

        :returns: API response

        .. code-block:: python

            {
                "rows":[
                    {
                        "amount":"10.00000000",
                        "asset":"BHFT",
                        "divTime":1563189166000,
                        "enInfo":"BHFT distribution",
                        "tranId":2968885920
                    },
                    {
                        "amount":"10.00000000",
                        "asset":"BHFT",
                        "divTime":1563189165000,
                        "enInfo":"BHFT distribution",
                        "tranId":2968885920
                    }
                ],
                "total":2
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_asset_dividend_history", **params)

    async def get_trade_fee(self, **params):
        """Get trade fee.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/wapi-api.md#trade-fee-user_data

        :param symbol: optional
        :type symbol: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "tradeFee": [
                    {
                        "symbol": "ADABNB",
                        "maker": 0.9000,
                        "taker": 1.0000
                    }, {
                        "symbol": "BNBBTC",
                        "maker": 0.3000,
                        "taker": 0.3000
                    }
                ],
                "success": true
            }

        :raises: BinanceWithdrawException

        """
        return await self.client_helper("get_trade_fee", **params)

    async def get_asset_details(self, **params):
        """Fetch details on assets.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/wapi-api.md#asset-detail-user_data

        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "success": true,
                "assetDetail": {
                    "CTR": {
                        "minWithdrawAmount": "70.00000000", //min withdraw amount
                        "depositStatus": false,//deposit status
                        "withdrawFee": 35, // withdraw fee
                        "withdrawStatus": true, //withdraw status
                        "depositTip": "Delisted, Deposit Suspended" //reason
                    },
                    "SKY": {
                        "minWithdrawAmount": "0.02000000",
                        "depositStatus": true,
                        "withdrawFee": 0.01,
                        "withdrawStatus": true
                    }
                }
            }

        :raises: BinanceWithdrawException

        """
        return await self.client_helper("get_asset_details", **params)

    # Withdraw Endpoints

    async def withdraw(self, **params):
        """Submit a withdraw request.

        https://www.binance.com/restapipub.html

        Assumptions:

        - You must have Withdraw permissions enabled on your API key
        - You must have withdrawn to the address specified through the website and approved the transaction via email

        :param asset: required
        :type asset: str
        :type address: required
        :type address: str
        :type addressTag: optional - Secondary address identifier for coins like XRP,XMR etc.
        :type address: str
        :param amount: required
        :type amount: decimal
        :param name: optional - Description of the address, default asset value passed will be used
        :type name: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "msg": "success",
                "success": true,
                "id":"7213fea8e94b4a5593d507237e5a555b"
            }

        :raises: BinanceRequestException, BinanceAPIException, BinanceWithdrawException

        """
        return await self.client_helper("withdraw", **params)

    async def get_deposit_history(self, **params):
        """Fetch deposit history.

        https://www.binance.com/restapipub.html

        :param asset: optional
        :type asset: str
        :type status: 0(0:pending,1:success) optional
        :type status: int
        :param startTime: optional
        :type startTime: long
        :param endTime: optional
        :type endTime: long
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "depositList": [
                    {
                        "insertTime": 1508198532000,
                        "amount": 0.04670582,
                        "asset": "ETH",
                        "status": 1
                    }
                ],
                "success": true
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_deposit_history", **params)

    async def get_withdraw_history(self, **params):
        """Fetch withdraw history.

        https://www.binance.com/restapipub.html

        :param asset: optional
        :type asset: str
        :type status: 0(0:Email Sent,1:Cancelled 2:Awaiting Approval 3:Rejected 4:Processing 5:Failure 6Completed) optional
        :type status: int
        :param startTime: optional
        :type startTime: long
        :param endTime: optional
        :type endTime: long
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "withdrawList": [
                    {
                        "amount": 1,
                        "address": "0x6915f16f8791d0a1cc2bf47c13a6b2a92000504b",
                        "asset": "ETH",
                        "applyTime": 1508198532000
                        "status": 4
                    },
                    {
                        "amount": 0.005,
                        "address": "0x6915f16f8791d0a1cc2bf47c13a6b2a92000504b",
                        "txId": "0x80aaabed54bdab3f6de5868f89929a2371ad21d666f20f7393d1a3389fad95a1",
                        "asset": "ETH",
                        "applyTime": 1508198532000,
                        "status": 4
                    }
                ],
                "success": true
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_withdraw_history", **params)

    async def get_deposit_address(self, **params):
        """Fetch a deposit address for a symbol

        https://www.binance.com/restapipub.html

        :param asset: required
        :type asset: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "address": "0x6915f16f8791d0a1cc2bf47c13a6b2a92000504b",
                "success": true,
                "addressTag": "1231212",
                "asset": "BNB"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_deposit_address", **params)

    # User Stream Endpoints

    async def stream_get_listen_key(self):
        """Start a new user data stream and return the listen key
        If a stream already exists it should return the same key.
        If the stream becomes invalid a new key is returned.

        Can be used to keep the user stream alive.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#start-user-data-stream-user_stream

        :returns: API response

        .. code-block:: python

            {
                "listenKey": "pqia91ma19a5s61cv6a81va65sdf19v8a65a1a5s61cv6a81va65sdf19v8a65a1"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("stream_get_listen_key")

    async def stream_keepalive(self, listenKey):
        """PING a user data stream to prevent a time out.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#keepalive-user-data-stream-user_stream

        :param listenKey: required
        :type listenKey: str

        :returns: API response

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("stream_keepalive", listenKey)

    async def stream_close(self, listenKey):
        """Close out a user data stream.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#close-user-data-stream-user_stream

        :param listenKey: required
        :type listenKey: str

        :returns: API response

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("stream_close", listenKey)

    # Margin Trading Endpoints

    async def get_margin_account(self, **params):
        """Query margin account details

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/margin-api.md#query-margin-account-details-user_data

        :returns: API response

        .. code-block:: python

            {
                "borrowEnabled": true,
                "marginLevel": "11.64405625",
                "totalAssetOfBtc": "6.82728457",
                "totalLiabilityOfBtc": "0.58633215",
                "totalNetAssetOfBtc": "6.24095242",
                "tradeEnabled": true,
                "transferEnabled": true,
                "userAssets": [
                    {
                        "asset": "BTC",
                        "borrowed": "0.00000000",
                        "free": "0.00499500",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "0.00499500"
                    },
                    {
                        "asset": "BNB",
                        "borrowed": "201.66666672",
                        "free": "2346.50000000",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "2144.83333328"
                    },
                    {
                        "asset": "ETH",
                        "borrowed": "0.00000000",
                        "free": "0.00000000",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "0.00000000"
                    },
                    {
                        "asset": "USDT",
                        "borrowed": "0.00000000",
                        "free": "0.00000000",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "0.00000000"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_margin_account", **params)

    async def get_margin_asset(self, **params):
        """Query margin asset

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/margin-api.md#query-margin-asset-market_data

        :param asset: name of the asset
        :type asset: str

        .. code:: python

            asset_details = client.get_margin_asset(asset='BNB')

        :returns: API response

        .. code-block:: python

            {
                "assetFullName": "Binance Coin",
                "assetName": "BNB",
                "isBorrowable": false,
                "isMortgageable": true,
                "userMinBorrow": "0.00000000",
                "userMinRepay": "0.00000000"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_margin_asset", **params)

    async def get_margin_symbol(self, **params):
        """Query margin symbol info

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/margin-api.md#query-margin-pair-market_data

        :param symbol: name of the symbol pair
        :type symbol: str

        .. code:: python

            pair_details = client.get_margin_symbol(symbol='BTCUSDT')

        :returns: API response

        .. code-block:: python

            {
                "id":323355778339572400,
                "symbol":"BTCUSDT",
                "base":"BTC",
                "quote":"USDT",
                "isMarginTrade":true,
                "isBuyAllowed":true,
                "isSellAllowed":true
            }


        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_margin_symbol", **params)

    async def get_margin_price_index(self, **params):
        """Query margin priceIndex

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/margin-api.md#query-margin-priceindex-market_data

        :param symbol: name of the symbol pair
        :type symbol: str

        .. code:: python

            price_index_details = client.get_margin_pair(symbol='BTCUSDT')

        :returns: API response

        .. code-block:: python

            {
                "calcTime": 1562046418000,
                "price": "0.00333930",
                "symbol": "BNBBTC"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_margin_price_index", **params)

    async def transfer_margin_to_spot(self, **params):
        """Execute transfer between margin account and spot account.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/margin-api.md#margin-account-transfer-margin

        :param asset: name of the asset
        :type asset: str
        :param amount: amount to transfer
        :type amount: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code:: python

            transfer = client.transfer_margin_to_spot(asset='BTC', amount='1.1')

        :returns: API response

        .. code-block:: python

            {
                "tranId": 100000001
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("transfer_margin_to_spot", **params)

    async def transfer_spot_to_margin(self, **params):
        """Execute transfer between spot account and margin account.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/margin-api.md#margin-account-transfer-margin

        :param asset: name of the asset
        :type asset: str
        :param amount: amount to transfer
        :type amount: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code:: python

            transfer = client.transfer_spot_to_margin(asset='BTC', amount='1.1')

        :returns: API response

        .. code-block:: python

            {
                "tranId": 100000001
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("transfer_spot_to_margin", **params)

    async def transfer_spot_to_isolated_margin(self, **params):
        return await self.client_helper("transfer_spot_to_isolated_margin", **params)

    async def transfer_isolated_margin_to_spot(self, **params):
        return await self.client_helper("transfer_isolated_margin_to_spot", **params)

    async def create_margin_loan(self, **params):
        """Apply for a loan.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/margin-api.md#margin-account-borrow-margin

        :param asset: name of the asset
        :type asset: str
        :param amount: amount to transfer
        :type amount: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code:: python

            transaction = client.margin_create_loan(asset='BTC', amount='1.1')

        :returns: API response

        .. code-block:: python

            {
                "tranId": 100000001
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("create_margin_loan", **params)

    async def repay_margin_loan(self, **params):
        """Repay loan for margin account.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/margin-api.md#margin-account-repay-margin

        :param asset: name of the asset
        :type asset: str
        :param amount: amount to transfer
        :type amount: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code:: python

            transaction = client.margin_repay_loan(asset='BTC', amount='1.1')

        :returns: API response

        .. code-block:: python

            {
                "tranId": 100000001
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("repay_margin_loan", **params)

    async def create_margin_order(self, **params):
        """Post a new order for margin account.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/margin-api.md#margin-account-new-order-trade

        :param symbol: required
        :type symbol: str
        :param side: required
        :type side: str
        :param type: required
        :type type: str
        :param quantity: required
        :type quantity: decimal
        :param price: required
        :type price: str
        :param stopPrice: Used with STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT, and TAKE_PROFIT_LIMIT orders.
        :type stopPrice: str
        :param timeInForce: required if limit order GTC,IOC,FOK
        :type timeInForce: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param icebergQty: Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.
        :type icebergQty: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; MARKET and LIMIT order types default to
            FULL, all other orders default to ACK.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        Response ACK:

        .. code-block:: python

            {
                "symbol": "BTCUSDT",
                "orderId": 28,
                "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
                "transactTime": 1507725176595
            }

        Response RESULT:

        .. code-block:: python

            {
                "symbol": "BTCUSDT",
                "orderId": 28,
                "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
                "transactTime": 1507725176595,
                "price": "1.00000000",
                "origQty": "10.00000000",
                "executedQty": "10.00000000",
                "cummulativeQuoteQty": "10.00000000",
                "status": "FILLED",
                "timeInForce": "GTC",
                "type": "MARKET",
                "side": "SELL"
            }

        Response FULL:

        .. code-block:: python

            {
                "symbol": "BTCUSDT",
                "orderId": 28,
                "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
                "transactTime": 1507725176595,
                "price": "1.00000000",
                "origQty": "10.00000000",
                "executedQty": "10.00000000",
                "cummulativeQuoteQty": "10.00000000",
                "status": "FILLED",
                "timeInForce": "GTC",
                "type": "MARKET",
                "side": "SELL",
                "fills": [
                    {
                        "price": "4000.00000000",
                        "qty": "1.00000000",
                        "commission": "4.00000000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3999.00000000",
                        "qty": "5.00000000",
                        "commission": "19.99500000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3998.00000000",
                        "qty": "2.00000000",
                        "commission": "7.99600000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3997.00000000",
                        "qty": "1.00000000",
                        "commission": "3.99700000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3995.00000000",
                        "qty": "1.00000000",
                        "commission": "3.99500000",
                        "commissionAsset": "USDT"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException,
            BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException,
            BinanceOrderInactiveSymbolException

        """
        return await self.client_helper("create_margin_order", **params)

    async def cancel_margin_order(self, **params):
        """Cancel an active order for margin account.

        Either orderId or origClientOrderId must be sent.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/margin-api.md#margin-account-cancel-order-trade

        :param symbol: required
        :type symbol: str
        :param orderId:
        :type orderId: str
        :param origClientOrderId:
        :type origClientOrderId: str
        :param newClientOrderId: Used to uniquely identify this cancel. Automatically generated by default.
        :type newClientOrderId: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "symbol": "LTCBTC",
                "orderId": 28,
                "origClientOrderId": "myOrder1",
                "clientOrderId": "cancelMyOrder1",
                "transactTime": 1507725176595,
                "price": "1.00000000",
                "origQty": "10.00000000",
                "executedQty": "8.00000000",
                "cummulativeQuoteQty": "8.00000000",
                "status": "CANCELED",
                "timeInForce": "GTC",
                "type": "LIMIT",
                "side": "SELL"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("cancel_margin_order", **params)

    async def get_margin_loan_details(self, **params):
        """Query loan record

        txId or startTime must be sent. txId takes precedence.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/margin-api.md#margin-account-cancel-order-trade

        :param asset: required
        :type asset: str
        :param txId: the tranId in of the created loan
        :type txId: str
        :param startTime:
        :type startTime: str
        :param endTime: Used to uniquely identify this cancel. Automatically generated by default.
        :type endTime: str
        :param current: Currently querying page. Start from 1. Default:1
        :type current: str
        :param size: Default:10 Max:100
        :type size: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "rows": [
                    {
                        "asset": "BNB",
                        "principal": "0.84624403",
                        "timestamp": 1555056425000,
                        //one of PENDING (pending to execution), CONFIRMED (successfully loaned), FAILED (execution failed, nothing happened to your account);
                        "status": "CONFIRMED"
                    }
                ],
                "total": 1
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_margin_loan_details", **params)

    async def get_margin_repay_details(self, **params):
        """Query repay record

        txId or startTime must be sent. txId takes precedence.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/margin-api.md#margin-account-cancel-order-trade

        :param asset: required
        :type asset: str
        :param txId: the tranId in of the created loan
        :type txId: str
        :param startTime:
        :type startTime: str
        :param endTime: Used to uniquely identify this cancel. Automatically generated by default.
        :type endTime: str
        :param current: Currently querying page. Start from 1. Default:1
        :type current: str
        :param size: Default:10 Max:100
        :type size: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "rows": [
                    {
                        //Total amount repaid
                        "amount": "14.00000000",
                        "asset": "BNB",
                        //Interest repaid
                        "interest": "0.01866667",
                        //Principal repaid
                        "principal": "13.98133333",
                        //one of PENDING (pending to execution), CONFIRMED (successfully loaned), FAILED (execution failed, nothing happened to your account);
                        "status": "CONFIRMED",
                        "timestamp": 1563438204000,
                        "txId": 2970933056
                    }
                ],
                "total": 1
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_margin_repay_details", **params)

    async def get_margin_order(self, **params):
        """Query margin accounts order

        Either orderId or origClientOrderId must be sent.

        For some historical orders cummulativeQuoteQty will be < 0, meaning the data is not available at this time.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/margin-api.md#query-margin-accounts-order-user_data

        :param symbol: required
        :type symbol: str
        :param orderId:
        :type orderId: str
        :param origClientOrderId:
        :type origClientOrderId: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "clientOrderId": "ZwfQzuDIGpceVhKW5DvCmO",
                "cummulativeQuoteQty": "0.00000000",
                "executedQty": "0.00000000",
                "icebergQty": "0.00000000",
                "isWorking": true,
                "orderId": 213205622,
                "origQty": "0.30000000",
                "price": "0.00493630",
                "side": "SELL",
                "status": "NEW",
                "stopPrice": "0.00000000",
                "symbol": "BNBBTC",
                "time": 1562133008725,
                "timeInForce": "GTC",
                "type": "LIMIT",
                "updateTime": 1562133008725
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_margin_order", **params)

    async def get_open_margin_orders(self, **params):
        """Query margin accounts open orders

        If the symbol is not sent, orders for all symbols will be returned in an array.

        When all symbols are returned, the number of requests counted against the rate limiter is equal to the number
        of symbols currently trading on the exchange.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/margin-api.md#query-margin-accounts-open-order-user_data

        :param symbol: optional
        :type symbol: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            [
                {
                    "clientOrderId": "qhcZw71gAkCCTv0t0k8LUK",
                    "cummulativeQuoteQty": "0.00000000",
                    "executedQty": "0.00000000",
                    "icebergQty": "0.00000000",
                    "isWorking": true,
                    "orderId": 211842552,
                    "origQty": "0.30000000",
                    "price": "0.00475010",
                    "side": "SELL",
                    "status": "NEW",
                    "stopPrice": "0.00000000",
                    "symbol": "BNBBTC",
                    "time": 1562040170089,
                    "timeInForce": "GTC",
                    "type": "LIMIT",
                    "updateTime": 1562040170089
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_open_margin_orders", **params)

    async def get_all_margin_orders(self, **params):
        """Query all margin accounts orders

        If orderId is set, it will get orders >= that orderId. Otherwise most recent orders are returned.

        For some historical orders cummulativeQuoteQty will be < 0, meaning the data is not available at this time.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/margin-api.md#query-margin-accounts-open-order-user_data

        :param symbol: required
        :type symbol: str
        :param orderId: optional
        :type orderId: str
        :param startTime: optional
        :type startTime: str
        :param endTime: optional
        :type endTime: str
        :param limit: Default 500; max 1000
        :type limit: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            [
                {
                    "id": 43123876,
                    "price": "0.00395740",
                    "qty": "4.06000000",
                    "quoteQty": "0.01606704",
                    "symbol": "BNBBTC",
                    "time": 1556089977693
                },
                {
                    "id": 43123877,
                    "price": "0.00395740",
                    "qty": "0.77000000",
                    "quoteQty": "0.00304719",
                    "symbol": "BNBBTC",
                    "time": 1556089977693
                },
                {
                    "id": 43253549,
                    "price": "0.00428930",
                    "qty": "23.30000000",
                    "quoteQty": "0.09994069",
                    "symbol": "BNBBTC",
                    "time": 1556163963504
                }
            ]


        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_all_margin_orders", **params)

    async def get_margin_trades(self, **params):
        """Query margin accounts trades

        If fromId is set, it will get orders >= that fromId. Otherwise most recent orders are returned.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/margin-api.md#query-margin-accounts-trade-list-user_data

        :param symbol: required
        :type symbol: str
        :param fromId: optional
        :type fromId: str
        :param startTime: optional
        :type startTime: str
        :param endTime: optional
        :type endTime: str
        :param limit: Default 500; max 1000
        :type limit: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            [
                {
                    "commission": "0.00006000",
                    "commissionAsset": "BTC",
                    "id": 34,
                    "isBestMatch": true,
                    "isBuyer": false,
                    "isMaker": false,
                    "orderId": 39324,
                    "price": "0.02000000",
                    "qty": "3.00000000",
                    "symbol": "BNBBTC",
                    "time": 1561973357171
                }, {
                    "commission": "0.00002950",
                    "commissionAsset": "BTC",
                    "id": 32,
                    "isBestMatch": true,
                    "isBuyer": false,
                    "isMaker": true,
                    "orderId": 39319,
                    "price": "0.00590000",
                    "qty": "5.00000000",
                    "symbol": "BNBBTC",
                    "time": 1561964645345
                }
            ]


        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_margin_trades", **params)

    async def get_max_margin_loan(self, **params):
        """Query max borrow amount for an asset

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/margin-api.md#query-max-borrow-user_data

        :param asset: required
        :type asset: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "amount": "1.69248805"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_max_margin_loan", **params)

    async def get_max_margin_transfer(self, **params):
        """Query max transfer-out amount

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/margin-api.md#query-max-transfer-out-amount-user_data

        :param asset: required
        :type asset: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "amount": "3.59498107"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_max_margin_transfer", **params)

    async def margin_stream_get_listen_key(self):
        """Start a new margin data stream and return the listen key
        If a stream already exists it should return the same key.
        If the stream becomes invalid a new key is returned.

        Can be used to keep the user stream alive.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/margin-api.md#start-user-data-stream-for-margin-account-user_stream

        :returns: API response

        .. code-block:: python

            {
                "listenKey": "pqia91ma19a5s61cv6a81va65sdf19v8a65a1a5s61cv6a81va65sdf19v8a65a1"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("margin_stream_get_listen_key")

    async def margin_stream_keepalive(self, listenKey):
        """PING a margin data stream to prevent a time out.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/margin-api.md#ping-user-data-stream-for-margin-account--user_stream

        :param listenKey: required
        :type listenKey: str

        :returns: API response

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("margin_stream_keepalive", listenKey)

    async def margin_stream_close(self, listenKey):
        """Close out a margin data stream.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/margin-api.md#delete-user-data-stream-for-margin-account--user_stream

        :param listenKey: required
        :type listenKey: str

        :returns: API response

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("margin_stream_close", listenKey)

    # Lending Endpoints

    async def get_lending_product_list(self, **params):
        """Get Lending Product List

        https://binance-docs.github.io/apidocs/spot/en/#get-flexible-product-list-user_data

        """
        return await self.client_helper("get_lending_product_list", **params)

    async def get_lending_daily_quota_left(self, **params):
        """Get Left Daily Purchase Quota of Flexible Product.

        https://binance-docs.github.io/apidocs/spot/en/#get-left-daily-purchase-quota-of-flexible-product-user_data

        """
        return await self.client_helper("get_lending_daily_quota_left", **params)

    async def purchase_lending_product(self, **params):
        """Purchase Flexible Product

        https://binance-docs.github.io/apidocs/spot/en/#purchase-flexible-product-user_data

        """
        return await self.client_helper("purchase_lending_product", **params)

    async def get_lending_daily_redemption_quota(self, **params):
        """Get Left Daily Redemption Quota of Flexible Product

        https://binance-docs.github.io/apidocs/spot/en/#get-left-daily-redemption-quota-of-flexible-product-user_data

        """
        return await self.client_helper("get_lending_daily_redemption_quota", **params)

    async def redeem_lending_product(self, **params):
        """Redeem Flexible Product

        https://binance-docs.github.io/apidocs/spot/en/#redeem-flexible-product-user_data

        """
        return await self.client_helper("redeem_lending_product", **params)

    async def get_lending_position(self, **params):
        """Get Flexible Product Position

        https://binance-docs.github.io/apidocs/spot/en/#get-flexible-product-position-user_data

        """
        return await self.client_helper("get_lending_position", **params)

    async def get_lending_account(self, **params):
        """Get Lending Account Details

        https://binance-docs.github.io/apidocs/spot/en/#lending-account-user_data

        """
        return await self.client_helper("get_lending_account", **params)

    async def get_lending_purchase_history(self, **params):
        """Get Lending Purchase History

        https://binance-docs.github.io/apidocs/spot/en/#get-purchase-record-user_data

        """
        return await self.client_helper("get_lending_purchase_history", **params)

    async def get_lending_redemption_history(self, **params):
        """Get Lending Redemption History

        https://binance-docs.github.io/apidocs/spot/en/#get-redemption-record-user_data

        """
        return await self.client_helper("get_lending_redemption_history", **params)

    async def get_lending_interest_history(self, **params):
        """Get Lending Interest History

        https://binance-docs.github.io/apidocs/spot/en/#get-interest-history-user_data-2

        """
        return await self.client_helper("get_lending_interest_history", **params)

    # Sub Accounts

    async def get_sub_account_list(self, **params):
        """Query Sub-account List.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/wapi-api.md#query-sub-account-listfor-master-account

        :param email: optional
        :type email: str
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param page: optional
        :type page: int
        :param limit: optional
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "success":true,
                "subAccounts":[
                    {
                        "email":"123@test.com",
                        "status":"enabled",
                        "activated":true,
                        "mobile":"91605290",
                        "gAuth":true,
                        "createTime":1544433328000
                    },
                    {
                        "email":"321@test.com",
                        "status":"disabled",
                        "activated":true,
                        "mobile":"22501238",
                        "gAuth":true,
                        "createTime":1544433328000
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_sub_account_list", **params)

    async def get_sub_account_transfer_history(self, **params):
        """Query Sub-account Transfer History.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/wapi-api.md#query-sub-account-transfer-historyfor-master-account

        :param email: required
        :type email: str
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param page: optional
        :type page: int
        :param limit: optional
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "success":true,
                "transfers":[
                    {
                        "from":"aaa@test.com",
                        "to":"bbb@test.com",
                        "asset":"BTC",
                        "qty":"1",
                        "time":1544433328000
                    },
                    {
                        "from":"bbb@test.com",
                        "to":"ccc@test.com",
                        "asset":"ETH",
                        "qty":"2",
                        "time":1544433328000
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_sub_account_transfer_history", **params)

    async def create_sub_account_transfer(self, **params):
        """Execute sub-account transfer

        https://github.com/binance-exchange/binance-official-api-docs/blob/9dbe0e961b80557bb19708a707c7fad08842b28e/wapi-api.md#sub-account-transferfor-master-account

        :param fromEmail: required - Sender email
        :type fromEmail: str
        :param toEmail: required - Recipient email
        :type toEmail: str
        :param asset: required
        :type asset: str
        :param amount: required
        :type amount: decimal
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "success":true,
                "txnId":"2966662589"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("create_sub_account_transfer", **params)

    async def get_sub_account_assets(self, **params):
        """Fetch sub-account assets

        https://github.com/binance-exchange/binance-official-api-docs/blob/9dbe0e961b80557bb19708a707c7fad08842b28e/wapi-api.md#query-sub-account-assetsfor-master-account

        :param email: required
        :type email: str
        :param symbol: optional
        :type symbol: str
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "success":true,
                "balances":[
                    {
                        "asset":"ADA",
                        "free":10000,
                        "locked":0
                    },
                    {
                        "asset":"BNB",
                        "free":10003,
                        "locked":0
                    },
                    {
                        "asset":"BTC",
                        "free":11467.6399,
                        "locked":0
                    },
                    {
                        "asset":"ETH",
                        "free":10004.995,
                        "locked":0
                    },
                    {
                        "asset":"USDT",
                        "free":11652.14213,
                        "locked":0
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return await self.client_helper("get_sub_account_assets", **params)

    # Futures API

    async def futures_ping(self):
        """Test connectivity to the Rest API

        https://binance-docs.github.io/apidocs/futures/en/#test-connectivity

        """
        return await self.client_helper("futures_ping")

    async def futures_time(self):
        """Test connectivity to the Rest API and get the current server time.

        https://binance-docs.github.io/apidocs/futures/en/#check-server-time

        """
        return await self.client_helper("futures_time")

    async def futures_exchange_info(self):
        """Current exchange trading rules and symbol information

        https://binance-docs.github.io/apidocs/futures/en/#exchange-information-market_data

        """
        return await self.client_helper("futures_exchange_info")

    async def futures_order_book(self, **params):
        """Get the Order Book for the market

        https://binance-docs.github.io/apidocs/futures/en/#order-book-market_data

        """
        return await self.client_helper("futures_order_book", **params)

    async def futures_recent_trades(self, **params):
        """Get recent trades (up to last 500).

        https://binance-docs.github.io/apidocs/futures/en/#recent-trades-list-market_data

        """
        return await self.client_helper("futures_recent_trades", **params)

    async def futures_historical_trades(self, **params):
        """Get older market historical trades.

        https://binance-docs.github.io/apidocs/futures/en/#old-trades-lookup-market_data

        """
        return await self.client_helper("futures_historical_trades", **params)

    async def futures_aggregate_trades(self, **params):
        """Get compressed, aggregate trades. Trades that fill at the time, from the same order, with the same
        price will have the quantity aggregated.

        https://binance-docs.github.io/apidocs/futures/en/#compressed-aggregate-trades-list-market_data

        """
        return await self.client_helper("futures_aggregate_trades", **params)

    async def futures_klines(self, **params):
        """Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.

        https://binance-docs.github.io/apidocs/futures/en/#kline-candlestick-data-market_data

        """
        return await self.client_helper("futures_klines", **params)

    async def futures_mark_price(self, **params):
        """Get Mark Price and Funding Rate

        https://binance-docs.github.io/apidocs/futures/en/#mark-price-market_data

        """
        return await self.client_helper("futures_mark_price", **params)

    async def futures_funding_rate(self, **params):
        """Get funding rate history

        https://binance-docs.github.io/apidocs/futures/en/#get-funding-rate-history-market_data

        """
        return await self.client_helper("futures_funding_rate", **params)

    async def futures_ticker(self, **params):
        """24 hour rolling window price change statistics.

        https://binance-docs.github.io/apidocs/futures/en/#24hr-ticker-price-change-statistics-market_data

        """
        return await self.client_helper("futures_ticker", **params)

    async def futures_symbol_ticker(self, **params):
        """Latest price for a symbol or symbols.

        https://binance-docs.github.io/apidocs/futures/en/#symbol-price-ticker-market_data

        """
        return await self.client_helper("futures_symbol_ticker", **params)

    async def futures_orderbook_ticker(self, **params):
        """Best price/qty on the order book for a symbol or symbols.

        https://binance-docs.github.io/apidocs/futures/en/#symbol-order-book-ticker-market_data

        """
        return await self.client_helper("futures_orderbook_ticker", **params)

    async def futures_liquidation_orders(self, **params):
        """Get all liquidation orders

        https://binance-docs.github.io/apidocs/futures/en/#get-all-liquidation-orders-market_data

        """
        return await self.client_helper("futures_liquidation_orders", **params)

    async def futures_open_interest(self, **params):
        """Get present open interest of a specific symbol.

        https://binance-docs.github.io/apidocs/futures/en/#open-interest-market_data

        """
        return await self.client_helper("futures_open_interest", **params)

    async def futures_leverage_bracket(self, **params):
        """Notional and Leverage Brackets

        https://binance-docs.github.io/apidocs/futures/en/#notional-and-leverage-brackets-market_data

        """
        return await self.client_helper("futures_leverage_bracket", **params)

    async def transfer_history(self, **params):
        """Get future account transaction history list

        https://binance-docs.github.io/apidocs/futures/en/#new-future-account-transfer

        """
        return await self.client_helper("transfer_history", **params)

    async def futures_create_order(self, **params):
        """Send in a new order.

        https://binance-docs.github.io/apidocs/futures/en/#new-order-trade

        """
        return await self.client_helper("futures_create_order", **params)

    async def futures_get_order(self, **params):
        """Check an order's status.

        https://binance-docs.github.io/apidocs/futures/en/#query-order-user_data

        """
        return await self.client_helper("futures_get_order", **params)

    async def futures_get_open_orders(self, **params):
        """Get all open orders on a symbol.

        https://binance-docs.github.io/apidocs/futures/en/#current-open-orders-user_data

        """
        return await self.client_helper("futures_get_open_orders", **params)

    async def futures_get_all_orders(self, **params):
        """Get all futures account orders; active, canceled, or filled.

        https://binance-docs.github.io/apidocs/futures/en/#all-orders-user_data

        """
        return await self.client_helper("futures_get_all_orders", **params)

    async def futures_cancel_order(self, **params):
        """Cancel an active futures order.

        https://binance-docs.github.io/apidocs/futures/en/#cancel-order-trade

        """
        return await self.client_helper("futures_cancel_order", **params)

    async def futures_cancel_all_open_orders(self, **params):
        """Cancel all open futures orders

        https://binance-docs.github.io/apidocs/futures/en/#cancel-all-open-orders-trade

        """
        return await self.client_helper("futures_cancel_all_open_orders", **params)

    async def futures_cancel_orders(self, **params):
        """Cancel multiple futures orders

        https://binance-docs.github.io/apidocs/futures/en/#cancel-multiple-orders-trade

        """
        return await self.client_helper("futures_cancel_orders", **params)

    async def futures_account_balance(self, **params):
        """Get futures account balance

        https://binance-docs.github.io/apidocs/futures/en/#future-account-balance-user_data

        """
        return await self.client_helper("futures_account_balance", **params)

    async def futures_account(self, **params):
        """Get current account information.

        https://binance-docs.github.io/apidocs/futures/en/#account-information-user_data

        """
        return await self.client_helper("futures_account", **params)

    async def futures_change_leverage(self, **params):
        """Change user's initial leverage of specific symbol market

        https://binance-docs.github.io/apidocs/futures/en/#change-initial-leverage-trade

        """
        return await self.client_helper("futures_change_leverage", **params)

    async def futures_change_margin_type(self, **params):
        """Change the margin type for a symbol

        https://binance-docs.github.io/apidocs/futures/en/#change-margin-type-trade

        """
        return await self.client_helper("futures_change_margin_type", **params)

    async def futures_change_position_margin(self, **params):
        """Change the position margin for a symbol

        https://binance-docs.github.io/apidocs/futures/en/#modify-isolated-position-margin-trade

        """
        return await self.client_helper("futures_change_position_margin", **params)

    async def futures_position_margin_history(self, **params):
        """Get position margin change history

        https://binance-docs.github.io/apidocs/futures/en/#get-postion-margin-change-history-trade

        """
        return await self.client_helper("futures_position_margin_history", **params)

    async def futures_position_information(self, **params):
        """Get position information

        https://binance-docs.github.io/apidocs/futures/en/#position-information-user_data

        """
        return await self.client_helper("futures_position_information", **params)

    async def futures_account_trades(self, **params):
        """Get trades for the authenticated account and symbol.

        https://binance-docs.github.io/apidocs/futures/en/#account-trade-list-user_data

        """
        return await self.client_helper("futures_account_trades", **params)

    async def futures_income_history(self, **params):
        """Get income history for authenticated account

        https://binance-docs.github.io/apidocs/futures/en/#get-income-history-user_data

        """
        return await self.client_helper("futures_income_history", **params)

