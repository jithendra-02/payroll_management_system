import tkinter as tkinter
from tkinter import *
import mysql.connector as mysql
from datetime import datetime
import pwinput
from tabulate import tabulate
database_name='payroll'
table_name1='employee'
table_name2='pay'
db= mysql.connect(host='localhost',user='root',password='Jith9347@2002',database='payroll')
mycursor=db.cursor()
def record_check(query):
    mycursor.execute(query)
    myrecord=mycursor.fetchall()
    if myrecord:
        return myrecord
    else:
        return False
        
def check_employee(en):
    operation='select Empno from '+ table_name1
    mycursor.execute(operation)
    data_check=mycursor.fetchall()
    for i in data_check:
        if i[0]==int(en):return True
    return False

def login_employee(en):
    operation='select Emppass from '+table_name1+' where Empno='+en
    mycursor.execute(operation)
    login=mycursor.fetchall()
    while True:
        password=pwinput.pwinput(prompt='Enter password: ',mask='*')
        if password==login[0][0]:
            return True
        
        elif password.upper()=='EXIT':
            break
        else:
            print("Enter 'EXIT' as password to return to home:".center(117))
            print("Entered password is wrong,please try again..... ".center(117))
    print("\n")
    return True


def login_admin():
    operation='select Password from admin'
    mycursor.execute(operation)
    login=mycursor.fetchall()
    while pwinput.pwinput(prompt='Enter password: ',mask='*')!=login[0][0]:
        print("Entered password is wrong,please try again..... ".center(117))
    print("\n")
    return True  


          
def add_records():
    print("Enter employee information: ".center(117))
    emp_no=int(input("Enter employee no: "))
    if not check_employee(str(emp_no)):
        print("Create a password to login as user:")
        emp_pass=input("Enter a password:")
        emp_name=input("Enter employee name: ")
        emp_dob=input("Enter D.O.B in DD-MM-YYYY format: ")
        emp_phone=int(input("Enter phone number:"))
        emp_job=input("Enter employee job: ")
        emp_department=input("Enter department: ")
        emp_basicsalary=float(input("Enter basic salary:"))
        if emp_job.upper()=="OFFICER":
            emp_da=emp_basicsalary*0.5
            emp_hra=emp_basicsalary*0.35
            emp_tax=emp_basicsalary*0.2
        elif emp_job.upper()=="MANAGER":
            emp_da=emp_basicsalary*0.45
            emp_hra=emp_basicsalary*0.30
            emp_tax=emp_basicsalary*0.15
        else:
            emp_da=emp_basicsalary*0.40
            emp_hra=emp_basicsalary*0.25
            emp_tax=emp_basicsalary*0.1
        emp_grosssalary=emp_basicsalary+emp_da+emp_hra
        emp_netsalary=emp_grosssalary-emp_tax
        now=datetime.now()
        emp_hiretime=now.strftime("%H:%M:%S")
        emp_hiredate=now.strftime("%d-%m-%y")
        data_in1=(emp_no,emp_pass,emp_name.upper(),emp_dob,emp_phone,emp_job.upper(),emp_department,emp_hiredate,emp_hiretime)
        data_in2=(emp_no,emp_basicsalary,emp_da,emp_hra,emp_grosssalary,emp_tax,emp_netsalary)
        query1="insert into "+table_name1+" values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        query2="insert into "+table_name2+" values (%s,%s,%s,%s,%s,%s,%s)"
        mycursor.execute(query1,data_in1)
        mycursor.execute(query2,data_in2)
        db.commit()
        print("Record added successfully........☺")
    else:
        print("Entered employee id already exists,please try again and enter unique employee id.....".center(117))
    print("\n")
   

def display_all_records():
    query='select Empno,Name,DOB,EmpPhone,Job,Department,HireDate,HireTime from '+table_name1
    myrecord=record_check(query)
    if myrecord!=False:
        print(tabulate(myrecord ,headers=['Empno','Name','DOB','EmpPhone','Job','Department','HireDate','HireTime'],tablefmt='psql'))
    else:
        print("No records in database......".center(117))
    print("\n")
    

def particular_record(en):
    query='select Empno,Name,DOB,EmpPhone,Job,Department,HireDate,HireTime from '+table_name1+' where Empno='+en
    myrecord=record_check(query)
    if myrecord!=False:
        print(tabulate(myrecord ,headers=['Empno','Name','DOB','EmpPhone','Job','Department','HireDate','HireTime'],tablefmt='psql'))
    else:
        print("No records in database.....".center(117))
    print("\n")


def delete_all_records():
    query='select * from '+table_name1
    myrecord=record_check(query)
    if myrecord!=False:
        ch=input("Do you want to delete all the records (y/n): ")
        if ch.upper()=="Y":
            mycursor.execute('delete from '+table_name1)
            mycursor.execute('delete from '+table_name2)
            db.commit()
    else:
        print("The database is already empty.....".center(117))
    print("\n")
        

def delete_particular_record():
    query='select * from '+table_name1
    myrecord=record_check(query)
    if myrecord!=False:
        en=input("Enter the employee number that is need to be deleted: ")
        if check_employee(en):
            query1='delete from '+table_name1+' where Empno='+en
            query2='delete from '+table_name2+' where Empno='+en
            mycursor.execute(query1)
            mycursor.execute(query2)
            db.commit()
            print("Employee record deleted successfully.....".center(117))
        else:
            print("Employee does not exist.....🤔🤔🤔".center(117))
    else:
         print("No records in database.....".center(117))
    print("\n")
    
        
def update_record():
    query='select * from '+table_name1
    myrecord=record_check(query)
    if myrecord!=False:
        en=input("Enter employee number to be updated: ")
        query1='select * from '+table_name1+' where Empno='+en
        query2='select * from '+table_name2+' where Empno='+en
        mycursor.execute(query1)
        myrecord1=mycursor.fetchall()
        mycursor.execute(query2)
        myrecord2=mycursor.fetchall()
        if not check_employee(en):
            print("Employee does not exists......🤔".center(117))
        else:
            print("CURRENT STATUS OF RECORD OF THE EMPLOYEE...............")
            print("->Employee No              : "+str(myrecord1[0][0]))
            print("->Employee Name            : "+str(myrecord1[0][2]))
            print("->Employee DOB             : "+str(myrecord1[0][3]))
            print("->Employee Contact         : "+str(myrecord1[0][4]))                     
            print("->Employee Job             : "+str(myrecord1[0][5]))
            print("->Employee Department      : "+str(myrecord1[0][6]))
            print("->Employee BasicSalary     : "+str(myrecord2[0][1]))
            print("\n")
            emp_name=myrecord1[0][2]
            emp_dob=myrecord1[0][3]
            emp_phone=myrecord1[0][4]
            emp_job=myrecord1[0][5]
            emp_department=myrecord1[0][6]
            emp_basicsalary=myrecord2[0][1]
            check=input("Do you want to change the name(y/n):")
            if check.upper()=="Y":
                emp_name=input("Enter new name: ")
            check=input("Do you want to change the DOB(y/n):")
            if check.upper()=="Y":
                emp_dob=input("Enter new DOB: ")
            check=input("Do you want to change the contact number(y/n):")
            if check.upper()=="Y":
                emp_phone=input("Enter new contact number: ")
            check=input("Do you want to change the job(y/n):")
            if check.upper()=="Y":
                emp_job=input("Enter new job: ")
            check=input("Do you want to change the Department(y/n):")
            if check.upper()=="Y":
                emp_department=input("Enter new Department: ")
            check=input("Do you want to change the basic salary(y/n):")
            if check.upper()=="Y":
                emp_basicsalary=input("Enter new basic salary: ")
            print()
            query1='update '+ table_name1 +' set Name='+"'"+ emp_name +"'"+","+'dob='+"'"+emp_dob+"'"+","+'EmpPhone='+"'"+emp_phone+"'"+","+'Job='+"'"+emp_job+"'"+","+'Department='+"'"+emp_department+"'"+' where Empno='+en
            mycursor.execute(query1)
            query2='update '+ table_name2 +'set BasicSalary='+str(emp_basicsalary)+' where Empno='+en
            db.commit()
            print("Record modified......😀 ".center(117))
    else:
        print("No records in database......🤔".center(117))
    print("\n")

def payroll():
    query='select * from '+table_name1
    myrecord=record_check(query)
    if myrecord!=False:
        query1='select Empno,Name,DOB,EmpPhone,Job,Department,HireDate,HireTime from '+table_name1
        query2='select BasicSalary,DA,HRA,GrossSalary,Tax,NetSalary from '+table_name2
        mycursor.execute(query1)
        myrecord1=mycursor.fetchone()
        mycursor.execute(query2)
        myrecord2=mycursor.fetchone()
        new_record=myrecord1+myrecord2
        print(new_record)
        print(tabulate([new_record] ,headers=['Empno','Name','DOB','EmpPhone','Job','Department','HireDate','HireTime','BasicSalary','DA','HRA','GrossSalary','Tax','NetSalary'],tablefmt='psql'))
    else:
        print("No records in database......".center(117))
    
def pay_slip(en):
    query='select * from '+table_name1
    myrecord=record_check(query)
    if myrecord!=False:
        query1='select Empno,Name,DOB,EmpPhone,Job,Department,HireDate,HireTime from '+table_name1+' where Empno='+en
        query2='select BasicSalary,DA,HRA,GrossSalary,Tax,NetSalary from '+table_name2+' where Empno='+en
        mycursor.execute(query1)
        myrecord1=mycursor.fetchone()
        mycursor.execute(query2)
        myrecord2=mycursor.fetchone()
        new_record=myrecord1+myrecord2
        print(tabulate([new_record] ,headers=['Empno','Name','DOB','EmpPhone','Job','Department','HireDate','HireTime','BasicSalary','DA','HRA','GrossSalary','Tax','NetSalary'],tablefmt='psql'))
    else:
        print("No records in database......".center(117))

def main():
    print("*"*117)      
    print("Please select user:".center(117))
    print("*"*117)
    print("1. Admin...")
    print("2. Employee...")
    print("3. To exit...")
    user_check=int(input("Enter respective key:"))
    if user_check==1:
        if login_admin():
            while True:
                print("*"*117)
                print("HOME".center(117))
                print("*"*117)
                print("1. ADD EMPLOYEE RECORDS")
                print("2. DISPLAY RECORDS OF ALL EMPLOYEES")
                print("3. DELETE RECORDS OF ALL EMPLOYEES")
                print("4. DELETE RECORD OF A PARTICULAR EMPLOYEE")
                print("5. UPDATE RECORD OF A EMPLOYEE")
                print("6. DISPLAY PAYROLL OF ALL EMPLOYEES")
                print("7. SWITCH USER")
                print("8. LOGOUT ")
                print("="*117)
                choice=int(input("Enter the respective key for a operation: "))
                print("\n")
                if choice==1:
                    add_records()
                elif choice==2:
                    display_all_records()
                elif choice==3:
                    delete_all_records()
                elif choice==4:
                    delete_particular_record()
                elif choice==5:
                    update_record()
                elif choice==6:
                    payroll()
                elif choice==7:
                    main()
                elif choice==8:
                    exit()
    elif user_check==2:
        en=input("Enter employee_id:")
        if check_employee(en):
            if login_employee(en):
                while True:
                    print("*"*117)
                    print("HOME".center(117))
                    print("*"*117)
                    print("1. DISPLAY RECORD")
                    print("2. DISPLAY SALARY SLIP")
                    print("3. SWITCH USER")
                    print("4. LOGOUT ")
                    print("="*117)
                    choice=int(input("Enter the respective key for a operation: "))
                    print("\n")
                    if choice==1:
                        particular_record(en)
                    elif choice==2:
                        pay_slip(en)
                    elif choice==3:
                        main()
                    elif choice==4:
                        exit()
        else:
            print("Employee does not exists......".center(117))
            print("\n")
            main()
    else:
        exit()
main()
        


        



            

