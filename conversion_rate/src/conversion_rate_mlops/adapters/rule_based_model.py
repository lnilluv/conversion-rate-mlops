from dataclasses import dataclass


@dataclass
class RuleBasedModel:
    threshold: int


class RuleBasedClassificationAdapter:
    def train(self, rows: list[dict], labels: list[int]) -> object:
        positive_pages: list[int] = []
        negative_pages: list[int] = []

        for row, label in zip(rows, labels, strict=False):
            pages = int(row["total_pages_visited"])
            if int(label) == 1:
                positive_pages.append(pages)
            else:
                negative_pages.append(pages)

        if not positive_pages or not negative_pages:
            threshold = 10
        else:
            threshold = int((sum(positive_pages) / len(positive_pages) + sum(negative_pages) / len(negative_pages)) / 2)

        return RuleBasedModel(threshold=threshold)

    def predict(self, model: object, rows: list[dict]) -> list[int]:
        predictions: list[int] = []
        if not isinstance(model, RuleBasedModel):
            raise TypeError("Expected RuleBasedModel instance")
        threshold = model.threshold

        for row in rows:
            pages = int(row["total_pages_visited"])
            predictions.append(1 if pages >= threshold else 0)
        return predictions
