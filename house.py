#coding:utf-8
import urllib.request
import urllib.error
import sys,ssl,getopt,xlwt,math
from parsel import Selector
baseUrl = 'https://nj.lianjia.com/ershoufang/gulou/pg'
wbk = xlwt.Workbook(encoding='utf-8')
opts, args = getopt.getopt(sys.argv[1:], "h")
for op, value in opts:
    print(value)
    if op == "-h":
        print('house.py cityname districtname')
        sys.exit()
sheet = wbk.add_sheet("南京市鼓楼区二手房")
colsnames = ['地址', '厅室', '面积', '朝向', '楼层', '总层数', '电梯', '装修','年代', '结构', '总价', '均价/平米']
for index, val in enumerate(colsnames):
    sheet.write(0,index,colsnames[index])
context = ssl._create_unverified_context()
lists = []
def getPages(page):
    for i in range(1,page):
        getData(i)
def getData(page): 
    try:
        data = urllib.request.urlopen('''https://%s.lianjia.com/ershoufang/%s/pg%s/'''%(args[0], args[1],page),context = context)
    except urllib.error.URLError as e:
        print('当前网络有问题')
        return 
    text = data.read().decode(sys.getfilesystemencoding())
    selector = Selector(text=text)
    messes = selector.css("div.info.clear").getall()
    for mess in messes:
        Mess = Selector(mess)
        address = Mess.xpath('//div[@class="houseInfo"]/text()').getall() #地址信息
        addressName = Mess.xpath('//div[@class="houseInfo"]//a/text()').getall() #地址名
        transAddress = address[0].strip()[1:].split('|')
        
        rooms = transAddress[0] #厅室
        area = transAddress[1] #面积
        dire = transAddress[2] #朝向
        decorate = transAddress[3] #装修
        try:
            elevator = transAddress[4] #电梯
        except:
            elevator = '未知'
        detail = Mess.xpath('//div[@class="positionInfo"]/text()').getall()
        transData = detail[0].replace('-', '').rstrip()
        floor = transData[0 : transData.find('(')] #楼层信息
        totalFloor = transData[transData.find('(') + 1 : transData.find(')')] #总层数
        year = '未知' if transData.find('建') == -1 else transData[transData.find(')') + 1 : transData.find('建')]
        constructor = transData[transData.find(')') + 1 : ] if transData.find('建') == -1 else transData[transData.find('建') + 1 : ]
        position = Mess.xpath('//div[@class="positionInfo"]/a/text()').getall() #位置信息
        totalPrice = Mess.xpath('//div[@class="totalPrice"]//span/text()').getall() #总价信息
        avage = float(totalPrice[0])/float(area[0:area.find('平')])
        lists.append({
         'address': addressName[0],
         'rooms': rooms,
         'area': area,
         'dire': dire,
         'floor': floor,
         'totalFloor': totalFloor,
         'elevator': elevator,
         'decorate': decorate,
         'year':year,
         'constructor': constructor,
         'totalPrice': totalPrice[0]+'万',
         'avage': '%.2f' % avage + '万'
    
        })
    return lists

def write2xls(data): 
    colsname = ['address', 'rooms', 'area', 
    'dire','floor', 'totalFloor', 'elevator',
    'decorate','year', 'constructor', 'totalPrice', 'avage']
    for index,val in enumerate(data):
        row = index + 1
        for col, name in enumerate(colsname):
            sheet.write(row, col, val[name])
    wbk.save('city.xls') 
getPages(10)           
write2xls(lists)            

