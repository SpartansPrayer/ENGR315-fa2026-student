import math

import numpy as np


def parse_tensile_file(path_to_file):
    file = open(path_to_file)
    # required meta-data
    gage_diameter = -1
    maximum_force = - 1
    maximum_strain = -1
    # determine when to begin reading into these files
    begin_reading = False
    time = []
    displacement = []
    force = []
    strain = []
    # begin iterating through file
    for line in file:
        if line == '' or line == '\n':
            continue

        splits = line.strip().split(",")

        if begin_reading == False:

            # gather various meta data
            if splits[0] == "Gage Diameter":
                cleaned = splits[2].replace('\"', '')
                gage_diameter = float(cleaned)
            if splits[0] == "Maximum Force":
                cleaned = splits[2].replace('\"', '')
                maximum_force = float(cleaned)
            if splits[0] == "Maximum Strain":
                cleaned = splits[2].replace('\"', '')
                maximum_strain = float(cleaned)

        else:
            # parse the actual data
            time.append(float(splits[0].replace('\"', '')))
            displacement.append(float(splits[1].replace('\"', '')))
            force.append(float(splits[2].replace('\"', '')))
            strain.append(float(splits[3].replace('\"', '')))

        # try to find start of data
        if splits[0] == "(s)":
            begin_reading = True
    file.close()

    return gage_diameter, np.asarray(time), np.asarray(displacement), np.asarray(force), np.asarray(strain)


# ---------------------------------------------------------------------------------------------
# The four functions below are the ones you wrote in the Tensile Testing assignment (3.4.2).
# Copy your completed versions from your tensile-strength-step4.py file into this file,
# replacing each placeholder function with your own. Do not change the function names.
#
# The Gradescope autograder for THIS assignment uses its own correct copy of these functions,
# so it only grades your generate_csv_file() function. You only need these to run locally.
# ---------------------------------------------------------------------------------------------


def calculate_stress(force, sample_diameter):
    """
    Calculate the stress (MPa) experienced by the test given a series of forces/loads (kN) and
    a sample diameter (mm)
    :param force: An array of forces/loads applied to the sample in Kilo Newtons (kN)
    :param sample_diameter: The diameter of the sample in millimeters (mm)
    :return: An array of stresses experienced by the sample in MegaPascals (MPa)
    """

    # copy your calculate_stress() from Tensile Testing here
    area = math.pi * (sample_diameter / 2)**2
   
    stress = (force * 1000) / area
    
    return stress


def calculate_max_strength_strain(strain, stress):
    """
    Calculate the Ultimate Tensile Stress and Fracture Strain
    :param strain: An array of Strain data
    :param stress: An array of Stress data (MPa)
    :return:
    Ultimate Tensile Stress: the maximum stress experienced
    Fracture Strain: the maximum strain experienced before fracture
    """

    # calculate the maximum stress experienced
    ultimate_tensile_stress = np.max(stress)
        
            # calculate the maximum strain experienced
    fracture_strain = np.max(strain)
        
    return ultimate_tensile_stress, fracture_strain


def calculate_elastic_modulus(strain, stress):
    """
    Given a set of stress strain data, use the Secant Modulus at 40% method to determine
    the elastic modulus
    :param strain: An array of Strain data
    :param stress: An array of Stress data (MPa)
    :return:
    linear_index: the index within the strain/stress data that is the end of the linear region
    slope: the slope for the linear region of the strain/stress data
    intercept: y-intercept for linear region best fit of strain/stress data
    """

    # copy your calculate_elastic_modulus() from Tensile Testing here
# dummy variables the function should over write
    linear_index = None
    slope = None
    intercept = None

    ### YOUR SOLUTION FROM STEP 3 TEMPLATE HERE ###
    peak_stress = np.max(stress) * 0.40


    diffs = np.abs(stress - peak_stress)
    
    linear_index = np.argmin(diffs)

    linear_stress = stress[0:linear_index]
    linear_strain = strain[0:linear_index]

    slope, intercept = np.polyfit(linear_strain, linear_stress, 1)
    return linear_index, slope, intercept


def calculate_percent_offset(slope, strain, stress):
    """
    Use the 0.2% offset method to find where the offset line crosses the stress/strain curve
    :param slope: The elastic modulus (slope of the linear region)
    :param strain: An array of Strain data
    :param stress: An array of Stress data (MPa)
    :return:
    offset_line: the 0.2% offset line
    intercept_index: the index where the offset line crosses the stress/strain curve
    """

   # set the desired offset for the line
    offset = 0.002
   
       # calculate the offset line: y=m(x-0.002) + 0
    offset_line = slope * (strain - offset)
   
       # measure distance from all points on graph to this line. Consider using the
       # abs() method to ensure values are positive
    distance = np.abs(stress - offset_line)
    indices = np.where(strain >= offset)[0]
    if len(indices) == 0:
           return None, -1
       # use argmin to find the index where the distance is minimal
    intercept_index = indices[np.argmin(distance[indices])]
   
    return offset_line, intercept_index


def calculate_yield_strength(strain, stress, modulus):
    """
    Determine the yield strength (MPa) via the 0.2% offset method.
    This one is provided for you. It uses your calculate_percent_offset() above.
    """
    offset_line, intercept_index = calculate_percent_offset(modulus, strain, stress)

    if intercept_index == -1:
        return -1

    return stress[intercept_index]


class MaterialSample:
    """
    A simple class to hold results from materials tensile analysis
    """

    def __init__(self):
        self.name = ""
        self.material_type = ""
        self.tensile_strength = -1
        self.fracture_strain = -1
        self.elastic_modulus = -1
        self.yield_strength = -1
