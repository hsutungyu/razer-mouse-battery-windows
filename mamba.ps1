# ask for user input for the time interval (default = 15)
$default_time_interval = 15
$time_interval = Read-Host "Please enter a time interval (in minutes) for the notification (Press Enter for default: [$($default_time_interval)])"
$time_interval = ($default_time_interval, $time_interval)[[bool]$time_interval]

# install python packages
python.exe -m pip install -r ./requirements.txt

# set scheduled task, run script every 15 minutes
$action = New-ScheduledTaskAction -Execute 'pythonw.exe' -Argument 'mamba.pyw'
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes $time_interval)
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "Mamba Wireless Battery Indicator" -Description "A Python script that shows the battery level of a Razer Mamba Wireless mouse as a tray notification every 15 minutes by default."