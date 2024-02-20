import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    # evidence, labels = load_data("Scripts/shopping_reduziert.csv")
    evidence, labels = load_data(sys.argv[1])
    
    # use train_test_split function from sklearn and split data
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    # flatten y_test object
    y_test = [item for sublist in y_test for item in sublist]
    # print(f'len y_test: {len(y_test)}')
    # print(f'len predictions: {len(predictions)}')
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")

# Convert data into defined data types
    
def get_value_type(value):
    try:
        # Try converting to integer
        int_value = int(value)
        return int_value
    except ValueError:
        try:
            # Try converting to float
            float_value = float(value)
            return float_value
        except ValueError:
            # Check if the value is Month
            if value in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
                return ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'].index(value)
            # Check if the value is VisitorType
            elif value == 'Returning_Visitor':
                return 1
            elif value == 'New_Visitor':
                return 0
            # Check if the value is Weekend or Revenue
            elif value == 'TRUE':
                return 1
            elif value == 'FALSE':
                return 0
            else:
                ValueError(f'Wrong value: {value}')
                return value
            
                
def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # Import .csv
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        # Skip header
        next(reader)

        # create two lists evidence, label
        data = []
        for row in reader:
            data.append(
                {"evidence": [get_value_type(cell) for cell in row[:17]],
                 "label": [1 if row[17] == "TRUE" else 0],
                 })

        evidence = [row["evidence"] for row in data]
        labels = [row["label"] for row in data]
        
        """print("Evidence:")
        for e in evidence:
            print(e)
        
        print("labels:")
        for l in labels:
            print(l)
        """
        return (evidence, labels)

# print("test")
# evidence, labels = load_data("Scripts/shopping_reduziert.csv")
# print(f'evidence: {evidence}')
# print(f'labels: {labels}')
    

model = KNeighborsClassifier(n_neighbors=1)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    k_model = model.fit(evidence, labels)
    return k_model


"""X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

mode = train_model(X_train, y_train)
predictions = model.predict(X_test)
"""


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    #print("############ evaluate ###############*")
    #print(f'lables from y_test sample: {labels}')
    #print(f'predictions made by the model: {predictions}')
    
    # set init values
    nbr_pos_labels = 0
    correct_sensitivity = 0
    incorrect_sensitivity = 0
    # flatten labels object
    #labels = [item for sublist in labels for item in sublist]

    # loop over labels and predictions and compare
    for label, prediction in zip(labels, predictions):
        #print(f'label: {label}')
        #print(f'prediciton: {prediction}')
        # true positive - sensitivity
        if label == 1:
            nbr_pos_labels += 1
            if label == prediction:
                correct_sensitivity += 1
            else:
                incorrect_sensitivity +=1
    # print(f'corrct sens: {correct_sensitivity}')
    # print(f'incorrct sens: {incorrect_sensitivity}' )
    sensitivity_rate = correct_sensitivity/nbr_pos_labels
    # print(f'Sensitivity rate: : {sensitivity_rate}' )
    
    # init values
    nbr_neg_labels = 0
    correct_specifity = 0
    incorrect_specifity = 0
    
    # loop over labels and predictions and compare
    for label, prediction in zip(labels, predictions):
        #print(f'label: {label}')
        #print(f'prediciton: {prediction}')
        # true positive - specifity
        if label == 0:
            nbr_neg_labels += 1
            if label == prediction:
                correct_specifity += 1
            else:
                incorrect_specifity +=1
    # print(f'corrct spec: {correct_specifity}')
    # print(f'incorrct spec: {incorrect_specifity}' )
    specifity_rate = correct_specifity/nbr_neg_labels
    # print(f'Specifity rate: : {specifity_rate}' )
    return (sensitivity_rate, specifity_rate)

# f = evaluate(y_test, predictions)


if __name__ == "__main__":
    main()
