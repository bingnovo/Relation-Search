# unicoding:utf-8
import wx
import wx.richtext as rt
import PageRank
from PageRank import multymeaning 
#import AI_new
#from AI_new import multymeaning 

class ButtonFrame(wx.Frame):  
    def __init__(self):
        wx.Frame.__init__(self, None,-1,"Intelligent",size=(400, 400))
        self.Center()
        CopyPanel(self)

class CopyPanel(wx.Panel):
     
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
     
        self.msg = ""
        self.initGUI()
     
    def initGUI(self):
        self.__create_componts()
        self.__set_properties()
        self.__do_layout()
        
    def __set_properties(self):
        pass
        
    def __create_componts(self):
        
        self.Qbutton = wx.Button(self,label= "查询") 
        self.Rbutton=wx.Button(self,label='重置')
        self.inputText=wx.TextCtrl(self,style=wx.TE_MULTILINE)
        self.outputText=wx.TextCtrl(self,style=wx.TE_MULTILINE)
        
        self.Bind(wx.EVT_BUTTON, self.Query, self.Qbutton)
        self.Bind(wx.EVT_BUTTON, self.Close, self.Rbutton)
        
    def __do_layout(self):
        
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.mainSizer)
        
        self.upSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Input Txt"), wx.HORIZONTAL)
        self.downSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Output Txt"), wx.HORIZONTAL)
        
        self.buttonSizer = wx.BoxSizer(wx.VERTICAL)
          
        self.buttonSizer.Add(self.Qbutton,1,wx.EXPAND | wx.ALL, 10)
        self.buttonSizer.Add(self.Rbutton,1,wx.EXPAND | wx.ALL, 10)
        
        self.upSizer.Add(self.inputText,2,wx.EXPAND | wx.ALL, 10)
        self.upSizer.Add(self.buttonSizer,1,wx.EXPAND | wx.ALL, 10)
        self.downSizer.Add(self.outputText,3,wx.EXPAND | wx.ALL, 10)
      
        self.mainSizer.Add(self.upSizer, 3, wx.EXPAND | wx.ALL, 10)
        self.mainSizer.Add(self.downSizer, 3, wx.EXPAND | wx.ALL, 10)
    def Query(self,evt):  
        msg = self.inputText.GetValue()
        self.msg = msg
        if(self.msg==""):
            self.outputText.SetValue("请输入词条！")
        else:
            judge=multymeaning(self.msg)
            self.outputText.SetValue(judge)
            if(judge[0]!='您'):
                self.pic=wx.Image("PageRank_Date.png",wx.BITMAP_TYPE_PNG).ConvertToBitmap()
                self.frame1 = wx.Frame(self,size=(self.pic.GetWidth(),self.pic.GetHeight()))
                self.frame1.Show()
                self.button2=wx.BitmapButton(self.frame1,-1,self.pic, pos=(10,10))
                self.button2.SetDefault()
        
        
    def Close(self,evt):  
        self.inputText.SetValue("")
        self.outputText.SetValue("")
        self.button2.Destroy()
        self.frame1.Destroy()
        
if __name__ == '__main__':  
    app = wx.PySimpleApp()
    frame = ButtonFrame()
    frame.Show()  
    app.MainLoop()  