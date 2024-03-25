import math

def calculate_speed_reward(speed, steering_angle):
    """Calculate reward based on speed and steering."""
    if abs(steering_angle) < 20:
        return 2.0 if speed > 3 else 1.0 if speed > 2 else 0
    else:
        return 0.1 if speed > 2 else 1

def calculate_track_adherence_reward(all_wheels_on_track, is_offtrack):
    """Calculate penalty for going off-track."""
    reward = 0
    if not all_wheels_on_track:
        reward -= 0.5
    if is_offtrack:
        reward -= 1
    return reward

def calculate_directional_alignment_reward(track_direction, heading):
    """Calculate penalty based on the difference in direction."""
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff
    return -0.5 if direction_diff > 15 else 0

def calculate_progress_reward(progress, steps):
    """Calculate reward based on progress per step."""
    step_reward = (progress / steps) * 100
    step_multiplier = 1.0 + (progress / 100)
    return step_reward * step_multiplier

def get_track_direction(waypoints, closest_waypoints):
    """Calculate the direction of the track."""
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    return math.degrees(track_direction)

def reward_function(params):
    default_reward = 1e-3
    track_direction = get_track_direction(params["waypoints"], params["closest_waypoints"])
    
    speed_reward = calculate_speed_reward(params["speed"], params["steering_angle"])
    track_adherence_reward = calculate_track_adherence_reward(params["all_wheels_on_track"], params["is_offtrack"])
    directional_alignment_reward = calculate_directional_alignment_reward(track_direction, params["heading"])
    progress_reward = calculate_progress_reward(params["progress"], params["steps"])
    
    total_reward = default_reward + speed_reward + track_adherence_reward + directional_alignment_reward + progress_reward
    
    return float(total_reward)
