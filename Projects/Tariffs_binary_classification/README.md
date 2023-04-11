
Based on subscriber data for a certain period, several classification models were built, whose metrics were compared and the most suitable model was identified, which shows accuracy in predictions of more than 80%, which is higher than the minimum required value of 75%.

Brief summary of completed tasks
Step 1. Data Overview
The necessary libraries for research were imported
Data was loaded and read, alternative ways of obtaining source data were provided
Information about the data was evaluated
Data types were changed where necessary, and data was checked for explicit duplicates
Step 2. Data Splitting
The source data was divided into three sets: training, validation, and test, in a ratio of 3:1:1, respectively
Each of the datasets was locally saved
Step 3. Model Selection
The following models were considered as candidates for the best model:
LogisticRegression
RandomForestClassifier
For each model, K-fold cross-validation was performed and optimal hyperparameters were selected using GridSearchCV. Additionally, the three best models in each class were compared and the best one was selected from them.
Observations were made for each model based on the resulting metric values:
Accuracy
Precision
Recall
F1-score
Step 4. Model Testing on the Test Set
The models with optimal hyperparameters from each category were tested on the test data
Observations were described, and the RandomForestClassifier model was selected.
Step 5. Checking the Model for Adequacy
The value of the Accuracy metric of the selected RandomForestClassifier model was compared with the value of the same metric of the DummyClassifier model. The model turned out to be adequate.
How to use the obtained result in business? How to make money on these predictions?
After obtaining results that meet the technical specifications (in our case, it was required to achieve a minimum accuracy of 75%), personally, I would work on presenting them in the form of, for example, a presentation, which I would then show to sales managers.

It would be reasonable to include graphs in it that would visualize the dynamics of sales growth after implementing my algorithm.

If the growth is significant, then I would propose considering the possibility of implementing my algorithm into the existing recommendation system.

The main thing I wanted to convey: the algorithm will allow targeting the purchasing power of those customers who really do not understand why it is worth overpaying for a better tariff, and if expanding in this direction, the recommendation system will be able to select the optimal tariff for the client, and the mobile operator will make some money for this convenience.

What could lead to incomplete results?
Small data volume. Because of this, the models were prone to underfitting, which negatively affects metric values.
Small number of features. As it was found, logistic regression models are difficult to classify objects when there are few truly significant features.
