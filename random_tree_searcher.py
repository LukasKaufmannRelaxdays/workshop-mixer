import util
import ourcopy as copy

maximum_nodes = 10000


def random_tree_searcher(participants, rounds_template):
    rounds = [util.round_parse(round_template, participants) for round_template in rounds_template]
    meeting_matrix, rounds = util.random_solution(participants, rounds)
    optimal_meeting_count = sum(sum(i) for i in meeting_matrix) / (len(participants) * (len(participants) - 1))
    best_score = current_score = util.score_meeting_matrix(meeting_matrix, optimal_meeting_count)
    best_solution = copy.deepcopy(rounds)
    known_plans = {(current_score, util.rounds_hash(rounds, participants))}
    dfs_stack = [[meeting_matrix, rounds, 0, current_score]]
    was_bigger_than_cutoff_dfs_size = False
    for i in range(maximum_nodes):
        if len(dfs_stack) == 0:
            rounds = [util.round_parse(round_template, participants) for round_template in rounds_template]
            meeting_matrix, rounds = util.random_solution(participants, rounds)
            optimal_meeting_count = sum(sum(i) for i in meeting_matrix) / (len(participants) * (len(participants) - 1))
            current_score = util.score_meeting_matrix(meeting_matrix, optimal_meeting_count)
            known_plans.add((current_score, util.rounds_hash(rounds, participants)))
            dfs_stack = [[meeting_matrix, copy.deepcopy(rounds), 0, current_score]]
            was_bigger_than_cutoff_dfs_size = False
        best_score, best_solution, stack_grew = execute_swap(best_score, best_solution, dfs_stack, known_plans,
                                                             optimal_meeting_count, participants,
                                                             calculate_cutoff(i / maximum_nodes)
                                                             if was_bigger_than_cutoff_dfs_size else 0)
        if len(dfs_stack) > 200:
            was_bigger_than_cutoff_dfs_size = True
        if best_score == 0:
            break
        if not stack_grew:
            dfs_stack = dfs_stack[:-1]

    print(f"The optimal meeting count between each participant would be {optimal_meeting_count}")
    print(util.calculate_meeting_matrix(participants, best_solution))
    print(*[str(plan["plan"]) + "\n" for plan in best_solution])


def calculate_cutoff(percentage):
    return percentage**0.5


def execute_swap(best_score, best_solution, dfs_stack, known_plans, optimal_meeting_count, participants, cutoff):
    instance = dfs_stack[len(dfs_stack)-1]
    meeting_matrix, rounds, swap_number, current_score = instance
    max_meet_count = max(max(i) for i in meeting_matrix)
    swap_id = 0
    for first_participant_index in range(len(participants)):
        first_participant_meeting_counts = meeting_matrix[first_participant_index]
        if max_meet_count not in first_participant_meeting_counts:
            continue
        for max_meet_participant_index in range(len(first_participant_meeting_counts)):
            if first_participant_meeting_counts[max_meet_participant_index] == max_meet_count:
                first_participant_meeting_counts[first_participant_index] = first_participant_meeting_counts[
                                                                                max_meet_participant_index] + 1
                min_meet_count = min(min(i) for i in meeting_matrix)
                if max_meet_count - min_meet_count >= 2:
                    for min_meet_participant_index in range(len(first_participant_meeting_counts)):
                        if first_participant_meeting_counts[min_meet_participant_index] == min_meet_count:
                            for round_index in range(len(rounds)):
                                plan = copy.deepcopy(rounds[round_index]["plan"])
                                improve = try_find_and_apply_swap(participants[first_participant_index],
                                                                  participants[max_meet_participant_index],
                                                                  participants[min_meet_participant_index],
                                                                  plan)
                                if improve:
                                    if swap_id == swap_number:
                                        rounds[round_index]["plan"] = plan
                                        new_rounds_hash = util.rounds_hash(rounds, participants)

                                        new_meeting_matrix = util.calculate_meeting_matrix(participants, rounds)
                                        new_score = util.score_meeting_matrix(new_meeting_matrix,
                                                                              optimal_meeting_count)
                                        best_score, best_solution = update_best(best_score, best_solution,
                                                                                new_score, rounds)
                                        if best_score / new_score < cutoff:
                                            first_participant_meeting_counts[first_participant_index] = 0
                                            return best_score, best_solution, False
                                        if (new_score, new_rounds_hash) not in known_plans:
                                            first_participant_meeting_counts[first_participant_index] = 0
                                            known_plans.add((new_score, new_rounds_hash))
                                            dfs_stack.append([new_meeting_matrix, copy.deepcopy(rounds), 0, new_score])
                                        instance[2] += 1
                                        return best_score, best_solution, True
                                    swap_id += 1

                first_participant_meeting_counts[first_participant_index] = 0
    return best_score, best_solution, False


def update_best(best_score, best_solution, current_score, rounds):
    if current_score < best_score:
        best_score = current_score
        best_solution = copy.deepcopy(rounds)
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
    participants = "James,Robert,John,Michael,William,David,Richard,Joseph".split(
        ",")
    rounds_template = [
        "____|____",
        "____|____",
        "____|____",
    ]
    for i in range(len(rounds_template)):
        if len(participants) != rounds_template[i].count("_"):
            raise Exception(f"In round {i} the number of participants doesn't "
                            f"match the number of _ in the round template")
    random_tree_searcher(participants, rounds_template)


if __name__ == '__main__':
    main()
