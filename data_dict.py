import sqlite3
import argparse
import os
import sys
os.system("color")




def create_table(Ty):     
    conn = sqlite3.connect('DICT.db')
    cursor = conn.cursor()
    creat_table =('''CREATE TABLE %s
                (ID INTEGER PRIMARY KEY   AUTOINCREMENT,
                VALUE        CHAR(50)     NOT NULL);'''%(Ty))
    cursor.execute(creat_table)
    conn.commit()
    conn.close()
    print("\n\033[0;32;40m   %s type data created successfully\033[0m"%(Ty))




def delete_duplicate(Ty):   
    conn = sqlite3.connect('DICT.db')
    cursor = conn.cursor()
    Delete_duplicate_sql="DELETE FROM "+ Ty +" WHERE ID NOT IN(SELECT MAX(rowid) rowid FROM "+ Ty +" GROUP BY VALUE)";
    cursor.execute(Delete_duplicate_sql)
    conn.commit()
    conn.close()
    print("\n\033[0;32;40m   %s type data De duplication succeeded\033[0m"%(Ty))



def add_value(file_name,Ty):   
    conn = sqlite3.connect('DICT.db')
    cursor = conn.cursor()
    with open(file_name, "r") as f:
        dict = f.readlines()
        for i in dict:
            value = i.strip()
            add_sql = "insert into" + " " + Ty + "(VALUE) VALUES('%s')" % (value)
            cursor.execute(add_sql)
    conn.commit()
    conn.close()
    print("\n\033[0;32;40m   %s type data written successfully\033[0m"%(Ty))
    delete_duplicate(Ty)


def exam_exit(file_name,Ty):   
    try:
        add_value(file_name,Ty)
    except UnboundLocalError as e:
        print("\n\033[31m   %s\033[0m"%(e))
    except FileNotFoundError as e1:
        print("\n\033[31m   %s\033[0m"%(e1))
    except:
        print("\n\033[31m   The dictionary of this type does not exist, do you want to create it? Please select (Y/N)\033[0m")
        if input("\n\033[31m   Please input: \033[0m").upper() == "Y":
            create_table(Ty)   
            add_value(file_name,Ty)   


def union_ty_tmp(Ty):    
    conn = sqlite3.connect('DICT.db')
    cursor = conn.cursor()
    try:
        cursor.execute("insert into Temp (VALUE) select VALUE from %s"%(Ty))
        print("\n\033[0;32;40m   %s type merged successfully\033[0m" % (Ty))
    except sqlite3.OperationalError:
        print("\n\033[0;32;40m   A dictionary of type %s does not exist\033[0m" % (Ty))
    conn.commit()
    conn.close()





def write_value(filename,Ty):   
    conn = sqlite3.connect('DICT.db')
    cursor = conn.cursor()
    take_sql="SELECT VALUE FROM '%s'"%(Ty)
    cursor.execute(take_sql)
    with open(filename,"w+") as f:
        for i in cursor.fetchall():
            f.write(i[0]+"\n")
    conn.commit()
    conn.close()
    print("\n\033[32m   Database dictionary exported successfully\033[0m")


def del_tmp():
    conn = sqlite3.connect('DICT.db')
    cursor = conn.cursor()
    cursor.execute("delete from Temp")
    conn.commit()
    conn.close()
    print("\n\033[32m   Temp data dictionary cleared successfully\033[0m")




def show_all():    
    conn = sqlite3.connect('DICT.db')
    cursor = conn.cursor()
    cursor.execute("select name from sqlite_master where type='table' order by name")
    table_list=cursor.fetchall()
    try:
        table_list.remove(('Temp',))
        table_list.remove(('sqlite_sequence',))
        if not table_list:
            print("\n\033[31m   Your database dictionary is empty\033[0m")
        for i in table_list:
            cursor.execute("select count(*) from %s"%(i))
            mat = "\n\033[32m   Dictionary type:"+"{:^15}"+"-"*20+" Rows: {}\033[0m"
            print(mat.format(i[0],cursor.fetchall()[0][0]))
    except ValueError:
        create_table("Temp")
        show_all()
    except:
        print("\n\033[31m   Your database dictionary is empty\033[0m")
    conn.commit()
    conn.close()



def main():
    parser = argparse.ArgumentParser(description='A database dictionary',usage="-h | -s | -i bb.txt -t aa | -o result.txt -t aa bb cc")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i',help='input a dictionary file')
    group.add_argument('-o',help='output a dictionary file')
    parser.add_argument('-s',help='Show existing dictionary types',action="store_true")
    parser.add_argument('-t',help='Select a type to store in the database || Select one or more dictionary types to export',nargs="*")
    args = parser.parse_args()
    if str(args).count("None") == 3 and not args.s:
        print("\n\033[0;31;40m   Please select at least one parameter\033[0m")
        print("\n\033[0;31;40m   Example: %s -h\033[0m"%(sys.argv[0]))
    elif args.i:
        print(len(args.t))
        if len(args.t) == 1:
            exam_exit(args.i,args.t[0])
        elif len(args.t) > 1:
            print("\n\033[0;31;40m   When - t is matched with - i, only one parameter needs to be provided to - t\033[0m")
        else:
            print("\n\033[0;31;40m   Missing parameter -t\033[0m")
    elif args.o:
        if args.t:
            for i in args.t:
                union_ty_tmp(i)
            delete_duplicate("Temp")
            write_value(args.o,"Temp")
            del_tmp()
            print("\n\033[0;32;40m   Dictionary generated successfully at %s\\%s\033[0m"%(os.getcwd(),args.o))
        else:
            print("\n\033[0;31;40m   Missing parameter -t\033[0m")
    elif args.s:
        show_all()



if __name__=="__main__":
    main()

