import math


def deg_to_rad(degree):
    # Convert degree to radian
    rad = degree * math.pi / 180

    return rad


def rad_to_deg(radian):
    # Convert radian to degree
    deg = radian * 180 / math.pi

    return deg


def deg_calculator(sin_deg, cos_deg):
    # Four different cases in total
    # cos > 0; sin > 0 --> 1
    if cos_deg > 0 and sin_deg > 0:
        degree = rad_to_deg(math.acos(cos_deg))
    # cos > 0; sin < 0 --> 4
    elif cos_deg > 0 and sin_deg < 0:
        degree = 360 - rad_to_deg(math.acos(cos_deg))
    # cos < 0: sin < 0 --> 3
    elif cos_deg < 0 and sin_deg < 0:
        degree = 360 - rad_to_deg(math.acos(cos_deg))
    # cos < 0; sin > 0 --> 2
    else:
        degree = rad_to_deg(math.acos(cos_deg))

    return degree


def cal_delta2(lambda1, delta1):
    # Unit conversion
    lam_rad = deg_to_rad(lambda1)
    del_rad = deg_to_rad(delta1)

    # formula: cos(delta2) = sin(lambda1) * sin(delta1)
    del2_rad = math.acos(math.sin(lam_rad) * math.sin(del_rad))
    delta2 = rad_to_deg(del2_rad)

    print(f"Delta2 = {delta2:.2f}")

    return delta2


def cal_lambda2(lambda1, delta1, delta2):
    # Unit conversion
    lam1_rad = deg_to_rad(lambda1)
    del1_rad = deg_to_rad(delta1)
    del2_rad = deg_to_rad(delta2)

    if math.sin(delta2) == 0:
        print("Error: Delta2 cannot be 0")
        return False

    # Step 1: Calculate sin(lambda2)
    # formula: cos(delta1) = sin(lambda2) * sin(delta2)
    sin_lam2 = math.cos(del1_rad) / math.sin(del2_rad)
    print(f"sin(lambda2) = {sin_lam2:.3f}")

    # Step 2: Calculate cos(lambda2)
    # formula1: cos(lambda1) = sin(delta2) * sin(phi1 - phi2)
    # formula2: cos(lambda2) = sin(delta1) * sin(phi2 - phi1)
    sin_phi1_min_phi2 = math.cos(lam1_rad) / math.sin(del2_rad)  # sin(phi1 - phi2)
    cos_lam2 = math.sin(del1_rad) * (- sin_phi1_min_phi2)
    print(f"cos(lambda2) = {cos_lam2:.3f}")

    # Step 3: Calculate lambda2
    lambda2 = deg_calculator(sin_lam2, cos_lam2)
    print(f"Lambda2 = {lambda2:.2f}")

    return lambda2


def cal_phi2(lambda1, delta1, delta2, phi1):
    # Unit conversion
    lam1_rad = deg_to_rad(lambda1)
    del1_rad = deg_to_rad(delta1)
    del2_rad = deg_to_rad(delta2)

    if math.sin(del2_rad) == 0 or math.tan(del1_rad) == 0 or math.tan(del2_rad) == 0:
        print("Error: Division by zero")
        return False

    # Step 1: Calculate sin(phi1 - phi2)
    # formula: cos(lambda1) = sin(delta2) * sin(phi1 - phi2)
    sin_phi1_min_phi2 = math.cos(lam1_rad) / math.sin(del2_rad)
    print(f"sin(phi1 - phi2) = {sin_phi1_min_phi2:.3f}")

    # Step 2: Calculate cos(phi1 - phi2)
    # formula: tan(delta1) * tan(delta2) * cos(phi1 - phi2) = -1
    cos_phi1_min_phi2 = - 1 / math.tan(del1_rad) / math.tan(del2_rad)
    print(f"cos(phi1 - phi2) = {cos_phi1_min_phi2:.3f}")

    # Step 3: Calculate (phi1 - phi2)
    phi1_min_phi2 = deg_calculator(sin_phi1_min_phi2, cos_phi1_min_phi2)

    # Step 4: Calculate phi2
    phi2 = abs(phi1 - phi1_min_phi2)
    print(f"Phi2 = {phi2:.2f}")

    return phi2


def cal_nodal(phi1, delta1, lambda1):
    # Calculate the second nodal plane
    # Given the fault parameter of the first plane
    # phi1, delta1, lambda1

    delta2 = cal_delta2(lambda1, delta1)
    lambda2 = cal_lambda2(lambda1, delta1, delta2)
    phi2 = cal_phi2(lambda1, delta1, delta2, phi1)

    if delta2 > 90:
        # Convert the parameters
        phi2 = 180 + phi2
        delta2 = 180 - delta2
        lambda2 = 360 - lambda2
        print(f"Delta2 > 90, so phi2 = {phi2:.2f} delta2 = {delta2:.2f} lambda2 = {lambda2:.2f}")

    return


cal_nodal(228, 66, 4)

