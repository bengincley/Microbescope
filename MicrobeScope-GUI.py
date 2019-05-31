"""Sets up a GUI for running the MicrobeScope main program. Highest
level of abstraction
Written by Ben Gincley and Zach Flinkstrom"""
from guizero import App, Text, TextBox, PushButton, CheckBox, ButtonGroup
from time import sleep
import datetime
import controls
import time


def save_inputs():
    '''Saves user input values'''
    #print(input_log_name.value)
    #print(save_img_check.value)
    #print(save_img_dir.value)
    #print(sample_frequency.value)
    #print(sample_volume.value)
    print("Settings saved.")
    save_button.bg = "#a0db8e"
    save_button.bg = "#a0db8e"
    save_button.text = "Settings Saved."
    #return logfile_name, save_img, sample_frequency, save_img_dir_name
    ##Save values to be accessible by controls


def reset():
    save_button.bg = "#ff4b4b"
    save_button.text = "Save Settings?"


def calibrate():
    '''Opens a preview window allowing user to focus camera'''
    print("calibrating microbescope...")
    controls.calibrate_preview()
    print("calibration step completed.")
    #background = controls.calibrate_preview()
    #return background

def run():
    '''Calls controls module to actually run the device
    ie cycle valve, take image, and process'''
    print("Hunting microbes...")
    Text(app, text="Running the ARTIMiS...")
    start_time = datetime.datetime.now()
    s_t = time.time()
    sample_interval = float(sample_frequency.value)
    print("Start Time: %s" % s_t)
    print("Sample Interval: %s seconds" % sample_interval)
    sleep(1)
    s_t = time.time()
    sample = controls.Sample(sample_interval, sample_volume.value,
                             input_log_name.value, save_img_check.value,
                             save_img_dir.value)
    sample.sample_run()
    end_time = datetime.datetime.now()
    e_t = time.time()
    print("End Time: %s" % e_t)
    run()


'''Lays out the GUI that pops up'''
app = App(title="ARTIMiS")
welcome_message = Text(app, text="Welcome to the ARTIMiS", size=24, color="#0000FF")

#Log File
outputfile_name = Text(app, text="Specify a save path/name for log file:", size=10, color="#000000")
input_log_name = TextBox(app, width=30, text="/home/pi/Desktop/4-19/LOGFILE")
#Save Images
save_img_check = CheckBox(app, text="Keep images?", grid=[1, 1], align="left")
Text(app, "Specify save directory:", size=10, color="#000000")
save_img_dir = TextBox(app, width=20, text="/home/pi/Desktop/4-19/")
#Sampling
sample_freq_text = Text(app, text="Specify sample frequency:", size=10, color="#000000")
sample_frequency = ButtonGroup(app, options=[["1min", "60"],["30min", "1800"], ["1hr", "3600"], ["2hr", "7200"], ["6hr", "21600"], ["12hr", "43200"]],
                              selected="1", horizontal=True, grid=[1, 2], align="left")
#Sample Volume
sample_volume_box = Text(app, text="Specify sample volume (uL):", size=10, color="#000000")
sample_volume = TextBox(app, width=3, text="1")

#Save Button
save_button = PushButton(app, text="Save Settings?")
save_button.bg = "#ff4b4b"
save_button.when_clicked = save_inputs
input_log_name.when_clicked = reset
save_img_check.when_clicked = reset
save_img_dir.when_clicked = reset
sample_frequency.when_clicked = reset
sample_volume_box.when_clicked = reset

#Calibrate Button
cal_button = PushButton(app, text="Calibrate MicrobeScope")
cal_button.when_clicked = calibrate

#Run Button
run_button = PushButton(app, text="Run MicrobeScope")
run_button.when_clicked = run

#Stop Button
Text(app, "To stop, enter Ctrl+C in the command line.", size=12, color="#000000")

app.display()

