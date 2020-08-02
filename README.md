# file-activity-checker
Tracks last modification time of a specified file. In case of inactivity for a certain time, the checker emits minutely sound signals according to the following schedule:

 | Time of inactivity |Signal |
 | :---               | :---  |
 |>=20 minutes        | Level 1 alert (short single beep)    |
 |>=40 minutes        | Level 2 alert (short and long beeps) |  
 |>=70 minutes        | Level 3 alert (three long beeps)     |

The indicated timeouts and beep patterns are hardcoded but can be easily changed.  

The checker was originally created as a reminder for Pomodoro's time management methodology. However, it can be used for other similar scenarios when it is necessary to track activity of a given file.  
