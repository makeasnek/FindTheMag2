#####################################################################
############## GENERAL SETTINGS. YOU SHOULD EDIT THESE ##############
#####################################################################
## This is the default config.py. You can make edits here, but it is suggested to make a file "user_config.py" in this same
## directory, copy the contents of this file there, and make edits in user_config. This way, you can update with "git pull" and not
## have your settings over-written by defaults. Settings in user_config.py always override config.py.

## Editing tip: If using "None" for a setting, it must be written as None without any quotes. Capitalization matters

# Your "preferred projects list". Work will be split among these projects according to a given percentage (10, 20, 80).
# For example, if you want 80% of your "preferred project crunching time" to go to a particular project, put in 80. These values must add up to 100.
# If you just want to crunch the most profitable projects all the time (default), leave as is. To customize weight for projects, comment out the next line (and un-comment the subsequent lines) and add projects according to format given:
preferred_projects={}
#preferred_projects={
#    'https://www.sidock.si/sidock/':20,
#    'https://www.project2.com':80,
#}
# percent of resources to dedicate to preferred projects
preferred_projects_percent=10  # example: 80. This is ignored if preferred_projects has no projects in it. Rest of weight is assigned to most profitable project according to further settings below
# projects on the IGNORED_PROJECTS list will always have their weight set to zero.
IGNORED_PROJECTS=['https://foldingathome.div72.xyz/', 'http://exampleproject.com/project2'] # leave as is if you have no ignored projects
##########################################################################################################################################
##############    PROFITABILITY SETTINGS. EDIT THESE IF YOU WANT PROFITABILITY TAKEN INTO ACCOUNT WHEN SUGGESTING WEIGHTS   ##############
##########################################################################################################################################
local_kwh=0.1542 # your local price of energy per kwh in USD. Default: 0.1542 (US National average). You can find this on your electric bill.
grc_sell_price=None # the price you intend to sell your mined GRC at. Leave None to use "current price" or put in USD value of 1 GRC. This is used to determine if mining is "profitable" or not
exchange_fee=0 # amount to factor into "sell price" when determining profitability. For 3% put .03, for 10% put .10 etc. Default is 0
only_BOINC_if_profitable=False # suspend BOINC completely whenever crunching is not profitable
only_mine_if_profitable=False # only run non-preferred projects when doing so is profitable. Benchmarking will still occur.
host_power_usage=70 # estimated wattage of your mining rig at full use. Check your power supply for the maximum it can deliver and use that number if unsure. Default 70
min_profit_per_hour=0.00 # mining is only "profitable" if it generates greater than this amount of profit in USD. Default: 0.00

##########################################################################################################################################
##############      BOINC CONTROLLER. EDIT THESE IF YOU WANT TO CONTROL THE BOINC CLIENT ACCORDING TO SUGGESTED WEIGHTS     ##############
##########################################################################################################################################
control_boinc=True # Set to True to use this as your BOINC manager and directly manage the BOINC client. You can still use BOINC Manager/boinctui to monitor its progress. Default: False
# Dev fee: I hope you'll see that this is only a portion of the efficency gain this tool will give you.
dev_fee=.05 # % of processing power to donate to developer, .05=5%, .10 = 10%, etc. This also gets sidestaked to the Gridcoin foundation and gridcoinstats as this script relies on them for some stats if you don't have the wallet installed. Minimum is .01. All energy still goes to science, you just crunch under the developer's account. Note this is skipped if you have sidestaking to dev enabled, which I suggest doing for simplicity. It will also save you up to 10GB of disk space.
SCRIPTED_RUN:bool=False # If True, skip steps where we ask user for input and instead handle everything automatically.
SKIP_TABLE_UPDATES:bool=False # If true, don't print table updates. Useful for scripted runs to reduce output.

##########################################################################################################################################
############      TEMPERATURE SETTINGS. EDIT THESE IF YOU WANT TO CONTROL THE BOINC CLIENT ACCORDING TO TEMPERATURE           ############
##########################################################################################################################################
ENABLE_TEMP_CONTROL=False # Enable controlling BOINC based on temp. Default: False
START_TEMP=65 # Start crunching if temp > this number, whole numbers only! Default: 65.
STOP_TEMP=75 # Stop crunching is temp > this number, whole numbers only! Default: 75
# Methods of fetching temp data, only use one!
TEMP_URL=None # URL to fetch temperature data from, Default: None. # Note this will check temperature quite frequently. This is fine for your smart thermostats on a local IP but not great for publicly-accesible data points. Example: 'https://mytempcheck.com'
TEMP_COMMAND=None # Shell command to run to check temp data. Must use absolute paths ie '/bin/bash /home/user/tempcheck.sh'.
TEMP_REGEX= r'\d*' # Regular expression used to scrape temp from command, URL, or other specified source. This just grabs the first sequence of numbers it finds. Default: r'\d*'. Examples: https://www.dataquest.io/blog/regex-cheatsheet/
TEMP_SLEEP_TIME=10 # If we should stop crunching due to temp, sleep this many minutes before checking again. Default: 10
# If you want to write a custom function to retrieve temperature information, put it here. It must return a string value such as '70' or None
def TEMP_FUNCTION():
    # blah blah blah your code here
    return None
##########################################################################################################################################
##############                ADVANCED SETTINGS. DO NOT EDIT THESE IF YOU DON'T UNDERSTAND THEIR IMPLICATIONS               ##############
##########################################################################################################################################
lookback_period=30 # Number of days to look back to calculate credit -> MAG ratios from various projects. You can set this as low as 1 if you want FTM to respond quickly to profitability changes of projects. If you don't have Gridcoin wallet installed/connected, this setting is always 30 and can't be changed. Default: 30
abort_unstarted_tasks=False # when we start controlling BOINC, should we abort unstarted tasks? Default is False, it's nicer to projects this way.
boinc_data_dir=None # Example: '/var/lib/boinc-client' or 'C:\\ProgramData\\BOINC\\'. Only needed if in a non-standard location, otherwise None.
GRIDCOIN_DATA_DIR=None # Example: '/home/user/.GridcoinResearch' or 'C:\\Users\\username\\AppData\\Roaming\\GridcoinResearch\\'. Only needed if in a non-standard location, otherwise None
recalculate_stats_interval=60 # Interval in minutes to re-calculate stats. Default: 60
price_check_interval=1440 # how often to check GRC price in minutes, minimum delay of 60 minutes between checks. Default is 1440 (24 hrs)
log_level='WARNING' # Options are: 'DEBUG','INFO','WARNING','ERROR','NONE', default is 'WARNING'
max_logfile_size_in_mb=10 # Default: 10
rolling_weight_window=60 # Use stats up to x days old for calculating intended weights vs actual crunch time, Default: 60. Note that "benchmarking" is applied to total time, not windowed time. Benchmarking will take 1% of ALL crunching time across ALL time history. This enables you set smaller "windows" and get faster reaction to weight changes without over-doing benchmarking.

# BENCHMARKING SETTINGS:
# Benchmarking is needed to determine profitability of a project. It is strongly suggested you keep these settings as they are, they are sane defaults.
# These defaults insure our mag/hr calculation is within 10% of what the actual answer is, and that accuracy improves over time
# Until a project is considered "benchmarked", it will be crunched regardless of all other settings (such as profitability) unless skip_benchmarking is set to True.
# Skipping benchmarking means we can't determine what are the most profit or mag-efficient projects. You have been warned!
# Benchmarking in total for all projects will take 1% of processing time. So for a whitelist with 10 projects on it, each project will get .01% of processing time.
# Initial benchmarking criteria: If /any/ of these following two benchmarking criteria are met, projects will considered "benchmarked" and things like profitability criteria can start to apply
benchmarking_minimum_wus=5 # minimum number of WUs to consider a project benchmarked
benchmarking_minimum_time=10 # minimum wall time in hours for WUs to be run on a project to consider it "benchmarked"
# Additional benchmarking criteria/options
benchmarking_delay_in_days=160 # if we have not had a WU from a project in this many days, request a batch. This helps prevent the script from getting in a loop where all projects are considered "unprofitable" but no new WUs are ever ordered so script never realizes project has since become profitable due to a change in the project's credit award system or WU application. Anytime BOINC is allowed to crunch, projects will still benchmark at 1% of crunching time total regardless of this setting.
skip_benchmarking=False # You can use this to skip all benchmarking. Useful if you've already benchmarked on another identical device and determined most profitable project(s)
# these are not fully implemented yet, but would theoretically allow you to control a non-local BOINC client. They may or may not work idk.
boinc_ip='127.0.0.1' # defaults to '127.0.0.1' with quotes
boinc_username=None # defaults to None without quotes
boinc_password=None # defaults to None, password to the BOINC rpc
boinc_port=31416


