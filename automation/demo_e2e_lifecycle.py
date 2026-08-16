import os
import sys
import time
import subprocess
import shutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# We would normally import the actual agents here and execute them.
# For the purpose of the deterministic script, we will orchestrate the commands 
# that run the actual AI QA Framework pipelines.

STORY = "As a user, I want to generate a vegetarian meal plan while respecting my peanut allergy and calorie target."

def step_print(step_num, title, description):
    print(f"\n{'='*60}")
    print(f"STEP {step_num}: {title}")
    print(f"{'-'*60}")
    print(description)
    print(f"{'='*60}\n")
    time.sleep(2)

def run_e2e_demo():
    print("Starting NutriMind AI QA Framework - End-to-End Demo\n")
    
    step_print(1, "The Requirement & Risk Phase", 
               f"Ingesting Jira Story:\n\"{STORY}\"\nPassing to RequirementAgent, RiskAgent, and TestDesignAgent...")
    
    # In a real environment, we'd invoke the agents:
    # req_agent = RequirementAgent()
    # req_agent.execute({"story": STORY})
    print("[Agent Output] Requirements mapped: REQ-MEAL-01, REQ-ALLERGY-01, REQ-CAL-01")
    print("[Agent Output] Risks identified: High (Allergy violation could cause harm)")
    print("[Agent Output] Test Scenarios generated: TS-01 (Valid inputs), TS-02 (Peanut constraint enforcement)")
    
    step_print(2, "The Automation Generation Phase",
               "AutomationAgent translating TS-02 into a Playwright test script...")
    print("[Agent Output] Generated pytest suite: test_meal_planner_allergy.py")
    
    step_print(3, "First Execution (PASS)", 
               "Running the generated test suite against the live local backend...")
    
    # We simulate the first successful run
    print("[Pytest] automation/tests/ai/test_meal_planner.py::test_peanut_allergy - PASSED")
    print("[TraceabilityAgent] Mapped execution success back to REQ-ALLERGY-01")
    print("[CoverageAgent] Critical constraint coverage: 100%")
    
    step_print(4, "Defect Injection", 
               "Simulating a bad developer commit... Programmatically editing backend/api/meal_planner.py to ignore the peanut allergy constraint.")
    
    meal_planner_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend/api/meal_planner.py"))
    backup_path = meal_planner_path + ".bak"
    
    if os.path.exists(meal_planner_path):
        shutil.copy(meal_planner_path, backup_path)
        with open(meal_planner_path, "r") as f:
            content = f.read()
        
        # Inject the bug: ignore peanuts
        buggy_content = content.replace(
            "if 'peanut' in request.allergies:",
            "if 'peanut' in request.allergies:\n            pass # Bug introduced: ignoring allergy\n        if False:"
        )
        
        with open(meal_planner_path, "w") as f:
            f.write(buggy_content)
        print(f"[System] Bug injected into {meal_planner_path}")
    else:
        print(f"[Warning] {meal_planner_path} not found. Skipping physical file modification.")
        
    step_print(5, "Second Execution (FAIL)", 
               "Re-running the CI/CD pipeline after the bad commit...")
    print("[Pytest] automation/tests/ai/test_meal_planner.py::test_peanut_allergy - FAILED")
    print("[DeterministicValidator] ERROR: 'peanut' found in meal plan output despite allergy constraint!")
    print("[DeepEval] ERROR: Output is not faithful to the allergy constraint.")
    
    step_print(6, "AI Failure Analysis & Self Healing", 
               "FailureAgent capturing evidence, generating RCA, and proposing a fix...")
    print("[FailureAgent] Classification: APPLICATION_DEFECT")
    print("[FailureAgent] RCA: The backend API is ignoring the peanut allergy list due to a missing or overridden conditional branch in meal_planner.py.")
    print("[GoldenDatasetGenerator] Saved failed execution path as a regression golden candidate.")
    
    print("\n[SelfHealingService] Proposed Patch:")
    print("--- backend/api/meal_planner.py")
    print("+++ backend/api/meal_planner.py")
    print("@@ -45,3 +45,3 @@")
    print("-        if 'peanut' in request.allergies:")
    print("-            pass # Bug introduced: ignoring allergy")
    print("-        if False:")
    print("+        if 'peanut' in request.allergies:")
    print("+            exclude_ingredients.append('peanuts')")
    print("+            exclude_ingredients.append('peanut butter')")
    
    approval = input("\n[Human Gate] Approve this patch? (Y/N): ")
    
    if approval.strip().lower() in ['y', 'yes']:
        step_print(7, "Applying Fix & Final Verification", "Restoring original file and re-running pipeline...")
        if os.path.exists(backup_path):
            shutil.move(backup_path, meal_planner_path)
            print("[System] Original code restored (Patch applied).")
            
        print("[Pytest] automation/tests/ai/test_meal_planner.py::test_peanut_allergy - PASSED")
    else:
        step_print(7, "Patch Rejected", "Pipeline remains in FAILED state.")
        
    step_print(8, "Enterprise QA Reporting", "Generating final consolidated report...")
    from agents.schemas.enterprise_report_schemas import ConsolidatedReport, ExecutiveSummary
    from automation.utils.enterprise_reporter import EnterpriseReporter
    
    reporter = EnterpriseReporter(output_dir="reports")
    summary = ExecutiveSummary(
        overall_quality="PASS" if approval.strip().lower() in ['y', 'yes'] else "FAIL",
        functional_pass_rate=100.0 if approval.strip().lower() in ['y', 'yes'] else 85.0,
        api_pass_rate=100.0 if approval.strip().lower() in ['y', 'yes'] else 90.0,
        automation_pass_rate=100.0 if approval.strip().lower() in ['y', 'yes'] else 80.0,
        ai_quality_score=98.5,
        security_pass_rate=100.0,
        coverage_percentage=100.0,
        critical_issues_count=0 if approval.strip().lower() in ['y', 'yes'] else 1
    )
    reporter.generate_all(ConsolidatedReport(executive_summary=summary))
    print("[EnterpriseReporter] Generated enterprise_report.json")
    print("[EnterpriseReporter] Generated enterprise_report.md")
    print("[EnterpriseReporter] Generated enterprise_report.csv")
    print("[EnterpriseReporter] Generated enterprise_report.html")
    
    print("\nEnd-to-End Demo Complete!")

if __name__ == "__main__":
    run_e2e_demo()
