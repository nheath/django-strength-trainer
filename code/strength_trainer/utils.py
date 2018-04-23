from .models import NewWorkout, User_Profile_Model, WorkoutWeek
import math

def create_workout_week(request, init_multiplier, workout_name):
    pretty_name = workout_name[-1:]
    if pretty_name == "1":
        weeks_reps = "5/5/5+"
    if pretty_name == "2":
        weeks_reps = "3/3/3+"
    if pretty_name == "3":
        weeks_reps = "5/3/1+"
    if pretty_name == "4":
        weeks_reps = "5/5/5"
    pretty_name = 'Week ' + pretty_name
    cur_user = request.user
    cur_user_workout = NewWorkout.objects.get(user_id=cur_user.id)
    multiplier = init_multiplier
    bench_reps = list()
    squat_reps = list()
    deadlift_reps = list()
    overhead_reps = list()
    for i in range(3):
        temp_b_rep = math.floor((cur_user_workout.max_bench * .90) * multiplier)
        bench_reps.append(str(temp_b_rep))
        temp_s_rep = math.floor((cur_user_workout.max_squat * .90) * multiplier)
        squat_reps.append(str(temp_s_rep))
        temp_d_rep = math.floor((cur_user_workout.max_deadlift * .90) * multiplier)
        deadlift_reps.append(str(temp_d_rep))
        temp_o_rep = math.floor((cur_user_workout.max_overhead * .90) * multiplier)
        overhead_reps.append(str(temp_o_rep))                   
        multiplier += .1

    new_workout_week = WorkoutWeek(
        name = workout_name,
        prettyName = pretty_name,
        reps = weeks_reps,
        bench = ','.join(bench_reps),
        squat = ','.join(squat_reps),
        deadlift = ','.join(deadlift_reps),
        overhead = ','.join(overhead_reps),
        associated_workout = cur_user_workout
    )
    new_workout_week.save()