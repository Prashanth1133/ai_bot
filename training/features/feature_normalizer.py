from sklearn.preprocessing import StandardScaler
import joblib


class FeatureNormalizer:

    def __init__(self):

        self.scaler = StandardScaler()

    ###########################################################

    def fit(

        self,

        dataframe,

    ):

        numeric = dataframe.select_dtypes(

            include="number"

        )

        self.scaler.fit(

            numeric

        )

        joblib.dump(

            self.scaler,

            "models/scaler.pkl",

        )

    ###########################################################

    def transform(

        self,

        dataframe,

    ):

        numeric = dataframe.select_dtypes(

            include="number"

        )

        dataframe[numeric.columns] = (

            self.scaler.transform(

                numeric

            )

        )

        return dataframe