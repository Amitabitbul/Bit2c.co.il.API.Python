from Bit2cClient import *

client = Bit2cClient("https://www.bit2c.co.il/" , "your-api-key","your.api.secret")

#balance = client.Balance()

#Trades = client.GetTrades(PairType.BtcNis)

#ticker = client.GetTicker()

#orderBook = client.GetOrderBook()

''' OrderData Example
data = OrderData()
data.Amount = 1
data.IsBid = False
data.Pair = PairType.BtcNis
data.Price = 3500.000
data.Total = 3500.000

orderRespose = client.AddOrder(data)
'''

''' MyOrders Example
myOrders = client.MyOrders(PairType.BtcNis)
'''

''' Clear All Bids and Asks
client.ClearMyOrders(PairType.BtcNis)

''' 

''' Account History Example
    !important, the datetime must be in iso8601 format to make it work - example : yyyy-MM-dd'T'HH:mm:ss.SSS'Z
fromDate = "2013-11-08T07:04:06.666Z"
toDate = "2014-01-08T07:04:06.666Z"
accountHistory = client.AccountHistory(fromDate, toDate)
'''

''' Create Checkout Example 
checkoutLM = CheckoutLinkModel()
checkoutLM.CoinType = CoinType.NIS
checkoutLM.Description = "blablabla"
checkoutLM.NotifyByEmail = True
checkoutLM.Price = 1
checkoutLM.CancelURL = ""
checkoutLM.ReturnURL = ""

checkoutRes = client.CreateCheckout(checkoutLM)
'''