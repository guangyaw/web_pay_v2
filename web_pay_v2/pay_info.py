# coding=UTF-8
import base64
import hashlib
import requests
from Crypto.Cipher import AES
from django.http import HttpResponse
# from bottle import route, run, template

# testcard   4000-2211-1111-1111


BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]

def encrypt(message):
    hkey = 'Kj4PiW6Mkte2bEtvFW5ctWnqScxRg8vk'
    iv = 'cWOUpDXX06a2eCBm'
    message = pad(message)
    aes = AES.new(hkey, AES.MODE_CBC, iv)
    return base64.b16encode(aes.encrypt(message))


def decrypt(encrypted):
    hkey = 'Kj4PiW6Mkte2bEtvFW5ctWnqScxRg8vk'
    iv = 'cWOUpDXX06a2eCBm'
    encrypted = base64.b16decode(encrypted)
    aes = AES.new(hkey, AES.MODE_CBC, iv)
    return unpad(aes.decrypt(encrypted[16:]))


def payinfor(request):
    hkey = 'Kj4PiW6Mkte2bEtvFW5ctWnqScxRg8vk'
    iv = 'cWOUpDXX06a2eCBm'
    mydata = "MerchantID=MS36057042&" \
        "RespondType=JSON&" \
        "TimeStamp='201904251441'&" \
        "Version=1.5&" \
        "MerchantOrderNo=order001&" \
        "Amt=10&" \
        "ItemDesc='商品資訊(自行修改)'&" \
        "ReturnURL=http://140.134.51.49/return&" \
        "NotifyURL=http://140.134.51.49/notify&" \
        "ClientBackURL=http://140.134.51.49/cancelback&" \
        "Email=xyaw@pchome.com.tw&" \
        "EmailModify=0&" \
        "OrderComment= '論文編號001'&" \
        "CREDIT=1&" \
        "LangType=en"



    tradeInfo_data = encrypt(mydata)
    #tradeInfo_data='BD0449E9EE5CD8DB6224FEB7C7C853D6BEE1C9889933B099E38343E9E634E241068AB2A0C9741D146BA644675239FA5C3C3CC61EE2121821E635CFDBFFDE88DAC988D7C2F195FF40EFD4CA3B4B1256762C81F3F817185096FD5E89029BC5647E162FA9E422176BBA4221179DF154DA7EC2C4798465C83C9CC7E1A2EEB5591A9970A972691C8EF045A52052766C5DEF3280177A4745E171AA09BC9596539A2BCFF3FC1B85017EEB8044F079BAB4602E1A51B7FC2C247DDF654065F82482A8D17B52BE6FB9C1CE2C93030F83B2351573B390EF87B1889C731AD4550F157EC3BBD8E63F23513042D02B2B6A3868CA00C1DC3C44CAC6F6D4EA58DD9A2FBEB64C6B1F245DEF1E00E5D7D26712B034178A57049633A0343F296E9E30E2A1936F614218B92BA66F6397D45E113ABE2EF7D9A81B8B9F780130C2DDBC641F8F002BC78D5B724A4029C879FF27864930ECDA1C9D17EA7A9EC6B275935F2F825EA12BDB65158466AEB2AEBAE7C752F80F8B685DC260947E9D441874BEFF6407428F3304742F'
    # mydata = decrypt(emydata)
    # return HttpResponse(tradeInfo_data)
    data_sha256 = "HashKey="+hkey+"&"+tradeInfo_data+"&HashIV="+iv

    sha256 = hashlib.sha256()
    sha256.update(data_sha256.encode('utf-8'))
    res = sha256.hexdigest()
    tradesha_data = res.upper()

    transfer_data = {
        'MerchantID': 'MS36057042',
        'TradeInfo': tradeInfo_data,
        'TradeSha': tradesha_data,
        'Version': 1.5
    }

    r = requests.post('https://ccore.newebpay.com/MPG/mpg_gateway', data=transfer_data)
    return HttpResponse(r.text)


def returnurl(request):
    return HttpResponse('return')


def notifyurl(request):
    return HttpResponse('notifyurl')


def cancelbackurl(request):
    return HttpResponse('cancelback')


