
import xml.etree.ElementTree as ET
import wx,os,sys,time

from wxPython.wx import *


import MainGui_Prev as MainGui
import LiefXML


#    f = locals()[Event]
#    f()
#        print vars()        
#        for k, v in globals().items():
#            print k, "=", v 
    
def EH(Event,_GUI, evt = ""):
#    if _GUI.cEvent <> "":
#        _GUI.Event_Edit.AppendText(Event+" ignored - " + _GUI.cEvent + " still Active.\n")
#        return
    _GUI.cEvent = Event
    _GUI.cEventTime = time.clock()
    
    if Event == "EH_OpenXML":
        _GUI.NEvent( Event )
        LiefXML.OpenXMLFile(_GUI,_GUI.OpenXMLFiles()[0])
        _GUI.CEvent()
        return 1
    elif Event == "EH_Help":
        print "help clicked"
        LiefXML.UpdateHTMLHelp(_GUI)
    elif Event == "EH_RightClicked":
        RCClicked = _GUI.RClickDic[ evt.GetId() ]
        cNode = _GUI.RCNode
        print RCClicked,cNode.text
        if RCClicked == "Transfer" and cNode.ctype == "ITEM":
            print cNode.path
            path = cNode.path[:cNode.path.find("/",cNode.path.find("/")+1)] + "/Transfer/" + cNode.text
            LiefXML.addnode(path,_GUI,cNode.ctype,cNode.table,1,"",-1)
            LiefXML.UpdateTransfer(cNode,_GUI)
    elif Event == "EH_RightClick":
        _GUI.NEvent( Event )
        itm = evt.GetItem()
        cNode = _GUI.RCNode = LiefXML.GetNodeFromTreeItem(_GUI, itm )
        itmtext = _GUI.Tree.GetItemText( itm )
        
        print cNode.ctype, cNode.text
        if cNode.ctype == "ITEM":
            menu = wxMenu()
            for (id,title) in _GUI.RClickDic.items():
                menu.Append( id, title )
                EVT_MENU( menu, id, _GUI.OnRightClick )
            _GUI.PopupMenu( menu, evt.GetPoint() )
            menu.Destroy() # destroy to avoid mem leak         

        _GUI.CEvent()
    elif Event == "EH_Add":
        _GUI.NEvent( Event )      
        LiefXML.AddFilter(_GUI)
        _GUI.CEvent()
        return 1        

    elif Event == "EH_Filter":
        _GUI.NEvent( Event )       
        LiefXML.Filter(_GUI)
        _GUI.CEvent()
        return 1            

    elif Event == "EH_OpenDBA":
        _GUI.NEvent( Event )      
        LiefXML.OpenDBAFile(_GUI)
        _GUI.CEvent()
        return 1            

    elif Event == "EH_HSE":
        _GUI.NEvent( Event )       
        LiefXML.UpdateByHslider(_GUI)
        _GUI.CEvent()
        return 1            

    elif Event == "EH_XPATH":
        _GUI.NEvent( Event )     
        cNode = LiefXML.GetCurrentXMLNode(_GUI)
        if cNode.XMLFileListNo < 0:
            LiefXML.UpdateDBADisplay_Query( _GUI.text_xpath.GetValue() ,_GUI)
        else:
            LiefXML.UpdateXMLDisplay_xpath( _GUI.text_xpath.GetValue() ,_GUI)
        _GUI.CEvent()
        return 1

    elif Event == "EH_Tree_Sel_Changed":
        _GUI.NEvent( Event )       
        print "EH_Tree_Sel_Changed"
        LiefXML.TreeEvent(_GUI)
        _GUI.CEvent()
        return 1            
        
    elif Event == "EH_SaveXML":
        _GUI.NEvent( Event ) 
        print "EH_SaveXML"
        _GUI.CEvent()
        return 1            
        
    elif Event == "EH_OpenDBA":
        _GUI.NEvent( Event )  
        print "EH_OpenDBA"
        _GUI.CEvent()
        return 1            
        
    elif Event == "EH_Exit":
        _GUI.NEvent( Event )
        print "EH_Exit"
        answer = _GUI.MsgBoxYN("Exit?","Are You Sure???")
#        if answer == wx.YES:
        os._exit(1)
#        sys.exit()
#        quit()
    else:
        print "Event Not Found:",Event


if __name__ == "__main__":
    MainID = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    
    _GUI = MainGui.MGUI(None, -1, "")
    MainID.SetTopWindow(_GUI)
    _GUI.Show()

    LiefXML.initXMLTree(_GUI)
    MainID.MainLoop()    
    #    print vars()
    #    print