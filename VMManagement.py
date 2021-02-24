import paramiko


class VMManagement:

    def __init__(self, conn_obj, db):
        self.conn_obj = conn_obj
        self.db = db

    def get_repository_details(self):
        """
            get the vm details from the database
            get the data and store it in dict object
            the function returns the dict object for all the VMs that will be part of the pool
        """
        return self.db.get_vm_pool_data()

    def vm_check_in(self, ip, user):
        """
            check in the vm which the user wants to and write the same in to db
            vm_check_in table will have list of vms checked in by the user.
            a vm will be successfully checked in if it is not in available repository but part of the larger pool of vm and is checked in by the same user who checked out.
        """
        chk_out_data = self.db.get_check_out_vm_data()
        if ip in chk_out_data.keys() and chk_out_data[ip] == user:
            print("Checking back VM into POOL ...")
            # Delete the record from database in VM_CHECK_OUT_DATA
            try:
                self.conn_obj.execute("delete from VM_CHECK_OUT_DATA where IP = ? and user = ?", (ip, user))
                self.conn_obj.commit()
            except Exception as e:
                print("Error in deleting the record")
                print("Error : ", e)
            else:
                print("Clean up in progress ...")
                data = self.conn_obj.execute("select * from VM_INVENTORY where IP = ?", (ip,))
                for row in  data:
                    print(row)
                #self.vm_cleanup(ip, data[4], data[5])
                print("Record Deleted successfully ...")
        elif ip in chk_out_data.keys():
            print("Vm is checked out by another user")
            print("VM : %s can be checked in by User : %s" % (ip, chk_out_data[ip]))
        else:
            print("Currently the VM is not checked out")
            print("VM can be checked in only when it is checked out!")

    def vm_check_out(self, ip, user):
        """
            check out the vm which the user wants to check out and write the same in to db
            vm_check_out table will have list of vms checked out by the user.
            a vm will be successfully checked out if it is available in the repository
        """
        chk_out_data = self.db.get_check_out_vm_data()
        if ip in chk_out_data.keys() and chk_out_data[ip] == user:
            print("VM already checked out by the user.")
            #repo.remove(ip)
        elif ip in chk_out_data.keys():
            print("VM is checked out by another user : ", chk_out_data[ip])
            #repo.remove(ip)
        else:
            if ip in self.db.get_vm_pool_data():
                print("VM is available in pool of VMs and can be checked out!")
                print("VM : %s is checked out by user : %s" % (ip, user))
                # enter the details in checked out table in db
                try:
                    self.conn_obj.execute("insert into VM_CHECK_OUT_DATA(IP, USER) values(?, ?)", (ip, user))
                    self.conn_obj.commit()
                except Exception as e:
                    print("Error in inserting the record : ", e)
                else:
                    #repo.remove(ip)
                    print("Record Inserted successfully")
            else:
                print("VM is not part of the available VMs for check in check out!")

    def vm_cleanup(self, ip, vm_username, vm_password):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=vm_username, password=vm_password)
        stdin, stdout, stderr = ssh.exec_command('rm -rf /tmp')
        ssh.close()
