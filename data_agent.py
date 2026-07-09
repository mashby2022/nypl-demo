import os
import zipfile
import shutil
from kaggle.api.kaggle_api_extended import KaggleApi

class KaggleSourcingAgent:
    def __init__(self, target_dir="assets/sample_images"):
        self.target_dir = target_dir
        # Initialize and authenticate the Kaggle API
        self.api = KaggleApi()
        self.api.authenticate()
        
        # Ensure target directory exists and is clean
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)

    def download_by_ref(self, ref):
        """Downloads and extracts a specific dataset given its Kaggle ref (owner/dataset-slug)."""
        print(f"[AGENT] Downloading dataset: {ref}...")

        staging_dir = "assets/temp_staging"
        os.makedirs(staging_dir, exist_ok=True)

        self.api.dataset_download_files(ref, path=staging_dir, unzip=False)
        self._extract_and_filter(staging_dir)

        shutil.rmtree(staging_dir)
        print(f"[AGENT] Ingestion complete. Images ready in {self.target_dir}.")

    def search_and_download(self, search_term, max_datasets=1):
        """Searches Kaggle for a term and downloads the top dataset."""
        print(f"[AGENT] Searching Kaggle for: '{search_term}'...")
        datasets = self.api.dataset_list(search=search_term)
        
        if not datasets:
            print("[AGENT] No datasets found.")
            return

        # Pick the most relevant dataset
        target_dataset = datasets[0].ref
        print(f"[AGENT] Found dataset: {target_dataset}. Downloading...")
        
        # Download to a temporary staging area
        staging_dir = "assets/temp_staging"
        os.makedirs(staging_dir, exist_ok=True)
        
        self.api.dataset_download_files(target_dataset, path=staging_dir, unzip=False)
        self._extract_and_filter(staging_dir)
        
        # Clean up staging
        shutil.rmtree(staging_dir)
        print(f"[AGENT] Ingestion complete. Images ready in {self.target_dir}.")

    def _extract_and_filter(self, staging_dir):
        """Unzips files and moves only valid images to the target directory."""
        valid_extensions = {".jpg", ".jpeg", ".png"}
        
        for file in os.listdir(staging_dir):
            if file.endswith(".zip"):
                zip_path = os.path.join(staging_dir, file)
                print(f"[AGENT] Extracting {file}...")
                
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    # Extract to a temp folder first
                    extract_path = os.path.join(staging_dir, "extracted")
                    zip_ref.extractall(extract_path)
                    
                    # Walk through the extracted files and cherry-pick the images
                    for root, _, files in os.walk(extract_path):
                        for ext_file in files:
                            ext = os.path.splitext(ext_file)[1].lower()
                            if ext in valid_extensions:
                                source_path = os.path.join(root, ext_file)
                                # Rename to avoid collisions and move to target
                                safe_name = f"kaggle_{os.path.basename(root)}_{ext_file}"
                                dest_path = os.path.join(self.target_dir, safe_name)
                                shutil.move(source_path, dest_path)

# ==========================================
# Run the Agent
# ==========================================
if __name__ == "__main__":
    agent = KaggleSourcingAgent()
    # Let's pull a dataset of squirrels or urban animals
    # You can change this search term to whatever fits your configuration
    agent.search_and_download("squirrels", "pigeons", "urban wildlife", "rats", "raccoons", "birds")