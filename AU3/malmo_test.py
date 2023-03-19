from math import radians, degrees
import matplotlib.pyplot as plt
import numpy as np

# Sun hours for each month in Visby, Sweden
sun_hours_visby = [41, 70, 156, 243, 317, 315, 314, 261, 188, 102, 42, 31]

# Calculate the average sun hours for each day in the month
sun_hours_visby = sun_hours_visby * np.array(
    [1 / 31, 1 / 28, 1 / 31, 1 / 30, 1 / 31, 1 / 30, 1 / 31, 1 / 31, 1 / 30, 1 / 31, 1 / 30, 1 / 31]
)

days_months = [
    31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31
]

sum = 0

for day in days_months:
    sum += day

print(sum)


# ---- Solar panel parameters ---------------------------------

I_0 = 1360.0                    # Solar constant

panel_lat   = radians(57.6)     # Latitude of the solar panel
panel_alt   = radians(44.4)     # Altitude of the solar panel
panel_az    = radians(210.0)    # Azimuth of the solar panel

panel_eff   = 0.15              # Efficiency of the solar panel
panel_area  = 50                # Area of the solar panel

day         = 121               # Day of the year
time        = 14.5              # Time of day in hours

# -------------------------------------------------------------

def calculate_power(day = day, time = time, panel_alt = panel_alt, panel_az = panel_az, follow_sun = False, sun_hour = True):

    '''
    
        Calculates the power of a solar panel at a given time of day and day of the year.
        The solar panel can either follow the sun or be fixed to a given altitude and azimuth.

        1. Calculate the declination angle of the sun   (Eq. 2)
        2. Calculate the hour angle of the sun          (Eq. 3)
        3. Calculate the solar elevation angle          (Eq. 1)
        4. Calculate the solar azimuth angle            (Eq. 4)

        5. Calculate the solar irradiance on a horizontal surface (Eq. 5)
        6. Calculate the solar irradiance on a panel surface      (Eq. 6)
        7. Calculate the delivered power of the solar panel       (Eq. 7)

        If the power returned is negative, it is set to 0.
    
    '''

    declination     = -1 * radians(23.44) * np.cos(radians(360.0/365.0 * day))
    hour_angle      = radians(15.0) * time - radians(180.0)

    hour_angle = hour_angle if hour_angle != 0 else 0.05

    solar_elevation = np.arcsin(np.sin(declination) * np.sin(panel_lat) + np.cos(declination) * np.cos(panel_lat) * np.cos(hour_angle))
    solar_azimuth   = radians(180.0) + (-1 if hour_angle > 0 else 1) * np.arccos(
        (np.sin(panel_lat) * np.sin(solar_elevation) - np.sin(declination)) / (np.cos(panel_lat) * np.cos(solar_elevation))
    )

    if hour_angle > 0:

        solar_azimuth   = radians(180.0) - 1 * np.arccos(
            (np.sin(panel_lat) * np.sin(solar_elevation) - np.sin(declination)) / (np.cos(panel_lat) * np.cos(solar_elevation))
        )

    else: 

        solar_azimuth   = radians(180.0) +  1 * np.arccos(
            (np.sin(panel_lat) * np.sin(solar_elevation) - np.sin(declination)) / (np.cos(panel_lat) * np.cos(solar_elevation))
        )

    panel_az    = solar_azimuth     if follow_sun else panel_az
    panel_alt   = solar_elevation   if follow_sun else panel_alt

    # Here, we will check if it a sun hour or not and adjust the power accordingly, if it is not a sun hour, we will set the power to 120 W
    # or less.

    I_h = 1.1 * I_0 * 0.7 ** (1.0 / np.sin(solar_elevation)) ** 0.678
    I_h = I_h if sun_hour else np.random.randint(0, 120)
    I_p = I_h * (np.cos(panel_alt - solar_elevation) * np.cos(panel_az - solar_azimuth) + (1 - np.cos(panel_az - solar_azimuth)) * np.sin(panel_alt) * np.sin(solar_elevation))
    P   = I_p * panel_eff * panel_area

    if type(P) == np.ndarray:
        P[P < 0] = 0
        P[np.isnan(P)] = 0
        return P
    else:

        if np.isnan(P):
            P = 0

        return max(P, 0)

def calculate_power_over_day(sun_hours, day = day, panel_alt = panel_alt, panel_az = panel_az, follow_sun = False):

    '''

        Calculates the power over a day for a given solar panel. This function also adjusts the outputted power
        depending on the given available sun hours for the given day.

        1. Create a random array of True and False values, where True represents a sun hour and False represents a non-sun hour.
        2. Shuffle the array to create a random distribution of sun hours.
        3. Calculate the power for each hour of the day.

    '''

    # First we calculate over day disregarding sun hours
    y = [calculate_power(time=hour, day=day, follow_sun=follow_sun, panel_alt=panel_alt) for hour in range(24)]

    # Now we get the available total sun hours for that day by checking when the first and last sun hour is
    y1, y2 = 0, 0
    y1_indexed = False

    for hour, power in enumerate(y):
        if power > 120 and not y1_indexed:
            y1 = hour
            y1_indexed = True
        if (power < 120 or np.isnan(power)) and y1_indexed:
            y2 = hour
            break

    sun_hours = np.array([True] * int(sun_hours) + [False] * ((y2 - y1) - int(sun_hours)))
    np.random.shuffle(sun_hours)

    # Now we start at y1 and add the sun hours to the array
    for is_hour, hour in zip(sun_hours, range(y1, y2 + 1)):
        y[hour] = calculate_power(time=hour, day=day, follow_sun=follow_sun, sun_hour=is_hour, panel_alt=panel_alt)

    return y

# -----------------------------------------------

# plt.figure(figsize=[9, 5])

# day = 0
# desired_month = 5
# for month in days_months[0:desired_month]:
#     day += month

# total_energy_delivered = []

# for day in range(day, day + days_months[5]):

#     y = calculate_power_over_day(sun_hours=24, day=day, follow_sun=False)
#     total_energy_delivered.append((np.sum(y) * 24) / 1000)

# total_energy = np.sum(total_energy_delivered)

# print(total_energy)

# -----------------------------------------------

def calculate_jan_month():

    day = 0
    desired_month = 0
    for month in days_months[0:desired_month]:
        day += month

    total_energy_delivered = []

    for day in range(day, day + days_months[0]):

        y = calculate_power_over_day(sun_hours=sun_hours_visby[0], day=day, follow_sun=False)
        # y = calculate_power_over_day(sun_hours=24, day=day, follow_sun=False)

        total_energy_delivered.append((np.sum(y)) / 1000)

    total_energy = np.sum(total_energy_delivered)

    print("Total energy delivered: {} kWh".format(total_energy))

    plt.figure(figsize=[9, 5])  
    plt.stem(total_energy_delivered, label='Fixed panel')
    plt.legend(fontsize=15)
    plt.xlabel('Day',fontsize=15)
    plt.ylabel('Energy (kWh)',fontsize=15)
    plt.xticks(range(0, days_months[0]), fontsize=10)
    plt.yticks(fontsize=12)
    plt.title('Energy delivered in January')
    plt.grid()
    plt.show()

def calculate_june_month():

    day = 0
    desired_month = 5
    for month in days_months[0:desired_month]:
        day += month

    total_energy_delivered = []

    for day in range(day, day + days_months[desired_month]):

        y = calculate_power_over_day(sun_hours=sun_hours_visby[desired_month], day=day, follow_sun=False)
        # y = calculate_power_over_day(sun_hours=24, day=day, follow_sun=False)

        total_energy_delivered.append((np.sum(y)) / 1000)

    total_energy = np.sum(total_energy_delivered)

    print("Total energy delivered: {} kWh".format(total_energy))

    plt.figure(figsize=[9, 5])  
    plt.stem(total_energy_delivered, label='Fixed panel')
    plt.legend(fontsize=15)
    plt.xlabel('Day',fontsize=15)
    plt.ylabel('Energy (kWh)',fontsize=15)
    plt.xticks(range(0, days_months[0]), fontsize=10)
    plt.yticks(fontsize=12)
    plt.title('Energy delivered in June')
    plt.grid()
    plt.show()


def calculate_june_day():

    day = 0
    desired_month = 5
    for month in days_months[0:desired_month]:
        day += month

    y = calculate_power_over_day(sun_hours=24, day=day, follow_sun=False)
    y2 = calculate_power_over_day(sun_hours=24, day=day, follow_sun=True)

    total_energy_delivered = (np.sum(y) * 24) / 1000
    print("Total energy delivered: {} kWh".format(total_energy_delivered))

    plt.figure(figsize=[9, 5])
    plt.plot(y, label='Fixed panel')
    plt.plot(y2, label='Maximum power', linestyle='--')
    plt.legend(fontsize=15)
    plt.xlabel('Time (t)',fontsize=15)
    plt.ylabel('Power (W)',fontsize=15)
    plt.title('Power over a day',fontsize=15)
    plt.xticks(range(0, 25), fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid()
    plt.show()

def calculate_january_day():

    y = calculate_power_over_day(sun_hours=24, day=10, follow_sun=False)
    y2 = calculate_power_over_day(sun_hours=24, day=10, follow_sun=True)

    total_energy_delivered = (np.sum(y) * 24) / 1000
    print("Total energy delivered: {} kWh".format(total_energy_delivered))

    plt.figure(figsize=[9, 5])
    plt.plot(y, label='Fixed panel')
    plt.plot(y2, label='Maximum power', linestyle='--')
    plt.legend(fontsize=15)
    plt.xlabel('Time (t)',fontsize=15)
    plt.ylabel('Power (W)',fontsize=15)
    plt.title('Power over a day',fontsize=15)
    plt.xticks(range(0, 25), fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid()
    plt.show()

def calculate_year(altitude=panel_alt):

    total_energy_delivered = []
    total_energy_delivered_2 = []

    month = 0
    day_of_month = 0

    for day in range(0, 365):

        y = calculate_power_over_day(sun_hours=sun_hours_visby[month], day=day, follow_sun=True)
        y_2 = calculate_power_over_day(sun_hours=24, day=day, follow_sun=True)

        total_energy_delivered.append((np.sum(y)) / 1000)
        total_energy_delivered_2.append((np.sum(y_2)) / 1000)

        day_of_month += 1

        if day_of_month == days_months[month]:
            month += 1
            day_of_month = 0


    total_energy = np.sum(total_energy_delivered)

    # return total_energy

    print("Total energy delivered: {} kWh".format(total_energy))

    plt.figure(figsize=[9, 5])  
    plt.plot(total_energy_delivered, label='Follow sun')
    plt.plot(total_energy_delivered_2, label='No clouds', linestyle='--')
    plt.legend(fontsize=15)
    plt.xlabel('Day',fontsize=15)
    plt.ylabel('Energy (kWh)',fontsize=15)
    plt.xticks(range(0, 365, 30), fontsize=10)
    plt.yticks(fontsize=12)
    plt.title('Energy delivered in a year')
    plt.grid()
    plt.show()

def calculate_best_altitude():

    altitudes = np.arange(1, 90, 1)

    total_energy_delivered = []

    for altitude in altitudes:

        total_energy_delivered.append(calculate_year(altitude=radians(altitude)))

    best_altitude = np.argmax(total_energy_delivered)
    print("Best altitude: {} degrees".format((altitudes[best_altitude])))

    plt.figure(figsize=[9, 5])  
    plt.stem(altitudes, total_energy_delivered, label='Fixed panel')
    plt.legend(fontsize=15)
    plt.xlabel('Altitude',fontsize=15)
    plt.ylabel('Energy (kWh)',fontsize=15)
    plt.xticks(range(0, 90, 10), fontsize=10)
    plt.yticks(fontsize=12)
    plt.title('Energy delivered for different altitudes')
    plt.grid()
    plt.show()

def calculate_with_average():

    target_month    = 5
    follow_sun      = False
    sun_hours       = False

    start_day = 0
    for month in days_months[0:target_month]:
        start_day += month

    end_day = start_day + days_months[target_month]

    power_hours = [

        calculate_power_over_day(
            
            sun_hours=sun_hours_visby[target_month] if sun_hours else 24, day=day, follow_sun=follow_sun

        ) for day in range(start_day, end_day)
    ]

    print(np.sum(power_hours / 1000))

    # y = 
    
    # for day in range(start_day, end_day):

    #     y = calculate_power_over_day(sun_hours=sun_hours_visby[target_month], day=day, follow_sun=True)

    #     if day == start_day:
    #         total_energy_delivered = y
    #     else:
    #         total_energy_delivered += y

    # print(start_day)

# Uppgift 2 ---------------

# calculate_january_day()
# calculate_june_day()
# calculate_jan_month()
# calculate_june_month()
# calculate_year()

# Uppgift 3 ---------------

# calculate_best_altitude()

# Uppgift 4 ---------------

calculate_with_average()