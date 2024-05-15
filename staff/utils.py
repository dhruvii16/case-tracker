def generate_ics_file(date, time, title):
    # Generate the content of the .ics file
    cal_content = f'''BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//MyLawFirm//EN
BEGIN:VEVENT
SUMMARY:{title}
DTSTART;TZID=Asia/Kolkata:{date.strftime("%Y%m%dT%H%M%S")}
DTEND;TZID=Asia/Kolkata:{date.strftime("%Y%m%dT%H%M%S")}
END:VEVENT
END:VCALENDAR
'''
    return cal_content
