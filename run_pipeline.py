from data_agent import KaggleSourcingAgent
import app # Your phase-3 refactored code

def run():
    # 1. Agent acquires fresh data dynamically
    agent = KaggleSourcingAgent(target_dir="assets/sample_images")
    agent.search_and_download("urban wildlife") # Or "new york city streets"
    
    # 2. The pipeline processes the fresh data
    print("[PIPELINE] Starting Vision Engine...")
    app.main()

if __name__ == "__main__":
    run()

