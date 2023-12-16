from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from ml.features.preprocessing import scale_data


def train_extra_tree(stock_data):

    X = stock_data.drop(['Target'], axis=1)
    train_x, test_x, train_y, test_y = train_test_split(X, stock_data['Target'], test_size=0.20, random_state=42)

    #train_x, test_x = scale_data(train_x, test_x)

    etc = ExtraTreesClassifier(n_estimators=2000, random_state=42)
    etc.fit(train_x, train_y)

    y_pred = etc.predict(test_x)
    accuracy = accuracy_score(test_y, y_pred)
    print(f"Modellname: {etc.__class__.__name__}")
    print(f"Genauigkeit: {accuracy}")

    return etc, accuracy

