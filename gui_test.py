from guizero import App, Text, TextBox, PushButton, CheckBox, ButtonGroup
from time import sleep
#import controls


def save_inputs():
    print(input_log_name.value)
    print(save_img_check.value)
    print(sample_frequency.value)
    print(save_img_dir.value)
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
    Text(app, text="Running the Microbescope...")
    #sample = controls.Sample(sample_frequency.value, input_log_name.value, save_img_check.value, save_img_dir.value)
    #sample.sample_run()


# def stop():
#     print("stopping microbescope...")
#     Text(app, text="Stopping the Microbescope")
#     global governor
#     governor = False
#     # Stop program


#Initialize
#logfile_name = "default"
#sample_frequency = 24

app = App(title="Hello world")
welcome_message = Text(app, text="Welcome to the Microbescope", size=24, color="#0000FF")

#Log File
outputfile_name = Text(app, text="Specify a name for log file:", size=10, color="#000000")
input_log_name = TextBox(app, width=20)
#Save Images
save_img_check = CheckBox(app, text="Keep images?", grid=[1, 1], align="left")
Text(app, "Specify image directory:", size=10, color="#000000")
save_img_dir = TextBox(app, width=20, text="/home/pi/")
#Sampling
sample_freq_text = Text(app, text="Specify # samples per day:", size=10, color="#000000")
sample_frequency = ButtonGroup(app, options=[["48", "48"], ["24", "24"], ["12", "12"], ["6", "6"], ["2", "2"]],
                              selected="24", horizontal=True, grid=[1, 2], align="left")
#Save Button
save_button = PushButton(app, text="Save Settings?")
save_button.bg = "#ff4b4b"
save_button.when_clicked = save_inputs
input_log_name.when_clicked = reset
save_img_check.when_clicked = reset
save_img_dir.when_clicked = reset
sample_frequency.when_clicked = reset

#Calibrate Button
cal_button = PushButton(app, text="Calibrate Microbescope")
cal_button.when_clicked = calibrate

#Run Button
run_button = PushButton(app, text="Run Microbescope")
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