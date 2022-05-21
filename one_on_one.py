import ourcopy
import util
from random_improver import try_find_and_apply_swap, update_best


def one_on_one(participants):
    if len(participants) % 2 == 1:
        participants += ["KeinPartner"]
    round_template = "|".join(["__" for _ in range(len(participants)//2 + 1)])[:-3+(len(participants) % 2) * 2]
    rounds_template = [round_template for _ in range(len(participants) + len(participants) % 2 - 1)]
    rounds = [util.round_parse(round_template, participants) for round_template in rounds_template]
    meeting_matrix, rounds = util.random_solution(participants, rounds)
    optimal_meeting_count = 1
    best_score = current_score = util.score_1on1(meeting_matrix, optimal_meeting_count)
    best_solution = ourcopy.deepcopy(rounds)
    repeated_score_number = 0
    while best_score != 0:
        max_meet_count = max(max(i) for i in meeting_matrix)
        improvable_round = False
        for first_participant_index in range(len(participants)):
            first_participant_meeting_counts = meeting_matrix[first_participant_index]
            if max_meet_count not in first_participant_meeting_counts:
                continue
            max_meet_participant_index = max(enumerate(first_participant_meeting_counts), key=lambda x: x[1])[0]
            first_participant_meeting_counts[first_participant_index] = max_meet_count + 1
            min_meet_participant_index = min(enumerate(first_participant_meeting_counts), key=lambda x: x[1])[0]
            first_participant_meeting_counts[first_participant_index] = 0
            if first_participant_meeting_counts[max_meet_participant_index] - first_participant_meeting_counts[
                min_meet_participant_index] >= 2:
                for round_index in range(len(rounds)):
                    plan = ourcopy.deepcopy(rounds[round_index]["plan"])
                    improve = try_find_and_apply_swap(participants[first_participant_index],
                                                      participants[max_meet_participant_index],
                                                      participants[min_meet_participant_index], plan)

                    if improve:
                        old_plan = rounds[round_index]["plan"]
                        rounds[round_index]["plan"] = plan
                        new_meeting_matrix = util.calculate_meeting_matrix(participants, rounds)
                        new_score = util.score_1on1(new_meeting_matrix, optimal_meeting_count)
                        if new_score < current_score:
                            current_score = new_score
                            meeting_matrix = new_meeting_matrix
                            repeated_score_number = 0
                            improvable_round = True
                        elif new_score == current_score:
                            current_score = new_score
                            meeting_matrix = new_meeting_matrix
                            repeated_score_number += 1
                            improvable_round = repeated_score_number < 10
                        else:
                            rounds[round_index]["plan"] = old_plan
                        best_score, best_solution = update_best(best_score, best_solution, current_score, rounds)
        if not improvable_round:
            # local maximum was reached -> new random
            rounds = [util.round_parse(round_template, participants) for round_template in rounds_template]
            meeting_matrix, rounds = util.random_solution(participants, rounds)
            meeting_matrix = util.calculate_meeting_matrix(participants, rounds)
            current_score = util.score_1on1(meeting_matrix, optimal_meeting_count)
            repeated_score_number = 0
    return {
        "optimalMeetingCount": optimal_meeting_count,
        "meetingMatrix": util.calculate_meeting_matrix(participants, best_solution),
        "plan": [plan["plan"] for plan in best_solution]
    }


if __name__ == '__main__':
    print(one_on_one([chr(ord("a") + i) for i in range(23)]))
