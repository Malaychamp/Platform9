import datetime
import sys
import os.path as op

from ConnectDB import ConnectDB
from DBOps import DBOps
from VMManagement import VMManagement


def receive_input():
    opt = eval(input('Press 1 : to get current repository of VMs\nPress 2 : to add VM to pool of VMs\nPress 3 : to '
                     'Check in VM in to pool of VMs\nPress 4 : to Check out VM from the pool of VMs\nPress 5 : to get '
                     'list of checked out VMs\nPress 6 : to get list of available VMs\nPress 0 : to exit VM '
                     'Management\nInput Your option : '))
    return opt


def vm_management():
    db_path = op.join(op.dirname(__file__), 'DB', 'VMManagement.db')
    print("DB PATH : ", db_path)
    opt = receive_input()
    db_obj = ConnectDB(db_path)
    conn_obj = db_obj.connect()
    db = DBOps(conn_obj)
    vm_manage_obj = VMManagement(conn_obj, db)
    while 0 <= opt < 7:
        if opt == 1:
            print("Current Pool of VM inventory ...")
            c = 1
            for i in vm_manage_obj.get_repository_details():
                print("%d) %s" %(c, i))
                c += 1
            opt = receive_input()
        elif opt == 2:
            """
                Add VM to the inventory
            """
            ip = input("Enter Ip address of the vm to be added : ")
            name = input("Enter the name of the vm : ")
            os = input("Enter the OS type : ")
            dt = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            vm_user = input("Enter VMs username : ")
            vm_pass = input("Enter Vms password : ")
            db.add_vm_to_inventory(ip, name, os, dt, vm_user, vm_pass)
            opt = receive_input()
        elif opt == 3:
            """
                Check in VM to the inventory
            """
            if db.get_check_out_vm_data():
                ip = input("Enter Ip address of the vm to be checked in : ")
                user = input("Enter the user name : ")
                vm_manage_obj.vm_check_in(ip, user)
            else:
                print("No VM for check out yet ...")
            opt = receive_input()
        elif opt == 4:
            """
                Check out vm of the inventory
            """
            if list(db.get_check_out_vm_data().keys()) == db.get_vm_pool_data():
                print("All VMs are currently checked out. No VMs available")
                print("Please Try after some time ...")
            else:
                ip = input("Enter Ip address of the vm to be checked out : ")
                user = input("Enter the user name : ")
                vm_manage_obj.vm_check_out(ip, user)
            opt = receive_input()
        elif opt == 5:
            c = 1
            if db.get_check_out_vm_data():
                print("List of Checked out VMs are as follows : ")
                for k, v in db.get_check_out_vm_data().items():
                    print("%d) %s --> %s" %(c, k, v))
                    c += 1
            else:
                print("No VM is currently being checked out!")
            opt = receive_input()
        elif opt == 6:
            print("List of available VMs : ")
            c = 1
            for i in db.get_list_of_available_vms():
                print("%d) %s" %(c, i))
                c += 1
            opt = receive_input()
        elif opt == 0:
            print("Exiting VM Management System ...")
            sys.exit()
    else:
        print("Incorrect Option entered ...")
        print("Please Try again ...")


if __name__ == '__main__':
    vm_management()
