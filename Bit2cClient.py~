import time
import json
import hmac
import hashlib
import pycurl
import cStringIO
from datetime import datetime

from Balance import *
from AccountAction import *
from ExchangesTrade import *
from Ticker import *
from OrderBook  import *
from AccountRaw import *
from AddOrderResponse import *
from OrderStatusType import *
from PairType import *
from CoinType import *
from Orders import *
from od import *
from OrderData import *
from CheckoutLinkModel import *
from CheckoutResponse import *

class Bit2cClient:
    
    def __init__(self,Url, Key, Secret):
        self.Key = Key
        self.Secret = Secret
        self.nonce = int(time.time())
        self.Url = Url

    def ComputeHash(self, message):
        return hmac.new(self.Secret.upper() , message , hashlib.sha512).digest().encode("base64").replace("\n","")

    def Query(self, qString, url, sign):
        buf = cStringIO.StringIO()

        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        curl.setopt(pycurl.WRITEFUNCTION, buf.write)
        curl.setopt(pycurl.POSTFIELDS, qString)
        curl.setopt(pycurl.HTTPHEADER, ['Key:'+self.Key,
                                    'Sign:'+(sign)])
        curl.perform()
        res = buf.getvalue()
        buf.close()

        return res
        

    def Balance(self):
        qString = "nonce=" + str(self.nonce)
        sign = self.ComputeHash(qString)
        url = self.Url + "Account/Balance"
        response = self.Query(qString, url, sign)
        _json = json.loads(response)
        return Balance(_json['BalanceNIS'], _json['BalanceLTC'], _json['BalanceBTC'])

    def DownloadString(self, url):
        buf = cStringIO.StringIO()
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        curl.setopt(pycurl.WRITEFUNCTION, buf.write)

        curl.perform()
        res = buf.getvalue()
        buf.close()
        return res

    def GetTrades(self, Pair, since = 0, date = 0):
        url = self.Url+ "Exchanges/" + str(Pair) + "/trades.json"
        response = self.DownloadString(url)
        _json = json.loads(response)
        ExchangesTrades = []
        for jsonObj in _json:
            exTrade = ExchangesTrade(jsonObj['date'], jsonObj['price'], jsonObj['amount'], jsonObj['tid'])
            ExchangesTrades.append(exTrade)
        return ExchangesTrades

    def GetTicker(self, Pair = PairType.BtcNis):
        url = self.Url + "Exchanges/" + str(Pair) + "/Ticker.json"
        response = self.DownloadString(url)
        _json = json.loads(response)
        return Ticker(_json['h'], _json['l'], _json['ll'], _json['a'], _json['av'])

    def GetOrderBook(self, Pair = PairType.BtcNis):
        url = self.Url + "Exchanges/" + str(Pair) + "/orderbook.json"
        response = self.DownloadString(url)
        _json = json.loads(response)
        orderBook = OrderBook()

        jsonAsks = _json['asks']
        jsonBids = _json['bids']

        for ask in jsonAsks:
            orderBook.asks.append(ask)

        for bid in jsonBids:
            orderBook.bids.append(bid)

        return orderBook

    def AddOrder(self, data):
        qString = "Amount=" + str(data.Amount) + "&Price=" + str(data.Price) + "&Total=" + str(data.Total) + "&IsBid=" + str(data.IsBid) + "&Pair=" + str(data.Pair) + "&nonce=" + (str(int(time.time())))
        sign = self.ComputeHash(qString)
        url = self.Url + "Order/AddOrder"
        response = self.Query(qString, url, sign)
        _json = json.loads(response)
        orderResponse = OrderResponse()

        orderResponse.HasError = bool(_json['OrderResponse']['HasError'])
        orderResponse.Error = _json['OrderResponse']['Error']

        newOrder = od()

        newOrder.a = _json['NewOrder']['a']
        newOrder.aa = _json['NewOrder']['aa']
        newOrder.d = _json['NewOrder']['d']
        newOrder.id = _json['NewOrder']['id']
        newOrder.p = _json['NewOrder']['p']
        newOrder.p1 = _json['NewOrder']['p1']
        newOrder.s = _json['NewOrder']['s']
        newOrder.t = _json['NewOrder']['t']

        addOrder = AddOrderResponse()

        addOrder.NewOrder = newOrder
        addOrder.OrderResponse = orderResponse
        return addOrder
    
    def MyOrders(self, Pair):
        qString = "pair=" + str(Pair) + "&nonce=" + (str(int(time.time())))
        sign = self.ComputeHash(qString)
        url = self.Url + "Order/MyOrders"
        response = self.Query(qString, url, sign)
        _json = json.loads(response)
        orders = Orders()
        if 'bids' in _json:
            for bid in _json['bids']:
                tOrder = TradeOrder()
                tOrder.a = bid['a']
                tOrder.d = bid['d']
                tOrder.id = bid['id']
                tOrder.isBid = bid['isBid']
                tOrder.p = bid['p']
                tOrder.pair = bid['pair']
                tOrder.s = bid['s']

                orders.bids.append(tOrder)

            for ask in _json['asks']:
                tOrder = TradeOrder()
                tOrder.a = ask['a']
                tOrder.d = ask['d']
                tOrder.id = ask['id']
                tOrder.isBid = ask['isBid']
                tOrder.p = ask['p']
                tOrder.pair = ask['pair']
                tOrder.s = ask['s']

                orders.asks.append(tOrder)

        return orders

    def CancelOrder(self, id):
        qString = "id=" + str(id) + "&nonce=" + (str(int(time.time())))
        sign = self.ComputeHash(qString)
        url = self.Url + "Order/CancelOrder"
        response = self.Query(qString, url, sign)

    def ClearMyOrders(self, Pair):
        myOrders = self.MyOrders(Pair)
        for bid in myOrders.bids:
            if Pair is bid.pair:
                self.CancelOrder(bid.id)

        for ask in myOrders.asks:
            if Pair is ask.pair:
                self.CancelOrder(ask.id)      
                
    def AccountHistory(self,  fromTime, toTime):
        qString = "fromTime=" + fromTime + "&toTime=" + toTime + "&nonce=" + (str(int(time.time())))
        sign = self.ComputeHash(qString)
        url = self.Url + "Order/AccountHistory"
        response = self.Query(qString, url, sign)
        _json = json.loads(response)
        accountRaws = []
        for raw in _json:
            accountRaw = AccountRaw()
            accountRaw.BalanceBTC = raw['BalanceBTC']
            accountRaw.BalanceLTC = raw['BalanceLTC']
            accountRaw.BalanceNIS = raw['BalanceNIS']
            accountRaw.Created = raw['Created']
            accountRaw.Fee = raw['Fee']
            accountRaw.FeeInNIS = raw['FeeInNIS']
            accountRaw.id = raw['id']
            accountRaw.OrderCreated = raw['OrderCreated']
            accountRaw.PricePerCoin = raw['PricePerCoin']
            accountRaw.Ref = raw['Ref']
            accountRaw.TypeId = raw['TypeId']
            accountRaws.append(accountRaw)

        return accountRaws

    def CreateCheckout(self, data):
        qString = "Price=" + str(data.Price) + "&Description=" + str(data.Description) + "&CoinType=" + str(data.CoinType) + "&ReturnURL=" + str(data.ReturnURL) + "&CancelURL=" + str(data.CancelURL) + "&NotifyByEmail=" + str(data.NotifyByEmail) + "&nonce=" + (str(int(time.time())))
        sign = self.ComputeHash(qString)
        url = self.Url + "Merchant/CreateCheckout"
        response = self.Query(qString, url, sign)
        checkoutResponse = CheckoutResponse()
        _json = json.loads(response)
        if 'error' in _json:
            checkoutResponse.Error = _json['error']
        if 'id' in _json:
            checkoutResponse.id = _json['id']

        return checkoutResponse











