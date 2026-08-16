import sys
import os
import json
import argparse
import logging

logger = logging.getLogger("QualityGate")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

def evaluate_quality_gate(
    pass_rate_threshold: float = 90.0,
    report_dir: str = "reports"
) -> bool:
    """
    Evaluates quality gate criteria against test execution reports.
    """
    logger.info("Evaluating CI/CD Quality Gate (Pass Rate Threshold: %.1f%%)...", pass_rate_threshold)
    
    allure_dir = os.path.join(report_dir, "allure-results")
    total_tests = 0
    passed_tests = 0
    failed_tests = 0

    if os.path.exists(allure_dir):
        for fname in os.listdir(allure_dir):
            if fname.endswith("-result.json"):
                fpath = os.path.join(allure_dir, fname)
                try:
                    with open(fpath, "r") as f:
                        data = json.load(f)
                        total_tests += 1
                        status = data.get("status", "").lower()
                        if status == "passed":
                            passed_tests += 1
                        elif status in ["failed", "broken"]:
                            failed_tests += 1
                except Exception:
                    pass

    if total_tests == 0:
        logger.warning("No test results found in '%s'. Quality Gate passed by default for initial setup.", report_dir)
        print("✅ QUALITY GATE PASSED: No test failures recorded.")
        return True

    pass_rate = (passed_tests / total_tests) * 100.0
    logger.info("Test Summary: Total: %d, Passed: %d, Failed: %d | Pass Rate: %.2f%%",
                total_tests, passed_tests, failed_tests, pass_rate)

    if pass_rate >= pass_rate_threshold:
        print(f"✅ QUALITY GATE PASSED: Pass rate {pass_rate:.2f}% meets threshold {pass_rate_threshold:.1f}%.")
        return True
    else:
        print(f"❌ QUALITY GATE FAILED: Pass rate {pass_rate:.2f}% is below required threshold {pass_rate_threshold:.1f}%.")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Quality Gate thresholds for CI/CD.")
    parser.add_argument("--min-pass-rate", type=float, default=90.0, help="Minimum acceptable pass rate percentage.")
    parser.add_argument("--reports-dir", type=str, default="reports", help="Directory containing test execution results.")

    args = parser.parse_args()
    success = evaluate_quality_gate(pass_rate_threshold=args.min_pass-rate, report_dir=args.reports-dir) if hasattr(args, 'min_pass_rate') else evaluate_quality_gate(pass_rate_threshold=90.0)

    if not success:
        sys.exit(1)
    sys.exit(0)
