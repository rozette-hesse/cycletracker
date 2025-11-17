from datetime import datetime, timedelta
import statistics
import streamlit as st

class CyclePredictor:
    def __init__(self, period_start_dates):
        self.period_dates = [datetime.strptime(d, "%Y-%m-%d") for d in period_start_dates if d]
        self.cycle_lengths = self._calculate_cycle_lengths()

    def _calculate_cycle_lengths(self):
        return [
            (self.period_dates[i+1] - self.period_dates[i]).days
            for i in range(len(self.period_dates) - 1)
        ] if len(self.period_dates) > 1 else []

    def predict_next_period(self):
        if len(self.period_dates) < 2:
            return {
                "error": "Not enough data. Please log at least 2 cycles."
            }

        avg_cycle_length = round(statistics.mean(self.cycle_lengths))
        last_period_start = self.period_dates[-1]
        predicted_start = last_period_start + timedelta(days=avg_cycle_length)

        prediction_range = [
            (predicted_start - timedelta(days=2)).strftime("%Y-%m-%d"),
            (predicted_start + timedelta(days=2)).strftime("%Y-%m-%d")
        ]

        return {
            "predicted_start_date": predicted_start.strftime("%Y-%m-%d"),
            "range": prediction_range,
            "confidence": f"Moderate — Based on average of {len(self.cycle_lengths)} cycle(s)",
            "based_on": "average cycle length"
        }

    def get_current_phase(self, current_date=None):
        if len(self.period_dates) < 1:
            return "Insufficient data to determine current phase."

        if not current_date:
            current_date = datetime.today()
        else:
            current_date = datetime.strptime(current_date, "%Y-%m-%d")

        last_start = self.period_dates[-1]
        days_since_last_period = (current_date - last_start).days

        if days_since_last_period < 0:
            return "Invalid current date: before last period logged"

        if days_since_last_period <= 5:
            return f"Cycle Day {days_since_last_period + 1} — Menstrual Phase"
        elif days_since_last_period <= 12:
            return f"Cycle Day {days_since_last_period + 1} — Follicular Phase"
        elif days_since_last_period <= 15:
            return f"Cycle Day {days_since_last_period + 1} — Ovulatory Phase"
        else:
            return f"Cycle Day {days_since_last_period + 1} — Luteal Phase"

# Static input example for environments without input()
if __name__ == "__main__":
    print("Cycle Predictor — Static Input Example")

    period_logs = ["2025-10-06", "2025-11-01"]

    if len(period_logs) < 2:
        print("Insufficient data. Please log at least 2 period start dates.")
    else:
        predictor = CyclePredictor(period_logs)
        prediction = predictor.predict_next_period()
        today_str = datetime.today().strftime("%Y-%m-%d")
        phase = predictor.get_current_phase(today_str)

        print("\nPrediction Result:")
        print(f"Predicted Next Period: {prediction.get('predicted_start_date')}")
        print(f"Range: {prediction.get('range')}")
        print(f"Confidence: {prediction.get('confidence')}")
        print(f"Based on: {prediction.get('based_on')}")

        print("\nCurrent Phase:")
        print(f"Today: {today_str}\n{phase}")
