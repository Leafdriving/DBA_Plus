import firebirdsql

class DBA():
    def __init__(self,filepath):
        self.filepath = filepath
        self.cur = ""
        self.con = firebirdsql.connect(dsn="localhost:"+filepath, user='sysdba', password='masterkey')
        self.cur = "" #self.con.cursor()
        self.BOMMNO = { }
        out = self.select("PITEMCODE,BOMMNO","BOMMASTER")[1:]
        for each in out:
            self.BOMMNO[ each[0] ] = each[1]
            
    def IsItem(self,itmn):
        if len(self.select("ITEMCODE","ITEM","where ITEMCODE like '" + itmn + "'")) == 1:
            return False
        else:
            return True

    def Item(self,itmn):
        return Item(self,itmn)
    def Method(self,itmn,meth):
        return Method(self,itmn,meth)
    def SubItem(self, ClassItem ,qty ):
        return SubItem(ClassItem ,qty )
    def ItemLink(self,DB,itmn,descript):
        return ItemLink(self,DB,itmn,descript)

    def select(self,field,table,where=""):
        exetext = "select " + field + " from " + table + " " + where
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
        self.retlist = retlist
        self.cur.close()        
        return retlist
    
class Item():
    def __init__(self,DB,itmn):
        self.name = itmn
        self.out = DB.select("*","ITEM","where ITEMCODE like '" + itmn + "'")
        self.dic = { }
        self.Methods = [ ]
        self.Links = [ ]
        fields = self.out[0]
        values = self.out[1]
        x = 0
        for each in fields:
            self.dic[ each ] = values[x]
            x += 1
        if DB.BOMMNO.has_key(itmn):
            meths = DB.select( "STAGE,DESCRIPT,WORKCENTERNAME" , "BOMSTAGES", " where BOMMNO =" + DB.BOMMNO[itmn])[1:]
            for each in meths:
                self.Methods.append( Method(DB,itmn,each[0]) )

        for each in DB.select( "DESCRIPT","ITEMDOC", " where ITEMID like '" + itmn + "'")[1:]:
            self.Links.append( ItemLink(DB,itmn,each[0]) )
    def __iter__(self):
        return iter(self.Methods)
    
    def Field(self,f):
        return self.dic[f]

class SubItem():
    def __init__(self, ClassItem , qty):
        self.item = ClassItem
        self.qty = qty
    
class ItemLink():
    def __init__(self,DB,itmn,descript):
        self.item = itmn
        self.description = descript
        self.dic = { }
        out = DB.select( "*","ITEMDOC", " where ITEMID like '" + itmn + "' and DESCRIPT like '" + descript +"'")
        fields = out[0]
        values = out[1]
        x = 0
        for each in fields:
            self.dic[ each ] = values[x]
            x += 1

class Method():
    def __init__(self,DB,itmn,meth):
        self.item = itmn
        self.method = meth
        self.dic = { }
        self.SubItems = [ ] 
        out = DB.select("*", "BOMSTAGES", " where BOMMNO=" + DB.BOMMNO[itmn] + " and STAGE like '" + meth + "'")
        fields = out[0]
        values = out[1]
        x = 0
        for each in fields:
            self.dic[ each ] = values[x]
            x += 1
       
        for each in DB.select( "CITEMCODE,USAGE", "BOMDEL", " where PITEMCODE='" + itmn + "' AND STAGEID='" + meth + "'")[1:]:
            self.SubItems.append( SubItem(Item(DB,each[0]) ,each[1]) )
            
    def __iter__(self):
        return iter(self.SubItems)            
            
    def Field(self,f):
        return self.dic[f]

if __name__ == "__main__":
    DB = DBA("C:\Users\Lief-W7\Desktop\Dropbox\EJDB.FDB")
    item = DB.Item("71191-03")
    for each in item.Links:
        print each.item,each.description
        

    
