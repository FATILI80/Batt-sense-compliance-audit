class BattSenseBenchmark:
    """Vergleicht BATT-SENSE Urteile mit der wissenschaftlichen Wahrheit."""
    def __init__(self, auditor):
        self.auditor = auditor
        self.results = []

    def run_test_case(self, df, battery_id, expected_label):
        """expected_label: 0 = Sauber, 1 = Defekt/Rauschen"""
        report = self.auditor.execute(df, battery_id=battery_id, label=expected_label)
        self.results.append(report)

    def get_statistics(self):
        tp = fp = tn = fn = 0
        for r in self.results:
            flagged = 1 if r["verdict"] == "REJECT" else 0
            actual = r["ground_truth"]

            if flagged == 1 and actual == 1: tp += 1
            elif flagged == 1 and actual == 0: fp += 1
            elif flagged == 0 and actual == 1: fn += 1
            elif flagged == 0 and actual == 0: tn += 1

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        
        return {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "confusion_matrix": {"TP": tp, "FP": fp, "TN": tn, "FN": fn}
        }
