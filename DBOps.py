class DBOps:

    def __init__(self, conn_obj):
        self.conn_obj = conn_obj

    def add_vm_to_inventory(self, ip, name, os, dt, vm_username, vm_password):
        try:
            self.conn_obj.execute("insert into VM_INVENTORY (IP, vm_name, os, date, vm_username, vm_password) values("
                                  "?, ?, ?, ?, ?, ?)",
                                  (ip, name, os, dt, vm_username, vm_password))
            self.conn_obj.commit()
        except Exception as e:
            print("Error in inserting VM in to pool!")
            print("Error : ", e)
        else:
            print("VM inserted in to pool successfully ...")

    def get_vm_pool_data(self):
        try:
            cursor_obj = self.conn_obj.execute("select * from VM_INVENTORY")
        except Exception as e:
            print("Error in fetching data")
            print("Error : ", e)
        else:
            repo = []
            for row in cursor_obj:
                repo.append(row[0])
            return repo

    def get_check_out_vm_data(self):
        try:
            cursor_obj = self.conn_obj.execute("select * from VM_CHECK_OUT_DATA")
        except Exception as e:
            print("Error in fetching check out data")
            print("Error : ", e)
        else:
            checked_out_data = {}
            for row in cursor_obj:
                checked_out_data[row[0]] = row[1]
            return checked_out_data

    def get_list_of_available_vms(self):
        repo = self.get_vm_pool_data()
        checked_out_data = list(self.get_check_out_vm_data().keys())
        if set(checked_out_data).issubset(repo):
            return list(set(repo) - set(checked_out_data))

