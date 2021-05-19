import datetime

import python_bitbankcc
import requests

from .settings import set_token, set_key


class PostNotify():
    def __init__(self):
        self.pub = python_bitbankcc.public()
        self.prv = python_bitbankcc.private(*set_key())

    def _post_line_notify(self, post_message: str):
        api = 'https://notify-api.line.me/api/notify'
        headers = {'Authorization': f'Bearer {set_token()}'}
        data = {'message': f'{post_message}'}

        requests.post(api, headers=headers, data=data)

    def send_ticker(self):
        dict_pair = {
            'btc_jpy': 'BTC/JPY',
            'eth_jpy': 'ETH/JPY',
            'xrp_jpy': 'XRP/JPY',
            'ltc_jpy': 'LTC/JPY',
            'mona_jpy': 'MONA/JPY',
            'bcc_jpy': 'BCC/JPY',
            'xlm_jpy': 'XLM/JPY',
            'qtum_jpy': 'QTUM/JPY',
            'bat_jpy': 'BAT/JPY'
            }

        message = '現在価格 (前日比)'
        for pair, value in dict_pair.items():
            ticker = self.pub.get_ticker(pair)['last']
            price_open = self.pub.get_candlestick(pair, '1day', self._today('1day'))['candlestick'][0]['ohlcv'][-1][0]
            roc = self._rate_of_change(ticker, price_open)
            message += f'\n{value}   {ticker} ({roc})'

        self._post_line_notify(message)

    def _today(self, c_type: str):
        keys = ['1min', '5min', '15min', '30min', '1hour', '4hour', '8hour', '12hour', '1day', '1week']
        values = ['%Y%m%d'] * 5 + ['%Y'] * 5
        d = dict(zip(keys, values))

        return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date().strftime(d[c_type])

    def _rate_of_change(self, ticker: str, price_open: str):
        ticker = float(ticker)
        price_open = float(price_open)
        roc = round((ticker - price_open) / price_open * 100, 2)
        if roc < 0.00:
            roc_str = '▼ ' + str(roc) + '%'
        else:
            roc_str = '△ +' + str(roc) + '%'

        return roc_str

    def send_asset(self):
        dict_pair = {
            'btc_jpy': 'BTC',
            'eth_jpy': 'ETH',
            'xrp_jpy': 'XRP',
            'ltc_jpy': 'LTC',
            'mona_jpy': 'MONA',
            'bcc_jpy': 'BCC',
            'xlm_jpy': 'XLM',
            'qtum_jpy': 'QTUM',
            'bat_jpy': 'BAT'
            }

        message = ''
        asset = self.prv.get_asset()
        total = float(asset['assets'][0]['onhand_amount'])
        for i, (pair, currency) in zip(range(len(dict_pair)), dict_pair.items()):
            value = float(self.pub.get_ticker(pair)['last']) * float(asset['assets'][i + 1]['onhand_amount'])
            total += value
            if value > 1.:
                message += f"\n{currency}:  {asset['assets'][i + 1]['onhand_amount']}"
        total = int(total)

        message = '資産\n'\
                  + '総資産  ¥{:,}\n'.format(total)\
                  + f"JPY:  {int(float(asset['assets'][0]['onhand_amount']))}"\
                  + message

        self._post_line_notify(message)

    def send_orders(self):
        list_pair = [
            'btc_jpy', 'ltc_jpy', 'xrp_jpy', 'eth_jpy', 'mona_jpy', 'bcc_jpy',
            'ltc_btc', 'xrp_btc', 'eth_btc', 'mona_btc', 'bcc_btc'
            ]

        message = '注文一覧'
        for pair in list_pair:
            message += self._show_orders(self.prv.get_active_orders(pair)['orders'])

        self._post_line_notify(message)

    def _show_orders(self, orders: list):
        dict_pair = {
            'btc_jpy': 'BTC/JPY',
            'ltc_jpy': 'LTC/JPY',
            'xrp_jpy': 'XRP/JPY',
            'eth_jpy': 'ETH/JPY',
            'mona_jpy': 'MONA/JPY',
            'bcc_jpy': 'BCC/JPY',
            'ltc_btc': 'LTC/BTC',
            'xrp_btc': 'XRP/BTC',
            'eth_btc': 'ETH/BTC',
            'mona_btc': 'MONA/BTC',
            'bcc_btc': 'BCC/BTC'
            }
        dict_side = {
            'buy': '買',
            'sell': '売'
            }
        dict_type = {
            'limit': '指値',
            'market': '成行'
            }

        message = ''
        for order in orders:
            message += f"\n{dict_pair[order['pair']]}  {dict_type[order['type']]}  {dict_side[order['side']]}  "\
                       f"{order['price']}  {order['start_amount']}"

        return message
