import collections


def to(actions: dict[int, list[int]]) -> list[int]:
    action_cnt: int = len(actions) + 1
    actions = plus1(actions)

    edges = collections.defaultdict(list)
    indeg = [0] * action_cnt
    result: list[int] = list()

    for key, values in actions.items():
        for value in values:
            edges[value].append(key)
            indeg[key] += 1

    q = collections.deque([u for u in range(action_cnt) if indeg[u] == 0])

    while q:
        u = q.popleft()
        result.append(u)
        for v in edges[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    result: list[int] = sub1(result)
    if len(result) != action_cnt:
        result = list()

    return result


def plus1(actions) -> dict[int, list[int]]:
    actions_copy: dict[int, list[int]] = {}
    for key, values in actions.items():
        actions_copy[key + 1] = []
        for value in values:
            actions_copy[key + 1].append(value + 1)
    return actions_copy


def sub1(actions: list[int]) -> list[int]:
    for i in range(len(actions)):
        actions[i] -= 1
    return actions
