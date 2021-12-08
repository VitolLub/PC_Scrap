import getpass
from pymongo import MongoClient
import psutil
# get all proccesses from WMI
import wmi
import platform


def get_process_cpu_usage(pid):
    # get CUP usage by process pid

    # get process
    p = psutil.Process(pid)
    res = psutil.virtual_memory()[2]

    # get process CPU usage
    print(f'get process CPU usage {pid}')
    print(res)
    return p.cpu_percent(interval=1)


def get_memory_usage(i):
    # get memory usage by process pid
    p = psutil.Process(i)
    # get memory usage
    return p.memory_percent()

# Press the green button in the gutter to run the script.
def connect_to_db():
    db = MongoClient('mongodb+srv://testuser21:testuser21@cluster0.vtlen.mongodb.net/test?retryWrites=true&w=majority')
    db = db['pc_scrap_data']
    collections = db['pc_scrap_data']
    return collections


def parser_pc_data():


    platform.node()
    username = getpass.getuser()

    c = wmi.WMI()
    arr = []
    name_and_id = []

    for process in c.Win32_Process():
        # process CPU usage
        name_and_id_dict = {}
        name_and_id_dict['name'] = process.Name
        name_and_id_dict['id'] = process.ProcessId
        print(process.ProcessId, process.Name)
        arr.append(process.ProcessId)
        name_and_id.append(name_and_id_dict)

    """
    function receive proccess id and return process usage procent

    """

    # loop name_and_id key value
    index = 0
    full_dict = []
    for i in name_and_id:
        try:
            # get process CPU usage
            cpu = get_process_cpu_usage(i['id'])
            i['cpu'] = cpu
            # get memory usage
            ram = get_memory_usage(i['id'])
            i['ram'] = ram
            full_dict.append(i)
            # get process name
            index += 1
        except:
            pass
    print("Full arr")
    print(full_dict)

    # PC run time
    import ctypes

    # getting the library in which GetTickCount64() resides
    lib = ctypes.windll.kernel32

    # calling the function and storing the return value
    t = lib.GetTickCount64()

    # since the time is in milliseconds i.e. 1000 * seconds
    # therefore truncating the value
    t = int(str(t)[:-3])
    # extracting hours, minutes, seconds & days from t
    # variable (which stores total time in seconds)
    mins, sec = divmod(t, 60)
    hour, mins = divmod(mins, 60)
    days, hour = divmod(hour, 24)

    print("Primary params:")
    print(f"Computer name {platform.node()}")
    print(f"User name {username}")
    # Calling psutil.cpu_precent() for 4 seconds
    cpu_used = psutil.cpu_percent(4)
    print('The CPU usage is: ', cpu_used)
    cpu_aval = 100 - float(cpu_used)
    print('The CPU avaliable is: ', cpu_aval)
    # gives a single float value
    # gives an object with many fields
    print(f"Virtual memory: {psutil.virtual_memory()}")
    # you can convert that object to a dictionary
    # dict(psutil.virtual_memory()._asdict())
    # you can have the percentage of used RAM
    print(f"Virtual memory used:{psutil.virtual_memory().percent}")
    avaibe_memory = 100 - float(psutil.virtual_memory().percent)
    avail_memory = round(avaibe_memory, 2)
    print(f"Virtual memory available:{round(avaibe_memory, 2)}")
    # you can calculate percentage of available memory
    a = psutil.virtual_memory().available
    b = a / 1000000
    # round b to 2 digits after comas
    aval_memory_in_mb = round(b, 2)
    # float to string
    aval_memory_in_str = str(aval_memory_in_mb) + " MB"
    print(f"Virtual memory available in MB:{aval_memory_in_str}  ")
    # psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
    print("PC run time")
    print(f"{days} days, {hour:02}:{mins:02}:{sec:02}")
    duration = f"{days} days, {hour:02}:{mins:02}:{sec:02}"
    # get datetime now
    import datetime
    # get current date and time
    now = datetime.datetime.now()

    from datetime import datetime

    from datetime import datetime, timedelta

    d = datetime.today() - timedelta(hours=hour, minutes=mins, seconds=sec)

    time_1 = d.strftime('%D %H:%M %p')


    collections = connect_to_db()
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = {}

    data['Computer Name'] = platform.node()
    data['date_scrap'] = date_time
    data['Login_sessions'] = {"Comouter name": platform.node(), "logged in User name": username, "Login time": time_1,
                              "Log off time": "", "Duration logged in": duration}
    data['Power_sessions'] = {"Computer Name": platform.node(), "Turned on time": time_1, "Turned off time": "",
                              "Duration": duration}
    data['Application Summary'] = full_dict
    data['CPU Usage sumary'] = {"CPU used": cpu_used, "CPU Available": cpu_aval, "average usage": ""}
    data['Memory usage'] = {"Used Memmory": psutil.virtual_memory().percent, "Available Memory": avail_memory,
                            "Available Memory in MB": aval_memory_in_str}

    collections.insert_one(data)


if __name__ == '__main__':
    parser_pc_data()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
