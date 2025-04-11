# NAME=V-PRICE
# DESCRIPTION=成交量加权平均价波段策略


prop = [
    # ('index_name', lambda x: x.func())
]


def func(self):
    self.set_price_buy('low')
    self.set_price_sell('high')
    n = 20
    nr = 10
    for k, v in self.market.tell.items():
        # write your strategy here
        # `self.li_buy.add(k)` for buy
        # `self.li_sell.add(k)` for sell
        if v.code not in self.static:
            amo = v.get_series('amount')
            vol = v.get_series('volume')
            x = 100 if v.code[0] == 's' else 1
            v_price = amo / vol / x
            mv = v.ema(6, v_price)
            c = v.get_series('close')
            o = v.get_series('open')
            vol = v.get_series('volume')
            inc = c / v.ref(1, c)
            vinc = vol / v.ref(1, vol)
            sync = inc / vinc
            masy = v.ema(n, v.ema(n, sync))
            difsy = 10 * (masy - v.ref(1, masy))
            chg = difsy * v.ref(1, difsy) < 0
            dif = c - o
            buy1 = (chg & (difsy * dif < 0))
            up = v.count((inc > 1) & (vinc > 1), n) / v.count(inc > 1, n)
            down = v.count((inc <= 1) & (vinc < 1), n) / v.count(inc <= 1, n)
            power = up + down
            pwm1 = v.ema(3, power)
            pwm2 = v.ema(14, power)
            buy2 = v.cross(pwm1, pwm2) | v.cross(pwm2, pwm1)
            difp = power - v.ref(1, power)
            vrsi = 100 * v.ema(nr, v.sma(nr, 1, v.max(difp, 0) / v.sma(nr, 1, abs(difp))))
            buy3 = v.ref(1, vrsi < v.ref(1, vrsi)) & (vrsi > v.ref(1, vrsi))
            close = v.get_series('close')
            zt = close >= v.zt_price(v.ref(1, close), .1)
            self.static[v.code] = (
                v.cross(close, mv) & zt & buy1 & v.exist(buy3, 6) & v.between(v.count(buy2, 4), 0, 3),
                v.cross(mv, close)
            )
        if self.static[v.code][0][v.date]:
            self.li_buy.add(k)
            continue
        if self.static[v.code][1][v.date]:
            self.li_sell.add(k)
