import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.neighbors import KNeighborsClassifier

data = pd.read_excel("fm_l2_updated.xlsx")
df_ccta = pd.read_csv("dummy_ccta.csv")
df_dgnl = pd.read_csv("dummy_dgnl.csv")

sample_ccta = df_ccta.sample(n=200, random_state=42)
sample_dgnl = df_dgnl.sample(n=200, random_state=42)
test_case = pd.concat([sample_ccta, sample_dgnl], ignore_index=True)

target = 'ma_xet_tuyen'
x_train = data.drop(columns=[target])
y_train = data[target]
x_test = test_case.copy()

num_ntt = ['Học phí', 'điểm quy đổi', 'hk10', 'hk11', 'hk12', 'hl10', 'hl11', 'hl12', 'nhom_nganh']
nom_ntt = ['Điểm chuẩn', 'Tổ hợp môn', 'tên ccta', 'điểm ccta']

for col in nom_ntt:
    x_train[col] = x_train[col].astype(str)
    x_test[col] = x_test[col].astype(str)

num_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="mean")),
    ("scaler", StandardScaler())
])

nom_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(sparse_output=False, handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(transformers=[
    ("num_feature", num_transformer, num_ntt),
    ("nom_feature", nom_transformer, nom_ntt)
])

neigh = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", KNeighborsClassifier(n_neighbors=1))
])

neigh.fit(x_train, y_train)
y_predict = neigh.predict(x_test)

predictions = x_test.copy()
predictions["ma_xet_tuyen"] = y_predict

predictions.to_excel("pred_sample_dgnl_ccta.xlsx", index=False)
