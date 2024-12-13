import mlflow
import numpy as np
from sklearn.linear_model import LogisticRegression
import pandas as pd
from mlflow.models.signature import infer_signature


def log_to_mlflow():

    X = np.random.randn(100, 2)
    y = (X[:, 0] + X[:, 1] > 0).astype(int)

    mlflow.set_tracking_uri("http://mlflow:5000")
    mlflow.set_experiment("test-run")

    with mlflow.start_run() as run:
        mlflow.log_param("n_samples", len(X))

        model = LogisticRegression()
        model.fit(X, y)

        mlflow.log_metric("accuracy", model.score(X, y))

        df = pd.DataFrame(X, columns=['feature1', 'feature2'])
        df['target'] = y
        df.to_csv("data.csv", index=False)

        mlflow.log_artifact("data.csv")
        
        # Log model
        input_example = pd.DataFrame(X, columns=['feature1', 'feature2'])
        signature = infer_signature(input_example, model.predict(X))
        mlflow.sklearn.log_model(model, "model", signature=signature, input_example=input_example)
        
        print(f"Test completed successfully!")
        print(f"Run ID: {run.info.run_id}")
        print(f"Experiment ID: {run.info.experiment_id}")

if __name__ == "__main__":
    log_to_mlflow()