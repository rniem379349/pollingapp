from django.utils import timezone

class WhenWasObjectCreatedMixin(object):
    def when_was_created(self, pub_date):
        """
        Return a string saying when an object (with the creation date of pub_date) was published, from minutes up to years.
        """
        # print("pub date: ", pub_date)
        now = timezone.now()
        # print("now is: ", now)
        difference = now - pub_date
        # print(difference)

        unit_of_time_str = ""
        unit_of_time_num = 0

        if (difference.days > 0):
            if (difference.days == 1):
                unit_of_time_str = "day"
                unit_of_time_num = 1
            elif (1 < difference.days < 7):
                unit_of_time_str = "days"
                unit_of_time_num = difference.days
            elif (7 <= difference.days < 14):
                unit_of_time_str = "week"
                unit_of_time_num = difference.days // 7
            elif (14 <= difference.days < 30):
                unit_of_time_str = "weeks"
                unit_of_time_num = difference.days // 7
            elif (30 <= difference.days < 60):
                unit_of_time_str = "month"
                unit_of_time_num = difference.days // 30
            elif (60 <= difference.days < 365):
                unit_of_time_str = "months"
                unit_of_time_num = difference.days // 30
            elif (365 <= difference.days < 730):
                unit_of_time_str = "year"
                unit_of_time_num = difference.days // 365
            else:
                unit_of_time_str = "years"
                unit_of_time_num = difference.days // 365
        elif (difference.days == 0):
            if (difference.seconds < 300):
                return "just now"
            elif (300 <= difference.seconds < 3600):
                unit_of_time_str = "minutes"
                unit_of_time_num = difference.seconds // 60
            elif (3600 <= difference.seconds < 7200):
                unit_of_time_str = "hour"
                unit_of_time_num = difference.seconds // 3600
            elif (7200 <= difference.seconds < 86400):
                unit_of_time_str = "hours"
                unit_of_time_num = difference.seconds // 3600
            
        return "%i %s" % (unit_of_time_num, unit_of_time_str)