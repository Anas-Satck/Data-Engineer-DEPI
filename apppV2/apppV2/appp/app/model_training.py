import mlflow
import pandas as pd
from data_loader import load_loan_data  
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.model_selection import train_test_split, GridSearchCV
import matplotlib.pyplot as plt
import json
import warnings
from sklearn.exceptions import ConvergenceWarning

# Set the custom folder to store MLflow logs with the correct URI scheme
# mlflow.set_tracking_uri("file:///C:/Users/Sarah/Desktop/flask-ml/mlruns")  # <-- Note the 'file://' prefix and specify a subdirectory if desired


# Function to set up MLflow experiment
def set_mlflow_experiment(experiment_name):
    mlflow.set_experiment(experiment_name)

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning, module="mlflow.*")
warnings.filterwarnings("ignore", category=ConvergenceWarning)

def prepare_data(loan_data):
    # One-hot encode categorical variables
    encoded_loan_data = pd.get_dummies(loan_data, drop_first=True)

    # Define features and target variable
    X = encoded_loan_data.drop('not.fully.paid', axis=1)  # Features
    y = encoded_loan_data['not.fully.paid']  # Target variable

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, stratify=y, random_state=2022)

    return X_train, X_test, y_train, y_test

def validate_model(model, X, y):
    from sklearn.model_selection import cross_val_score
    scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')  # 5-fold cross-validation
    mlflow.log_metric("cross_val_mean_accuracy", scores.mean())
    mlflow.log_metric("cross_val_std_accuracy", scores.std())
    return scores

def train_model(X_train, y_train, X_test, y_test):
    with mlflow.start_run():
        # Hyperparameter tuning
        param_grid = {'C': [0.1, 1, 10]}
        grid = GridSearchCV(LogisticRegression(), param_grid, cv=5)
        grid.fit(X_train, y_train)

        best_model = grid.best_estimator_
        mlflow.log_param("best_C", grid.best_params_['C'])

        # Make predictions
        y_pred = best_model.predict(X_test)

        # Evaluate the model
        metrics = classification_report(y_test, y_pred, output_dict=True)
        print(confusion_matrix(y_test, y_pred))

        # Log parameters, metrics, and model with MLflow
        mlflow.log_param("model_type", "Logistic Regression")
        mlflow.log_param("train_size", X_train.shape[0])
        mlflow.log_param("test_size", X_test.shape[0])

        # Log metrics
        mlflow.log_metric("accuracy", metrics["accuracy"])
        mlflow.log_metric("precision", metrics["1"]["precision"])
        mlflow.log_metric("recall", metrics["1"]["recall"])
        mlflow.log_metric("f1-score", metrics["1"]["f1-score"])

        # Log AUC-ROC
        auc = roc_auc_score(y_test, best_model.predict_proba(X_test)[:, 1])
        mlflow.log_metric("roc_auc", auc)

        # Log the trained model
        mlflow.sklearn.log_model(best_model, "model")

         # Register the model
        model_uri = "runs:/{}/model".format(mlflow.active_run().info.run_id)
        mlflow.register_model(model_uri, "Loan_Default_Prediction")  # Replace with your desired model name


        # Save and log ROC curve
        fpr, tpr, thresholds = roc_curve(y_test, best_model.predict_proba(X_test)[:, 1])
        plt.figure()
        plt.plot(fpr, tpr, color='blue', label='ROC curve (area = %0.2f)' % auc)
        plt.plot([0, 1], [0, 1], color='red', linestyle='--')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic')
        plt.legend(loc='lower right')
        plt.savefig("roc_curve.png")
        mlflow.log_artifact("roc_curve.png")

        # Save feature importance
        feature_importance = best_model.coef_[0]
        importance_dict = {feature: coef for feature, coef in zip(X_train.columns, feature_importance)}
        with open("feature_importance.json", "w") as f:
            json.dump(importance_dict, f)
        mlflow.log_artifact("feature_importance.json")

        return best_model, metrics

def main_train_model():
    try:
        set_mlflow_experiment("Loan Default Prediction")  # Set your desired experiment name
        loan_data = load_loan_data()
        print("Loaded loan data:", loan_data.head())  # Debug print
        X_train, X_test, y_train, y_test = prepare_data(loan_data)
        model, metrics = train_model(X_train, y_train, X_test, y_test)
        print("Model training completed successfully.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main_train_model()

