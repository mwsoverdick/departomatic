# Departomatic


Ride the bus? Have to walk to the stop? Hate not knowing if now's a good time to leave?

Well, now there's Departomatic. Paste your bus schedule into `times.csv`, configure yourr `options.yaml` and run this script at startup. 

You'll get a windows tray icon that changes color:

## Icon color meainings
red: Don't bother going, you'll be at the stop forever
green: Go now, you won't wait very long
yellow: It's a bit iffy but you'll probs make it in time
white: Idk, maybe an error, who knows

## Limitations

- This was written in less than an hour
- It is for Windows and Windows only
- Up to you to find the rest

## "installing"

1. Hit Win + R and type `shell:startup` and hit enter
2. Copy `departomatic.bat` to the folder that opens
3. Edit the copied `departomatic.bat` to have the `cd` line point to where this code is checked out