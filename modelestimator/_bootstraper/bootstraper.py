import copy
import random
import numpy as np
import math
from modelestimator._bw_estimator.bw_estimator import bw_estimator

def _resample_columns(sequence_list):
    return_list = [""] * len(sequence_list)
    SEQUENCE_LENGTH = len(sequence_list[0])

    for _ in range(SEQUENCE_LENGTH):
        RANDOM_INDEX = random.randint(0, SEQUENCE_LENGTH - 1)

        for SEQUENCE_INDEX, SEQUENCE in enumerate(sequence_list):
            SEQUENCE_ELEMENT = SEQUENCE[RANDOM_INDEX]
            return_list[SEQUENCE_INDEX] = return_list[SEQUENCE_INDEX] + SEQUENCE_ELEMENT

    return return_list

def _calculate_bw_for_resamplings(FORMAT, RESAMPLINGS, THRESHOLD, MULTIALIGNMENT):
    q_list = []
    eq_list = []
    number_of_times_bw_estimator_failed = 0

    for _ in range(RESAMPLINGS):
        MULTIALIGNMENT = copy.deepcopy(MULTIALIGNMENT)
        MULTIALIGNMENT = _resample_columns(MULTIALIGNMENT)
        MULTIALIGNMENT_LIST = [MULTIALIGNMENT]

        try:
            Q, EQ = bw_estimator(FORMAT, THRESHOLD, MULTIALIGNMENT_LIST)
            q_list.append(Q)
            eq_list.append(EQ)
        except:
            number_of_times_bw_estimator_failed +=1

    FAILED_PERCENTAGE = number_of_times_bw_estimator_failed / RESAMPLINGS
    return q_list, FAILED_PERCENTAGE

def q_diff_mean(REFERENCE_Q, RESAMPLED_Q_LIST):
    Q_DIFF_NORM_LIST = []

    for Q in RESAMPLED_Q_LIST:
        Q_DIFF = REFERENCE_Q - Q
        Q_DIFF_NORM = np.linalg.norm(Q_DIFF)
        Q_DIFF_NORM_LIST.append(Q_DIFF_NORM)

    Q_DIFF_MEAN = np.mean(Q_DIFF_NORM_LIST)

    return Q_DIFF_MEAN

#   Interface
def bootstraper(FORMAT, RESAMPLINGS, THRESHOLD, MULTIALIGNMENT):
    MULTIALIGNMENT_LIST = [MULTIALIGNMENT]
    REFERENCE_Q,_ = bw_estimator(FORMAT, THRESHOLD, MULTIALIGNMENT_LIST)

    RESAMPLED_Q_LIST, FAILED_PERCENTAGE = _calculate_bw_for_resamplings(FORMAT, RESAMPLINGS, THRESHOLD, MULTIALIGNMENT)
    Q_DIFF_MEAN = q_diff_mean(REFERENCE_Q, RESAMPLED_Q_LIST)
    Q_DIFF_MEAN *= 10000

    return Q_DIFF_MEAN, FAILED_PERCENTAGE