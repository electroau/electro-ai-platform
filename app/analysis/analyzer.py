def analyze_dataframe(df):
    analysis = {}

    # أسماء الأعمدة
    analysis["columns"] = list(df.columns)

    # نوع البيانات
    analysis["dtypes"] = {col: str(df[col].dtype) for col in df.columns}

    # القيم المفقودة
    analysis["missing_values"] = df.isnull().sum().to_dict()

    # الصفوف المكررة
    analysis["duplicate_rows"] = int(df.duplicated().sum())

    # الأعمدة الفارغة
    analysis["unnamed_columns"] = [
        col for col in df.columns if "unnamed" in col.lower()
    ]

    # عينة من البيانات
    analysis["sample_data"] = df.head(5).to_dict(orient="records")

    return analysis
