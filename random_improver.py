import ourcopy
import util


def random_improver(participants, rounds_template):
    if rounds_template == "":
        if len(participants) % 2 == 1:
            participants.append("KeinPartner")
        round_template = "|".join(["__" for _ in range(len(participants) // 2)])
        rounds_template = [round_template for _ in range(len(participants) - 1)]
    rounds = [util.round_parse(round_template, participants) for round_template in rounds_template]
    meeting_matrix, rounds = util.random_solution(participants, rounds)
    optimal_meeting_count = sum(sum(i) for i in meeting_matrix) / (len(participants) * (len(participants) - 1))
    best_score = current_score = util.score_meeting_matrix(meeting_matrix, optimal_meeting_count)
    best_solution = ourcopy.deepcopy(rounds)
    repeated_score_number = 0
    for i in range(1000):
        if best_score == 0:
            break
        improvable_round = False
        for first_participant_index in range(len(participants)):
            max_meet_count = max(max(i) for i in meeting_matrix)
            first_participant_meeting_counts = meeting_matrix[first_participant_index]
            if max_meet_count not in first_participant_meeting_counts:
                continue
            max_meet_participant_index = first_participant_meeting_counts.index(max_meet_count)
            first_participant_meeting_counts[first_participant_index] = max_meet_count + 1
            min_meet_participant_count = min(first_participant_meeting_counts)
            min_meet_participant_index = first_participant_meeting_counts.index(min_meet_participant_count)
            first_participant_meeting_counts[first_participant_index] = 0
            if max_meet_count - first_participant_meeting_counts[min_meet_participant_index] >= 2:
                for round_index in range(len(rounds)):
                    plan = ourcopy.deepcopy(rounds[round_index]["plan"])
                    improve = try_find_and_apply_swap(participants[first_participant_index],
                                                      participants[max_meet_participant_index],
                                                      participants[min_meet_participant_index], plan)

                    if improve:
                        old_plan = rounds[round_index]["plan"]
                        rounds[round_index]["plan"] = plan
                        new_meeting_matrix = util.calculate_meeting_matrix(participants, rounds)
                        new_score = util.score_meeting_matrix(new_meeting_matrix, optimal_meeting_count)
                        if new_score < current_score:
                            current_score = new_score
                            meeting_matrix = new_meeting_matrix
                            improvable_round = True
                            repeated_score_number = 0
                        elif new_score == current_score:
                            current_score = new_score
                            meeting_matrix = new_meeting_matrix
                            repeated_score_number += 1
                            improvable_round |= repeated_score_number < 10
                        else:
                            rounds[round_index]["plan"] = old_plan
                        best_score, best_solution = update_best(best_score, best_solution, current_score, rounds)
        if not improvable_round:
            # local maximum was reached -> new random
            rounds = [util.round_parse(round_template, participants) for round_template in rounds_template]
            meeting_matrix, rounds = util.random_solution(participants, rounds)
            meeting_matrix = util.calculate_meeting_matrix(participants, rounds)
            current_score = util.score_meeting_matrix(meeting_matrix, optimal_meeting_count)
            repeated_score_number = 0
        best_score, best_solution = update_best(best_score, best_solution, current_score, rounds)
    return {
        "optimalMeetingCount": optimal_meeting_count,
        "meetingMatrix": util.calculate_meeting_matrix(participants, best_solution),
        "plan": [plan["plan"] for plan in best_solution]
    }


def update_best(best_score, best_solution, current_score, rounds):
    if current_score < best_score:
        best_score = current_score
        best_solution = ourcopy.deepcopy(rounds)
    return best_score, best_solution


def try_find_and_apply_swap(participant, participant_met_most_often, participant_met_least_often, plan):
    for group in plan:
        if participant_met_most_often in group and participant in group and participant_met_least_often not in group:
            for other_group in plan:
                if participant_met_least_often in other_group:
                    other_group.remove(participant_met_least_often)
                    other_group.append(participant_met_most_often)
                    group.append(participant_met_least_often)
                    group.remove(participant_met_most_often)
                    return True
    return False


def main():
    participants = "James,Robert,John,Michael,William,David,Richard,Joseph,Thomas,Charles,Christopher,Daniel".split(
        ",")
    rounds_template = [
        "___|___|___|___",
        "___|___|___|___",
        "___|___|___|___",
        "___|___|___|___",
        "___|___|___|___",
        "___|___|___|___",
    ]
    for i in range(len(rounds_template)):
        if len(participants) != rounds_template[i].count("_"):
            raise Exception(f"In round {i} the number of participants doesn't "
                            f"match the number of _ in the round template")
    print(random_improver(participants, rounds_template))


if __name__ == '__main__':
    main()
