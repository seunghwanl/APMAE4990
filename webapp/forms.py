from flask_wtf import Form
from wtforms.fields import DecimalField, SubmitField, SelectField
from wtforms.validators import Required, Length, NumberRange

class LatLongForm(Form):
    months_pairs = [('4', "April"), ('5', "May"), ('6', "June"), ('7', "July"), ('8', "August"), ('9', "September")]
    days_pairs = [('0', "Monday"), ('1', "Tuesday"), ('2', "Wednesday"), ('3', "Thursday"), ('4', "Friday"), ('5', "Saturday"), ('6', "Sunday")]
    hours_pairs = [('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), \
                   ('11', '11'), ('12', '12')]
    minutes_pairs = [('0', '00'), ('10', '10'), ('20', '20'), ('30', '30'), ('40', '40'), ('50', '50')]
    am_pm_pairs = [('0', 'AM'), ('1', 'PM')]
    
    month1 = SelectField('Month 1: ', choices = months_pairs)
    day1 = SelectField('Day 1: ', choices = days_pairs)
    hour1 = SelectField('Hour 1: ', choices = hours_pairs)
    minute1 = SelectField('Minute 1:', choices = minutes_pairs)
    am_pm1 = SelectField('AM / PM 1:', choices = am_pm_pairs)
    latitude1 = DecimalField('Latitude 1: ', validators=[NumberRange(min=40.6, max=40.87, message ='value greater than 40.6 and smaller than 40.87'), Required()])
    longitude1 = DecimalField('Longitude 1: ', validators=[NumberRange(min=-74.05, max=-73.9, message ='value greater than -74.05 and smaller than -73.9'), Required()])

    
    month2 = SelectField('Month 2: ', choices = months_pairs)
    day2 = SelectField('Day 2: ', choices = days_pairs)
    hour2 = SelectField('Hour 2: ', choices = hours_pairs)
    minute2 = SelectField('Minute 2:', choices = minutes_pairs)
    am_pm2 = SelectField('AM / PM 2:', choices = am_pm_pairs)
    latitude2 = DecimalField('Latitude 2: ', validators=[NumberRange(min=40.6, max=40.87, message ='value greater than 40.6 and smaller than 40.87'), Required()])
    longitude2 = DecimalField('Longitude 2: ', validators=[NumberRange(min=-74.05, max=-73.9, message ='value greater than -74.05 and smaller than -73.9'), Required()])
    
    submit = SubmitField('Enter!')

    
