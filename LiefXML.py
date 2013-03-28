
#def test_myoutput(capsys): # or use "capfd" for fd-level
#    print ("hello")
#    sys.stderr.write("world\n")
#    out, err = capsys.readouterr()
#    assert out == "hello\n"
#    assert err == "world\n"
#    print "next"
#    out, err = capsys.readouterr()
#    assert out == "next\n"


import os.path
import wx
import xml.etree.ElementTree as ET
import time
import os
import firebirdsql
import sys
import string
import shutil

XMLPathList = [ ]
NodeList = [ ]
XMLFileList = [ ]
DBAFileList = [ ]

SysPath = sys.path[0]
if SysPath[-3:] == "exe":
    x = SysPath.rfind("\\")
    SysPath = SysPath[:x]
SysPath = SysPath.replace("\\","\\\\")

#SettingsPath = "C:\Users\Lief-W7\Desktop\Dropbox\Python\Work\Settings.xml"
SettingsPath = SysPath + "\\\\Settings.xml"

html_header = ""
html_footer = ""
html_itemm = ""
html_itemp = ""
html_bomstages = ""

DBATables = ["ACCT","ACCTGROUP","ACCTGRPS","ACCTSUM","ACCTTTL","ACCTYPES","ADDFIELDS","ADDMODULES",
             "AGING","ANALYSIS","ANSWERTABLE","AP","APAGING","APBATCH","APBTCHDT","APMEMO","AR",
             "ARBATCH","ARBTCHDT","ARCHAEVT","ARCHASSET","ARCHEXP","ARCHINVC","ARCHJNOT","ARCHJOBD",
             "ARCHJOBS","ARCHKB","ARCHPAYM","ARCHPODETL","ARCHPORD","ARCHPORECS","ARCHSINV","ARCHSINVDEL",
             "ARMEMO","ASETDOC","ASSET","ASSETACQUTYPE","ASSETAUTHORIZE","ASSETCATALOGS","ASSETCHAR",
             "ASSETCONSUMABL","ASSETCONTRACT","ASSETCYCLE","ASSETCYCLEDETL","ASSETDEPRCHART","ASSETDEPRIDENTITY",
             "ASSETDEPT","ASSETDISPOTYPE","ASSETFIXED","ASSETFIXEDDEPR","ASSETFIXEDDETL","ASSETGROUP",
             "ASSETHRCH","ASSETMANDETL","ASSETMANUAL","ASSETREVALUE","ASSETSETUP","ASSETSOURCE","ASSETUDF",
             "ASSEVENT","ASSTPRED","ASTYPES","ATTRIBUTES","ATTRIDETL","AUTOREF","BANKACCS","BANKLIST",
             "BANKTRANSFER","BATCHDET","BATCHTTL","BATCHTYPE","BDGTCAT","BOMCONSEL","BOMDEFAULT",
             "BOMFMLELEMENT","BOMLIST","BOMMASTER","BOMMDTYPE","BOMREFERENCES","BOMTEMP",
             "BOM_COMP_SWAP","BOM_COMP_SWAP_LINES","BOM_PROCESS_SWAP","BOM_PROCESS_SWAP_LINES","BOOKJOB",
             "BREAKPRICE","BREAKQUANTITY","BUDGET","CALENDARDEL","CALENDARS","CALLDEL","CALLTYPES",
             "CASHBUDEX","CASHBUDIN","CASHFLOWSU","CATAFORMAT","CATALOG","CATEGORY","CCARD_EXP_DTL",
             "CCARD_EXP_HDR","CCONTACTS","CHARBOM","CHARCOMP","CHARVALID","CHARVALIDDEL","CHAR_ITEM_SERIAL",
             "CHECKS","CHKREG","COL_DEF_SETTINGS","COMMISSION","COMMISSIONMASTER","COMMISSIONPAY","COMMONTEXT",
             "COMPSTANDARDS","COMPSTDS","COMPTRIGGERS","CONFANSWER","CONFQUESTION","CONTRACT","CONTRDOC",
             "CONTYPES","COPYDETAIL","COSTRATE","COSTTYPE","CSTCTR","CUCONTRA","CURCODES","CURTABLE","CUST",
             "CUSTCONT","CUSTDEL","CUSTDEPOSIT","CUSTDESC","CUSTDISC","CUSTDISCDETAIL","CUSTDISCMASTER",
             "CUSTDOC","CUSTITEM","CUSTMENU","CUSTRENAMEHIST","CUSTSTATUS","CUSTTD","CUSTTDY","CUSTTERMS",
             "CUSTTI","CUSTTICA","CUSTTYPE","CUSTTYPEDISC","CUSTUDF","CUST_CREDIT_ALERT","CYCLECODE",
             "CYCLETIME","DAILYLOADING","DATADICTCONSTRAINTS","DATADICTFIELDS","DATADICTTABLES","DBA_SETTINGS",
             "DEFAULTMJ","DELETIONCODES","DEPARTMENTID","DEPEVENT","DEPOSIT","DESCCOSTING","DESCDOC",
             "DESCLASSIS","DESCRIPT","DESCTYPE","DISCBASIS","DISCCODE","DISPTYPE","DOCGROUPS",
             "DOCSTORE","EMPLOYEES","EMPLOYTYPE","ENTITY","EVENTDOC","EVENTHRC","EXPCLASS","EXPENSE",
             "EXPENSEDETL","EXPENSEHEAD","EXPENSEPAID","EXPENSEPAID_TEMP","EXPENSEPAY","EXPSUM","FEATUREREF",
             "FEATUREREFMAS","FEATURES","FORMULADETAIL","FORMULALIST","FORMULAVAR","FSETUP","GL",
             "GLACCOUNTCLASS","GLACCOUNTTYPES","GLACCTASSIGN","GLANALCOLS","GLANALSEL","GLANALYSIS"
             "GLBEGINBAL","GLBUDGET","GLBUDGETNO","GLCODES","GLCODES1","GLCODES2","GLEXCEPTION","GLFILE",
             "GLFILE1","GLFILE2","GLFILEARCHIVE","GLFILEARCHIVE1","GLFILEARCHIVE2","GLFILEPRINT","GLHIST",
             "GLINVDETAIL","GLINVSOURCE","GLJOURNAL","GLJOURNAL1","GLJOURNAL2","GLJOURNALDFT","GLJOURNALDFT1",
             "GLJOURNALDFT2","GLLEDPOSTHIST","GLMAINTYPE","GLMATCHDEFAULT","GLOUTPUTFORMAT","GLPERIODS",
             "GLPOSTLOCK","GLPOSTOPT","GLPOSTOPT1","GLPOSTOPT2","GLSETUP","GLSOURCEDFT","GLSOURCEDFT1",
             "GLSOURCEDFT1","GLSOURCEDFT2","GLSTD_ACCTASSIGN","GLSTD_CLASS","GLSTD_COA","GLSTD_GROUP",
             "GLSTRUCTURE","GLSTRUCTUREIMPT","GLSTRUCTURE_LOG","GLTYPES","GL_COACONVERT_TEMP",
             "GL_CONVERSION_HIST","GL_TRANSFER_DTL","GL_TRANSFER_HDR","GL_TRXNTYPE","ICATEG","ICATEGCOST",
             "IMGPATHS","IMPORT","IMPORTMAPPING","INCOMETYPES","INSURANPOLICY","INSURANVALUE","INVALID_LOCATIONNS",
             "INVDETL","INVDETLTAX","INVENTTYPES","INVFORMATS","INVOICE","IP","IPDET","ITEMCATALOGS",
             "ITEMCATDISC","ITEMCHAR","ITEMCODEDISC","ITEMCOST","ITEMH","ITEMHBAL","ITEMLEVELCODES",
             "ITEMPLAN","ITEMPOTEMP","ITEMSTATUS","ITEMTEMPLIST","ITEMUDF","ITEMUOM","ITEM_CALC_REORD",
             "ITEM_CAPACITY","ITEM_CHAR_DEF_HIST","ITEM_LOCATIONS","ITYPE","JOBCHARG","JOBDELETIONS",
             "JOBDOC","JOBLABORSETTINGS","JOBNOTES","JOBPRINTTXT","JOBREFERENCE","JOBSTATS",
             "JOBTYPE","JOB_DETL_RET","JOB_ISSUES","JOB_WIPVAR","KBDOC","KBTABLE","KITSETELEMENT","KPI",
             "LABORENTRY","LABORSETUP","LABOR_ACCTS","LABOURCODE","LEAD","LEDGERTRANS","LOCATIONCLASS",
             "LOCATIONS","LOCCLASS","LOCSTATUS","MACHINES","MAILBOXES","MAILFILES","MANUFACTURERS","MASTERLISTS",
             "MCONFIGRATION","MERCH_TSFR_DTL_D","MERCH_TSFR_DTL_p","MERCH_TSFR_HDR","MERCH_TSFR_UNTRANSF_D",
             "MERCH_TSFR_UNTRANSF_P","MODEL","MODELCATAGORY","MODELFORMULA","MODELGRP","MODELGRPLINE",
             "MODELKIT","MODELKITLINE","MODELINKBOM","MODELOPERATABLE","MODELOPERATE","MODELOPRES","MODELSETUP",
             "MODELSTAGE","MODELTASK","MODELUSER","MODLATTRIBUTE","MODLCALVALUE","MODLCONDITION","MODLFIXED",
             "MODLGROUP","MODLOPERATION","MODLOPERMATCH","MODLOPRES","MODLPRINTTXT","MODLRESOURCE","MODULE",
             "MOPTIONS","MRPSETUP","MVF","MVV","NONCHARG","NONSTD","NOTECODES","NOTETYPE","ODPERIOD","OPERATDEL",
             "OPERATIONBOM","OPERATIONS","OPTIONSELE","OPTYPES","OUTCONTACTS","OUTEVENTS","OUTRECORDIDS",
             "OUTRESOURCES","OUTTASKS","OVERHEAD_ACCTS","OWNERSHIP","PALMUSER","PAYMASTER","PAYMENT",
             "PAYMETHOD","PAYREGISTER","PAYROLL","PAYROLLSETUP","PAYTYPES","PAYTYPE_AR","PICKCHAR","PICKEDQTY",
             "POCHARTEMP","PODETL","POLICYDOC","PORDER","PORECS","POSETUP","POTYPES","PO_RECEIPTS","PO_REC_RET",
             "PREFERCE","PRICECODE","PROJDOC","PROJECTS","QUERIES","QUESTIONFOLLOW","QUESTIONLIST",
             "QUESTIONMATRIX","QUESTIONOPT","QUESTIONORDER","QUESTIONSUBORDER","RABTCHDT","RBATCH","RBTCHDT",
             "RBTCHHD","RB_FIELD","RB_FILTER","RB_FOLDER","RB_GROUPS","RB_ITEM","RB_JOIN","RB_TABLE",
             "RB_TBL_DESC","REACTION","REASON","RECONCIL","REDEMANDS","REMINDER","REPCOMMISSION","REPORTFOLDER",
             "REPORTNAME","REPS","REPTYPE","RESOLUTN","RESOURCES","RESPONS","RESPONSBLOCK","RESPONSEXCEPTION",
             "RESUGG","RESUPPLY","RPTSET_DETAIL","RPTSET_MASTER","RRDOC","RSLTNRSN","RSPNTYPE","SALECODE",
             "SALESBYPERIOD","SALESPAYTIME","SALESSETUP","SCATALOGGRP","SCATALOGNAME","SCHEDFIXED","SCHEDFREQ",
             "SCHEDLETTERS","SCHEDMAIN","SCHEDNOTES","SCONTACTS","SCREENDOC","SCRIPTERIMPORT","SERVICELABOR",
             "SETUP","SETUPPLAN","SEXPENSE","SHIPDETL","SHIPMASTER","SHIPMETHODS","SHIPPING","SHIPZONES",
             "SHOPRATESHIST","SPREADSHEETREPORT","SREGION","STAGE","STAGECOST","STAGE_CTGRY","STAGE_CTGRY_PRCS",
             "STATPRIC","STDETAIL","STMASTER","STRWORKTABLE","SUBCON_PROCESS","SUBCONTDOC","SUPPCODE",
             "SUPPDEL","SUPPDESC","SUPPDOC","SUPPEXPDETL","SUPPINV","SUPPINVDEL","SUPPINV_REV","SUPPITEM",
             "SUPPLIER","SUPPRENAMEHIST","SUPPSTATUS","SUPPTERMS","SUPPTYPE","SUPPUDF","SUREGION","SYS",
             "SYSTEMDEF","TABLES","TASK","TASKNOTE","TAXACT","TAXAUTHRT","TAXBAS","TAXDETAIL","TAXGRPS",
             "TAXORIGIN","TAXTABLE","TELLME","TEMPBALANCE","TEMPDATA","TEMPSALESBYPERIOD","TEMP_RPT_JOBCOST",
             "TIMESHEET","TIMESHTDTL","TIMESHTMST","TRANSFD","TRANSH","UFILTERDEFAULTS","UGROUP","UNITS",
             "USLOG","VACATIONS","VALWORKTABLE","VATRATES","VEND","VW_BOM_DEF_ROOTS","WARRANTY","WCRESOURCES",
             "WC_PRCS_TASK","WC_PROCESS","WEBLINKS","WFGROUPS","WORKCENTER","WORKCENTERTYPE","WORKFLOWLINKS",
             "WORKMASTSHIFT","WORKMASTSHIFT_DT","XITEMCODES","XITEMCODESLINK","XREFCODES"]


class FireBird:
    def __init__(self,path):
        self.path = path
        print "path",path
        self.con = firebirdsql.connect(dsn="localhost:"+path, user='sysdba', password='masterkey')
        self.cur = self.con.cursor()
        self.item = ""
        self.table = ""
        self.where = ""
        self.limit = ""
        self.retlist = []
        
        self.Items = [ ]
        self.cur.execute("SELECT ITEMCODE FROM ITEM")
        self.NoItems=0
        for row in self.cur:
            self.Items.append( str(row[0]) )
            self.NoItems +=1
        self.lastselect = ""
        self.Jobs = [ ]
        self.CJobs = [ ]
        self.SO = [ ]
        self.cur.execute("select JOBNO,JOBSTATS from JOBS")
        self.NoJobs=0
        self.NoCJobs=0
        self.NoSales=0
        for row in self.cur:
            if str(row[1]) == "CLOSED":
                self.CJobs.append( str(row[0]) )
                self.NoCJobs +=1
            else:
                if row[0][0] == "S":
                    self.SO.append( str(row[0]) )
                    self.NoSales +=1
                else:
                    self.Jobs.append( str(row[0]) )
                    self.NoJobs +=1
    def select(self,item,table="",where="",limit=10000):
        self.item = item
        self.table = table
        self.limit = limit
        self.where = where
        
        if table == "":
            exetext = item
        else:
            exetext = "select " + item + " from " + table + " " + where
            
        self.lastselect = exetext

        print exetext

        self.cur.close()
        self.cur = self.con.cursor()
        
        self.cur.execute(exetext)
        retlist = [ ]
        sublist = [ ]
        for fieldDesc in self.cur.description:
            sublist.append( fieldDesc[0] )
        retlist.append( sublist )
        
        fieldIndices = range(len(self.cur.description))
        x=0
        for row in self.cur:
            sublist = [ ]
            for fieldIndex in fieldIndices:
                sublist.append( str(row[fieldIndex]) )
            retlist.append( sublist )
            x +=1
            if x > (limit-1):
                break
        self.retlist = retlist            
        return retlist
    
class XMLFile:
    def __init__(self,path):
        self.path = path
        self.ID = ET.parse(path)
        self.root = self.ID.getroot()

class GUITreeNode:
    def __init__(self,path,_GUI):
        self.ID = -1  # will have GUI added here
        self.ctype = ""
        self.text = ""
        self.table = ""
        self.path = path
        self.qty = 1
        self.selected = 1 # of qty.
        self._GUI = _GUI
        self.XMLFileListNo = len(XMLFileList)-1
        self.extra = ""
        self.display=""

    def makedisplay(self,_GUI,newnode):
        if self.ctype == "ITEM":
            FB = XMLFileList[self.XMLFileListNo * -1]            
            self.display = self.text
            if "M" == FB.select( "MORP","ITEM", " where ITEMCODE like '" + self.text + "'" )[1][0]:
                _GUI.cicon = _GUI.iconITEM
            else:
                _GUI.cicon =_GUI.iconPODETL
        elif self.ctype == "TRANSFER":
            self.display = self.text
            _GUI.cicon = _GUI.iconTRANSFER
        elif self.ctype == "FILE":
            self.display = self.text
            _GUI.cicon = _GUI.iconFILE
        elif self.ctype == "":
            self.display = self.text       
        elif self.ctype == "PODETL":
            self.display = "x" + str(self.qty) + " " + self.text + "  " + self.extra
            _GUI.cicon = _GUI.iconPODETL
        elif self.ctype == "PORDER":
            self.display = self.text + " " + self.extra
            _GUI.cicon = _GUI.iconPORDER
        elif self.ctype == "JOBS":
            self.display = self.text + " (x" + str(self.qty) + ") " + self.extra
            _GUI.cicon = _GUI.iconJOBS
        elif self.ctype == "SALES":
            self.display = self.text + " " + self.extra
            _GUI.cicon = _GUI.iconSALES
        elif self.ctype == "SUBITEM":
            FB = XMLFileList[self.XMLFileListNo * -1]               
            self.display = "[x" + str(self.qty) + "] " + self.text
            if "M" == FB.select( "MORP","ITEM", " where ITEMCODE like '" + self.text + "'" )[1][0]:
                _GUI.cicon = _GUI.iconSUBITEM
            else:
                _GUI.cicon =_GUI.iconPODETL            
        elif self.ctype == "HEADING":
            self.display = self.text + "[" + str(self.qty) + "]"
            _GUI.cicon = _GUI.iconHEADING
        elif self.ctype == "METHOD":
            self.display = "[" + str(self.qty) + "] " + self.text + "{" + self.extra + "}"
            _GUI.cicon = _GUI.iconMETHOD
        elif self.ctype == "XML":
            _GUI.cicon = _GUI.iconXML            
            if self.qty > 1:
                self.display = "<" + self.text + ">[" + str(self.selected) + "/" + str(self.qty) + "]"
            else:
                self.display = "<" + self.text + ">"
        else:
            self.display = self.text + " Error " + self.ctype

    def gettext(self):
        return self._GUI.Tree.GetItemText( self.ID )
    
def initXMLTree(_GUI):
    global html_header,html_footer,html_itemm, html_itemp ,html_bomstages
    XMLPathList.append( "Root" )
    root = GUITreeNode( "Root" ,_GUI)
    root.ID = _GUI.Tree.AddRoot('Root')
    root.text = "Root"
    root.XMLFileListNo = -999
 
    NodeList.append( root )
    
    XMLPathList.append( "XML-Files" )
    XML = GUITreeNode( "XML-Files" ,_GUI)
    XML.ID = _GUI.Tree.AppendItem( root.ID , "XML-Files")
    XML.text = "XML-Files"
    XML.XMLFileListNo = -999
    XML.ctype = "FILE"
    NodeList.append( XML )
    _GUI.Tree.SetPyData(XML.ID, None)
    _GUI.Tree.SetItemImage(XML.ID, _GUI.iconLABEL , wx.TreeItemIcon_Normal)     
    
    XMLPathList.append( "DBA-Database" )
    DBA = GUITreeNode( "DBA-Database" ,_GUI)
    DBA.ID = _GUI.Tree.AppendItem( root.ID , "DBA-Database")
    DBA.text = "DBA-Database"
    DBA.XMLFileListNo = -999
    DBA.ctype = "FILE"
    NodeList.append( DBA )
    _GUI.Tree.SetPyData(DBA.ID, None)
    _GUI.Tree.SetItemImage(DBA.ID, _GUI.iconLABEL , wx.TreeItemIcon_Normal)       
    
    OpenXMLFile(_GUI,SettingsPath)
    _GUI.Update()
    
    html_header = FromSettings("./Html/Header")
    html_footer = FromSettings("./Html/Footer")
    html_itemm = FromSettings("./Html/ITEMM")
    html_itemp = FromSettings("./Html/ITEMP")    
    html_bomstages = FromSettings("./Html/BOMSTAGES")
    temp_path = FromSettings("./DBAFiles/TempPath")
    Training_path = FromSettings("./DBAFiles/Training")
    Main_path = FromSettings("./DBAFiles/Main")
    
    if os.path.isfile(temp_path + "\\Training.FDB"):
        os.remove(temp_path + "\\Training.FDB")
    if os.path.isfile(temp_path + "\\Main.FDB"):
        os.remove(temp_path + "\\Main.FDB")
    shutil.copy2(Training_path, temp_path + "\\Training.FDB")
    shutil.copy2(Main_path, temp_path + "\\Main.FDB")
    OpenDBAFile(_GUI,temp_path + "\\Training.FDB","Training")
    OpenDBAFile(_GUI,temp_path + "\\Main.FDB","Main")
###################################################  definition end #############################################################################################


parseStr = lambda x: x.isalpha() and x or x.isdigit() and int(x) or x.isalnum() and x or len(set(string.punctuation).intersection(x)) == 1 and x.count('.') == 1 and float(x) or x

def formattime( seconds ):
    minutes = 0
    hours = 0
    rettext = ""
    if seconds > 60:
        minutes = int(seconds/60.0)
        if minutes > 60:
            hours = int(minutes/60.0)
            rettext += str(hours) + " Hr"
            minutes = int(seconds/60.0)-hours*60
        if minutes > 0:
            rettext += " " + str(minutes) + " Min"
        seconds -= hours*60*60+minutes*60
    if seconds > 0 and hours == 0:
        rettext += " " + str(seconds) + " Sec"
    return rettext

def UpdateHTMLDisplay(cNode,_GUI,qmult=1):
    FB = XMLFileList[cNode.XMLFileListNo * -1]
    table = FB.table
    html_body = UpdateHTMLDisplayRecursive(cNode.text,cNode,_GUI,qmult)
    html_code = html_header + html_body + html_footer
    _GUI.Display_HTML.SetPage(html_code)
    _GUI.Display_Source.SetValue(html_code)
    print html_code
    
def UpdateHTMLDisplayRecursive(Itm , cNode , _GUI,qmult=1,indent = 1):
    global html_header,html_footer,html_itemm,html_itemp ,html_bomstages
    FB = XMLFileList[cNode.XMLFileListNo * -1]
    table = FB.table
####################################### First Do ITEM #########################    
    selectlist = FromSettings("./Tables/ITEM").replace(" ","").split(",")
    for each in ["PICTURE","MORP"]:
        if each not in selectlist:
            selectlist.append( each )
    retlist = FB.select(",".join(selectlist),"ITEM","where ITEMCODE='" + Itm + "'")[1]
    if retlist[ selectlist.index("MORP") ] == "M":
        ret = html_itemm[:]
    else:
        ret = html_itemp[:]
    x=0
    for each in selectlist:
        if each == "PICTURE":
            retlist[x] = retlist[x].replace("\\","/")
            if not os.path.isfile(retlist[x]):
                retlist[x] = SysPath.replace("\\\\","/") + "/Icons/NA-48.png"
        ret = ret.replace("{" + each + "}",retlist[x])
        x += 1
####################################### Then Do BOMSTAGES #########################
    cBOMMNO = FB.select("BOMMNO","BOMMASTER","where PITEMCODE='" + Itm + "'")
    if len(cBOMMNO) > 1:
        cBOMMNO = str(cBOMMNO[1][0])
        selectlist = FromSettings("./Tables/BOMSTAGES").replace(" ","").split(",")
        for each in ["STAGE"]:
            if each not in selectlist:
                selectlist.append( each )        
        retlist = FB.select( ",".join(selectlist),"BOMSTAGES"," where BOMMNO=" + cBOMMNO, int( FromSettings("./Tables/DQTY") ) )[1:]
        for rlist in retlist:
            mret = html_bomstages[:]
            x=0
            for each in selectlist:
                mret = mret.replace("{"+ each + "}",rlist[x])
                x += 1

            ret += mret
            subs = FB.select( "USAGE,CITEMCODE", "BOMDEL", " where PITEMCODE='" + Itm + "' AND STAGEID=" + str(rlist[ selectlist.index("STAGE") ] ))[1:]
            for esub in subs:
                ret += UpdateHTMLDisplayRecursive( esub[1] , cNode , _GUI, qmult* float( esub[0] ) , indent+1 )
    ret = ret.replace("{SYSPATH}",SysPath.replace("\\\\","/"))
    ret = ret.replace("{INDENT}",str(indent))                  
    return ret
#if retlist[ selectlist.index("MORP") ] == "M"

def MSubElement(ParentID,ElementName,Value=""):
    newele = ET.SubElement(ParentID,ElementName)
    if Value <> "":
        newele.text = Value
    return newele

 
def addnode(path,_GUI,ctype="",table="",qty=1,extra="",mult=1):
    newnode = GUITreeNode(path,_GUI)
    
    x = path.rfind("/")
    newnode.text = path[x+1:]
    newnode.ctype = ctype
    newnode.table = table
    newnode.qty = qty
    newnode.extra = extra
    if mult == -1:
        newnode.XMLFileListNo = newnode.XMLFileListNo * -1
    
    if XMLPathList.count( path[:x] ) > 0:
        XMLPathList.append( path )        
        parentID = NodeList[ XMLPathList.index( path[:x] ) ].ID
        newnode.makedisplay(_GUI,newnode)
        newnode.ID = _GUI.Tree.AppendItem( parentID , newnode.display )
        
        _GUI.Tree.SetPyData(newnode.ID , None)
        _GUI.Tree.SetItemImage(newnode.ID , _GUI.cicon , wx.TreeItemIcon_Normal)        
        
        NodeList.append(newnode)
    else:
        _GUI.NError("ERROR: could not find path:\n" + path)
    return newnode


def GetNodeFromTreeItem(_GUI, itm ):
    x = 0
    for each in NodeList:
        if each.ID == itm:
            return each
        else:
            x += 1
    return x

def GetCurrentXMLNode(_GUI):
    Sel_ID = _GUI.Tree.GetSelection()
    x = 0
    for each in NodeList:
        if each.ID == Sel_ID:
            break
        else:
            x += 1
    return NodeList[x]     

def UpdateXMLDisplay_xpath(xpath,_GUI):
    cNode = GetCurrentXMLNode(_GUI)

    _GUI.XMLGrid.ClearGrid()    
    line = 0
    _GUI.text_xpath.ChangeValue( xpath )
    
    element = XMLFileList[ cNode.XMLFileListNo ].ID.find( xpath )
    
    _GUI.XMLGrid.SetCellValue(line,1,element.tag + str(element.attrib))
    for child in element:
        _GUI.XMLGrid.SetCellValue(line,2,child.tag)
        _GUI.XMLGrid.SetCellValue(line,3,str(child.attrib))
        _GUI.XMLGrid.SetCellValue(line,4,child.text)
        line += 1
        if line > 99:
            break
    
def UpdateByHslider(_GUI):
    cNode = GetCurrentXMLNode(_GUI)
    cNode.selected = _GUI.Hslider.GetValue()
    UpdateXMLDisplay(_GUI)
    cNode.settext("")


def AddFilter(_GUI):
    cNode = GetCurrentXMLNode(_GUI)
    FB = XMLFileList[cNode.XMLFileListNo * -1]
    table = FB.table
    print "add filter clicked"
    
    FBList = FB.retlist[1:]
    
    if cNode.text == "POrders":
        for each in FBList:
            addnode(cNode.path + "/" + each[0],_GUI,"PORDER",table,1,each[1],-1)
            POList = FB.select( "QTY,REFERENCE,SUPPPARTNO","PODETL"," where PONUM like '" + each[0] + "'" )
            if len(POList) > 1:
                for LI in POList[1:]:
                    addnode(cNode.path + "/" + each[0] + "/" + LI[1],_GUI,"PODETL",table,LI[0],LI[2],-1)
    
    if cNode.text == "SalesOrders":
        for each in FB.retlist[1:]:
            addnode(cNode.path + "/" + each[0],_GUI,"SALES",table,1,each[4],-1)
            for subeach in FB.select("QTY,REFID","JOBDETL"," where JOBNO like '" + each[0] + "'")[1:]:
                addnode(cNode.path + "/" + each[0] + "/" + subeach[1],_GUI,"SUBITEM",table,subeach[0],"",-1)

    if cNode.text == "Jobs":
        for each in FB.retlist[1:]:
            string = each[1]
            a = string.find(" - ")
            astr = string[:a]
            string = string[a+3:]
            a = string.find(" - ")
            addnode(cNode.path + "/" + each[0],_GUI,"JOBS",table,int( string[:a] ),string[a+3:],-1)

    if cNode.text == "Items":
        for each in FB.retlist[1:]:
            addnode(cNode.path + "/" + each[0],_GUI,"ITEM",table,1,"",-1)
            cBOMMNO = FB.select("BOMMNO","BOMMASTER","where PITEMCODE='" + each[0] + "'")
            if len(cBOMMNO) > 1:
                cBOMMNO = cBOMMNO[1][0]
                cSTAGES = FB.select( "STAGE,DESCRIPT,WORKCENTERNAME" , "BOMSTAGES", " where BOMMNO=" + str(cBOMMNO) , int( FromSettings("./Tables/DQTY") ) )[1:]
                for eSTAGE in cSTAGES:
                    addnode(cNode.path + "/" + each[0] + "/" + eSTAGE[2],_GUI,"METHOD",table,int(eSTAGE[0]),eSTAGE[1],-1)
                    subs = FB.select( "USAGE,CITEMCODE", "BOMDEL", " where PITEMCODE='" + each[0] + "' AND STAGEID=" + str( int( eSTAGE[0] ) ))[1:]
                    for esub in subs:
                        addnode(cNode.path + "/" + each[0] + "/" + eSTAGE[2] + "/" + esub[1],_GUI,"SUBITEM",table,esub[0],"",-1)

def Filter(_GUI):
    cNode = GetCurrentXMLNode(_GUI)
    FB = XMLFileList[cNode.XMLFileListNo * -1]
    atext = ""
    
    cb1 = _GUI.combo_box_1.GetValue()
    if cb1 <> "":
        cb2 = _GUI.combo_box_2.GetValue()
        cb3 = _GUI.combo_box_3.GetValue()
        atext = " where " + cb1 + " " + cb2 + " '" + cb3 + "'"
        cb4 = _GUI.combo_box_4.GetValue()

        if cb4 <> "":
            cb5 = _GUI.combo_box_5.GetValue()
            cb6 = _GUI.combo_box_6.GetValue()
     
            atext = "{0} AND where {1} {2} '{3}'".format(atext,cb4,cb5,cb6)
        GridList = FB.select( FB.item, FB.table , atext , FB.limit )
        _GUI.DBAGridUpdate( GridList , FB )

def UpdateDBADisplay_Query( Query, _GUI):
    cNode = GetCurrentXMLNode(_GUI)
    FB = XMLFileList[cNode.XMLFileListNo * -1]    

    GridList = FB.select( Query , "", "" , int( FromSettings("./Tables/DQTY") ) )
    _GUI.DBAGridUpdate( GridList , FB )
    _GUI.Tree_Tabs.ChangeSelection(1)      

def TreeEvent(_GUI):
    cNode = GetCurrentXMLNode(_GUI)
    _GUI.text_expansion.ChangeValue( cNode.path + " (type='" + cNode.ctype + "')")

    if cNode.XMLFileListNo == -999:
        _GUI.XMLGrid.ClearGrid()        
        _GUI.text_path.ChangeValue( "<No XML File Selected>" )
        _GUI.text_xpath.ChangeValue( "<No XML File Selected>" )
        _GUI.HPos.ChangeValue("1/1")
    elif cNode.XMLFileListNo > -1:
        cXMLFile = XMLFileList[ cNode.XMLFileListNo ]      
        _GUI.text_path.ChangeValue( cXMLFile.path )

        count = cNode.path.count("/")

        if count == 0: # must have clicked XML-Files
            _GUI.XMLGrid.ClearGrid()
        elif count == 1: # must have clicked MCS.xml
            _GUI.XMLGrid.ClearGrid()
        elif count == 2: # must have clicked MPL
            xpath = "."
            _GUI.HPos.SetValue(str(cNode.selected) + "/" + str(cNode.qty))
            _GUI.Hslider.SetRange( 1, cNode.qty)
            _GUI.Hslider.SetValue(cNode.selected)
            UpdateXMLDisplay_xpath(xpath,_GUI)
        else:
            x = cNode.path.find("/")
            x = cNode.path.find("/",x+1)
            x = cNode.path.find("/",x+1)
            print cNode.path,cNode.path[x+1:],x
            xpath = "./" + cNode.path[x+1:] + "[" + str(cNode.selected) + "]"
            _GUI.HPos.SetValue(str(cNode.selected) + "/" + str(cNode.qty))
            _GUI.Hslider.SetRange( 1, cNode.qty)
            _GUI.Hslider.SetValue(cNode.selected)
        
            UpdateXMLDisplay_xpath(xpath,_GUI)
    else:
        FB = XMLFileList[cNode.XMLFileListNo * -1]
        if cNode.text[:5] == "Items":
            print "Items"
            GridList = FB.select( FromSettings("./Tables/ITEM") , "ITEM", "" , int( FromSettings("./Tables/DQTY") ) )
            _GUI.DBAGridUpdate( GridList , FB )
            _GUI.Tree_Tabs.ChangeSelection(1)
        elif cNode.text[:7] == "POrders":
            print "POrders"
            GridList = FB.select( "PONUM,SUPPNAME,RAISDATE,ADDR1,REGION,STATUS","PORDER"," where STATUS <> 'Closed'", int( FromSettings("./Tables/DQTY") )  )
            _GUI.DBAGridUpdate( GridList , FB )
            _GUI.Tree_Tabs.ChangeSelection(1)            
        elif cNode.text[:5] == "Sales":
            print "Sales Orders"
            GridList = FB.select( FromSettings("./Tables/JOBS") , "JOBS", "  where JOBNO LIKE 'S%' AND JOBSTATS='ORDERED'" , int( FromSettings("./Tables/DQTY") ) )
            _GUI.DBAGridUpdate( GridList , FB )
            _GUI.Tree_Tabs.ChangeSelection(1)
        elif cNode.text[:4] == "Jobs":
            print "Jobs"
            GridList = FB.select( FromSettings("./Tables/JOBS") , "JOBS", "    where JOBNO LIKE 'M%' AND JOBSTATS <> 'CLOSED' AND JOBSTATS <> 'FINISHED'" , int( FromSettings("./Tables/DQTY") ) )
            _GUI.DBAGridUpdate( GridList , FB )
            _GUI.Tree_Tabs.ChangeSelection(1)            
        elif cNode.text[:6] == "Closed":
            print "Closed"
        elif (cNode.ctype == "ITEM") or (cNode.ctype == "SUBITEM"):
            UpdateHTMLDisplay(cNode,_GUI)
            _GUI.Tree_Tabs.ChangeSelection(2)
            if cNode.ctype == "SUBITEM":
                if _GUI.Tree.ItemHasChildren(cNode.ID):
                    return 1
                else:
#                _GUI.MsgBox("SubItem","SubItem- has NO Children")
                    cNode = GetCurrentXMLNode(_GUI)
                    FB = XMLFileList[cNode.XMLFileListNo * -1]
                    table = FB.table

                    cBOMMNO = FB.select("BOMMNO","BOMMASTER","where PITEMCODE='" + cNode.text + "'")
                    if len(cBOMMNO) > 1:
                        cBOMMNO = cBOMMNO[1][0]
                        cSTAGES = FB.select( "STAGE,DESCRIPT,WORKCENTERNAME" , "BOMSTAGES", " where BOMMNO=" + str(cBOMMNO) , int( FromSettings("./Tables/DQTY") ) )[1:]
                        for eSTAGE in cSTAGES:
                            addnode(cNode.path + "/" + eSTAGE[2],_GUI,"METHOD",table,int(eSTAGE[0]),eSTAGE[1],-1)
                            print "error checking ---" + cNode.path + "/" + eSTAGE[2]
                            subs = FB.select( "USAGE,CITEMCODE", "BOMDEL", " where PITEMCODE='" + cNode.text + "' AND STAGEID=" + str( int( eSTAGE[0] ) ))[1:]
                            for esub in subs:
                                addnode(cNode.path + "/" + eSTAGE[2] + "/" + esub[1],_GUI,"SUBITEM",table,esub[0],"",-1)                
        else:
            print "whatd your click?",cNode.text,cNode.table
def FromSettings( xpath ):
    return XMLFileList[0].ID.find( xpath ).text

def OpenDBAFile(_GUI,filename="",dbname="Other"):
    if filename == "":
        filename = _GUI.OpenDBAFiles()
        filename = filename[0]

    FB = FireBird(filename)
    XMLFileList.append( FB )
    addnode("DBA-Database/" + dbname,_GUI,"FILE","",1,"",-1)
    addnode("DBA-Database/" + dbname + "/Items",_GUI,"HEADING","",FB.NoItems,"",-1)
    addnode("DBA-Database/" + dbname + "/SalesOrders",_GUI,"HEADING","",FB.NoSales,"",-1)    
    addnode("DBA-Database/" + dbname + "/Jobs",_GUI,"HEADING","",FB.NoJobs,"",-1)
    addnode("DBA-Database/" + dbname + "/Closed_Jobs",_GUI,"HEADING","",FB.NoCJobs,"",-1)
    addnode("DBA-Database/" + dbname + "/POrders",_GUI,"HEADING","",FB.NoCJobs,"",-1)
    addnode("DBA-Database/" + dbname + "/Transfer",_GUI,"TRANSFER","",1,"",-1)
    
    
    
    
    
    

def OpenXMLFile(_GUI,filename):

    XMLF = XMLFile( filename )
    XMLFileList.append( XMLF )

    Lfile = filename[filename.rfind("\\")+1:]
   
    addnode("XML-Files/" + Lfile,_GUI,"FILE")
    MakePathList(  XMLF.root.findall(".") ,"XML-Files/" + Lfile,_GUI)

def MakePathList( pathlist , prefix,_GUI):
    for child in pathlist:
        path = prefix + "/" + child.tag
        if path in XMLPathList:
            NodeList[ XMLPathList.index(path) ].qty += 1
        else:
            addnode(path,_GUI,"XML")
        MakePathList( child , prefix + "/" + child.tag,_GUI)



    
