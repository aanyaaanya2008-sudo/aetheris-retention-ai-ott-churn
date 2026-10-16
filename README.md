# AETHERIS — OTT Churn Prediction Prototype

A Flask web application for demonstrating churn-risk scoring for a synthetic OTT/SVOD subscriber dataset.

> **Dataset disclosure:** This project uses synthetic Netflix-style streaming data. It is not real Netflix customer data, is not affiliated with Netflix, and its scores do not establish actual Netflix churn performance.

## Features

- Subscriber form and churn probability
- Configurable threshold loaded from the training notebook
- RFLH-inspired behavioral feature engineering
- JSON prediction API at `/api/predict`
- Health endpoint at `/health`

## 1. Export trained artifacts from the notebook

Run the training, validation model-selection, and threshold-tuning cells first. Before exporting, make sure `best_clf`, `best_model_name`, `preprocessor`, and `opt_threshold` all refer to the same final model and validation-selected threshold.

Run this cell in the same notebook after those variables exist:

```python
from pathlib import Path
import json
import joblib

artifact_dir = Path("deploy_artifacts")
artifact_dir.mkdir(exist_ok=True)

joblib.dump(preprocessor, artifact_dir / "preprocessor.joblib")
joblib.dump(best_clf, artifact_dir / "model.joblib")

with open(artifact_dir / "config.json", "w", encoding="utf-8") as f:
    json.dump({
        "optimal_threshold": float(opt_threshold),
        "champion_model": str(best_model_name)
    }, f, indent=2)

print("Exported artifacts:", [p.name for p in artifact_dir.iterdir()])
```

The preprocessor must be the exact fitted preprocessor used to train `best_clf`. Do not fit a new preprocessor on test data. Test that the model and preprocessor load successfully in a fresh Python process.

## 2. Install and test locally (Windows PowerShell)

Install Python 3.11 or 3.12, then open PowerShell in this repository folder:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use this command for the current terminal only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Copy the three exported artifact files into `deploy_artifacts/`, then run:

```powershell
python app.py
```

Open `http://127.0.0.1:10000`. Verify `http://127.0.0.1:10000/health`.

If artifacts are missing, the app intentionally stops with an explanatory error. Do not commit fake or empty model files.

## 3. GitHub

Create an empty repository named `aetheris-ott-churn` on https://github.com/new. Do not add a README there if you already have this README locally.

Before uploading, inspect the repository for API keys, personal data, source CSVs, and accidental notebook outputs. GitHub blocks regular files larger than 100 MB. If model artifacts are large, use Git LFS or store the model files in a suitable artifact/model registry and configure the host to retrieve them securely.

```powershell
git init
git add app.py requirements.txt README.md .gitignore deploy_artifacts/.gitkeep
git status
git commit -m "Initial AETHERIS OTT churn deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/aetheris-ott-churn.git
git push -u origin main
```

Replace `YOUR_USERNAME`. After you verify artifacts are safely handled, commit them with Git LFS or an appropriate storage solution if needed. Do not commit `.env`, private data, or credentials.

To add your notebook after cleaning its outputs and checking for secrets:

```powershell
mkdir notebooks
# Copy your cleaned notebook into notebooks/
git add notebooks/
git commit -m "Add research notebook"
git push
```

## 4. Deploy on Render

1. Push the code to GitHub.
2. Sign in at https://render.com and choose **New + → Web Service**.
3. Connect the `aetheris-ott-churn` repository.
4. Set runtime to Python.
5. Build command: `pip install -r requirements.txt`
6. Start command: `gunicorn app:app`
7. Ensure the three model artifact files are available at `deploy_artifacts/` during deployment. If they are stored outside GitHub, add a secure build/download step using a private artifact URL or use Git LFS supported by your setup.
8. Deploy and open the generated HTTPS URL.
9. Test `/health` and submit a prediction through the form.

Free hosting plans may sleep when idle and may have memory, build-time, or filesystem limitations. Never assume model artifacts persist on an ephemeral filesystem.

## 5. Important validation checklist

- The deployed model name equals the selected model in the notebook.
- The threshold comes from validation data and is not tuned against the test set.
- The preprocessor and model were trained together and have matching feature order.
- A smoke test succeeds after loading artifacts in a fresh process.
- The public README discloses that the dataset is synthetic.
- Report accuracy, precision, recall, F1, ROC-AUC and PR-AUC on the held-out test set; do not report accuracy alone.
- Treat retention ROI as a simulation until assumptions are validated with real intervention outcomes.
