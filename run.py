from tkinter import *
import sys
import tkinter.messagebox as tmsg
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle
from PIL import ImageTk,Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time as t
import os
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from appdirs import *

run=1
rep=1

start_scheduling=False
start_monitor = False
last_status="Offline"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

execute_dir=resource_path(os.getcwd())
User_Data=user_data_dir()

try:
    path=os.path.join(User_Data,"WMonster")
    os.mkdir(path)
    directory=os.path.join(path, "User_Data")

except:
    path=os.path.join(User_Data,"WMonster")
    directory=os.path.join(path, "User_Data")
    # print(directory)
    pass
    # print("Already there")
directory=path
config_path=path
config_path=os.path.join(config_path, "config.txt")
#To check if chrome is opened for the first time
conf=""
try:
    file = open(config_path, 'r+')
    conf=(file.readline())
except:
    file = open(config_path, 'w')
    file.write("First_Time=True")
file.close()


path=os.path.dirname(resource_path(__file__))

def search(name):
    search_box = driver.find_element_by_class_name("_2S1VP")
    search_box.clear()
    search_box.send_keys(name)
    t.sleep(1)
    try:
        search_box.send_keys(Keys.ENTER)
    except Exception as e:
        print("No such profile exist!")
        print(e)
        tmsg.showerror("error","No such profile exist!")
def send(message,repeat):
    msg_box = driver.find_element_by_class_name("_2WovP")
    i=0
    interval = 1
    for i in range(repeat):
        msg_box.send_keys(message)
        t.sleep(1)
        send = driver.find_element_by_class_name("_35EW6")
        send.click()
        t.sleep(interval)
    return("m_sent")
def get_dp():
    try:
        profile_pic = driver.find_element_by_xpath('//*[@id="main"]/header/div[1]/div/img')
        dp=profile_pic.get_attribute("src")
        driver.execute_script('''window.open("''' +dp + '''","_blank");''')
        driver.switch_to.window(driver.window_handles[1])
        os.chdir(resource_path(path))

        element= driver.find_element_by_xpath('/html/body/img')
        location = element.location
        size = element.size

        driver.save_screenshot("pro.png")
        driver.execute_script('''window.close();''')
        driver.switch_to.window(driver.window_handles[0])

        x = location['x']
        y = location['y']
        width = location['x']+size['width']
        height = location['y']+size['height']
        im = Image.open('pro.png')
        im = im.crop((int(x), int(y), int(width), int(height)))
        im.save('pro.png')

        return(os.path.join(resource_path(path), "pro.png"))
    except:
        return(os.path.join(resource_path(path), "no_dp.png"))
last_seen=datetime.now()
minutes=0
pa=datetime.now()
pb=datetime.now()

def display_update():
    status.insert(END,"%s last seen at %s\n"%(name.get(),last_seen))
    status.insert(END,"Total duration : %s minutes.\n"%(str(minutes)))

def monitor():
    global last_status
    global pa
    global pb
    global last_seen
    global minutes

    if(start_monitor):
        try:
            stat = driver.find_element_by_class_name("_3sgkv")
            if "seen" in stat.text:
                if last_status == "Online":
                    pb=datetime.now()
                    last_seen=datetime.now().strftime("%d/%m,%H:%M")
                    last_status = "Offline"
                    pt=(pb-pa)
                    minutes =round((pt.seconds/ 60),2)
                    display_update()
                    minutes=0
                cur_status.set("Offline")
                e4.config(fg='red')
            if "online" in stat.text:
                cur_status.set("Online")
                e4.config(fg='green')
                if last_status == "Offline":
                    pa=datetime.now()
                last_status = "Online"
        except:
            if last_status == "Online":
                pb=datetime.now()
                print("Offline time : ",pb)
                pt=(pb-pa)
                minutes = round((pt.seconds/ 60),2)
                last_seen=datetime.now().strftime("%d/%m,%H:%M")
                last_status = "Offline"
                display_update()
                minutes=0
                cur_status.set("Offine")
            e4.config(fg='red')
    window.after(500,monitor)
def schedule():
    global start_scheduling
    if start_scheduling:
        time_object = datetime.strptime(time.get(), '%I:%M:%p').time()
        time_str=time_object.strftime("%H:%M")
        now=datetime.now()
        time_now=now.strftime("%H:%M")
        if time_now == time_str:
            send(message.get(),rep)
            status.insert(END,"Scheduled message sent to %s.\n"%(name.get()))
            start_scheduling=False
        window.after(500,schedule)

window = Tk()
window.resizable(height = 0, width = 0)
window.iconbitmap(resource_path('icon.ico'))
style = ThemedStyle(window)
style.set_theme("scidgrey")

def on_closing():
    if tmsg.askokcancel("Quit", "Do you want to quit?"):
        global start_monitor
        start_monitor=False
        window.destroy()
        driver.close()
        driver.quit()
        sys.exit()

def W_main(main):
    main.title("Whatsapp Monster")
    main.update_idletasks()
    pady=(main.winfo_screenheight() // 2)
    padx=(main.winfo_screenwidth() // 2)
    main.geometry('+{}+{}'.format(padx,pady))

    # --- functions ---

    def quit():
        global start_monitor
        start_monitor=False
        window.quit()
        driver.close()
        driver.quit()
        sys.exit()


    def about():

        msg='''

                Designed and developed by
                        Nitesh

            Link to github.
                '''
        a=tmsg.showinfo("About Message Monster",msg)



    def show_url():
        tmsg.showinfo("Under Development","Under Development")
    def new_url():
        tmsg.showinfo("Under Development","Under Development")
    def write():
        tmsg.showinfo("Process Started","Under Development")
        #Add file name
        #graph

    #Menu
    mymenu=Menu(main)
    notimenu=Menu(mymenu,tearoff=0)
    mymenu.add_cascade(label="Notification",menu=notimenu)
    mymenu.add_command(label="About",command=about)
    mymenu.add_command(label="Exit",command=quit)

    notimenu.add_command(label="Show url",command=show_url)
    notimenu.add_separator()
    notimenu.add_command(label="Generate url",command=new_url)
    notimenu.add_command(label="Write to csv",command=write)
    main.config(menu=mymenu)


W_main(window)

frame1=Frame(window,height=window.winfo_height()/2,width=window.winfo_width()/2)#,bg="green"
frame1.grid(column=0,row=1,sticky="NS")
frame2=Frame(window,height=window.winfo_height()/2,width=window.winfo_width()/2)#,bg="red"
frame2.grid(column=1,row=1)#columnspan=2,



image = Image.open(os.path.join(resource_path(path), "no_dp.png"))

img = ImageTk.PhotoImage(image)
panel = Label(frame2, image=img, width = 200, height = 200)
panel.grid(row=0,rowspan=2)



# run=1
# rep=1

def submit():
    global run
    global rep
    global start_monitor
    if name.get() != "Name" and len(name.get()) != 0:
        # For First time clicking submit...Update Dp
        if run == 1 :
            search(name.get())
            start_monitor=True
            # print("Monitor value changed")
            monitor()
            response=get_dp()
            # print("Photo saved in : ",response)
            image2=Image.open(response)
            image2 = image2.resize((200,200))
            img2 = ImageTk.PhotoImage(image2)
            panel.configure(image=img2)
            panel.image = img2
            run=0

        if repeat.get() !=  "Default:1":
            rep=int(repeat.get())
        if len(message.get()) != 0: #Check if message field is empty
            if(time.get()!="HH:MM:(AM/PM)"): #Check if time field is empty
                rex = re.compile("^[0-9]{2}\:[0-9]{2}\:[A-Z]{2}$")
                if rex.match(time.get()):
                    search(name.get())
                    global start_scheduling
                    start_scheduling=True
                    schedule()
                    response="m_scheduled_sent"
                else:
                    print("Incorrect")
                    response=""
                    tmsg.showerror("Error","Incorrect format!")

            if(time.get()=="HH:MM:(AM/PM)"):
                    response=send(message.get(),rep)
            if response == "m_sent":
                status.insert(END,"Message sent to %s.\n"%(name.get()))
            elif response == "m_scheduled_sent":
                status.insert(END,"Message scheduled for sending to %s.\n"%(name.get()))
            else:
                status.insert(END,"Message send Failed.\n")

def clear():
    e1.delete(0, END)
    e2.delete(0, END)
    status.delete(END)
    e1.insert(0, "Name")
    e1.configure(state=DISABLED)
    e2.insert(0, "Messages")
    e2.configure(state=DISABLED)
    on_click_id = e1.bind('<Button-1>', on_click)
    e5.delete(0, END)
    e5.insert(0,"HH:MM:(AM/PM)")
    e5.configure(state=DISABLED)
    on_click_time_id = e5.bind("<1>",on_click_time)
    e6.delete(0, END)
    e6.insert(0, "Default:1")
    e6.configure(state=DISABLED)
    on_click_repeat_id = e6.bind("<1>",on_click_repeat)

    global run
    run=1 #if this is executing for the first time

label=Label( window, text="Message Monster" , fg="blue" , font="times 24",padx=20,pady=20)#,bg='blue'
label.grid(row=0,column=0)



name=StringVar()
e1=ttk.Entry(frame1,textvariable=name,style="EntryStyle.TEntry")
e1.grid(row=0,column=0,pady=0,padx=window.winfo_width()/2)
e1.insert(0, "Name")
e1.configure(state=DISABLED)

message=StringVar()
e2=ttk.Entry(frame1,textvariable=message)
e2.grid(row=1,column=0,pady=5,padx=window.winfo_width()/4)
e2.insert(0, "Messages")
e2.configure(state=DISABLED)

e3=Label(frame2,textvariable=name,font="times 12 bold",fg="green")
e3.grid(row=2)


cur_status=StringVar()
e4=Label(frame2,textvariable=cur_status,font="times 12 bold",fg="red")
e4.grid(row=3)
cur_status.set("Offline")


frame3=Frame(frame1,width=window.winfo_width()/4)#,,height=window.winfo_height()/2
frame3.grid(column=0,row=3,sticky='W')
frame4=Frame(frame1,width=window.winfo_width()/4)
frame4.grid(column=0,row=3,sticky="E")#columnspan=2,

l1=Label(frame3,text="Scheduled Time : ")
l1.grid(row=0,column=0,sticky="E",padx=[35,0])#6

time=StringVar()
e5=ttk.Entry(frame4,textvariable=time)
e5.grid(row=0,column=0,sticky="W",padx=[0,30])
e5.insert(0,"HH:MM:(AM/PM)")
e5.configure(state=DISABLED)


repeat=StringVar()
l2=Label(frame3,text="Spam times : ")
l2.grid(row=1,column=0,sticky="E",padx=[35,0],pady=5)

e6=ttk.Entry(frame4,textvariable=repeat)
e6.grid(row=1,column=0,sticky="W",padx=[0,30],pady=8)
e6.insert(0, "Default:1")
e6.configure(state=DISABLED)

def on_click(event):
    e1.configure(state=NORMAL)
    e1.delete(0, END)
    e2.configure(state=NORMAL)
    e2.delete(0, END)


on_click_id = e1.bind('<Button-1>', on_click)

def on_click_time(event):
    e5.configure(state=NORMAL)
    e5.delete(0,END)

on_click_time_id = e5.bind("<1>",on_click_time)

def on_click_repeat(event):
    e6.configure(state=NORMAL)
    e6.delete(0,END)

on_click_repeat_id = e6.bind("<1>",on_click_repeat)

status = Text(frame2,height=10,width=40)
status.grid(row=4,column=0)

status.insert(END,"Starting the Program\n")
scrollbar = ttk.Scrollbar(frame2)
scrollbar.grid(row=4,column=0,sticky = "NSE")
scrollbar.config( command = status.yview )

b1=ttk.Button(frame1,text="Submit",command=submit)
b1.grid(row=4,column=0,pady=[100,50],padx=50)

b2=ttk.Button(frame1,text="  Reset  ",command=clear)
b2.grid(row=5,column=0,pady=10,padx=10)

work_dir=os.getcwd()
os.chdir(directory)
chrome_options = Options()
chrome_options.add_argument('--user-data-dir=User_Data')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging']) #To supress promt in cmd
os.chdir(work_dir)
driver=webdriver.Chrome(resource_path("./driver/chromedriver.exe"),options=chrome_options)#Change it to make distribuable
driver.get("https://web.whatsapp.com/")
if conf=="First_Time=True":
    driver.maximize_window()
else:
    tmsg.showinfo("QR-Code","Scan the QR code")
    driver.maximize_window()
window.protocol("WM_DELETE_WINDOW",on_closing)
window.mainloop()
