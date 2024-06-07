import datetime as dt
def generate_end_time(time):
    parsed_time = dt.datetime.strptime(time, "%H:%M").time()
    end_time = (dt.datetime.combine(dt.date.today(), parsed_time) + dt.timedelta(hours=1)).time()
    return end_time.strftime("%H:%M")

print(generate_end_time("15:00"))