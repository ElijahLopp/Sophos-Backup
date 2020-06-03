# Import library
import os
from datetime import datetime, timedelta
import glob
from pyzabbix import ZabbixAPI

# Current Date
date = datetime.now()-timedelta(days=7)

# Zabbix Server Conection
url = '<url-zabbix>'
username = "<username>"
password = '<password>'

# Testing Conection
try:
    zapi = ZabbixAPI(url, timeout=4)
    zapi.login(username, password)
except Exception as err:
    print("Failed connect Zabbix API")
    print("Error: {}".format(err))

# Testing Request
try:
    req_host = zapi.host.get(
        filter={"status": "0"}, groupids="141", output=["host"])
except:
    print("Request fail")

for name in req_host:
    print("__________________________________________")
    try:
        print("Host name: {}".format(name["host"]))
        # Sophos' file list
        list_of_files = glob.glob('<folder-path-file-backups>'+name["host"]+"*")
        print("Total files found: {}".format(len(list_of_files)))
        # latest list file
        latest_file = max(list_of_files, key=os.path.getctime)

        # File Date
        data_last = datetime.fromtimestamp(os.path.getmtime(latest_file))
        print("Most recent date: {}".format(data_last))

        # File Size
        f_size = os.path.getsize(latest_file)

        # Date comparison
        if data_last < date:
            print("Failure date")
            os.system(
                'zabbix_sender -z <url-zabbix> -p <port> -s {} -k  <variable-zabbix> -o Failure'.format(name["host"]))

        # Size comparison
        elif f_size < 100:
            print("Failure size: {}".format(f_size))
            os.system(
                'zabbix_sender -z <url-zabbix> -p <port> -s {} -k  <variable-zabbix> -o Failure'.format(name["host"]))

        else:
            print("Success")
            # lst_success.append(name["host"])
            os.system(
                'zabbix_sender -z <url-zabbix> -p <port> -s {} -k  <variable-zabbix> -o Success'.format(name["host"]))

    except Exception as erro:
        print("Excepterro {}".format(erro))
        os.system(
            'zabbix_sender -z <url-zabbix> -p <port> -s {} -k  <variable-zabbix> -o Failure'.format(name["host"]))
if __name__ == "__main__":
    pass
 
