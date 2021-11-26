# ukey
# ukeyhash

# name:                     产品名称
# code:                     产品代码
# code_register:            登记编码
# bank_name                 银行名称
# bank_level                银行层级（国有银行、股份银行、城商银行、农商银行）
# currency:                 币种
# risk:                     风险等级

# rate_type:                净值型、预期收益型       “保本的”为预期收益型，“非保本的”为净值型
# 建设银行 用 七日年化收益率譬如3.6%，来表示 净值型产品的收益水平
# 工商银行 直接用 净值譬如1.2256，来表示 净值型产品的收益水平

# 【利率的参考，以产品说明书PDF文件为准】
# 只有一个利率时，默认首先保存rate_min
# rate_min:                 最低利率 或 净值参考     %转换为小数表述
# rate_max:                 最高利率 或 净值参考     %转换为小数表述
# rate_netvalue:            如果是净值型，且大于0.2，则将rate_min的值记录在这里， rate_min和rate_max都设置为None


# redeem_type:              封闭式、开放式，         即赎回规则
# fixed_type:               固定收益、浮动收益       如rate_type为净值型，则默认 浮动收益
# promise_type:             保本、非保本            如rate_type为净值型，则默认 非保本
# raise_type:               公募、私募              如未找到私募，则默认为公募

# date_open:                发行起始日期
# date_close:               发行到期日期
# date_start:               产品起息日期
# date_end:                 产品结束日期
# term:                     期限                          单位（天）
# term_looped:              YES, NO        投资周期顺延 自动再投资

# amount_size_min:          产品规模最小    单位(元)
# amount_size_max:          产品规模最大    单位(元)
# amount_buy_min:           起购金额        单位(元)
# amount_buy_max:           购买上限        单位(元)
# amount_per_buy            每份购买金额    单位(元)

# custodian:                托管机构
# fee_types:                托管费、申购费、赎回费、管理费、销售费等
# fee_rate:                 费用数量  加总        %转换为小数表述

# sale_areas:               销售区域  全国、上海、北京、江苏等
# sale_ways:                购买方式  手机、柜面等
# sale_agents:              代销机构
# sale_clients:             销售客群

# invest_on:                产品投资范围
# loan_rule:                融资服务， 如理财质押贷款

# manual_url:               产品说明书链接
# manual_download:          产品说明书下载状态
# manual_html:              产品说明书网页版、简要版
# notice_issue_url:         公告发布链接
# notice_start_url:         公告成立链接
# notice_end_url            公告终止连接
# memo:                     备忘录


# test为一个实例化的类
# 获取类中全部的自定义方法，不包含@property和@setter注释的方法, 注意：callable()方法里面的参数是类方法，而不是str
# b = set(filter(lambda m: callable(getattr(test, m)) and not m.startswith('__'), dir(test)))

# 获取类中全部的属性和方法，不包含'__'、'_', 'pattern'开头的方法
# b = [a for a in dir(test) if not (a.startswith('__') or a.startswith('_') or a.startswith('pattern'))]

import time
import farmhash
from constants.bank_dict import BankDict


class WealthOutline(object):

    list_bank_level = BankDict.list_bank_level

    def __init__(
        self,
        referencable: str,
        bank_name: str,
        code: str,
        name: str = None,
        code_register: str = None,
        currency: str = None,
        risk: int = None,
        rate_type: str = None,
        rate_max: float = None,
        rate_min: float = None,
        rate_netvalue: str = None,
        redeem_type: str = None,
        fixed_type: str = None,
        promise_type: str = None,
        raise_type: str = None,
        date_open: str = None,
        date_close: str = None,
        date_start: str = None,
        date_end: str = None,
        term: int = None,
        term_looped: str = None,
        amount_size_min: int = None,
        amount_size_max: int = None,
        amount_buy_min: int = None,
        amount_buy_max: int = None,
        amount_per_buy: int = None,
        custodian: str = None,
        fee_types: str = None,
        fee_rate: float = None,
        sale_areas: str = None,
        sale_ways: str = None,
        sale_agents: str = None,
        sale_clients: str = None,
        invest_on: str = None,
        loan_rule: str = None,
        manual_url: str = None,
        manual_download: str = 'undo',
        manual_download_fail: int = 0,
        manual_html: str = None,
        notice_issue_url: str = None,
        notice_start_url: str = None,
        notice_end_url: str = None,
        memo: str = None,
        status: str = 'undo',
    ):
        self._referencable = referencable
        self._bank_name = bank_name
        self._bank_level = self.list_bank_level[bank_name]
        self._code = code
        ukey = bank_name + '=' + code
        self._ukey = ukey
        self._ukeyhash = str(farmhash.hash64(ukey))

        self._name = name
        self._code_register = code_register
        self._currency = currency
        self._risk = risk
        self._rate_type = rate_type
        self._rate_max = rate_max
        self._rate_min = rate_min
        self._rate_netvalue = rate_netvalue
        self._redeem_type = redeem_type
        self._fixed_type = fixed_type
        self._promise_type = promise_type
        self._raise_type = raise_type
        self._date_open = date_open
        self._date_close = date_close
        self._date_start = date_start
        self._date_end = date_end
        self._term = term
        self._term_looped = term_looped
        self._amount_size_min = amount_size_min
        self._amount_size_max = amount_size_max
        self._amount_buy_min = amount_buy_min
        self._amount_buy_max = amount_buy_max
        self._amount_per_buy = amount_per_buy
        self._custodian = custodian
        self._fee_types = fee_types
        self._fee_rate = fee_rate
        self._sale_areas = sale_areas
        self._sale_ways = sale_ways
        self._sale_agents = sale_agents
        self._sale_clients = sale_clients
        self._invest_on = invest_on
        self._loan_rule = loan_rule

        self._manual_url = manual_url
        self._manual_download = manual_download
        self._manual_download_fail = manual_download_fail
        self._manual_html = manual_html
        self._notice_issue_url = notice_issue_url
        self._notice_start_url = notice_start_url
        self._notice_end_url = notice_end_url
        self._memo = memo
        self._status = status

    def __repr__(self):
        return f"[{self._bank_name}] Wealth ukeyhash: {self._ukeyhash}, " \
               f"name: {self._name}, bank_level: {self._bank_level}, code: {self._code}, code_register: {self._code_register}, currency: {self._currency}, risk: {self._risk}, " \
               f"rate_type: {self._rate_type}, rate_max: {self._rate_max}, rate_min: {self._rate_min}, rate_netvalue: {self._rate_netvalue}, " \
               f"raise_type: {self._raise_type}, fixed_type: {self._fixed_type}, promise_type: {self._promise_type}, " \
               f"redeem_type: {self._redeem_type}, " \
               f"date_open: {self._date_open}, date_close: {self._date_close}, date_start: {self._date_start}, date_end: {self._date_end}, term: {self._term}, term_looped: {self._term_looped}, " \
               f"amount_size_max: {self._amount_size_max}, amount_size_min: {self._amount_size_min}, amount_buy_min: {self._amount_buy_min}, " \
               f"amount_buy_max: {self._amount_buy_max}, amount_per_buy: {self._amount_per_buy}, " \
               f"fee_types: {self._fee_types}, fee_rate: {self._fee_rate}, custodian: {self._custodian}, " \
               f"sale_areas: {self._sale_areas}, sale_ways: {self._sale_ways}, sale_agents: {self._sale_agents}, sale_clients: {self._sale_clients}, " \
               f"loan_rule: {self._loan_rule}, invest_on: {self._invest_on}, manual_url: {self._manual_url}]"

    def do_dump(self):
        elements = [one for one in dir(self) if not (one.startswith('__') or one.startswith('_') or one.startswith('do_') or one.startswith('list_'))]
        data = {}
        for name in elements:
            value = getattr(self, name, None)
            data[name] = value
        # 为了保存进mongodb，增加_id，设置其值为ukey, 并添加保存时间
        data['_id'] = self.ukey
        data['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
        # 为下载PDF产品说明书，初始化设置manual_download_fail次数为0次
        data['manual_download_fail'] = 0
        return data

    @classmethod
    def do_load(cls, data: dict):
        outline = cls(referencable=data['referencable'], bank_name=data['bank_name'], code=data['code'])
        elements = [one for one in dir(cls) if not (one.startswith('__') or one.startswith('_') or one.startswith('do_') or one.startswith('list_'))]
        # print('elements有：', elements)
        elements.remove('referencable')
        elements.remove('bank_name')
        elements.remove('code')
        # print('准备载入的数据是：', data)
        for one in elements:
            if one in data.keys():
                setattr(outline, one, data[one])
        return outline

    @property
    def referencable(self):
        return self._referencable

    @referencable.setter
    def referencable(self, value):
        self._referencable = value

    @property
    def ukey(self):
        return self._ukey

    @ukey.setter
    def ukey(self, value):
        self._ukey = value

    @property
    def ukeyhash(self):
        return self._ukeyhash

    @ukeyhash.setter
    def ukeyhash(self, value):
        self._ukeyhash = value

    @property
    def bank_level(self):
        return self._bank_level

    @bank_level.setter
    def bank_level(self, value):
        self._bank_level = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def bank_name(self):
        return self._bank_name

    @bank_name.setter
    def bank_name(self, value):
        self._bank_name = value

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def code_register(self):
        return self._code_register

    @code_register.setter
    def code_register(self, value):
        self._code_register = value

    @property
    def raise_type(self):
        return self._raise_type

    @raise_type.setter
    def raise_type(self, value):
        self._raise_type = value

    @property
    def redeem_type(self):
        return self._redeem_type

    @redeem_type.setter
    def redeem_type(self, value):
        self._redeem_type = value

    @property
    def fixed_type(self):
        return self._fixed_type

    @fixed_type.setter
    def fixed_type(self, value):
        self._fixed_type = value

    @property
    def promise_type(self):
        return self._promise_type

    @promise_type.setter
    def promise_type(self, value):
        self._promise_type = value

    @property
    def invest_on(self):
        return self._invest_on

    @invest_on.setter
    def invest_on(self, value):
        self._invest_on = value

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, value):
        self._currency = value

    @property
    def risk(self):
        return self._risk

    @risk.setter
    def risk(self, value):
        self._risk = value

    @property
    def date_open(self):
        return self._date_open

    @date_open.setter
    def date_open(self, value):
        self._date_open = value

    @property
    def date_close(self):
        return self._date_close

    @date_close.setter
    def date_close(self, value):
        self._date_close = value

    @property
    def date_start(self):
        return self._date_start

    @date_start.setter
    def date_start(self, value):
        self._date_start = value

    @property
    def date_end(self):
        return self._date_end

    @date_end.setter
    def date_end(self, value):
        self._date_end = value

    @property
    def term(self):
        return self._term

    @term.setter
    def term(self, value):
        self._term = value

    @property
    def term_looped(self):
        return self._term_looped

    @term_looped.setter
    def term_looped(self, value):
        self._term_looped = value

    @property
    def rate_type(self):
        return self._rate_type

    @rate_type.setter
    def rate_type(self, value):
        self._rate_type = value

    @property
    def rate_max(self):
        return self._rate_max

    @rate_max.setter
    def rate_max(self, value):
        self._rate_max = value

    @property
    def rate_min(self):
        return self._rate_min

    @rate_min.setter
    def rate_min(self, value):
        self._rate_min = value

    @property
    def rate_netvalue(self):
        return self._rate_netvalue

    @rate_netvalue.setter
    def rate_netvalue(self, value):
        self._rate_netvalue = value

    @property
    def amount_size_min(self):
        return self._amount_size_min

    @amount_size_min.setter
    def amount_size_min(self, value):
        self._amount_size_min = value

    @property
    def amount_size_max(self):
        return self._amount_size_max

    @amount_size_max.setter
    def amount_size_max(self, value):
        self._amount_size_max = value

    @property
    def amount_buy_min(self):
        return self._amount_buy_min

    @amount_buy_min.setter
    def amount_buy_min(self, value):
        self._amount_buy_min = value

    @property
    def amount_buy_max(self):
        return self._amount_buy_max

    @amount_buy_max.setter
    def amount_buy_max(self, value):
        self._amount_buy_max = value

    @property
    def amount_per_buy(self):
        return self._amount_per_buy

    @amount_per_buy.setter
    def amount_per_buy(self, value):
        self._amount_per_buy = value

    @property
    def custodian(self):
        return self._custodian

    @custodian.setter
    def custodian(self, value):
        self._custodian = value

    @property
    def fee_types(self):
        return self._fee_types

    @fee_types.setter
    def fee_types(self, value):
        self._fee_types = value

    @property
    def fee_rate(self):
        return self._fee_rate

    @fee_rate.setter
    def fee_rate(self, value):
        self._fee_rate = value

    @property
    def sale_areas(self):
        return self._sale_areas

    @sale_areas.setter
    def sale_areas(self, value):
        self._sale_areas = value

    @property
    def sale_ways(self):
        return self._sale_ways

    @sale_ways.setter
    def sale_ways(self, value):
        self._sale_ways = value

    @property
    def sale_agents(self):
        return self._sale_agents

    @sale_agents.setter
    def sale_agents(self, value):
        self._sale_agents = value

    @property
    def sale_clients(self):
        return self._sale_clients

    @sale_clients.setter
    def sale_clients(self, value):
        self._sale_clients = value

    @property
    def loan_rule(self):
        return self._loan_rule

    @loan_rule.setter
    def loan_rule(self, value):
        self._loan_rule = value


    @property
    def manual_url(self):
        return self._manual_url

    @manual_url.setter
    def manual_url(self, value):
        self._manual_url = value

    @property
    def manual_download(self):
        return self._manual_download

    @manual_download.setter
    def manual_download(self, value):
        self._manual_download = value

    @property
    def manual_download_fail(self):
        return self._manual_download_fail

    @manual_download_fail.setter
    def manual_download_fail(self, value):
        self._manual_download_fail = value

    @property
    def manual_html(self):
        return self._manual_html

    @manual_html.setter
    def manual_html(self, value):
        self._manual_html = value

    @property
    def notice_issue_url(self):
        return self._notice_issue_url

    @notice_issue_url.setter
    def notice_issue_url(self, value):
        self._notice_issue_url = value

    @property
    def notice_start_url(self):
        return self._notice_start_url

    @notice_start_url.setter
    def notice_start_url(self, value):
        self._notice_start_url = value

    @property
    def notice_end_url(self):
        return self._notice_end_url

    @notice_end_url.setter
    def notice_end_url(self, value):
        self._notice_end_url = value

    @property
    def memo(self):
        return self._memo

    @memo.setter
    def memo(self, value):
        self._memo = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value