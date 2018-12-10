from guizero import App, Text, TextBox, PushButton, CheckBox, ButtonGroup
from time import sleep
import datetime
#import controls


def save_inputs():
    print(input_log_name.value)
    print(save_img_check.value)
    print(save_img_dir.value)
    print(sample_frequency.value)
    print(sample_volume.value)
    save_button.bg = "#a0db8e"
    save_button.bg = "#a0db8e"
    save_button.text = "Settings Saved."
    #return logfile_name, save_img, sample_frequency, save_img_dir_name
    ##Save values to be accessible by controls


def reset():
    save_button.bg = "#ff4b4b"


def calibrate():
    print("calibrating microbescope...")
    #controls.calibrate_preview()


def run():
    print("running microbescope...")
    Text(app, text="Running the MicrobeScope...")
    start_time = datetime.datetime.now()
    s_t = (start_time.minute + start_time.hour*60)*60+start_time.second
    sample_interval = round(float(sample_frequency.value)*3600)
    print(s_t)
    print(sample_interval)
    sleep(10)
    #sample = controls.Sample(sample_frequency.value, sample_volume.value, input_log_name.value, save_img_check.value, save_img_dir.value)
    #sample.sample_run()
    end_time = datetime.datetime.now()
    e_t = (end_time.hour*60 + end_time.minute)*60+end_time.second
    print(e_t)
    elapsed = e_t-s_t
    print(elapsed)
    print(sample_interval-elapsed)
    sleep(sample_interval-elapsed)
    run()


# def stop():
#     print("stopping microbescope...")
#     Text(app, text="Stopping the Microbescope")
#     global governor
#     governor = False
#     # Stop program


#Initialize
#logfile_name = "default"
#sample_frequency = 24

app = App(title="MicrobeScope")
welcome_message = Text(app, text="Welcome to the MicrobeScope", size=24, color="#0000FF")

#Log File
outputfile_name = Text(app, text="Specify a save path/name for log file:", size=10, color="#000000")
input_log_name = TextBox(app, width=30, text="/home/pi/Desktop/LOGFILE")
#Save Images
save_img_check = CheckBox(app, text="Keep images?", grid=[1, 1], align="left")
Text(app, "Specify save directory:", size=10, color="#000000")
save_img_dir = TextBox(app, width=20, text="/home/pi/")
#Sampling
sample_freq_text = Text(app, text="Specify sample frequency:", size=10, color="#000000")
sample_frequency = ButtonGroup(app, options=[["1min", "0.0167"],["30min", "0.5"], ["1hr", "1"], ["2hr", "2"], ["6hr", "6"], ["12hr", "12"]],
                              selected="1", horizontal=True, grid=[1, 2], align="left")
#Sample Volume
#Log File
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

#Calibrate Button
cal_button = PushButton(app, text="Calibrate MicrobeScope")
cal_button.when_clicked = calibrate

#Run Button
run_button = PushButton(app, text="Run MicrobeScope")
run_button.when_clicked = run

#Stop Button
Text(app, "To stop, enter Ctrl+C in the command line.", size=12, color="#000000")

# stop_button = PushButton(app, text="Stop Microbescope")
# stop_button.when_clicked = stop

app.display()
# Start Calibration
# Save images to file?
# Name for output log file
# Sample frequency - how many samples per day
# Run now