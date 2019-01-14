# Pymodoro

A simple, configurable pomodoro timer. 

## Features
- Desktop notifications (Linux only, requires `notify-send`)
- Customizable work/break intervals
- Optional email notifications via SMTP 


## Usage
To use, run `$ main.py`  with the following command line arguments:


|Argument|Description|
|--|--|--|
|`--email-conf=`, `-e`|Sets location of email configuration file. If this option is used, SMTP mail notifications will be enabled. See `email.conf.sample`.|
|`--pattern=`, `-p`|Defines pattern of work/break periods. Defaults to alternating between four 25min work periods and four 5min break periods. Read the **Patterns** section for more detail.|
|`--no-notification`, `-n`|Disables desktop notifications|

### Patterns
Work/break patterns are defined by strings:

```
work-interval = "w", number
break-interval = "b", number
pattern = {work-interval|break-interval}
```

Examples:

Notice that contiguous periods of the same type are NOT combined.

|Pattern|Explanation
|--|--|
|`w25b5`|Work 25 minutes, break 5 minutes|
|`w25b5b30w10`|Work 25 minutes, break 5 minutes, break 30 minutes, work 10 minutes`|
|`w10w10b5b10`|Work 10 minutes, work 10 minutes, break 5 minutes, break 10 minutes|

## TODO
- Desktop notifications on Windows and MacOS
- Better syntax for defining work/break periods