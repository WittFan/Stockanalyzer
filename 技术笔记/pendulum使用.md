# pendulum


index_daily['datetime'] = index_daily.apply(lambda x: pendulum.parse(x['trade_date']), axis=1)