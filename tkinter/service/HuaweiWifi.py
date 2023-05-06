import requests
import urllib.request
import xml.etree.ElementTree as ET
import random
import time
import hashlib
import hmac
import re

wifiURL = "http://192.168.8.1"
# wifiURL = "http://127.0.0.1:8000"

plmnURL = wifiURL + "/api/net/current-plmn"
tokenURL = wifiURL + "/api/webserver/token"
preLoginURL = wifiURL + "/api/user/challenge_login"
loginURL = wifiURL + "/api/user/authentication_login"
mainContentURL = wifiURL + "/html/content.html"
resetURL = wifiURL + "/api/device/control"

cookie = None
token = None
salt = None
iterations = -1
servernonce = None
firstNonce = None

def checkHuaWeiWIFIConnection():
    try:
        plmnResponse = requests.get(plmnURL)
        return plmnResponse.text.find('<FullName></FullName>') == -1
    except:
        return False

def getHuaWeiWIFIToken():
    global cookie, token
    if cookie == None:
        tokenResponse = requests.get(
            tokenURL, headers={"_ResponseSource": "Broswer"})
    else:
        tokenResponse = requests.get(
            tokenURL, headers={"_ResponseSource": "Broswer", "Cookie": cookie})
    tokenResponseXML = ET.fromstring(tokenResponse.text)
    tokenXML = tokenResponseXML.find('token')
    resToken = ""
    if tokenXML != None:
        resToken = str(tokenXML.text)
    token = resToken[-32:]
    if tokenResponse.headers.get('Set-Cookie') != None:
        cookie = tokenResponse.headers['Set-Cookie'].split(';')[0]
    if cookie!=None and token!=None:
        return True
    else:
        return False

def createXML(data):
    xmlStr = '<?xml version="1.0" encoding="UTF-8"?>'
    xmlStr += '<request>'
    for key in data:
        value = data[key]
        xmlStr += "<"+str(key)+">"
        xmlStr += str(value)
        xmlStr += "</"+str(key)+">"
    xmlStr += '</request>'
    return xmlStr.encode()

def randomString(randomLen):
    randomString = ""
    for i in range(randomLen):
        randomValue = int(random.random()*0xff)
        if randomValue<0xf:
            randomString += "0"
            randomString += hex(randomValue)[2:]
        else:
            randomString += hex(randomValue)[2:]
    return randomString


def hexStringToBytes(hexStr):
    hexStr = hexStr.encode()
    hexStrLen = int((len(hexStr)+1)/2)
    hexList = []
    for i in range(hexStrLen):
        value = 0
        if hexStr[i*2] >= 0x30 and hexStr[i*2] <= 0x39:
            value = (hexStr[i*2] - 0x30)<<4
        elif hexStr[i*2] >= 0x61 and hexStr[i*2] <= 0x66:
            value = (hexStr[i*2] - 0x61+10)<<4
        elif hexStr[i*2] >= 0x41 and hexStr[i*2] <= 0x46:
            value = (hexStr[i*2] - 0x41+10)<<4
        if hexStr[i*2+1] >= 0x30 and hexStr[i*2+1] <= 0x39:
            value += (hexStr[i*2+1] - 0x30)
        elif hexStr[i*2+1] >= 0x61 and hexStr[i*2+1] <= 0x66:
            value += (hexStr[i*2+1] - 0x61+10)
        elif hexStr[i*2+1] >= 0x41 and hexStr[i*2+1] <= 0x46:
            value += (hexStr[i*2+1] - 0x41+10)
        hexList.append(value)
    return bytes(hexList)

def resetLogin():
    global cookie,token,salt,iterations,servernonce,firstNonce
    cookie = None
    token = None
    salt = None
    iterations = -1
    servernonce = None
    firstNonce = None

def preLoginHuaWeiWIFI():
    global cookie,token,salt,iterations,servernonce,firstNonce
    preLoginHeaders = {
        "Connection": 'keep-alive',
        "Pragma": 'no-cache',
        "Cache-Control": 'no-cache',
        "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        "sec-ch-ua-mobile": '?0',
        "_ResponseSource": 'Broswer',
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        "Content-Type": 'application/x-www-form-urlencoded; charset=UTF-8;',
        "Accept": '*/*',
        "X-Requested-With": 'XMLHttpRequest',
        "__RequestVerificationToken": token,
        "sec-ch-ua-platform": '"Windows"',
        "Origin": wifiURL,
        "Sec-Fetch-Site": 'same-origin',
        "Sec-Fetch-Mode": 'cors',
        "Sec-Fetch-Dest": 'empty',
        "Referer": wifiURL+'/html/index.html',
        "Accept-Encoding": 'gzip, deflate, br',
        "Accept-Language": 'en-US,en;q=0.9,zh;q=0.8,zh-CN;q=0.7,de;q=0.6'
    }
    username = "admin"
    firstNonce = randomString(32)
    preLoginData = {
        "username": username,
        "firstnonce": firstNonce,
        "mode": 1
    }
    preLoginRequest = urllib.request.Request(preLoginURL, createXML(preLoginData))
    for key in preLoginHeaders:
        preLoginRequest.add_header(str(key), str(preLoginHeaders[key]))
    if cookie != None:
        preLoginRequest.add_header("Cookie", cookie)
    preLoginResponse = urllib.request.urlopen(preLoginRequest)
    token = preLoginResponse.getheader('__RequestVerificationToken')
    preLoginXML = ET.fromstring(preLoginResponse.read())
    saltXML = preLoginXML.find('salt')
    if saltXML != None:
        salt = str(saltXML.text)
    iterationsXML = preLoginXML.find('iterations')
    if iterationsXML != None:
        iterations = int(str(iterationsXML.text))
    servernonceXML = preLoginXML.find('servernonce')
    if servernonceXML != None:
        servernonce = str(servernonceXML.text)
    if salt != None and servernonce != None and salt != None and token != None and cookie != None and firstNonce != None and iterations != -1:
        return True
    else:
        return False

def loginHuaWeiWIFI(password = "12345678"):
    global firstNonce,servernonce,iterations,cookie,token
    passwordHashedValue = hashlib.pbkdf2_hmac('sha256', password.encode(), hexStringToBytes(salt), iterations)
    hmacClientKey = hmac.new(b'Client Key', digestmod=hashlib.sha256)
    hmacClientKey.update(passwordHashedValue)
    reHashClientKey = hashlib.sha256(hmacClientKey.digest())
    authMessage = str(firstNonce) + ',' + str(servernonce) + ',' + str(servernonce)
    hmacAuthMessage = hmac.new(authMessage.encode(), digestmod=hashlib.sha256)
    hmacAuthMessage.update(reHashClientKey.digest())
    hmacAuthMessage.hexdigest()
    hmacAuthMessageBytes = hmacAuthMessage.digest()
    hmacClientKeyBytes = hmacClientKey.digest()
    AuthMessageAndClientKeyBytes = []
    for i in range(len(hmacAuthMessageBytes)):
        AuthMessageAndClientKeyBytes.append(hmacClientKeyBytes[i] ^ hmacAuthMessageBytes[i])
    clientProof = bytearray(AuthMessageAndClientKeyBytes).hex()
    finalPostData = {
        "clientproof": clientProof,
        "finalnonce": servernonce
    }
    loginHeaders = {
        "Pragma": 'no-cache',
        "Cache-Control": 'no-cache',
        "Accept": '*/*',
        "X-Requested-With": 'XMLHttpRequest',
        "_ResponseSource": 'Broswer',
        "__RequestVerificationToken": token,
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        "Content-Type": 'application/x-www-form-urlencoded; charset=UTF-8;',
        "Origin": wifiURL,
        "Referer": wifiURL+'/html/index.html',
        "Accept-Encoding": 'gzip, deflate',
        "Accept-Language": 'en-US,en;q=0.9,zh;q=0.8,zh-CN;q=0.7,de;q=0.6',
        "Cookie":cookie
    }
    loginRequest = urllib.request.Request(loginURL, createXML(finalPostData))
    for key in loginHeaders:
        loginRequest.add_header(str(key), str(loginHeaders[key]))
    loginResponse = urllib.request.urlopen(loginRequest)
    loginContent = loginResponse.read()
    loginXML = ET.fromstring(loginContent)
    if loginResponse.getheader('Set-Cookie') != None:
        cookie = loginResponse.getheader('Set-Cookie').split(';')[0]
        return True
    else:
        return False

def getHuaWeiWIFIMainContent():
    global token, cookie
    if cookie == None:
        mainContentResponse = requests.get(
            mainContentURL, headers={"_ResponseSource": "Broswer"})
    else:
        mainContentResponse = requests.get(
            mainContentURL, headers={"_ResponseSource": "Broswer", "Cookie": cookie})
    contentTokenList = re.findall(
        r'<meta\s+name="csrf_token"\s+content="[\w]+"', mainContentResponse.text)
    if len(contentTokenList) > 0:
        token = contentTokenList[0].split('content="')[1][0:-1]
        if token != None:
            return True
    return False

def resetControlHuaWeiWIFI():
    global token,cookie
    resetHeaders = {
        "__RequestVerificationToken": token,
        "_ResponseSource": "Broswer",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9,zh;q=0.8,zh-CN;q=0.7,de;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8;",
        "Cookie": cookie,
        "Origin": wifiURL,
        "Pragma": "no-cache",
        "Referer": wifiURL+"/html/content.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    resetRequest = urllib.request.Request(resetURL, createXML({"Control":"1"}))
    for key in resetHeaders:
        resetRequest.add_header(str(key), str(resetHeaders[key]))
    resetResponse = urllib.request.urlopen(resetRequest)
    resetContent = resetResponse.read()
    return str(resetContent).find("<response>OK</response>") != -1

def resetHuaWeiWIFI():
    getTokeTimes = 3
    while getTokeTimes > 0:
        getTokeTimes -= 1
        try:
            if getHuaWeiWIFIToken():
                break
        except:
            return False
        time.sleep(0.5)
    if getTokeTimes <= 0:
        return False
    try:
        if not preLoginHuaWeiWIFI():
            return False
    except:
        return False
    time.sleep(0.5)
    try:
        if not loginHuaWeiWIFI():
            return False
    except:
        return False
    time.sleep(0.5)
    try:
        if not getHuaWeiWIFIMainContent():
            return False
    except:
        return False
    time.sleep(0.5)
    try:
        if not resetControlHuaWeiWIFI():
            return False
    except:
        return False
    return True


