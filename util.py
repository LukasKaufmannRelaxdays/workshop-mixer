import random

import numpy


def rounds_hash(rounds, participants):
    rounds_as_tuple = tuple(
        tuple(tuple(participants.index(participant) for participant in group) for group in single_round["plan"]) for
        single_round in rounds)
    return hash(
        rounds_as_tuple
    )


def meet(meeting_matrix, participants, first_participant, second_participant):
    first_participant_index = participants.index(first_participant)
    second_participant_index = participants.index(second_participant)
    meeting_matrix[first_participant_index][second_participant_index] += 1
    meeting_matrix[second_participant_index][first_participant_index] += 1


def score_meeting_matrix(meeting_matrix, optimal_meeting_count):
    maximum = numpy.max(meeting_matrix)
    for i in range(len(meeting_matrix)):
        meeting_matrix[i][i] = maximum + 1
    zero_count = (meeting_matrix == 0).sum()
    minimum = numpy.min(meeting_matrix)
    for i in range(len(meeting_matrix)):
        meeting_matrix[i][i] = 0
    ret = 0
    for row in meeting_matrix:
        for val in row:
            ret += (val - optimal_meeting_count) ** 2
    return (maximum - minimum) * (ret + zero_count * maximum * maximum * 100)


def calculate_meeting_matrix(participants, rounds):
    meeting_matrix = numpy.zeros((len(participants), len(participants)), dtype=int)
    for i in range(len(rounds)):
        for group_index in range(len(rounds[i]["plan"])):
            group_members = rounds[i]["plan"][group_index]
            for group_member_index in range(len(group_members)):
                for previous_group_member_index in range(group_member_index):
                    meet(meeting_matrix, participants, group_members[group_member_index],
                         group_members[previous_group_member_index])
    return meeting_matrix


def round_parse(round_template, participants):
    return {
        "plan": [list(group) for group in round_template.split("|")],
        "remain": participants.copy()
    }


def random_solution(participants, rounds):
    for i in range(len(rounds)):
        random.shuffle(rounds[i]["remain"])
        for group_index in range(len(rounds[i]["plan"])):
            group_members = rounds[i]["plan"][group_index]
            for group_member_index in range(len(group_members)):
                new_participant = rounds[i]["remain"].pop()
                random.shuffle(rounds[i]["remain"])
                group_members[group_member_index] = new_participant
    meeting_matrix = calculate_meeting_matrix(participants, rounds)

    return meeting_matrix, rounds