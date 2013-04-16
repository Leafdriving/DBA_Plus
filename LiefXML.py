
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
import DBA_Manu
from jinja2 import Template

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
        self.DB = DBA_Manu.DBA(path)
        self.TM_INTreeOUT = [ ]
        self.TM_IUTreeOUT = [ ]
        self.TM_IMTreeOUT = [ ]
        self.TM_ICTreeOUT = [ ]
        self.MT_INTreeOUT = [ ]
        self.MT_IUTreeOUT = [ ]
        self.MT_IMTreeOUT = [ ]
        self.MT_ICTreeOUT = [ ]
        
        self.Items = [ ]
        self.cur.execute("SELECT ITEMCODE FROM ITEM")
        self.NoItems=0
        for row in self.cur:
            self.Items.append( str(row[0]) )
            self.NoItems +=1
        self.lastselect = ""
        self.lastpreselect = ""
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
    def select(self,item,table="",where="",limit=10000,_GUI = -1):
        self.item = item
        self.table = table
        self.limit = limit
        self.where = where
        
        if table == "":
            exetext = item
        else:
            exetext = "SELECT " + item + " FROM " + table + " " + where
        
        self.lastselect = exetext
        

        print "Select Search Called:",exetext
        if _GUI != -1:
            _GUI.NEvent("SQL CALL: " + exetext)

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
        if _GUI != -1:        
            _GUI.NEvent("(" + str(len(retlist[0])) + " Columns x" +str(len(retlist)-1) + " Rows=  " + str( len(retlist[0])*(len(retlist)-1) ) + " entries returned)")
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
        self.DB = ""

    def makedisplay(self,_GUI,newnode):
        if self.ctype == "ITEM":
            FB = XMLFileList[self.XMLFileListNo * -1]
#            DB = FB.DB
#            self.DB = DB.Item(self.text)
            self.display = self.text
            temp = FB.select( "MORP","ITEM", " where ITEMCODE like '" + self.text + "'" )
            if len(temp) > 1:
                if "M" == FB.select( "MORP","ITEM", " where ITEMCODE like '" + self.text + "'" )[1][0]:
                    _GUI.cicon = _GUI.iconITEM
                else:
                    _GUI.cicon =_GUI.iconPODETL
            else:
                _GUI.cicon =_GUI.iconERROR
                _GUI.NError("Item Select: '" + self.text + "' is Neither M or P ??")
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
            rmorp = FB.select( "MORP","ITEM", " where ITEMCODE like '" + self.text + "'" )
            if len(rmorp) <= 1:
                print "Error - " + self.text + " returned empty"
                _GUI.cicon =_GUI.iconPODETL
            else:
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
    _GUI.SetStatus("Populating Internal Database...")
    _GUI.Progress1(2,6)
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
    
    _GUI.SetStatus("Reading Settings File")
    _GUI.Progress1(3,6)
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

    for tree in [ _GUI.TM_INTree, _GUI.MT_INTree, _GUI.TM_IUTree, _GUI.MT_IUTree , _GUI.TM_IMTree , _GUI.MT_IMTree,_GUI.TM_ICTree,_GUI.MT_ICTree]:
        tree.AddColumn("Transfer")
    for each in FromSettings("./Transfer/ITEM").split(','):
        for tree in [ _GUI.TM_INTree, _GUI.MT_INTree, _GUI.TM_IUTree, _GUI.MT_IUTree ]:
            tree.AddColumn(each)

    _GUI.TM_INTreeRoot = _GUI.TM_INTree.AddRoot("Root")
    _GUI.MT_INTreeRoot = _GUI.MT_INTree.AddRoot("Root")    
    _GUI.TM_IUTreeRoot = _GUI.TM_IUTree.AddRoot("Root")    
    _GUI.MT_IUTreeRoot = _GUI.MT_IUTree.AddRoot("Root")     

    for each in FromSettings("./Transfer/BOMSTAGES").split(','):
        if str(each) == "BOMMNO":
            _GUI.TM_IMTree.AddColumn("ITEMCODE")
            _GUI.MT_IMTree.AddColumn("ITEMCODE")             
        else:
            _GUI.TM_IMTree.AddColumn(str(each))
            _GUI.MT_IMTree.AddColumn(str(each))        
    _GUI.TM_IMTreeRoot = _GUI.TM_IMTree.AddRoot("Root")    
    _GUI.MT_IMTreeRoot = _GUI.MT_IMTree.AddRoot("Root")      

  
    for each in FromSettings("./Transfer/BOMDEL").split(','):
        _GUI.TM_ICTree.AddColumn(str(each))
        _GUI.MT_ICTree.AddColumn(str(each))        
    _GUI.TM_ICTreeRoot = _GUI.TM_ICTree.AddRoot("Root")    
    _GUI.MT_ICTreeRoot = _GUI.MT_ICTree.AddRoot("Root")

    x=0
    for width in FromSettings("./Transfer/ITEMCOLWIDTH").split(','):
        for tree in [_GUI.TM_INTree, _GUI.MT_INTree,_GUI.TM_IUTree,_GUI.MT_IUTree]:
            tree.SetColumnWidth(x,int(width))
        x +=1      

    x=0
    for width in FromSettings("./Transfer/BOMSTAGESCOLWIDTH").split(','):
        _GUI.TM_IMTree.SetColumnWidth(x,int(width))
        _GUI.MT_IMTree.SetColumnWidth(x,int(width))
        x +=1

    x=0
    for width in FromSettings("./Transfer/BOMDELCOLWIDTH").split(','):
        _GUI.TM_ICTree.SetColumnWidth(x,int(width))
        _GUI.MT_ICTree.SetColumnWidth(x,int(width))
        x +=1            
    _GUI.SetStatus("Reading DBA Training")
    _GUI.Progress1(4,6)
    OpenDBAFile(_GUI,temp_path + "\\Training.FDB","Training")
    _GUI.SetStatus("Reading DBA Main")
    _GUI.Progress1(4,6)    
    OpenDBAFile(_GUI,temp_path + "\\Main.FDB","Main")
    _GUI.Progress1(0,6)      
    
    
###################################################  definition end #############################################################################################




parseStr = lambda x: x.isalpha() and x or x.isdigit() and int(x) or x.isalnum() and x or len(set(string.punctuation).intersection(x)) == 1 and x.count('.') == 1 and float(x) or x

def writeCSS(fulllist,filename):
    delm = "|"
    out = ""
    for lst in fulllist:
        for item in lst[:-1]:
            out += item + delm
        out += lst[-1] + "\n"
    f = open(filename,'w')
    f.write(out)     
    f.close()

def Transfer():
    FB = XMLFileList[1]
    writeCSS(FB.TM_INTreeOUT,FromSettings("./DBAFiles/TempPath")+"\\NewItem.csv")
    writeCSS(FB.TM_IUTreeOUT,FromSettings("./DBAFiles/TempPath")+"\\UpdateItem.csv")
    writeCSS(FB.TM_IMTreeOUT,FromSettings("./DBAFiles/TempPath")+"\\Method.csv")
    writeCSS(FB.TM_ICTreeOUT,FromSettings("./DBAFiles/TempPath")+"\\Component.csv")    

def UpdateTransfer(cNode,_GUI):
    if cNode.XMLFileListNo == -2:
        print "From Training"
        DB = XMLFileList[2].DB
        ODB = XMLFileList[1].DB
    elif cNode.XMLFileListNo == -1:
        print "From Main"
        DB = XMLFileList[1].DB
        ODB = XMLFileList[2].DB
    else:
        print "From Where????"

    UpdateTransferFillItemTree(_GUI.TM_INTree , _GUI.TM_INTreeRoot,DB,ODB,cNode.text,1,_GUI)
    _GUI.TM_INTree.ExpandAll(_GUI.TM_INTreeRoot)
    
    UpdateTransferFillItemTree(_GUI.TM_IUTree , _GUI.TM_IUTreeRoot,DB,ODB,cNode.text,2,_GUI)
    _GUI.TM_IUTree.ExpandAll(_GUI.TM_IUTreeRoot)

    UpdateTransferFillItemTree(_GUI.TM_IMTree , _GUI.TM_IMTreeRoot,DB,ODB,cNode.text,3,_GUI)
    _GUI.TM_IMTree.ExpandAll(_GUI.TM_IMTreeRoot)
    
    UpdateTransferFillItemTree(_GUI.TM_ICTree , _GUI.TM_ICTreeRoot,DB,ODB,cNode.text,4,_GUI)
    _GUI.TM_ICTree.ExpandAll(_GUI.TM_ICTreeRoot)    

    
def SetMethodData(CTree,cNode,Method,DB,ODB,cITEMCODE):
    s = FromSettings("./Transfer/BOMSTAGES") 
    sl = s.split(',')
    dbBOMMNO = DB.select("BOMMNO","BOMMASTER","WHERE PITEMCODE LIKE '" + cITEMCODE + "'")[1][0]
    odbBOMMNO = ODB.select("BOMMNO","BOMMASTER","WHERE PITEMCODE LIKE '" + cITEMCODE + "'")
    AI = False # Already Identical
    dbs = [ ]
    o0dbs = [ ]
    if len(odbBOMMNO) > 1:
        odbBOMMNO = odbBOMMNO[1][0]
        dbs  =  DB.select(s,"BOMSTAGES"," WHERE STAGE LIKE '" + Method.dic[ "STAGE" ] + "' AND BOMMNO = " + dbBOMMNO + "")[1]
        odbs  =  ODB.select(s,"BOMSTAGES"," WHERE STAGE LIKE '" + Method.dic[ "STAGE" ] + "' AND BOMMNO = " + odbBOMMNO + "")
        if len(odbs) > 1:
            odbs = odbs[1]
            if dbs == odbs:
                AI = True
    if AI:
        for x in [1,2,3]:
            if sl[x-1] != "BOMMNO":
                CTree.SetItemText( cNode , dbs[x-1],x)
            else:
                CTree.SetItemText( cNode , cITEMCODE,x)
        CTree.SetItemText( cNode , "Already Identical",4)
        CTree.SetItemTextColour( cNode, "GRAY")
    else:
        x=1
        templist = [ ]
        for each in sl:
            if sl[x-1] != "BOMMNO":
                if dbs == [ ]:
                    CTree.SetItemText( cNode ,  "Error" , x )
                else:
                    CTree.SetItemText( cNode ,  dbs[x-1] , x )
                    templist.append( dbs[x-1] )
            else:
                CTree.SetItemText( cNode ,  cITEMCODE , x )
                templist.append( cITEMCODE )
            x += 1
        XMLFileList[1].TM_IMTreeOUT.append( templist )
        CTree.SetItemTextColour( cNode, "BLUE")           

        
def SetSubItemData(CTree,cNode,CItem,DB,ODB,pNode):
    s = FromSettings("./Transfer/BOMDEL") 
    sl = s.split(',')
    dbs  =  DB.select(s,"BOMDEL"," WHERE PITEMCODE LIKE '" + CTree.GetItemText(pNode) + "' AND CITEMCODE LIKE '" + CTree.GetItemText(cNode) + "'")
    odbs  =  ODB.select(s,"BOMDEL"," WHERE PITEMCODE LIKE '" + CTree.GetItemText(pNode) + "' AND CITEMCODE LIKE '" + CTree.GetItemText(cNode) + "'")    
    if len(dbs) != 1:
        if dbs == odbs:
            dbs = dbs[1]
            for x in [1,2,3]:
                CTree.SetItemText( cNode ,  dbs[x-1] , x )
            CTree.SetItemText( cNode ,  "Already Identical"  , 4 )
            CTree.SetItemTextColour( cNode, "GRAY")
        else:
            dbs = dbs[1]
            x=1
            templist = [ ]
            for each in sl:
                CTree.SetItemText( cNode ,  dbs[x-1] , x )
                templist.append( dbs[x-1] )
                x += 1
            XMLFileList[1].TM_ICTreeOUT.append( templist )
            CTree.SetItemTextColour( cNode, "BLUE")

def SetItemData(CTree,cNode,CItem,DB,ODB,Type):
    FB = XMLFileList[1]    
    S = FromSettings("./Transfer/ITEM").split(',')
    IsItem = ODB.IsItem(CItem.Field(S[0]))    
    if Type == 1:
        if IsItem:
            CTree.SetItemText( cNode ,  CItem.Field(S[0]) , 1 )
            CTree.SetItemText( cNode ,  CItem.Field(S[1]) , 2 )
            CTree.SetItemText( cNode ,  "Already" , 4 )
            CTree.SetItemText( cNode ,  "Exists" , 6 )            
            CTree.SetItemTextColour( cNode, "GRAY")
        else:
            CTree.SetItemTextColour( cNode, "BLUE")            
            x=1
            templist = [ ]
            for each in S:
                CTree.SetItemText( cNode ,  CItem.Field(each) , x )
                templist.append( CItem.Field(each) )
                x += 1
            FB.TM_INTreeOUT.append( templist )
    elif Type == 2:
        if IsItem:
            dbs  =  DB.select(FromSettings("./Transfer/ITEM"),"ITEM"," WHERE ITEMCODE LIKE '" + CItem.Field(S[0]) + "'")
            odbs = ODB.select(FromSettings("./Transfer/ITEM"),"ITEM"," WHERE ITEMCODE LIKE '" + CItem.Field(S[0]) + "'")
            if dbs == odbs:
                CTree.SetItemText( cNode ,  CItem.Field(S[0]) , 1 )
                CTree.SetItemText( cNode ,  CItem.Field(S[1]) , 2 )
                CTree.SetItemText( cNode ,  "Already" , 4 )
                CTree.SetItemText( cNode ,  "Identical" , 6 )            
                CTree.SetItemTextColour( cNode, "GRAY")   
            else:
                CTree.SetItemTextColour( cNode, "BLUE")            
                x=1
                templist = [ ]
                for each in S:
                    CTree.SetItemText( cNode ,  CItem.Field(each) , x )
                    templist.append( CItem.Field(each) )
                    x += 1
                FB.TM_IUTreeOUT.append( templist )
        else:
            CTree.SetItemText( cNode ,  CItem.Field(S[0]) , 1 )
            CTree.SetItemText( cNode ,  CItem.Field(S[1]) , 2 )
            CTree.SetItemText( cNode ,  "New" , 4 )
            CTree.SetItemText( cNode ,  "Item" , 6 )            
            CTree.SetItemTextColour( cNode, "GRAY")            
            
    elif Type == 3:
        pass
    elif Type == 4:
        pass
   

def UpdateTransferFillItemTree(CTree,cNodeParent,DB,ODB,cITEMCODE,Type,_GUI,Firstloop = True):
    CItem = DB.Item(cITEMCODE)
    
    if Type == 3:
        if Firstloop:
            cNode = CTree.AppendItem( cNodeParent , CItem.Field("ITEMCODE") )
            CTree.SetPyData(cNode , None)
            CTree.SetItemImage(cNode , _GUI.iconITEM , wx.TreeItemIcon_Normal)                 
            cNodeParent = cNode
    else:
        cNode = CTree.AppendItem( cNodeParent , CItem.Field("ITEMCODE") )
        CTree.SetPyData(cNode , None)
        if Firstloop:
            CTree.SetItemImage(cNode , _GUI.iconITEM , wx.TreeItemIcon_Normal)
        else:
            CTree.SetItemImage(cNode , _GUI.iconSUBITEM , wx.TreeItemIcon_Normal)            
        if Type == 4:
            if not Firstloop:
                SetSubItemData(CTree,cNode,CItem,DB,ODB,cNodeParent)
        else:
            SetItemData(CTree,cNode,CItem,DB,ODB,Type)
    
    for Method in CItem:
        CMethod = Method.Field("WORKCENTERNAME")
        if Type == 3:
            cNode = CTree.AppendItem( cNodeParent , "(" + Method.Field("STAGE") + ") " + CMethod + " (" + CItem.Field("ITEMCODE") + ")" )
            CTree.SetPyData(cNode , None)
            CTree.SetItemImage(cNode , _GUI.iconMETHOD , wx.TreeItemIcon_Normal)              
            #if not Firstloop:
            SetMethodData(CTree,cNode,Method,DB,ODB,CItem.Field("ITEMCODE"))
        for SubItem in Method:
            UpdateTransferFillItemTree(CTree,cNode,DB,ODB,SubItem.item.Field("ITEMCODE"),Type,_GUI, False)


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

def UpdateHTMLHelp(_GUI):
    HelpHTML = FromSettings("./Html/Help")
    _GUI.Display_Jinja.SetValue("")    
    _GUI.Display_Source.SetValue(HelpHTML)
    _GUI.Display_HTML.SetPage(HelpHTML)
    _GUI.MainVert_TreeAndTabs.ChangeSelection(0)
    _GUI.Tree_Tabs.ChangeSelection(2)
    _GUI.Display_TABS.ChangeSelection(0)
    
def UpdateHTMLDisplay(cNode,_GUI,qmult=1):
    _GUI.NEvent("Rendering HTML Display", True)
    DB = XMLFileList[cNode.XMLFileListNo * -1].DB
    JinjaItem = FromSettings("./Html/JinjaItem")
    html = Template(JinjaItem).render( SubItemList = [ DB.SubItem( DB.Item(cNode.text), 1) ] , Mult = 1, Indent = 16, Incrent = 16)
    
    _GUI.Display_Jinja.SetValue(JinjaItem)    
    _GUI.Display_Source.SetValue(html)
    _GUI.Display_HTML.SetPage(html)
    _GUI.NEvent("Idle:", True)

def UpdateHTMLDisplayOLD(cNode,_GUI,qmult=1):
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
        temp = XMLPathList.index( path[:x] )
        parentID = NodeList[ temp ].ID
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
        _GUI.NEvent( "POrders To TREE: (" + str(len(FBList)) + " Entries)", True )         
        for each in FBList:
            addnode(cNode.path + "/" + each[0],_GUI,"PORDER",table,1,each[1],-1)
            POList = FB.select( "QTY,REFERENCE,SUPPPARTNO","PODETL"," where PONUM like '" + each[0] + "'" )
            if len(POList) > 1:
                for LI in POList[1:]:
                    addnode(cNode.path + "/" + each[0] + "/" + LI[1],_GUI,"PODETL",table,LI[0],LI[2],-1)
    
    if cNode.text == "SalesOrders":
        _GUI.NEvent( "SalesOrders To TREE: (" + str(len(FBList)) + " Entries)" , True)         
        for each in FB.retlist[1:]:
            addnode(cNode.path + "/" + each[0],_GUI,"SALES",table,1,each[4],-1)
            for subeach in FB.select("QTY,REFID","JOBDETL"," where JOBNO like '" + each[0] + "'")[1:]:
                addnode(cNode.path + "/" + each[0] + "/" + subeach[1],_GUI,"SUBITEM",table,subeach[0],"",-1)

    if cNode.text == "Jobs":
        _GUI.NEvent( "Jobs To TREE: (" + str(len(FBList)) + " Entries)" , True )           
        for each in FB.retlist[1:]:
            string = each[1]
            a = string.find(" - ")
            astr = string[:a]
            string = string[a+3:]
            a = string.find(" - ")
            if a == -1:
                temp = 1
            else:
                try:
                    temp = int( string[:a] )
                except ValueError:
                    temp = 1
            addnode(cNode.path + "/" + each[0],_GUI,"JOBS",table,temp,string[a+3:],-1)

    if cNode.text == "Items":
        _GUI.NEvent( "Items To TREE: (" + str(len(FBList)) + " Entries)" , True)
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
                        
def UpdateSelect(_GUI,Refresh = False):
    cNode = GetCurrentXMLNode(_GUI)
    FB = XMLFileList[cNode.XMLFileListNo * -1]    
    cblist = [ ]
    for cbox in _GUI.combo_box:
        cblist.append( cbox.GetValue() )
    # text formatting
    print "FB.lastpreselect",FB.lastpreselect
    NewSelect = "" #FB.lastpreselect
    if cblist[0] != "":
        if cblist[1] == "":
            cblist[1] = "LIKE"            
            _GUI.combo_box[1].SetValue("LIKE")
        if cblist[2] == "":
            pass
            #retrieve list here
        else:
            pass
        if cblist[1] == "LIKE":
            NewSelect += " WHERE " + cblist[0] + " " + cblist[1] + " '%" + cblist[2] + "%'"
        else:
            NewSelect += " WHERE " + cblist[0] + " " + cblist[1] + " " + cblist[2]
        
        if cblist[3] != "":
            if cblist[4] == "":
                cblist[4] = "LIKE"
                _GUI.combo_box[4].SetValue("LIKE")
            if cblist[5] == "":
                pass
                #retrieve list here
            else:
                pass
            
            if cblist[4] == "LIKE":
                NewSelect += " AND " + cblist[3] + " " + cblist[4] + " '%" + cblist[5] + "%'"
            else:
                NewSelect += " AND " + cblist[3] + " " + cblist[4] + " " + cblist[5]
            if cblist[6] != "":
                if cblist[7] == "":
                    cblist[7] = "LIKE"
                    _GUI.combo_box[7].SetValue("LIKE")
                if cblist[8] == "":
                    pass
                    #retrieve list here
                else:
                    pass
                if cblist[7] == "LIKE":
                    NewSelect += " AND " + cblist[6] + " " + cblist[7] + " '%" + cblist[8] + "%'"
                else:
                    NewSelect += " AND " + cblist[6] + " " + cblist[7] + " " + cblist[8]

    _GUI.text_xpath.SetValue( "SELECT " + FB.item + " FROM " + FB.table + NewSelect )
    if Refresh:
        print "refresh",FB.item,FB.table ,NewSelect,FB.limit
        GridList = FB.select( FB.item, FB.table , NewSelect , FB.limit )
        #print GridList
        _GUI.DBAGridUpdate( GridList , FB ,FromSettings("./Tables/" + FB.table +  "COLWIDTH").split(","))

    # colour formatting
def Filter(_GUI):
    cNode = GetCurrentXMLNode(_GUI)
    FB = XMLFileList[cNode.XMLFileListNo * -1]
    atext = ""
    
    cb1 = _GUI.combo_box[0].GetValue()
    if cb1 <> "":
        cb2 = _GUI.combo_box[1].GetValue()
        cb3 = _GUI.combo_box[2].GetValue()
        atext = " where " + cb1 + " " + cb2 + " '" + cb3 + "'"
        cb4 = _GUI.combo_box[3].GetValue()

        if cb4 <> "":
            cb5 = _GUI.combo_box[4].GetValue()
            cb6 = _GUI.combo_box[5].GetValue()
     
            atext = "{0} AND where {1} {2} '{3}'".format(atext,cb4,cb5,cb6)
        GridList = FB.select( FB.item, FB.table , atext , FB.limit )
        _GUI.DBAGridUpdate( GridList , FB,FromSettings("./Tables/" + FB.table +  "COLWIDTH").split(",") )

def UpdateDBADisplay_Query( Query, _GUI):
    cNode = GetCurrentXMLNode(_GUI)
    FB = XMLFileList[cNode.XMLFileListNo * -1]
    fbt = FB.table
    GridList = FB.select( Query , "", "" , int( FromSettings("./Tables/DQTY") ) )
    FB.table = fbt
    #print "GRIDLIST",GridList
    _GUI.DBAGridUpdate( GridList , FB ,FromSettings("./Tables/" + FB.table +  "COLWIDTH").split(","))
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
            GridList = FB.select( FromSettings("./Tables/ITEM") , "ITEM", "" , int( FromSettings("./Tables/DQTY") ) , _GUI)
            _GUI.DBAGridUpdate( GridList , FB ,FromSettings("./Tables/ITEMCOLWIDTH").split(","))
            _GUI.Tree_Tabs.ChangeSelection(1)
        elif cNode.text[:7] == "POrders":
            print "POrders"
            GridList = FB.select( FromSettings("./Tables/PORDER"),"PORDER"," where STATUS <> 'Closed'", int( FromSettings("./Tables/DQTY") )  )
            _GUI.DBAGridUpdate( GridList , FB ,FromSettings("./Tables/PORDERCOLWIDTH").split(",") )
            _GUI.Tree_Tabs.ChangeSelection(1)            
        elif cNode.text[:5] == "Sales":
            print "Sales Orders"
            GridList = FB.select( FromSettings("./Tables/JOBS") , "JOBS", "  where JOBNO LIKE 'S%' AND JOBSTATS='ORDERED'" , int( FromSettings("./Tables/DQTY") ) )
            _GUI.DBAGridUpdate( GridList , FB ,FromSettings("./Tables/JOBSCOLWIDTH").split(",") )
            _GUI.Tree_Tabs.ChangeSelection(1)
        elif cNode.text[:4] == "Jobs":
            print "Jobs"
            GridList = FB.select( FromSettings("./Tables/JOBS") , "JOBS", "    where JOBNO LIKE 'M%' AND JOBSTATS <> 'CLOSED' AND JOBSTATS <> 'FINISHED'" , int( FromSettings("./Tables/DQTY") ) )
            _GUI.DBAGridUpdate( GridList , FB ,FromSettings("./Tables/JOBSCOLWIDTH").split(","))
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
                    _GUI.NEvent("Items To TREE ", True)
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
                    _GUI.NEvent("Idle:", True)
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
    
    


    #self.JobTab = wx.Notebook(self.Tree_Tabs, -1, style=wx.NB_LEFT)  #already done
    NewJobTab = wx.Notebook(_GUI.JobTabList[0], -1, style=0)
    _GUI.JobTabList.append( NewJobTab )
    _GUI.JobTabList[0].AddPage(NewJobTab,dbname)
    
    tabs = [ ]
    grids = [ ]
    data = FB.select(FromSettings("./Tables/STAGE"),"STAGE","WHERE SATAUS <> 'Closed'",10000,_GUI)
    for each in data[1:]:
        if each[0] not in tabs:
            tabs.append( each[0] )
            NewGrid = wx.grid.Grid(NewJobTab, -1, size=(1, 1))
            NewGrid.CreateGrid(0,len(each))
            NewGrid.SetRowLabelSize(20)
            NewGrid.SetColLabelSize(20)
            x=0
            for label in data[0]:
                NewGrid.SetColLabelValue(x,label)
                x +=1
            NewJobTab.AddPage( NewGrid ,each[0] )
            grids.append( NewGrid )
        cGrid = grids[ tabs.index(each[0]) ]
        cGrid.AppendRows(1)
        cRow = cGrid.GetNumberRows()
        width = FromSettings("./Tables/STAGECOLWIDTH").split(",")
        x=0
        for field in each:
            cGrid.SetCellValue(cRow-1,x,field)
            cGrid.SetColSize(x,int(width[x]))
            x +=1
            
#            AppendRows
#            x=0
#            while x < len(data)-1:
#                y=0
#                for each in data[x+1]:
#                    NewGrid.SetCellValue(x,y,each)
#                    y += 1
#                x += 1            

        
        
#    self.TrainingTab = wx.Notebook(self.JobTab, -1, style=0)
#    self.TrainingStation1Grid = wx.grid.Grid(self.TrainingTab, -1, size=(1, 1))
#    self.TrainingStation2Grid = wx.grid.Grid(self.TrainingTab, -1, size=(1, 1))
#    self.MainTab = wx.Notebook(self.JobTab, -1, style=0)
#    self.MainStation1Grid = wx.grid.Grid(self.MainTab, -1, size=(1, 1))
#    self.MainStation2Grid = wx.grid.Grid(self.MainTab, -1, size=(1, 1))
    
#    self.TrainingTab.AddPage(self.TrainingStation1Grid, "Station1")
#    self.TrainingTab.AddPage(self.TrainingStation2Grid, "Station2")
#    self.MainTab.AddPage(self.MainStation1Grid, "Station1")
#    self.MainTab.AddPage(self.MainStation2Grid, "Station2")
#    self.JobTab.AddPage(self.TrainingTab, "Training")
#    self.JobTab.AddPage(self.MainTab, "Main")
    
#    self.TrainingStation1Grid.CreateGrid(10, 3)
#    self.TrainingStation1Grid.SetRowLabelSize(20)
#    self.TrainingStation1Grid.SetColLabelSize(20)
#    self.TrainingStation2Grid.CreateGrid(10, 3)
#    self.TrainingStation2Grid.SetRowLabelSize(20)
#    self.TrainingStation2Grid.SetColLabelSize(20)
#    self.MainStation1Grid.CreateGrid(10, 3)
#    self.MainStation1Grid.SetRowLabelSize(20)
#    self.MainStation1Grid.SetColLabelSize(20)
#    self.MainStation2Grid.CreateGrid(10, 3)
#    self.MainStation2Grid.SetRowLabelSize(20)
#    self.MainStation2Grid.SetColLabelSize(20)     






    
    
    
    

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



    
