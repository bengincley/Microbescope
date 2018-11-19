from guizero import App, Text, TextBox, PushButton, CheckBox, ButtonGroup


def save_inputs():
    print(input_log_name.value)
    print(save_img_check.value)
    print(sampling_choice.value)
    print(save_img_dir.value)
    save_button.bg = "#a0db8e"
    save_button.text = "Settings Saved."
    ##Save values to be accessible by controls


def reset():
    save_button.bg = "#ff4b4b"


def run():
    print("running microbescope...")
    Text(app, text="Running the Microbescope...")
    ## Run control program


#Initialize
app = App(title="Welcome to Microbescope")
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
sampling_choice = ButtonGroup(app, options=[["48", "48"], ["24", "24"], ["12", "12"], ["6", "6"], ["2", "2"]],
                              selected="24", horizontal=True, grid=[1, 2], align="left")
#Save Button
save_button = PushButton(app, text="Save Settings?")
save_button.bg = "#ff4b4b"
save_button.when_clicked = save_inputs
input_log_name.when_clicked = reset
save_img_check.when_clicked = reset
sampling_choice.when_clicked = reset

#Run Button
run_button = PushButton(app, text="Run Microbescope")
run_button.when_clicked = run

app.display()

# Save images to file?
# Name for output log file
# Sample frequency - how many samples per day
# Run now