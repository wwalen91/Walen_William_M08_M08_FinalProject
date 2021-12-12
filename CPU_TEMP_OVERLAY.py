## CPU Temperature Overlay
## Author: William Walen (With loads of help from many online resources)
## Version: 1.0

## Program must be ran with Administrator permissions for it to read the temperature data

## In this section we are importing the modules and resources we need to run the program
import clr # the pythonnet module
clr.AddReference(r'\DLLs\OpenHardwareMonitorLib')
from tkinter import *
import tkinter as tk
from OpenHardwareMonitor.Hardware import Computer
from threading import Timer

c = Computer()
c.CPUEnabled = True  ## Getting the Info about CPU
c.GPUEnabled = True ## Getting the Info about GPU
c.Open()


## After tireless nights of trying to figure out how to get the temperatures to update automatically
## I finally got this class to do the heavy lifting for me
## I tried other methods, however, using 'while' loops would constantly crash the program
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

## These next two functions enable the user to move the window where they deem fit by clicking anywhere on the window itself
def SaveLastClickPos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y
def Dragging(event):
    x, y = event.x - lastClickX + window.winfo_x(), event.y - lastClickY + window.winfo_y()
    window.geometry("+%s+%s" % (x , y))

## This section I'm opening a window and naming it
window = Tk()
window.title("CPU Monitor")
window.geometry("+700+400")
window.attributes('-alpha', 0.5)
window.attributes('-topmost', True)
window.bind('<Button-1>', SaveLastClickPos)
window.bind('<B1-Motion>', Dragging)
window.configure(bg='black')
window.overrideredirect(True)
background_img = PhotoImage(file = 'images/darkground.png') ## Second image used for project completeness
background_label = Label(window, image=background_img)
background_label.place(x=-2, y=-2)

## I'm leaving this next line in the code for if anyone wants to replace the background color with complete transparency
##window.wm_attributes('-transparentcolor', '#ab23ff')


## The next section is the function that displays the temperature readouts for the cpu and gpu
def cpuRead():
        for a in range(0, len(c.Hardware[0].Sensors)):
            ## Where the following code states "if "/temperature/#"" this is identifying the specific temperature for the core number
            if "/temperature/1" in str(c.Hardware[0].Sensors[a].Identifier):
                cpu_temp = c.Hardware[0].Sensors[a].get_Value()
                cpu_core_1_C["text"]=str(cpu_temp)
                cpu_tempF = (cpu_temp * 9/5) + 32
                cpu_core_1_F["text"]=str(cpu_tempF)
                c.Hardware[0].Update()
            if "/temperature/2" in str(c.Hardware[0].Sensors[a].Identifier):
                cpu_temp = c.Hardware[0].Sensors[a].get_Value()
                cpu_core_2_C["text"]=str(cpu_temp)
                c.Hardware[0].Update()
                cpu_tempF = (cpu_temp * 9/5) + 32
                cpu_core_2_F["text"]=str(cpu_tempF)
            if "/temperature/3" in str(c.Hardware[0].Sensors[a].Identifier):
                cpu_temp = c.Hardware[0].Sensors[a].get_Value()
                cpu_core_3_C["text"]=str(cpu_temp)
                c.Hardware[0].Update()
                cpu_tempF = (cpu_temp * 9/5) + 32
                cpu_core_3_F["text"]=str(cpu_tempF)
            if "/temperature/4" in str(c.Hardware[0].Sensors[a].Identifier):
                cpu_temp = c.Hardware[0].Sensors[a].get_Value()
                cpu_core_4_C["text"]=str(cpu_temp)
                c.Hardware[0].Update()
                cpu_tempF = (cpu_temp * 9/5) + 32
                cpu_core_4_F["text"]=str(cpu_tempF)
            if "/temperature/5" in str(c.Hardware[0].Sensors[a].Identifier):
                cpu_temp = c.Hardware[0].Sensors[a].get_Value()
                cpu_core_5_C["text"]=str(cpu_temp)
                c.Hardware[0].Update()
                cpu_tempF = (cpu_temp * 9/5) + 32
                cpu_core_5_F["text"]=str(cpu_tempF)
            if "/temperature/6" in str(c.Hardware[0].Sensors[a].Identifier):
                cpu_temp = c.Hardware[0].Sensors[a].get_Value()
                cpu_core_6_C["text"]=str(cpu_temp)
                c.Hardware[0].Update()
                cpu_tempF = (cpu_temp * 9/5) + 32
                cpu_core_6_F["text"]=str(cpu_tempF)
            if "/temperature/7" in str(c.Hardware[0].Sensors[a].Identifier):
                cpu_temp = c.Hardware[0].Sensors[a].get_Value()
                cpu_core_7_C["text"]=str(cpu_temp)
                c.Hardware[0].Update()
                cpu_tempF = (cpu_temp * 9/5) + 32
                cpu_core_7_F["text"]=str(cpu_tempF)
            if "/temperature/8" in str(c.Hardware[0].Sensors[a].Identifier):
                cpu_temp = c.Hardware[0].Sensors[a].get_Value()
                cpu_core_8_C["text"]=str(cpu_temp)
                c.Hardware[0].Update()
                cpu_tempF = (cpu_temp * 9/5) + 32
                cpu_core_8_F["text"]=str(cpu_tempF)
        for a in range(0, len(c.Hardware[1].Sensors)):
            if "/temperature/0" in str(c.Hardware[1].Sensors[a].Identifier):
                gpu_temp = c.Hardware[1].Sensors[a].get_Value()
                gpu_core_C["text"]=str(gpu_temp)
                c.Hardware[1].Update()
                gpu_tempF = (gpu_temp * 9/5) + 32
                gpu_core_F["text"]=str(gpu_tempF)
## Though the most simplest looking part of this code, this part took a good while for me to figure out
## I found that I could use the RepeatedTimer class (that I found online) to get the values for the temperatures
## to update at the speed I'd pick (the 0.8 below), getting the program to be able to respond to other commands
## without crashing nearly made me cry
def start():
    global reader  ## Adding this simple bit of code allows the reader variable to be contacted by other functions
    reader = RepeatedTimer(0.8, cpuRead) ## the 0.8 here can be modified to update the temperatures faster if the user wishes
def stop():
    if 'reader' in globals(): ## Adding the 'if' statement allows the function to check if reader has been defined yet
        reader.stop()  ## After setting reader to a "global" variable, forcing the reading to stop was as simple as this command

def exit(): ## Without forcing reader to stop, the program will crash when trying to quit, which isn't the way we want it to work
    if 'reader' in globals():
        reader.stop()
        window.destroy()
    else:            ## In addition to adding the 'if' statement, adding the 'else' statement allows the function to execute in an either or condition
        window.destroy()

## This defines the function for opening my second window called "About Page"
def about():
    about_page = tk.Toplevel()
    def shutdown():
        about_page.destroy()
    about_page.title("About Page")
    background_image = tk.PhotoImage(file = 'images/Blackheartstudio_img.png') ## Original image
    about_page.geometry("214x231")
    about_page.geometry("+700+400")
    about_page.attributes('-alpha', 0.8)
    about_page.attributes('-topmost', True)
    about_page.configure(bg='black')
    about_page.overrideredirect(True)
    background = Button(about_page, image=background_image, command=shutdown)
    background.pack()
    about_page.mainloop()

## This next section is my drop down menu, totalling in 5 buttons with a 6th button if you include the about page button
options = Menubutton(window,text="Options",bg="gray",activebackground="white")
options.grid()
options.menu = Menu(options,tearoff=0)
options["menu"]=options.menu
options.menu.add_command(label="Start Reading", command=start)
options.menu.add_command(label="Stop Reading", command=stop)
options.menu.add_command(label="Close", command=exit)
options.menu.add_command(label="About", command=about)

## The following section are my labels
## Most important features here are the bg and fg colors
## Setting the bg color to black will allow the label to blend with the background of the window
## Setting the fg color to white allows for the maximum contrast color for readibility ( if that is a word )
celsius = Label(window, text="Celsius",bg="black",fg="white")
fahren = Label(window, text="Fahren",bg="black",fg="white")
cpu_core_1 = Label(window,text="Core 1:",bg="black",fg="white")
cpu_core_2 = Label(window,text="Core 2:",bg="black",fg="white")
cpu_core_3 = Label(window,text="Core 3:",bg="black",fg="white")
cpu_core_4 = Label(window,text="Core 4:",bg="black",fg="white")
cpu_core_5 = Label(window,text="Core 5:",bg="black",fg="white")
cpu_core_6 = Label(window,text="Core 6:",bg="black",fg="white")
cpu_core_7 = Label(window,text="Core 7:",bg="black",fg="white")
cpu_core_8 = Label(window,text="Core 8:",bg="black",fg="white")
gpucore = Label(window,text="GPU:",bg="black",fg="white")
cpu_core_1_C = Label(window,text="00.0",bg="black",fg="white")
cpu_core_2_C = Label(window,text="00.0",bg="black",fg="white")
cpu_core_3_C = Label(window,text="00.0",bg="black",fg="white")
cpu_core_4_C = Label(window,text="00.0",bg="black",fg="white")
cpu_core_5_C = Label(window,text="00.0",bg="black",fg="white")
cpu_core_6_C = Label(window,text="00.0",bg="black",fg="white")
cpu_core_7_C = Label(window,text="00.0",bg="black",fg="white")
cpu_core_8_C = Label(window,text="00.0",bg="black",fg="white")
gpu_core_C = Label(window,text="00.0",bg="black",fg="white")
cpu_core_1_F = Label(window,text="00.0",bg="black",fg="white")
cpu_core_2_F = Label(window,text="00.0",bg="black",fg="white")
cpu_core_3_F = Label(window,text="00.0",bg="black",fg="white")
cpu_core_4_F = Label(window,text="00.0",bg="black",fg="white")
cpu_core_5_F = Label(window,text="00.0",bg="black",fg="white")
cpu_core_6_F = Label(window,text="00.0",bg="black",fg="white")
cpu_core_7_F = Label(window,text="00.0",bg="black",fg="white")
cpu_core_8_F = Label(window,text="00.0",bg="black",fg="white")
gpu_core_F = Label(window,text="00.0",bg="black",fg="white")

## This section sets up the grid pattern for the GUI
options.grid(row=0,column=0)
celsius.grid(row=0,column=1)
fahren.grid(row=0,column=2)
cpu_core_1.grid(row=1,column=0)
cpu_core_1_C.grid(row=1,column=1)
cpu_core_1_F.grid(row=1,column=2)
cpu_core_2.grid(row=2,column=0)
cpu_core_2_C.grid(row=2,column=1)
cpu_core_2_F.grid(row=2,column=2)
cpu_core_3.grid(row=3,column=0)
cpu_core_3_C.grid(row=3,column=1)
cpu_core_3_F.grid(row=3,column=2)
cpu_core_4.grid(row=4,column=0)
cpu_core_4_C.grid(row=4,column=1)
cpu_core_4_F.grid(row=4,column=2)
cpu_core_5.grid(row=5,column=0)
cpu_core_5_C.grid(row=5,column=1)
cpu_core_5_F.grid(row=5,column=2)
cpu_core_6.grid(row=6,column=0)
cpu_core_6_C.grid(row=6,column=1)
cpu_core_6_F.grid(row=6,column=2)
cpu_core_7.grid(row=7,column=0)
cpu_core_7_C.grid(row=7,column=1)
cpu_core_7_F.grid(row=7,column=2)
cpu_core_8.grid(row=8,column=0)
cpu_core_8_C.grid(row=8,column=1)
cpu_core_8_F.grid(row=8,column=2)
gpucore.grid(row=10,column=0)
gpu_core_C.grid(row=10,column=1)
gpu_core_F.grid(row=10,column=2)

window.mainloop()