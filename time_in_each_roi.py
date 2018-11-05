import numpy as np


"""
    Functions to extract time spent by the mouse in each of a list of user defined ROIS 

    Example usage:
    rois        -->  a dictionary with name and position of each roi
    tracking    -->  a pandas dataframe with X,Y,Velocity for each bodypart
    bodyparts   -->  a list with the name of all the bodyparts
    
    -----------------------------------------------------------------------------------
    
    from collections import namedtuple
    
    data = namedtuple('tracking data', 'x y velocity')
    results = {}
    for bp in bodyparts:
        bp_tracking = data(tracking.bp.x.values, tracking.bp.y.values, tracking.bp.Velocity.values)
        res = get_timeinrois_stats(bp_tracking, roi, fps=30)
        results[bp] = res
    
"""


def get_roi_at_each_frame(bp_data, rois):
    """
    Given position data for a bodypart and the position of a list of rois, this function calculates which roi is
    the closest to the bodypart at each frame

    :param bp_data: numpy array: [nframes, 2] -> X,Y position of bodypart at each frame
                    [as extracted by DeepLabCut] --> df.bodypart.values
    :param rois: dictionary with the position of each roi. The position is stored in a named tuple with the location of
                    two points defyining the roi: topleft(X,Y) and bottomright(X,Y).
    :return: tuple, closest roi to the bodypart at each frame
    """

    if not isinstance(rois, dict): raise ValueError('rois locations should be passed as a dictionary')

    if not isinstance(bp_data, np.ndarray):
        if not isinstance(bp_data, tuple): raise ValueError('Unrecognised data format for bp tracking data')
        else:
            pos = np.zeros((len(bp_data.x), 2))
            pos[:, 0], pos[:, 1] = bp_data.x, bp_data.y
            bp_data = pos

    # Get the center of each roi
    centers = []
    for points in rois.values():
        center_x = (points.topleft[0] + points.bottomright[0]) / 2
        center_y = (points.topleft[1] + points.bottomright[1]) / 2
        center = np.asarray([center_x, center_y])
        centers.append(center)

    roi_names = list(rois.keys())

    # Calc distance toe ach roi for each frame
    data_length = len(bp_data[0])
    distances = np.zeros((data_length, len(centers)))
    for idx, center in enumerate(centers):
        cnt = np.tile(center, data_length).reshape((data_length, 2))
        dist = np.hypot(np.subtract(cnt[:, 0], bp_data[:, 0]), np.subtract(cnt[:, 1], bp_data[:, 1]))
        distances[:, idx] = dist

    # Get which roi the mouse is in at each frame
    sel_rois = np.argmin(distances, 1)
    roi_at_each_frame = tuple([roi_names[x] for x in sel_rois])
    return roi_at_each_frame


def get_timeinrois_stats(data, rois, fps=None):
    """
    Quantify number of times the animal enters a roi, comulative number of frames spend there, comulative time in seconds
    spent in the roi and average velocity while in the roi.

    In which roi the mouse is at a given frame is determined with --> get_roi_at_each_frame()


    Quantify the ammount of time in each  roi and the avg stay in each roi
    :param data: tracking data passed as a namedtuple (x,y,velocity)
    :param rois: dictionary with the position of each roi. The position is stored in a named tuple with the location of
                two points defyining the roi: topleft(X,Y) and bottomright(X,Y).
    :param fps: framerate at which video was acquired
    :return: dictionary
    """

    def get_indexes(lst, match):
        return np.asarray([i for i, x in enumerate(lst) if x == match])

    # get roi at each frame of data
    data_rois = get_roi_at_each_frame(data, rois)
    data_time_inrois = {name: data_rois.count(name) for name in set(data_rois)}  # total time (frames) in each roi

    # number of enters in each roi
    transitions = [n for i, n in enumerate(list(data_rois)) if i == 0 or n != list(data_rois)[i - 1]]
    transitions_count = {name: transitions.count(name) for name in transitions}

    # avg time spend in each roi (frames)
    avg_time_in_roi = {transits[0]: time / transits[1]
                       for transits, time in zip(transitions_count.items(), data_time_inrois.values())}

    # avg time spend in each roi (seconds)
    if fps is not None:
        data_time_inrois_sec = {name: t / fps for name, t in data_time_inrois.items()}
        avg_time_in_roi_sec = {name: t / fps for name, t in avg_time_in_roi.items()}
    else:
        data_time_inrois_sec, avg_time_in_roi_sec = None, None

    # get avg velocity in each roi
    avg_vel_per_roi = {}
    for name in set(data_rois):
        indexes = get_indexes(data_rois, name)
        vels = [data.velocity[x] for x in indexes]
        avg_vel_per_roi[name] = np.average(np.asarray(vels))

    results = dict(transitions_per_roi=transitions_count,
                   comulative_time_in_roi=data_time_inrois,
                   comulative_time_in_roi_sec=data_time_inrois_sec,
                   avg_time_in_roi=avg_time_in_roi,
                   avg_time_in_roi_sec=avg_time_in_roi_sec,
                   avg_vel_in_roi=avg_vel_per_roi)

    return results










