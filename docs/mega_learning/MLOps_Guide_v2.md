# Filename: MLOps_Guide_v2.md

# MLOps Guide v2: Production Lifecycle (Advanced Edition)

AI sirf model code nahi hai, ye poora software infrastructure hai. MLOps (Machine Learning Operations) ensure karta hai ki model production mein fail na ho.

## 1. CI/CD for ML: GitHub Actions
Har baar jab aap model code change karte hain, CI (Continuous Integration) tests run hone chahiye (Lints, Unit Tests). Aur CD (Continuous Deployment) naye container ko server pe deploy karne ke liye use hota hai.

```yaml
# Simple GitHub Action pipeline logic
# jobs:
#   test:
#     run: pytest tests/
#   deploy:
#     run: docker build -t my-ai . && docker push my-ai
```

## 2. Model Versioning: MLflow aur Registry
Aapne 10 models train kiye, kismein kya hyperparameters the aur prediction score kya tha? MLflow metadata track karta hai aur model registry mein "Production", "Staging" tags rakhta hai.

```python
import mlflow

# Tracking experiments
# with mlflow.start_run():
#     mlflow.log_param("lr", 0.001)
#     mlflow.log_metric("accuracy", 0.95)
#     mlflow.pytorch.log_model(model, "model")
```

## 3. Feature Stores: Feast ka Basic Example
Large systems mein same features (Age, History, etc.) multiple models use karte hain. Feature store isse centralize kar deta hai. 

## 4. A/B Testing for Models: 2 Models ka Muqabla
Production mein hum model change nahi karte, 2 models chalate hain (Model A 90% traffic, Model B 10% traffic). Jin 10% users ko naya model dikha rahe hain, unka response check karte hain metrics ke basis pe.

```python
# Traffic split pseudo-logic
# if random_user_hash % 100 < 10:
#     return model_B(query)
# else:
#     return model_A(query)
```

## 5. Data Pipelines: Airflow ya Prefect
AI model train karne ke liye raw data clean ho kar model tak aana chahiye. Airflow blocks/scheduled-tasks banata hai raw files process karne ke liye.

```python
# Airflow Task logic
# def process_data():
#     # clean csv code
#     pass
# task_1 = PythonOperator(task_id='clean_data', python_callable=process_data, dag=dag)
```

## 6. Model Drift Detection: Kab Model Purana Ho Gaya?
- **Concept Drift:** Log naye tarike se baat kar rahe hain, purana pattern (Hate Speech) change ho gaya.
- **Data Drift:** Log naya phones ya devices use kar rahe hain, input distributions badal gayi hain.

## 7. Mini Project: End-to-End MLOps Pipeline
Project Steps:
1. **GitHub Repository:** Model code + Dockerfile.
2. **MLflow Tracking:** Training metrics track karna (wandb integration).
3. **Docker Hub:** Auto-build aur push model images.
4. **Monitoring Dashboard:** Monitor latency with Grafana/Prometheus logic.
   - Command check: `mlflow ui` local UI dekhne ke liye.
   - Git push: Auto-trigger training logic through Webhooks.
