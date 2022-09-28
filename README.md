# uc-monitoring-bot

## Timer configuring

 `[time range or certain time] [minutes between sending in time ranges] days weekdays`
 
 `Examples:`
 - `20:00 * 2 *` - send at 20:00 every 2 days
 - `19:20-20:00,22:10 3 * 2,3,4` - send every 3 minutes between 19:20-20:00 and at 22:10 each tue, wed, thu
 - `15:20,15:50 * * *` - send every day at 15:20 and 15:50
 - `22:00-4:00 30 * *` - send every half on an hour from 22:00 to 4 am of the next day
