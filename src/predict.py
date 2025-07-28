# import pandas as pd
# import joblib
# from ml.src.schemas import PredictRequest, PredictResponse
# from ml.src.utils import preprocess_input_data

# # Load model once at module level
# # model = joblib.load("ml/models/model.pkl")

# def decode_label(label_id: str) -> dict:
#     """
#     Convert encoded label ID into detailed (university, major, method) info.
#     """
#     # university, major, method =
#     return {
#         # "university": university,
#         # "major": major,
#         # "method": method
#     }

# def predict_from_input(input_data: PredictRequest) -> PredictResponse:
#     """
#     Run preprocessing and make a prediction from input data.

#     Args:
#         input_data (dict): Input data as dictionary (already validated by Pydantic)

#     Returns:
#         dict: Dictionary of prediction items
#     """
#     # preprocess_input_data
#     # decode_label
#     return None
