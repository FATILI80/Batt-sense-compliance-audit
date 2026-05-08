class BattSenseBenchmark:
    def __init__(self, auditor):
        self.auditor = auditor
        self.results = []

    def add_test_case(self, df, battery_id, expected_label):
        """
        expected_label: 0 für CLEAN/USABLE, 1 für DEFECT/REJECT
        """
        report = self.auditor.execute(df, battery_id=battery_id, label=expected_label)
        self.results.append(report)

    def evaluate(self):
        tp = fp = tn = fn = 0
        for r in self.results:
            flagged = 1 if r["verdict"] == "REJECT" else 0
            actual = r["ground_truth"]

            if flagged == 1 and actual == 1: tp += 1 # Richtig erkannt als Defekt
            elif flagged == 1 and actual == 0: fp += 1 # Fehlalarm
            elif flagged == 0 and actual == 1: fn += 1 # Defekt übersehen
            elif flagged == 0 and actual == 0: tn += 1 # Richtig erkannt als sauber

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        
        print("--- BENCHMARK REPORT ---")
        print(f"Precision (Genauigkeit): {precision:.2%}")
        print(f"Recall (Trefferquote):  {recall:.2%}")
        print(f"Stats: TP={tp}, FP={fp}, TN={tn}, FN={fn}")
        return {"precision": precision, "recall": recall}
