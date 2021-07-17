import requests
import json
File=open('score.txt',mode='w')
#作者：ninjarospod
#云成绩成绩查询脚本
#请先下载云成绩app进行首次登陆后，再使用本脚本
#变量声明
user1=input("用户名或手机号：")
pwd=input("密码：")
print("正在登录")
browserHeaders={'user-agent':'Mozilla/5.0 (Linux; Android 9; ELE-AL00 Build/HUAWEIELE-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045710 Mobile Safari/537.36'}
headers={'user-agent':'ycj/5.1.0(Android;9)<okhttp>(<okhttp/3.10.0>)<brand_HUAWEI,model_ELE-AL00,maker_HUAWEI,device_HWELE>'}
#登录接口，方法POST，需要使用特定的UA请求（不确定），密码明文请求
loginUrl='https://www.yunchengji.net/app/login'
#登录请求
while True:
    loginuser=requests.post(loginUrl,{'j_username':user1,'j_password':pwd}, headers ,verify=False,allow_redirects=False)#headers
    if loginuser.status_code == 302: # expected here
        cookies1 = loginuser.cookies
        redirect_URL2 = loginuser.headers['Location']
        loginuser2 = requests.get(redirect_URL2, cookies=cookies1,verify=False)
    loginData=json.loads(loginuser2.text)

    if loginData['result'] == 'fail':
        print(loginData['desc'])
        user1=input("用户名或手机号：")
        pwd=input("密码：")
        print("正在登录")
    if loginData['result'] == '1':
        break
#遍历考试
#考试获取，方法POST，需要使用特定的UA请求（不确定）
scoreUrl='https://www.yunchengji.net/app/student/index'#headers
scoreRequest=requests.post(scoreUrl,headers,cookies=cookies1,verify=False)
scoreData=json.loads(scoreRequest.text)
#获取考试id
i=0
scoreDisplay={'name':[' ']*9999,'seid':[' ']*9999}
print('================================================')
print('id   考试名称')
print('------------------------------------------------')
while True:
    try:
        scoreDisplay['name'][i]=scoreData['desc']['selist'][i]['name']
        print(i,'  ',scoreDisplay['name'][i])
        scoreDisplay['seid'][i]=scoreData['desc']['selist'][i]['id']
        
    except IndexError:
        maxi=i-1
        break
    else:
        i=i+1

#输入查询编号，并转换
checknum=[' ']*9999
po=str(input("请输入你要查询的考试编号，多个查询请使用“-”或“,”例如“1-2”,“3,5”:"))
m=0
n=0
temp=0
temp2=0

while(po[len(po)-1]<'0' or po[len(po)-1]>'9' or po[0]<'0' or po[0]>'9'):
    po=str(input("您的输入有误，请输入你要查询的考试编号，多个查询请使用“-”或“,”例如“1-2”,“3,5”:"))

while n<len(po):
    if (po[n]>='0' and po[n]<='9'):
        temp=temp*10+(int(po[n])-int('0'))
    if po[n]=='-':
        n=n+1
        while n<len(po):
            if po[n]==',':
                while(temp2-temp+1):
                    checknum[m]=temp
                    m=m+1
                    temp=temp+1
                temp=0
                temp2=0
                break
            if po[n]>='0' and po[n]<='9':
                temp2=temp2*10+(int(po[n])-int('0'))
                if n==len(po)-1:
                    while(temp2-temp+1):
                        checknum[m]=temp
                        m=m+1
                        temp=temp+1
                    temp=0
                    temp2=0
                    break
                    n=n+1
    if po[n]==',' or n==len(po)-1:
        checknum[m]=temp
        temp=0
        m=m+1        
    n=n+1
s='123'
#遍历循环所有成绩
i2=0
i3=1
checkUrl="https://www.yunchengji.net/app/student/cj/report-total"
while True:
    if checknum[i2]==" ":
        break
    if checknum[i2]>maxi:
        continue
    scoreDetails=requests.get(checkUrl+'?seid='+str(scoreDisplay['seid'][checknum[i2]]+int('0')),browserHeaders,verify=False,cookies=cookies1)
    scoreDetail=json.loads(scoreDetails.text)
    #Debug
    #print(type(scoreDetail['desc']['stuOrder']['subjects'][0]['score']),type(scoreDetail['desc']['stuOrder']['subjects'][0]['classOrder']),type(scoreDetail['desc']['stuOrder']['subjects'][0]['schoolOrder']))
    #写基本信息（总体）
    print()
    s="考试名称："+scoreDetail['desc']['examName']+" "+"姓名："+scoreDetail['desc']['studentname']+'\n'+"考试类型："+scoreDetail['desc']['examTypeStr']+'考\n'
    File.write(s)
    s="总分："+scoreDetail['desc']['stuOrder']['subjects'][0]['score']+" "+"总分班排："+str(scoreDetail['desc']['stuOrder']['subjects'][0]['classOrder']+int('0'))+" "+"总分校排："+str(scoreDetail['desc']['stuOrder']['subjects'][0]['schoolOrder']+int('0'))+" "
    File.write(s)
    try:
        File.write("总分联排："+str(scoreDetail['desc']['stuOrder']['subjects'][0]['unionOrder']+int('0'))+'\n')
    except IndexError:
        z=1#无意义，仅供出错时跳出
    else:
        z=1
    File.write("本班级参加本次考试的总人数："+str(scoreDetail['desc']['stuOrder']['scoreGap']['classNum']+int('0'))+" "+"本学校参加本次考试的总人数："+str(scoreDetail['desc']['stuOrder']['scoreGap']['schoolNum']+int('0'))+" ")
    try:
        File.write("联考参加本次考试的总人数："+str(scoreDetail['desc']['stuOrder']['scoreGap']['unionNum']+int('0'))+'\n')
    except IndexError:
        z=1
    else:
        z=1
    File.write("班级最高分："+scoreDetail['desc']['stuOrder']['scoreGap']['classTop']+" "+"班级平均分："+scoreDetail['desc']['stuOrder']['scoreGap']['classAvg']+" "+"学校最高分："+scoreDetail['desc']['stuOrder']['scoreGap']['schoolTop']+" "+"学校平均分："+scoreDetail['desc']['stuOrder']['scoreGap']['schoolAvg']+" ")
    try:
        File.write("联考最高分："+scoreDetail['desc']['stuOrder']['scoreGap']['unionTop']+" "+"联考平均分："+scoreDetail['desc']['stuOrder']['scoreGap']['unionAvg']+'\n')
    except IndexError:
        z=1
    else:
        z=1
    while True:
        try:
            File.write("科目："+scoreDetail['desc']['stuOrder']['subjects'][i3]['name']+" "+"成绩："+scoreDetail['desc']['stuOrder']['subjects'][i3]['score']+" "+"班排："+str(scoreDetail['desc']['stuOrder']['subjects'][i3]['classOrder']+int('0'))+" "+"校排："+str(scoreDetail['desc']['stuOrder']['subjects'][i3]['schoolOrder']+int('0'))+" ")
            try:
                File.write("联排："+str(scoreDetail['desc']['stuOrder']['subjects'][i3]['unionOrder']+int('0'))+'\n')
            except IndexError:
                z=1
            else:
                z=1
        except IndexError:
            break
        else:
            i3=i3+1
    File.write('\n')
    i2=i2+1
File.close()   
    
   




            

