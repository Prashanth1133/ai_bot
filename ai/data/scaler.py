from sklearn.preprocessing import StandardScaler


class FeatureScaler:

    def __init__(self):

        self.scaler = StandardScaler()

    def fit(self, X):

        return self.scaler.fit(X)

    def transform(self, X):

        return self.scaler.transform(X)

    def fit_transform(self, X):

        return self.scaler.fit_transform(X)