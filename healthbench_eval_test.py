import json
import matplotlib.pyplot as plt


class RubricItem:
    def __init__(self, criterion: str, points: float, tags: list[str]):
        self.criterion = criterion
        self.points = points
        self.tags = tags

    def __str__(self):
        return f"[{self.points}] {self.criterion}"

    def to_dict(self):
        return {
            "criterion": self.criterion,
            "points": self.points,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            criterion=d["criterion"],
            points=d["points"],
            tags=d["tags"],
        )

def calculate_score(
    rubric_items: list[RubricItem], grading_response_list: list[dict]
) -> float | None:
    total_possible_points = sum(
        rubric_item.points for rubric_item in rubric_items if rubric_item.points > 0
    )
    if total_possible_points == 0:
        # should not happen for overall score, but may happen for tags
        return None

    achieved_points = sum(
        rubric_item.points
        for rubric_item, grading_response in zip(
            rubric_items, grading_response_list, strict=True
        )
        if grading_response["criteria_met"]
    )
    overall_score = achieved_points / total_possible_points
    return overall_score


def test_calculate_score():
    rubric_items = [
        RubricItem(criterion="test", points=7, tags=[]),
        RubricItem(criterion="test", points=5, tags=[]),
        RubricItem(criterion="test", points=10, tags=[]),
        RubricItem(criterion="test", points=-6, tags=[]),
    ]
    print(rubric_items)

    grading_response_list = [
        {"criteria_met": True},
        {"criteria_met": False},
        {"criteria_met": True},
        {"criteria_met": True},
    ]
    total_possible = 7 + 5 + 10
    achieved = 7 + 0 + 10 - 6
    print(calculate_score(rubric_items, grading_response_list))
    # assert (
    #     calculate_score(rubric_items, grading_response_list) == achieved / total_possible + 1
    # )

def calculate_score_new(data):
    rubric_items = []
    grading_response_list = []

    all_possibles = []
    achieved = []

    for row in data:
        for rubric in row['rubrics']:
            rubric_items.append(
                RubricItem(criterion="test", points=rubric['points'], tags=[])
            )
            grading_response_list.append(
                {"criteria_met": rubric['criteria_met']}
            )
            if rubric['points'] > 0:
                all_possibles.append(rubric['points'])
            
            if rubric['criteria_met'] == True: 
                achieved.append(rubric['points'])
            else:
                achieved.append(0)
           

    print(calculate_score(rubric_items, grading_response_list))
    return calculate_score(rubric_items, grading_response_list)
    # print(all_possibles)
    # print(achieved)
    # print(sum(all_possibles))
    # print(sum(achieved))



if __name__ == "__main__":
    # test_calculate_score()
    with open('data/gpt4_grader.json', 'r') as f:
        data = json.load(f)

    # calculate_score_new(data)
    overall_score = []

    for d in data:
        score = calculate_score_new([d])
        overall_score.append(score)

    print(overall_score)
    print(sum(overall_score)/len(data))

    # If your full data is in a file, you can load it instead.

    plt.figure(figsize=(15, 5))  # You can adjust the size

    # Plotting the bar chart
    plt.bar(range(len(overall_score)), overall_score, color='skyblue')

    # Optional: add a horizontal line at 0 to show positive vs negative
    plt.axhline(0, color='gray', linewidth=1)

    # Labeling
    plt.xlabel('Index')
    plt.ylabel('overall_score')
    plt.title('Bar Chart of 244 Values')

    plt.tight_layout()
    plt.show()