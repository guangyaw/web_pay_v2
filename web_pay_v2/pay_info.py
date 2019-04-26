# coding=UTF-8
import base64
# import datetime
import hashlib
import json
import random
# import requests
import string
import time
from Crypto.Cipher import AES
from django.http import HttpResponse
# from bottle import route, run, template
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt

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

# pay_information/?store=MS36057042&user_email=xyaw@pchome.com.tw&amount=101&paperno=paper1001&lang=en&itemscript=testitem001
# /pay_information/?user_email=xyaw@pchome.com.tw&amount=101&paperno=paper1001&lang=zh-TW
# /pay_information/?user_email=xyaw@pchome.com.tw&amount=101&paperno=paper1001&lang=en


def payinfor(request):
    if request.method == 'GET':
        user_email = str(request.GET['user_email'])
        amount = str(request.GET['amount'])
        paperno = str(request.GET['paperno'])
        language_flag = str(request.GET['lang'])
        store_id = str(request.GET['store'])
        itemscript = str(request.GET['itemscript'])

    hkey = 'Kj4PiW6Mkte2bEtvFW5ctWnqScxRg8vk'
    iv = 'cWOUpDXX06a2eCBm'

    version_data = '1.5'
    merchantid_data = store_id
    weburl = request.get_host()

    if not amount:
        amount = str(10)
    if not user_email:
        user_email = 'xyaw@pchome.com.tw'
    if not paperno:
        paperno='test0001'

    i = time.strftime("%Y/%m/%d")+time.strftime("%H:%M:%S")
    now_data = str(i)

    j = str(time.strftime("%Y%m%d"))
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 7))
    order_no = j + salt

    mydata = "MerchantID="+merchantid_data+"&" \
        "RespondType=JSON&" \
        "TimeStamp="+now_data+"&" \
        "Version=1.5&" \
        "MerchantOrderNo="+order_no+"&" \
        "Amt="+amount+"&" \
        "ItemDesc="+itemscript+"&" \
        "ReturnURL=http://"+weburl+"/return&" \
        "NotifyURL=http://"+weburl+"/notify&" \
        "ClientBackURL=http://"+weburl+"/cancelback&" \
        "Email="+user_email+"&" \
        "EmailModify=0&" \
        "OrderComment="+paperno+"&" \
        "CREDIT=1&" \
        "LangType="+language_flag



    tradeInfo_data = encrypt(mydata)
    #tradeInfo_data='BD0449E9EE5CD8DB6224FEB7C7C853D6BEE1C9889933B099E38343E9E634E241068AB2A0C9741D146BA644675239FA5C3C3CC61EE2121821E635CFDBFFDE88DAC988D7C2F195FF40EFD4CA3B4B1256762C81F3F817185096FD5E89029BC5647E162FA9E422176BBA4221179DF154DA7EC2C4798465C83C9CC7E1A2EEB5591A9970A972691C8EF045A52052766C5DEF3280177A4745E171AA09BC9596539A2BCFF3FC1B85017EEB8044F079BAB4602E1A51B7FC2C247DDF654065F82482A8D17B52BE6FB9C1CE2C93030F83B2351573B390EF87B1889C731AD4550F157EC3BBD8E63F23513042D02B2B6A3868CA00C1DC3C44CAC6F6D4EA58DD9A2FBEB64C6B1F245DEF1E00E5D7D26712B034178A57049633A0343F296E9E30E2A1936F614218B92BA66F6397D45E113ABE2EF7D9A81B8B9F780130C2DDBC641F8F002BC78D5B724A4029C879FF27864930ECDA1C9D17EA7A9EC6B275935F2F825EA12BDB65158466AEB2AEBAE7C752F80F8B685DC260947E9D441874BEFF6407428F3304742F'
    # mydata = decrypt(emydata)
    # return HttpResponse(tradeInfo_data)
    data_sha256 = "HashKey="+hkey+"&"+tradeInfo_data+"&HashIV="+iv

    sha256 = hashlib.sha256()
    sha256.update(data_sha256.encode('utf-8'))
    res = sha256.hexdigest()
    tradesha_data = res.upper()

    return render(request, 'confirm.html', locals())


@csrf_exempt
def returnurl(request):
    return HttpResponse(request.POST['Status'])


def cancelbackurl(request):
    return HttpResponse('cancelback')


