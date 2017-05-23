# -*- coding: utf-8 -*-
import wx
import wx.grid
import serial
import json
import hashlib
import time
import qrcode
import Image
import ctypes
import sys
import md5
import os


qccode_list = {"deviceid": "", "apikey": ""}

class SerailUI(wx.Frame):
    def __init__(self, title, pos, size):
        wx.Frame.__init__(self, None, -1, title, pos, size,style = wx.MINIMIZE_BOX | wx.SYSTEM_MENU |wx.CAPTION | wx.CLIP_CHILDREN | wx.CLOSE_BOX )
        self.icon = wx.Icon('itead.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        self.Center()
        self.file=''
        self.panel = wx.Panel(self, -1)
        self.panel.SetBackgroundColour("white")
        self.panel.SetForegroundColour("brown")
        
        self.current_data = { 'deviceid':'', 'factory_apikey':'', 'sta_mac':'',
        'sap_mac':'', 'device_model':''} 
        self.current = 0
        self.num_success = 0
        self.serial_log = 0
        self.file_log = 0
        self.download_flag = 1
        fd1 = open('record.txt','a+')
        count = fd1.read()
        if count == '':
            print ''
            #fd1.write('0')
        else:
            fd1.seek(0,0)    
            self.num_success = int(fd1.readline())
        fd1.close()

        headleft = self.LayoutHeadLeft()
        headright = self.LayoutHeadRight()
        head = self.LayoutHead(headleft,headright)
        RightCentre = self.LayoutCentreRight()
        RightLow = self.LayoutLowRight()
        #Rightdown = self.Layoutdown()
        #Right = self.LayoutRight(RightCentre, RightLow,Rightdown)
        Right = self.LayoutRight(RightCentre, RightLow)
        Low = self.LayoutLow(Right)
        All = self.LayoutAll(head, Low)
        
        self.use_date = '\n'+'\n'+'%d'%self.num_success 
        self.fileDate2.SetLabel(self.use_date)
        
        self.panel.SetSizer(All)
        All.Fit(self)
        All.SetSizeHints(self)

    def Layoutdown(self):
        global qccode_list


        font2 = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD)

        self.button = wx.Button(self.panel, -1, u"打印", size=(100, 108))
        self.button.SetFont(font2)
        self.Bind(wx.EVT_BUTTON, self.button_handle, self.button)

        qcbox = wx.StaticBox(self.panel, label=u'二维码区域')
        qcbbox = wx.StaticBoxSizer(qcbox, orient=wx.HORIZONTAL)

        qcbbox.Add(self.button, 0, wx.TOP, 0)
        #self.image = wx.Image("xgezhang.png", wx.BITMAP_TYPE_PNG)
        #self.map_show = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(self.image))
        #qcbbox.Add(self.map_show,0,wx.LEFT,0)
        self.create_code('100007eeb1','d35bb6b6-7ed9-4151-8e62-bbacc664dc5a')
        self.bmp = wx.Image("xgezhang.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.bmpbutton = wx.BitmapButton(self.panel, -1, self.bmp)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.bmpbutton)

        self.bmpbutton.SetDefault()
        qcbbox.Add(self.bmpbutton, 0, wx.LEFT, 0)

        '''
        self.qc_deviceID = wx.StaticText(self.panel, -1, 'deviceedid')
        self.qc_FactoryApikey1 = wx.StaticText(self.panel, -1, 'apikey')
        qc_info_box = wx.BoxSizer(wx.VERTICAL)
        qc_info_box.Add(self.qc_deviceID,0,wx.LEFT,0)
        qc_info_box.Add(self.qc_FactoryApikey1, 0, wx.LEFT, 0)

        qcbbox.Add(qc_info_box, 0, wx.LEFT, 0)
        '''
        return qcbbox

    def OnClick(self, event):
        print

    def change_qccode(self):
        self.bmp = wx.Image("xgezhang.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.bmpbutton.SetBitmap(self.bmp)
        self.panel.Refresh()

    def md5(self,str):
        m = md5.new()
        m.update(str)
        return m.hexdigest()

    def re_button_handle(self,event):
        self.download.Enable(True)

    def button_handle(self,event):
        global qccode_list

        try:
            tscdll = ctypes.WinDLL('TSCLib.dll')
            tscdll.openport("Gprinter  GP-2120T")

            tscdll.setup('40.0','30.0','4','8','0','2','0')
            tscdll.clearbuffer()
            '''
            id = qccode_list["deviceid"]
            key = qccode_list["apikey"]
            md5_hex = self.md5(id+key)
            str = 'api.coolkit.cc:8080/api/user/device/addGsm?\r\nid='+ md5_hex
            command = "QRCODE 58,20,L,6,A,0,\""+str+"\""
            print command
            tscdll.sendcommand("DIRECTION 1")
            tscdll.sendcommand(command)
            '''
            tscdll.sendcommand("DIRECTION 1")
            #tscdll.windowsfont(85,36,20,0,0,0,"Arial",""+qccode_list['deviceid'])
            tscdll.windowsfont(70, 10, 25, 0, 0, 0, "Arial", "1064887660272")
            tscdll.windowsfont(70, 60, 25, 0, 0, 0, "Arial", "1064887660273")
            tscdll.windowsfont(70, 110, 25, 0, 0, 0, "Arial", "1064887660274")
            tscdll.windowsfont(70, 160, 25, 0, 0, 0, "Arial", "1064887660280")
            #tscdll.downloadpcx("print.bmp","PR.BMP")
            #tscdll.sendcommand("PUTBMP 70,40,\"PR.BMP\"")
            tscdll.printlabel("1","1")
            tscdll.clearbuffer()
            tscdll.closeport()
        except Exception:
            print sys.exc_info()[0], sys.exc_info()[1]

    def create_code(self,devicedid,apikey):
        global qccode_list

        qccode_list['deviceid'] = devicedid
        qccode_list['apikey'] = apikey
        md5_hex = self.md5(qccode_list['deviceid'] + qccode_list['apikey'])
        str = 'api.coolkit.cc:8080/api/user/device/addGsm?\r\nid=' + md5_hex
        #str = qccode_list['deviceid']
        print qccode_list['deviceid']+'\n'+qccode_list['apikey']
        print str
        img = qrcode.make(str)
        (x,y) = img.size
        x_s = 100
        y_s = y*x_s/x
        out = img.resize((x_s, y_s), Image.ANTIALIAS)  # resize image with high-quality
        out.save('xgezhang.bmp')

        img2 = qrcode.make(str)
        (x, y) = img2.size
        x_s = 150
        y_s = y * x_s / x
        out = img2.resize((x_s, y_s), Image.ANTIALIAS)  # resize image with high-quality
        out.save('print.bmp')
    
    def LayoutHeadLeft(self):
        font2 = wx.Font(13, wx.SWISS, wx.NORMAL, wx.BOLD)
        font3 = wx.Font(11, wx.SWISS, wx.NORMAL,wx.NORMAL)
        self.loadFile = wx.Button(self.panel, -1, u"加载数据", size=(100,100))
        self.Bind(wx.EVT_BUTTON, self.OnLoadFile, self.loadFile)    #1 绑定按钮敲击事件  
        self.loadFile.SetFont(font2) 
        title2 =wx.StaticText(self.panel, -1, u"已使用：\n未使用：\n总记录：",style=wx.ALIGN_RIGHT)
        title21 = wx.StaticText(self.panel, -1, u"条\n条\n条")

        self.file_date = u"0\n0\n0  "
        self.fileDate = wx.StaticText(self.panel, -1, self.file_date )
        self.filePath = wx.TextCtrl(self.panel,-1,'',size = (400, -1), style=wx.TE_READONLY | wx.TE_MULTILINE  | wx.BRUSHSTYLE_TRANSPARENT | wx.HSCROLL)
        self.filePath.SetBackgroundColour(self.panel.BackgroundColour) 
        #self.filePath = wx.StaticText(self.panel, -1, '',size = (50, -1), style=wx.TE_MULTILINE)
        title2.SetFont(font2)
        title21.SetFont(font2)
        self.fileDate.SetFont(font2)
        self.filePath.SetFont(font3)
        
        vbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(self.loadFile, 0,wx.TOP, 12)
        sb = wx.StaticBox(self.panel, label=u"当前数据")
        sbs = wx.StaticBoxSizer(sb, orient=wx.HORIZONTAL)
        
        sbs.Add(title2, 0,wx.ALL, 0)
        num = wx.BoxSizer(wx.HORIZONTAL)
        num.Add(self.fileDate,0,wx.ALL, 0)
        num.Add(title21,0,wx.LEFT, 0)
        
        path = wx.BoxSizer(wx.HORIZONTAL)
        path.Add(num, 0,wx.ALL, 0)
        title22 =wx.StaticText(self.panel, -1, u" 路径：",style=wx.ALIGN_RIGHT)
        title22.SetFont(font2)
        path.Add(title22, 0,wx.ALL, 0)
        path.Add(self.filePath, 0,wx.ALL, 0)
        
        sbs.Add(path, 0, wx.ALL, 0)
        vbox.Add(sbs,0, wx.RIGHT|wx.LEFT|wx.TOP, 12)
        return vbox
    
    def LayoutHeadRight(self):
        font2 = wx.Font(13, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.emptyCount = wx.Button(self.panel, -1, u"清空计数", size=(100,100))
        self.Bind(wx.EVT_BUTTON, self.OnEmptyCount, self.emptyCount)    #1 绑定按钮敲击事件  
        self.emptyCount.SetFont(font2)
        
        self.closeWindow = wx.Button(self.panel, -1, u"退出", size=(100,100))
        self.Bind(wx.EVT_BUTTON, self.OnCloseWindow, self.closeWindow)    #1 绑定按钮敲击事件  
        self.closeWindow.SetFont(font2)
        
        title4 = wx.StaticText(self.panel, -1, u"计数\n\n成功:\n")
        title41 = wx.StaticText(self.panel, -1, u"\n\n 条")
        title4.SetFont(font2)
        title41.SetFont(font2)
        
        self.use_date = u"\n\n0"
        self.fileDate2 = wx.StaticText(self.panel, -1, self.use_date)
        self.fileDate2.SetFont(font2)
        
        vbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(self.emptyCount,0,wx.TOP, 12)
        
        sb = wx.StaticBox(self.panel, label=u"计数面板")
        sbs = wx.StaticBoxSizer(sb, orient=wx.HORIZONTAL) 
        sbs.Add(title4, 1, flag=wx.EXPAND)
        sbs.Add(self.fileDate2,0, wx.ALL, 0)
        sbs.Add(title41, 1, 0, wx.ALL, 0)
        vbox.Add(sbs,0, wx.RIGHT|wx.LEFT|wx.TOP, 12)
        vbox.Add(self.closeWindow,0,wx.TOP, 12)
        return vbox
   
    def LayoutHead(self,headleft,headright):
        box = wx.BoxSizer(wx.HORIZONTAL)    
        box.Add(headleft, 1, flag=wx.EXPAND)
        box.Add(headright, flag=wx.EXPAND)
        return box
    
    def LayoutCentreRight(self):
        font2 = wx.Font(13, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.serial_port_list = ['COM1','COM2','COM3','COM4','COM5','COM6','COM7',
            'COM8','COM9','COM10','COM11','COM12','COM13','COM14','COM15','COM16','COM17','COM18','COM19','COM20','COM21','COM22','COM23',
            'COM24', 'COM25', 'COM26', 'COM27', 'COM28', 'COM29', 'COM30', 'COM31', 'COM32', 'COM33','COM34', 'COM35', 'COM36', 'COM37', 'COM38', 'COM39'
            , 'COM40', 'COM41', 'COM42', 'COM43', 'COM44']
                
        serail_1 = wx.StaticText(self.panel, -1, u"烧写串口:", )
        serail_1.SetFont(font2)
        self.serail_2 = wx.Choice(self.panel, -1, choices=self.serial_port_list)
        self.choice1 = self.serail_2.SetSelection(0)
        self.choice1 = 0
        self.serail_2.Bind(wx.EVT_CHOICE, self.onFormatList1)
        
        self.baud_rate_list = ['4800', '9600', '19200', '38400', '43000', '56000',
                                     '57600', '115200','576000']
        
        baudrate = wx.StaticText(self.panel, -1, u"波特率:",)
        baudrate.SetFont(font2)
        self.baudrate2 = wx.Choice(self.panel, -1, choices=self.baud_rate_list)
        
        self.baudrate2.SetSelection(8)
        self.choice2 = 8
        self.baudrate2.Bind(wx.EVT_CHOICE, self.onFormatList2)
        
        self.serailSwitch = wx.Button(self.panel, -1, u"打开串口")
        self.Bind(wx.EVT_BUTTON, self.OnSerailSwitch, self.serailSwitch)    #1 绑定按钮敲击事件

        #self.Cserail = wx.StaticText(self.panel, -1, u"通信串口:", )
        #self.Cserail.SetFont(font2)
        #self.Cserail_cloise = wx.Choice(self.panel, -1, choices=self.serial_port_list)
        #self.C_choice = self.Cserail_cloise.SetSelection(0)
        self.re_button = wx.Button(self.panel, -1, u"复原")
        self.Bind(wx.EVT_BUTTON, self.re_button_handle, self.re_button)


        vbox = wx.BoxSizer(wx.VERTICAL)
        vvbox = wx.BoxSizer(wx.HORIZONTAL)
        vvbox.Add(serail_1,0, wx.ALL, 2)
        vvbox.Add(self.serail_2,0, wx.ALL, 2)
        vvbox.Add(baudrate,0, wx.ALL, 2)
        vvbox.Add(self.baudrate2,0, wx.ALL, 2)
        vvbox.Add(self.serailSwitch ,0,wx.LEFT, 10)
        vvbox.Add(self.re_button, 0, wx.LEFT, 10)
        #vvbox.Add(self.Cserail_cloise, 0, wx.LEFT, 10)
        
        vbox.Add(vvbox,1, flag=wx.EXPAND)
        font1 = wx.Font(25, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.title_current1 = u"当前记录信息"
        self.current_txt = wx.StaticText(self.panel, -1, self.title_current1 )
        self.current_txt.SetFont(font1)
        self.title_current2 = u"(未加载文件"
        self.title_current3 = "/"
        self.title_current4 = ""
        self.title_current = self.title_current2 + self.title_current3+self.title_current4+"):"
            
        self.current_information = wx.StaticText(self.panel, -1, self.title_current )
        self.current_information.SetFont(font1)
        title5 = wx.StaticText(self.panel, -1, u"DeviceID:\nFactoryApikey:\n"u"StationMac:\nSoftapMac:\n Model:",style=wx.ALIGN_RIGHT)
        title5.SetFont(font2)

        deviceID = u""
        FactoryApikey = u"                                          "
        StationMac = u""
        SoftapMac = u""
        Model = u""
        Information = u"状态:"
        Information_date = u"等待加载"

        self.deviceID1 = wx.StaticText(self.panel, -1, deviceID)
        self.FactoryApikey1 = wx.StaticText(self.panel, -1, FactoryApikey)
        self.StationMac1 = wx.StaticText(self.panel, -1, StationMac)
        self.SoftapMac1 = wx.StaticText(self.panel, -1, SoftapMac)
        self.Model1 = wx.StaticText(self.panel, -1, Model)

        self.deviceID1.SetFont(font2)
        self.FactoryApikey1.SetFont(font2)
        self.StationMac1.SetFont(font2)
        self.SoftapMac1.SetFont(font2)
        self.Model1.SetFont(font2)
        self.information_status = wx.StaticText(self.panel, -1, Information)
        self.information_status_data = wx.StaticText(self.panel, -1, Information_date)
        
        self.information_status_data.SetFont(font1)
        self.information_status.SetFont(font1)
        
        sb = wx.StaticBox(self.panel, label='')
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL) 
        new_box = wx.BoxSizer(wx.HORIZONTAL)
        new_box.Add(self.current_txt,0, wx.ALL, 2)
        new_box.Add(self.current_information, 0, wx.ALL, 2)
        sbs.Add(new_box,0, wx.ALL, 2)
        
        ssb = wx.StaticBox(self.panel, label='')
        sbss = wx.StaticBoxSizer(ssb, orient=wx.HORIZONTAL) 
        
        sssb1 = wx.StaticBox(self.panel, label='')
        sbss1 = wx.StaticBoxSizer(sssb1, orient=wx.HORIZONTAL) 
        sbss1.Add(title5, 0, wx.ALL, 2)
        
        sssb2 = wx.StaticBox(self.panel, label='')
        sbss2 = wx.StaticBoxSizer(sssb2, orient=wx.VERTICAL) 
        sbss2.Add(self.deviceID1, 0, wx.ALL, 0)
        sbss2.Add(self.FactoryApikey1, 0, wx.ALL, 0)
        sbss2.Add(self.StationMac1, 0, wx.ALL, 0)
        sbss2.Add(self.SoftapMac1, 0, wx.ALL, 0)
        sbss2.Add(self.Model1, 0, wx.ALL, 0)
        sbss.Add(sbss1, 0, wx.ALL, 0)
        sbss.Add(sbss2, 0, wx.ALL, 0)
        
        sbs.Add(sbss, 0, wx.ALL, 2)
        new_box2 = wx.BoxSizer(wx.HORIZONTAL)
        new_box2.Add(self.information_status,0, wx.ALL, 2)
        new_box2.Add(self.information_status_data,0, wx.ALL, 2)
        sbs.Add(new_box2, 0, wx.ALL, 2)
        vbox.Add(sbs,0, wx.ALL, 2)
        return vbox
    
    
        
    def LayoutLowRight(self):
        font3 = wx.Font(11, wx.SWISS, wx.NORMAL,wx.NORMAL)
        font2 = wx.Font(13, wx.SWISS, wx.NORMAL, wx.BOLD)
        next_information = wx.StaticText(self.panel, -1, u"下一条记录信息：")
        next_information.SetFont(font2)
        title6 = wx.StaticText(self.panel, -1, u"DeviceID:\nFactoryApikey:\n"u"StationMac:\nSoftapMac:\n Model:",style=wx.ALIGN_RIGHT)
        title6.SetFont(font3)
        
        next_deviceID = u""
        next_FactoryApikey = u"                                       "
        next_StationMac = u""
        next_SoftapMac = u""
        next_Model = u""
        next_Information = u"状态："
        
        self.deviceID2 = wx.StaticText(self.panel, -1, next_deviceID)
        self.FactoryApikey2 = wx.StaticText(self.panel, -1, next_FactoryApikey)
        self.StationMac2 = wx.StaticText(self.panel, -1, next_StationMac)
        self.SoftapMac2 = wx.StaticText(self.panel, -1, next_SoftapMac)
        self.Model2 = wx.StaticText(self.panel, -1, next_Model)
        
        self.deviceID2.SetFont(font3)
        self.FactoryApikey2.SetFont(font3)
        self.StationMac2.SetFont(font3)
        self.SoftapMac2.SetFont(font3)
        self.Model2.SetFont(font3)
        
        self.next_status = wx.StaticText(self.panel, -1, next_Information)
        self.next_status.SetFont(font2)
        
        sb = wx.StaticBox(self.panel, label='')
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL) 
        sbs.Add(next_information, 0, wx.ALL, 2)
        
        ssb = wx.StaticBox(self.panel, label='')
        sbss = wx.StaticBoxSizer(ssb, orient=wx.HORIZONTAL) 
        
        sssb1 = wx.StaticBox(self.panel, label='')
        sbss1 = wx.StaticBoxSizer(sssb1, orient=wx.HORIZONTAL) 
        sbss1.Add(title6, 0, wx.ALL, 2)
        
        sssb2 = wx.StaticBox(self.panel, label='')
        sbss2 = wx.StaticBoxSizer(sssb2, orient=wx.VERTICAL) 
        sbss2.Add(self.deviceID2, 0, wx.ALL, 0)
        sbss2.Add(self.FactoryApikey2, 0, wx.ALL, 0)
        sbss2.Add(self.StationMac2, 0, wx.ALL, 0)
        sbss2.Add(self.SoftapMac2, 0, wx.ALL, 0)
        sbss2.Add(self.Model2, 0, wx.ALL, 0)
        sbss.Add(sbss1, 0, wx.ALL, 0)
        sbss.Add(sbss2, 0, wx.ALL, 0)
        
        sbs.Add(sbss, 0, wx.ALL, 2)
        sbs.Add(self.next_status, 0, wx.ALL, 2)
        return sbs
    
    #def LayoutRight(self, RightCentre, RightLow,Rightdown):
    def LayoutRight(self, RightCentre, RightLow):
        box = wx.BoxSizer(wx.VERTICAL)    
        box.Add(RightCentre, 0, wx.ALL, 2)
        box.Add(RightLow, 0, wx.ALL, 2)
        #box.Add(Rightdown, 0, wx.ALL, 2)
        return box
    
    def LayoutLow(self, Right):
        font = wx.Font(50, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        box = wx.BoxSizer(wx.HORIZONTAL)    
        box.Add(Right, 1, flag=wx.EXPAND)
        self.download = wx.Button(self.panel, -1, u"烧写", size=(425,415))
        self.download.SetFont(font)
        self.Bind(wx.EVT_BUTTON, self.OnDownload, self.download)    #1 绑定按钮敲击事件 
        self.download.SetForegroundColour("red")
        self.download.SetBackgroundColour("white")
        box.Add(self.download,0, wx.LEFT|wx.TOP, 20)
        return box
    
    def LayoutAll(self, head, Low):
        box = wx.BoxSizer(wx.VERTICAL)    
        box.Add(head, 0, wx.ALL, 2)
        box.Add(Low, 0, wx.ALL, 2)
        return box
    
    
    def OnLoadFile(self, event):
        dialog=wx.FileDialog(None,'Itead Serail',style=wx.OPEN,wildcard = "*.csv*")
        choice = dialog.ShowModal()
        if  choice == wx.ID_OK:
            self.file=dialog.GetPath()
            self.filePath.SetLabel(self.file)
            self.OnFile()
            self.download_log = 0
        elif  choice == wx.ID_CANCEL:
            ret = wx.MessageBox(u"你没有选择文件！",  'Confirm', wx.OK)
            if ret == wx.OK:
                dialog.Destroy()
            
        dialog.Destroy()

    def OnFile(self):
        file=open(self.file,'a+')
        self.file_log = 1
        lines= file.readlines()
        self.sum = 0
        
        self.First_Y = 0
        for line in lines:  
            if line[0] == 'Y' or line[0] == 'N':
                self.sum = self.sum + 1 
                if line[0] == 'Y' and self.First_Y == 0:
                    self.current = self.sum 
                    self.First_Y = 1
            else:
                break
                
        if self.current > self.sum or self.current == 0:
            self.current = self.sum
        self.current_str = '%d'%self.current
        self.title_current2 = self.current_str
        self.sum = self.sum  
        self.sum_str = '%d'%self.sum
        self.done = 0
        self.leave = 0
        
        for line in lines:
                if line[0] == 'Y':
                    self.leave += 1 
                elif line[0] == 'N':    
                    self.done += 1 
        
        self.leave_str = '%d'%self.leave
        self.file_date ='%d'%self.done + '\n' + self.leave_str + '\n' +self.sum_str
        self.fileDate.SetLabel(self.file_date)  
        self.title_current4 = self.sum_str
        self.title_current = "(" + self.title_current2 + self.title_current3+self.title_current4+"):"
        
        self.current_information.SetLabel(self.title_current)  
        self.use_date = '\n'+'\n'+'%d'%self.num_success
        self.fileDate2.SetLabel(self.use_date)
        if self.current > 0:
            self.current = (self.current-1)*98
            
        file.seek(self.current)    
        status1 = file.read(1)
        self.information_status_data.SetForegroundColour("brown")
        if status1 == 'Y':
            self.information_status_data.SetLabel(u"未使用")
        elif status1 == 'N':
            self.information_status_data.SetLabel(u"已使用")
            
        file.seek(1,1)
        self.current_data['deviceid'] = file.read(10)
        self.deviceID1.SetLabel(self.current_data['deviceid'])
        file.seek(1,1)
        self.current_data['factory_apikey'] = file.read(36)
        self.FactoryApikey1.SetLabel(self.current_data['factory_apikey'])
        file.seek(1,1)
        self.current_data['sta_mac'] = file.read(17)
        self.StationMac1.SetLabel(self.current_data['sta_mac'])
        file.seek(1,1)
        self.current_data['sap_mac'] = file.read(17)
        self.SoftapMac1.SetLabel(self.current_data['sap_mac'])
        file.seek(1,1)
        self.current_data['device_model'] = file.read(10)
        self.Model1.SetLabel(self.current_data['device_model'])
        
        file.seek(2,1)
        status2 = file.read(1)
        if status2 == 'Y':
           self.next_status.SetLabel(u"状态：未使用")
        elif status2 == 'N':
           self.next_status.SetLabel(u"状态：已使用")
           
        file.seek(1,1)
        self.deviceID2.SetLabel(file.read(10))
        file.seek(1,1)
        self.FactoryApikey2.SetLabel(file.read(36))
        file.seek(1,1)
        self.StationMac2.SetLabel(file.read(17))
        file.seek(1,1)
        self.SoftapMac2.SetLabel(file.read(17))
        file.seek(1,1)
        self.Model2.SetLabel(file.read(10))
        file.close()

        #self.create_code(self.current_data['deviceid'],self.current_data['factory_apikey'])
        #self.change_qccode()
        
    def OnEmptyCount(self, event):
        ret = wx.MessageBox(u"你确定要清空计数吗？",  'Confirm', wx.OK|wx.CANCEL)
        if ret == wx.OK:
            self.num_success = 0
            self.use_date = '\n'+'\n'+'%d'%self.num_success
            self.fileDate2.SetLabel(self.use_date) 
            fd1 = open('record.txt','w+')
            fd1.write('%d'%self.num_success)
            fd1.close()
            
        
    def OnCloseWindow(self, event):
        ret = wx.MessageBox(u"你确定要退出吗？",  'Confirm', wx.OK|wx.CANCEL)
        if ret == wx.OK:
            wx.Exit()

    def OnDownload(self, event):
        #self.download.Enable(False)
        #lines = ''
        #if self.file_log == 0:
        #    wx.MessageBox(u"你没有打开串口或者加载文件！",  'Confirm', wx.OK)
        if 0:
            print

        #elif self.serial_log == 1:
        else :
            if self.download_flag == 1:
                self.download_flag = 0
                self.OnFile()

                file=open(self.file,'r+')
                lines = file.readlines()
                num = 0
                have_data = 0

                for line in lines:
                    num+=1
                    if line[0] == 'Y':
                        have_data = 1
                        buf = 'D:\\flash_one_firmware_hadata_tool\\exe_tool\\flash_stub_one_fireware_hadata_FNC.exe \"'+ self.serial_port_list[self.choice1] + '\" \"' + str(lines[num-1]) + '\"'
                        print str(lines[num-1])
                        try:
                            ret = os.system(buf)
                        except:
                            self.information_status_data.SetLabel(u"烧写程序没响应！！！")
                            return
                        self.download_flag = 1
                        print "download over................"
                        if ret == 0:
                                file.seek(98*(num-1),0)
                                line = 'N'+line[1:]
                                file.write(line)
                                file.close()
                                self.num_success+=1
                                self.information_status_data.SetForegroundColour("#0000FF")

                                self.information_status_data.SetLabel(u"已成功！！！")

                                fd1 = open('record.txt','w+')
                                fd1.write('%d'%self.num_success)
                                fd1.close()
                                self.use_date = '\n'+'\n'+'%d'%self.num_success
                                self.fileDate2.SetLabel(self.use_date)
                                #self.download.Enable()
                                break
                        elif ret == 2:
                            file.close()
                            self.information_status_data.SetForegroundColour("red")
                            self.information_status_data.SetLabel(u"烧写失败（同步没有数据返回）")
                            #self.download.Enable()
                            break
                        elif ret == 3:
                            file.close()
                            self.information_status_data.SetForegroundColour("red")
                            self.information_status_data.SetLabel(u"烧写失败（同步数据返回错误）")
                            #self.download.Enable()
                            break
                        elif ret == 1:
                            file.close()
                            self.information_status_data.SetForegroundColour("red")
                            self.information_status_data.SetLabel(u"烧写失败（烧录过程错误）")
                            #self.download.Enable()
                            break
                if have_data == 0:
                    file.close()
                    self.information_status_data.SetForegroundColour("red")
                    self.information_status_data.SetLabel(u"烧写失败（无可用数据）")
                    #self.download.Enable()



    def OnSerailSwitch(self, event):
        print "...."
        '''
        if self.serial_log == 0:
            if self.serial_port_list[self.choice1] == self.serial_port_list[self.Cserail_cloise.GetSelection()]:
                wx.MessageBox(u"串口号设置重复！", 'Confirm', wx.OK)
                return
            else:
                self.ser = serial.Serial(self.serial_port_list[self.choice1], self.baud_rate_list[self.choice2],bytesize=8, parity='N', stopbits=1, timeout=0.2, writeTimeout=0, xonxoff=0,rtscts=0)
                #self.Cser = serial.Serial(self.serial_port_list[self.Cserail_cloise.GetSelection()], 9600, bytesize=8,parity='N', stopbits=1, timeout=0, writeTimeout=0, xonxoff=0, rtscts=0)
            if self.ser > 0:
                self.serailSwitch.SetLabel(u"关闭串口") 
                self.serial_log = 1
                print "串口打开成功！"
                s = ['com\x0A\x0A\x07\x01\xFF\xFF\xFFzzz']
                self.ser.write(s[0])

            else:
                wx.MessageBox(u"你没有打开串口！",  'Confirm', wx.OK)
        elif self.serial_log == 1:
            self.ser.close()
            self.Cser.close()
            print "串口已关闭！"
            self.serailSwitch.SetLabel(u"打开串口") 
            self.serial_log = 0
         '''
        
        
    def onFormatList1(self, event):
        self.choice1=self.serail_2.GetSelection() 
        
    def onFormatList2(self, event):
        self.choice2=self.baudrate2.GetSelection() 




if __name__=='__main__':
    app = wx.App()
    frame = SerailUI(u"PSXTOOL(1.2.0)",(100,150),(960,600))
    frame.Show(True)
    app.MainLoop()

    
    
    
    
    
    
    
    
        
        
        
        
    
        
        


        