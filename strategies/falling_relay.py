# NAME=下跌中继
# DESCRIPTION=下跌中继做反弹


def func(self):
    """下跌中继做反弹"""
    for k, v in self.market.tell.items():
        ma5 = v.ma(5, 'close')
        ma10 = v.ma(10, 'close')
        offset = v.increasement(ma10, v.close)
        if ma5 > ma10:
            if offset > .425 and .085 > v.increase > .07:
                self.li_sell.add(k)
            elif .366 > offset > .343 and v.increase > .07 and (
                v.increase_day < .02 or .08 < v.increase_day < .09 or v.increase_day > .095
            ):
                self.li_sell.add(k)
            elif offset > .342 and v.increase > .07 and (
                .001 < v.increase_day < .02 or .08 < v.increase_day < .09 or v.increase_day > .095
            ):
                self.li_sell.add(k)
            elif offset > .252 and v.increase > .08 and .017 < v.increase_day < .022:
                self.li_sell.add(k)
            elif offset > .245 and v.increase < -.078 and v.increase_day < -.095:
                self.li_buy.add(k)
            elif offset > .214 and .06 > v.increase > .03 and .035 > v.increase_day > .025:
                self.li_sell.add(k)
            elif .193 > offset > .125 and (.09 > v.increase > .078 or .044 > v.increase > .024) and (
                    .089 > v.increase_day > -.02):
                self.li_sell.add(k)
            elif .124 > offset > .091 and (
                    .065 > v.increase > .057 or .048 > v.increase > .028
            ) and (
                    .062 > v.increase_day > -.012
            ):
                self.li_sell.add(k)
            elif .171 > offset > .08:
                if v.increase_day > .134 or .126 > v.increase_day > .11:
                    self.li_sell.add(k)
                elif -.048 < v.increase < -.031 and -.064 < v.increase_day < -.041:
                    self.li_sell.add(k)
                elif .094 > offset > .084 and .095 < v.increase_day:
                    self.li_sell.add(k)
            elif .101 > offset > .069 and .064 > v.increase > .052 and .065 > v.increase_day > .063:
                self.li_sell.add(k)
            elif .07 > offset > .067 and -.012 < v.increase < -.01 and -.012 < v.increase_day < -.01:
                self.li_buy.add(k)
            elif .088 > offset > .042 and .016 < v.increase < .029 and .019 < v.increase_day < .026:
                self.li_sell.add(k)
            elif .059 > offset > .056 and .031 < v.increase < .041 and .026 < v.increase_day < .034:
                self.li_sell.add(k)
            elif .055 > offset > .045 and -.036 < v.increase < -.031 and -.016 < v.increase_day < -.014:
                self.li_buy.add(k)
            elif .048 > offset > .038 and -.078 < v.increase < -.064 and -.045 < v.increase_day < -.036:
                self.li_buy.add(k)
            elif .04 > offset > .037:
                if -.048 < v.increase < -.04 and -.049 < v.increase_day < -.045:
                    self.li_buy.add(k)
                elif .04 > v.increase > .026 and .056 > v.increase_day > .027:
                    self.li_sell.add(k)
            elif .036 > offset > .033 and -.021 < v.increase < -.018 and v.increase_day < -.036:
                self.li_buy.add(k)
            elif .033 > offset > .022 and .01 < v.increase < .012 and -.002 < v.increase_day < .001:
                self.li_buy.add(k)
            elif .032 > offset > .026:
                if v.increase < -.092 and -.088 < v.increase_day < -.066:
                    self.li_buy.add(k)
                elif .014 < v.increase < .034 and .013 < v.increase_day < .036:
                    self.li_sell.add(k)
            elif .026 > offset > .012:
                if v.increase < -.001 and -.005 < v.increase_day < -.002:
                    self.li_sell.add(k)
                elif -.001 < v.increase < .001 and -.03 < v.increase_day < -.02:
                    self.li_sell.add(k)
                elif -.023 < v.increase < -.021 and -.016 < v.increase_day < -.015:
                    self.li_buy.add(k)
                elif -.021 < v.increase < -.02 and -.012 < v.increase_day < -.009:
                    self.li_buy.add(k)
                elif -.012 < v.increase < -.005 and -.003 < v.increase_day < -.002:
                    self.li_buy.add(k)
                elif .016 < v.increase < .017 and .03 > v.increase_day > .026:
                    self.li_buy.add(k)
                elif .028 < v.increase < .045 and .026 < v.increase_day < .041:
                    self.li_sell.add(k)
            elif .011 > offset > .01 and -.037 < v.increase < -.036 and -.039 < v.increase_day < -.038:
                self.li_buy.add(k)
            elif .011 > offset > .009 and -.041 < v.increase < -.036 and (
                    -.033 < v.increase_day < -.028 or -.023 < v.increase_day < -.02):
                self.li_buy.add(k)
            elif .01 > offset > .009:
                if -.001 < v.increase < .001 and -.003 < v.increase_day < -.002:
                    self.li_buy.add(k)
            elif -.028 > offset > -.031 and (
                    .016 > v.increase > .013 or .003 > v.increase > -.002
            ) and v.increase_day < .003:
                self.li_buy.add(k)
            elif -.008 > offset > -.01 and -.011 < v.increase < -.009 and -.015 < v.increase_day < -.014:
                self.li_buy.add(k)
            elif -.004 > offset > -.01 and -.016 < v.increase < -.013 and -.023 < v.increase_day < -.021:
                self.li_buy.add(k)
            elif -.007 > offset > -.011 and -.01 < v.increase < -.006 and -.001 < v.increase_day < .00:
                self.li_buy.add(k)
            elif -.005 > offset > -.01 and -.059 < v.increase < -.055 and -.045 < v.increase_day < -.041:
                self.li_buy.add(k)
            elif -.011 > offset > -.013:
                if -.03 < v.increase < -.026 and -.003 < v.increase_day < -.001:
                    self.li_buy.add(k)
                elif -.012 < v.increase < -.006 and -.017 < v.increase_day < -.016:
                    self.li_buy.add(k)
                elif -.036 < v.increase < -.019 and -.038 < v.increase_day < -.034:
                    self.li_buy.add(k)
            elif -.017 < offset < -.016 and -.012 < v.increase < -.01 and -.015 < v.increase_day < -.014:
                self.li_buy.add(k)
            elif -.025 < offset < -.023 and -.038 < v.increase < -.036 and -.04 < v.increase_day < -.037:
                self.li_buy.add(k)
            elif -.039 < offset < -.024 and -.046 < v.increase < -.044 and -.039 < v.increase_day < -.033:
                self.li_buy.add(k)
            elif -.035 < offset < -.031 and -.067 < v.increase < -.06 and -.041 < v.increase_day < -.037:
                self.li_buy.add(k)
            elif -.04 < offset < -.035 and -.06 < v.increase < -.055 and -.058 < v.increase_day < -.051:
                self.li_buy.add(k)
            elif -.039 < offset < -.035 and -.06 < v.increase < -.043 and (
                    -.046 < v.increase_day < -.043 or -.038 < v.increase_day < -.03
            ):
                self.li_buy.add(k)
            elif -.045 < offset < -.041 and -.055 < v.increase < -.051 and -.035 < v.increase_day < -.029:
                self.li_buy.add(k)
            elif -.062 < offset < -.058 and v.increase < -.092 and v.increase_day < -.09:
                self.li_buy.add(k)
        else:
            his = v.interval_max(10, 'close')
            quota = v.increasement(his, v.close)
            if quota < -.03:
                if (
                        v.increase < -.069 or -.051 < v.increase < -.047 or
                        -.042 < v.increase < -.038 or -.015 < v.increase < -.014
                ) and (
                        -.021 < v.increase_day < -.02 or -.018 < v.increase_day < -.017
                ) and v.open < ma10 * .986:
                    self.li_buy.add(k)
                elif (v.close > ma5 or v.high > ma10) and (
                        -.024 < v.increase < -.014 or -.011 < v.increase < -.009 or
                        -.008 < v.increase < -.006 or -.004 < v.increase < -.002 or
                        -.001 < v.increase < .009 or .014 < v.increase < .036 or
                        .037 < v.increase < .04 or .041 < v.increase < .044 or .065 < v.increase < .074 or .082 < v.increase
                ) and (
                        -.03 < v.increase_day < -.015 or -.014 < v.increase_day < -.012 or
                        -.011 < v.increase_day < -.005 or -.003 < v.increase_day < .004 or
                        .006 < v.increase_day < .008 or .012 < v.increase_day < .021 or
                        .023 < v.increase_day < .028 or .029 < v.increase_day < .0339 or
                        .035 < v.increase_day < .049 or .05 < v.increase_day < .051 or .055 < v.increase_day
                ) and (
                        quota < -.2 or -.197 < quota < -.171 or -.168 < quota < -.158 or -.157 < quota < -.100 or
                        -.099 < quota < -.069 or -.068 < quota < -.055 or -.054 < quota < -.045 or
                        -.044 < quota < -.037 or -.037 < quota
                ):
                    self.li_sell.add(k)
                if offset < -.09 and -.022 < v.increase < -.015 and -.012 < v.increase_day < -.008:
                    self.li_buy.add(k)
                elif -.103 < offset < -.072 and -.066 < v.increase and -.066 < v.increase_day < -.063:
                    self.li_buy.add(k)
                elif -.089 < offset < -.073 and -.055 < v.increase < -.05 and -.048 < v.increase_day < -.047:
                    self.li_buy.add(k)
                elif -.121 < offset < -.113 and -.072 < v.increase < -.066 and -.064 < v.increase_day < -.06:
                    self.li_buy.add(k)
                elif -.112 < offset < -.095 and -.051 < v.increase < -.048 < v.increase_day < -.044:
                    self.li_buy.add(k)
                elif -.191 < offset < -.076 and (
                        -.025 < v.increase < -.024 or -.02 < v.increase < -.012
                ) and v.increase_day < -.021:
                    self.li_buy.add(k)
                elif -.088 < offset < -.073:
                    if -.019 < v.increase < -.018 and -.02 < v.increase_day < -.018:
                        self.li_buy.add(k)
                    elif -.031 < v.increase < -.012 and -.047 < v.increase_day < -.038:
                        self.li_buy.add(k)
                    elif -.054 < v.increase < -.051 and -.044 < v.increase_day < -.041:
                        self.li_buy.add(k)
                    elif -.061 < v.increase < -.059 and -.052 < v.increase_day < -.048:
                        self.li_buy.add(k)
                    elif -.09 < v.increase < -.075 and -.065 < v.increase_day < -.058:
                        self.li_buy.add(k)
                elif -.075 < offset < -.073 and -.02 < v.increase < -.015 and .001 < v.increase_day < .003:
                    self.li_buy.add(k)
                elif -.085 < offset < -.067 and -.003 < v.increase < .001 and -.012 < v.increase_day < .001:
                    self.li_buy.add(k)
                elif -.071 < offset < -.066:
                    if (
                            -.046 < v.increase < -.039 or -.037 < v.increase < -.033
                    ) and -.049 < v.increase_day < -.041:
                        self.li_buy.add(k)
                elif -.061 < offset < -.049:
                    if -.056 < offset < -.053 and (
                        -.011 > v.increase_day > -.013 or -.023 > v.increase_day > -.024 or
                        -.037 > v.increase_day > -.04 or -.042 > v.increase_day > -.059
                    ) and (
                        -.006 > v.increase > -.022 or -.026 > v.increase > -.027
                    ):
                        self.li_buy.add(k)
                    elif .04 < v.increase < .06 and .05 < v.increase_day < .06:
                        self.li_sell.add(k)
                    elif -.032 < v.increase < -.026 and -.028 < v.increase_day < -.02:
                        self.li_sell.add(k)
                    elif -.053 < offset and -.023 < v.increase < -.021 and -.019 < v.increase_day < -.018:
                        self.li_buy.add(k)
                elif -.047 < offset < -.045 and -.005 > v.increase_day > -.009 and -.022 > v.increase > -.039:
                    self.li_buy.add(k)
                elif -.045 < offset < -.043 and -.015 > v.increase_day > -.019 and -.012 > v.increase > -.016:
                    self.li_buy.add(k)
                elif -.04 < offset < -.037 and -.023 > v.increase_day and -.022 > v.increase > -.024:
                    self.li_buy.add(k)
                elif -.036 < offset < -.032:
                    if .054 < v.increase_day < .065 and .043 < v.increase < .046:
                        self.li_sell.add(k)
                    elif .01 < v.increase_day < .03 and .012 < v.increase < .06:
                        self.li_sell.add(k)
                    elif -.015 < v.increase_day < -.011 and -.006 < v.increase < -.005:
                        self.li_buy.add(k)
                    elif -.001 < v.increase_day < .003 and -.017 < v.increase < -.015:
                        self.li_buy.add(k)
                    elif -.031 < v.increase_day < -.015 and .002 < v.increase < .005:
                        self.li_buy.add(k)
                elif -.031 < offset < -.018:
                    if -.045 < v.increase < -.033 and .005 < v.increase_day < .009:
                        self.li_buy.add(k)
                    elif -.023 < offset and -.029 < v.increase < -.027 and -.023 < v.increase_day < -.021:
                        self.li_buy.add(k)
                    elif -.026 < offset < -.023 and -.059 < v.increase < -.029 and -.015 < v.increase_day < -.009:
                        self.li_buy.add(k)
                    elif -.021 > offset > -.024 > v.increase > -.026 and -.02 < v.increase_day < -.017:
                        self.li_buy.add(k)
                    elif offset < -.027 and -.009 < v.increase < -.007 and -.014 < v.increase_day < -.013:
                        self.li_buy.add(k)
                elif -.015 < offset < -.009 and v.increase < -.038 and -.035 < v.increase_day < -.033:
                    self.li_buy.add(k)
                elif -.008 < offset < -.006 and -.005 < v.increase_day < -.002 and -.012 < v.increase < -.01:
                    self.li_buy.add(k)
                elif -.005 < offset < -.003 and -.02 < v.increase_day < -.016 and -.022 < v.increase < -.014:
                    self.li_buy.add(k)
                elif -.001 < offset < .008 and -.025 < v.increase_day < -.017 and (
                        -.009 < v.increase < -.006 or -.045 < v.increase < -.025
                ):
                    self.li_buy.add(k)
            if .01 < offset < .023 and (
                    -.008 < v.increase < .025 or .028 < v.increase < .031 or
                    .034 < v.increase < .04 or .044 < v.increase < .054 or v.increase > .06
            ):
                self.li_sell.add(k)
            elif .023 < offset < .032 and v.increase > .034 and v.increase_day > .045:
                self.li_sell.add(k)
            elif .033 < offset < .043 and (v.increase > .06 or .045 > v.increase > .03):
                self.li_sell.add(k)
            elif .032 < offset < .053 and v.increase > .03 and v.increase_day > .084:
                self.li_sell.add(k)
            elif .063 < offset < .069 and .002 < v.increase < .004 and .01 < v.increase_day < .017:
                self.li_sell.add(k)
            elif .069 < offset < .08 and .055 < v.increase < .084 and .06 < v.increase_day < .099:
                self.li_sell.add(k)
            elif offset < -.254 and v.increase < -.067 and v.increase_day < -.056:
                self.li_buy.add(k)
            elif offset < -.225 and .082 > v.increase > .03 and (
                    -.1 < v.increase_day < -.05 or .005 < v.increase_day < .016
            ):
                self.li_sell.add(k)
            elif offset < -.154 and (
                    -.078 < v.increase < -.076 or -.075 < v.increase < -.049
            ) and (
                    -.069 < v.increase_day < -.053 or -.044 < v.increase_day < -.02 or
                    -.019 < v.increase_day < -.015
            ):
                self.li_buy.add(k)
            elif -.157 < offset < -.15:
                if v.increase < -.04 and -.001 < v.increase_day < .001:
                    self.li_buy.add(k)
            elif offset < -.141:
                if -.05 < v.increase < -.04 and -.05 < v.increase_day < -.04:
                    self.li_buy.add(k)
            elif offset < -.131:
                if -.035 < v.increase < -.025 and -.055 < v.increase_day < -.026:
                    self.li_buy.add(k)
            elif offset < -.105:
                if -.063 < v.increase_day < -.058 and -.064 < v.increase < -.051:
                    self.li_buy.add(k)
                elif -.023 < v.increase_day < -.014 and -.048 < v.increase < -.036:
                    self.li_buy.add(k)
                elif .012 < v.increase < .031 and (
                        .00 < v.increase_day < .008 or .014 < v.increase_day < .018
                ):
                    self.li_sell.add(k)
            elif offset < -.081:
                if -.029 < v.increase < -.021 and -.008 < v.increase_day < -.004:
                    self.li_buy.add(k)
                elif (
                        -.074 < v.increase < -.062 or -.059 < v.increase < -.056
                ) and -.072 < v.increase_day < -.068:
                    self.li_buy.add(k)
            elif -.08 < offset < -.047:
                if .001 > v.increase_day > -.001 and -.005 > v.increase > -.006:
                    self.li_buy.add(k)
                elif offset < -.077 and -.066 < v.increase < -.06 and -.052 < v.increase_day:
                    self.li_buy.add(k)
                elif -.061 < offset < -.055 or -.053 < offset:
                    if -.029 > v.increase_day > -.032 and -.033 > v.increase > -.036:
                        self.li_buy.add(k)
                    elif -.025 > v.increase_day > -.03 and -.01 > v.increase > -.016:
                        self.li_buy.add(k)
                elif -.057 > v.increase_day > -.059 and -.063 > v.increase > -.066:
                    self.li_buy.add(k)
                if -.073 < offset < -.069:
                    if -.029 < v.increase < -.025 and -.031 < v.increase_day < -.026:
                        self.li_buy.add(k)
                    elif .011 < v.increase < .016 and .033 < v.increase_day < .045:
                        self.li_buy.add(k)
                elif -.065 < offset < -.061:
                    if -.009 < v.increase < -.002 and -.014 < v.increase_day < -.01:
                        self.li_buy.add(k)
                elif -.062 < offset < -.055:
                    if -.028 < v.increase < -.024 and -.017 < v.increase_day < -.016:
                        self.li_buy.add(k)
            elif -.046 < offset < -.04 and -.013 < v.increase < -.011 and -.016 < v.increase_day < -.012:
                self.li_buy.add(k)
            elif -.039 < offset < -.029:
                if -.006 < v.increase < -.005 < v.increase_day < -.004:
                    self.li_buy.add(k)
                elif -.03 < offset and -.026 < v.increase < -.024 and -.017 < v.increase_day < -.015:
                    self.li_buy.add(k)
                elif (
                        -.004 < v.increase < -.003 or .001 < v.increase < .008
                ) and (
                        -.019 < v.increase_day < -.005
                ):
                    self.li_sell.add(k)
            elif -.006 > offset > -.008 > v.increase_day > -.011 and -.009 < v.increase < -.008:
                self.li_buy.add(k)
