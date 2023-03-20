# file-activity-checker
Tracks last modification time of a specified file. In case of inactivity for a certain time, the checker emits minutely sound signals according to the following schedule:

 | Time of inactivity |Signal |
 | :---               | :---  |
 |>=20 minutes        | Level 1 alert (1 short single beep)    |
 |>=40 minutes        | Level 2 alert (1 short and 1 long beeps) |  
 |>=70 minutes        | Level 3 alert (3 long beeps with further workstation lock) |

The indicated timeouts and beep patterns (and also the tracked filename) are hardcoded, but can be easily changed.  

It's also possible to temporarily disable the checker untill some future time by specifying it in "snooze.txt" file in ISO format (like "2020-12-21T0900").  


The checker was originally created as a reminder for Pomodoro's time management methodology. However, it can be used for other similar scenarios when it is necessary to track activity of a given file.  
