# Departomatic: 🚶/🚲 ➡️ 🚌


Ride the bus to work? Have to walk/bike to the stop? Hate not knowing if now's a good time to leave? Don't like having to fumble with your phone to check?

Well, now there's ✨Departomatic🌈. Paste your bus schedule into `times.csv`, configure your `options.yaml` and run this script at starup.

When it is running, icons will appear in your system tray (Windows) or menu bar (Mac) indicating whether or not it's a good time to leave for the bus.

## Icons

🤷 = App does not know/error (idk)

🚶 = Now's a solid time to leave (go!)

⚠️ = Time's running out to leave, better hurry up (iffy)

✋ = Don't bother going, you'll be waiting at the stop a long time (wait)

## Limitations

- This works crudely for Windows and MacOS
- There is no intention to make this web scrape or call APIs
- Having it run automatically at startup is manually configured
- Only 1 schedule is supported

## Configuring

Currently, the app expects 2 files to be in the same directory it runs from:

1. `times.csv` - A single-column CSV with departure times for the stop you're interested in
2. `options.yaml` - The configuration of how the app should behave for you

### `times.csv`

This is where you put the scheduled departure times for your stop of interest. This is intended to be for bus routes where the schedule is the same Monday through Friday, which is typical for most routes.

This CSV expects the following format rules:

1. Only one column (so no commas in this csv)
2. Times must be in 12-hour format
3. Times must end in `AM`, `PM`, `a.m.`, or `p.m.`
4. Times must be formatted as such: `H:M P`
   - `H` is 1 or 2 digit hour
   - `M` is one or 2 digit minute
   - `P` is the AM/PM distinction

### `options.yaml`

`options.yaml` currently only supports the following parameters

1. `route` - A friendly name for the route (e.g. `Metro Route 44 Ballard`)
2. `wait` - The threshold for when it's too long of a time to departure to bother heading to the bus (in minutes)
3. `go` - The threshold for when it's a prime opportunity to head to the bus (in minutes)
4. `iffy` - The threshold for when you might risk missing the bus if you leave now (in minutes)

#### Thresholds Explained

Imagine the scenario where you work at an office in a bit of a transit desert. That is, there's no good bus connections near your office, and you need to walk or bike a sizable distance/time to get to your normal bus stop.

Let's say it normally takes you 5 minutes to reliably get to the bus stop before the bus comes. That means if you leave 4 minutes before the bus departs you might risk missing the bus, and if you leave 10 minutes before the bus departs, you're wasting time sitting at the bus stop.

Therefore, you may want this configuration:

```yaml
route: "Slightly inconvenient route"
wait: 8
go: 5
iffy: 4
```

This would tell you to go to the bus when there is 5 to 8 minutes until the scheduled departure. It would tell you that it is risky if there is 4-5 minutes to departure (you might need to run). And it would tell you to wait if there is less than 4 minutes to departure, or greater than 8 minutes.

## "installing"

### Windows

1. Hit Win + R and type `shell:startup` and hit enter
2. Copy `departomatic.bat` to the folder that opens
3. Edit the copied `departomatic.bat` to have the `cd` line point to where this code is checked out

### MacOS

1. Create a .sh script that launches Departomatic
2. In System Preferences > Users and Groups > Login Items, add the script you created
3. You're done.