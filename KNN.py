import numpy as np
import pandas as pd
import copy

### Sample Files
### Referenced GeeksforGeeks to read in a txt file https://www.geeksforgeeks.org/how-to-read-space-delimited-files-in-pandas/#
small_data_19 = pd.read_csv('/Users/kevintu/Documents/Python/CS205/CS_205/CS205_small_Data__19.txt', sep='  ', header=None)
### Referenced pandas library documentation for renaming a column https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html
small_data_19 = small_data_19.rename(columns={0 : "label"})

### Referenced GeeksforGeeks to read in a txt file https://www.geeksforgeeks.org/how-to-read-space-delimited-files-in-pandas/#
large_data_6 = pd.read_csv('/Users/kevintu/Documents/Python/CS205/CS_205/CS205_large_Data__6.txt', sep='  ', header=None)
### Referenced pandas library documentation for renaming a column https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html
large_data_6 = large_data_6.rename(columns={0 : "label"})

### Assigned Files
### Referenced GeeksforGeeks to read in a txt file https://www.geeksforgeeks.org/how-to-read-space-delimited-files-in-pandas/#
small_data_21 = pd.read_csv('/Users/kevintu/Documents/Python/CS205/CS_205/CS205_small_Data__21.txt', sep='  ', header=None)
### Referenced pandas library documentation for renaming a column https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html
small_data_21 = small_data_21.rename(columns={0 : "label"})

### Referenced GeeksforGeeks to read in a txt file https://www.geeksforgeeks.org/how-to-read-space-delimited-files-in-pandas/#
large_data_13 = pd.read_csv('/Users/kevintu/Documents/Python/CS205/CS_205/CS205_large_Data__13.txt', sep='  ', header=None)
### Referenced pandas library documentation for renaming a column https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html
large_data_13 = large_data_13.rename(columns={0 : "label"})

class KNN_Classifier:
    def __init__(self, train_set=None, test_set=None, k=None, nearest_neighbors=None):
        self.train_set = train_set
        self.test_set = test_set
        self.k = k
        self.nearest_neightbors = nearest_neighbors

    def distance(self, nums):
        sum = 0
        for num in nums:
            sum += num**2
        return np.sqrt(sum)
        
    def pred_class(self):
        pred_classes = []
        for row in range(self.k):
            # print("KNN: ", self.train_set[self.nearest_neighbors[row]])
            # print("KNN: ", self.train_set[self.nearest_neighbors[row]][0])
            pred_classes.append(self.train_set[self.nearest_neighbors[row]][0])
        ### Referenced NumPy unique to return the predicted class https://numpy.org/doc/stable/reference/generated/numpy.unique.html
        classes, counts = np.unique(pred_classes, return_counts=True)
        if len(counts) == 1:
            return classes
        if counts[0] > counts[1]:
            return classes[0]
        return classes[1]
    
    def train(self):
        ### Test every testing entry to training entry
        nearest_neighbors = []
        # print(self.test_set)
        for train_row in self.train_set:
            nearest_neighbors.append(self.distance(train_row[1:] - self.test_set[1:]))
        # print(nearest_neighbors)
        ### Referenced NumPy argsort to sort by index of distances https://numpy.org/doc/stable/reference/generated/numpy.argsort.html
        self.nearest_neighbors = np.argsort(nearest_neighbors)
        # print(self.nearest_neighbors)

class Feature_Selection:
    def __init__(self, dataset=None, k=None):
        self.dataset=dataset
        self.dataset_backwards=copy.deepcopy(self.dataset)
        self.k=k
        self.feature_set = []
        self.feature_set_backwards = []
        self.feature_subset = pd.DataFrame(dataset['label'])
        self.feature_subset_backwards = copy.deepcopy(self.dataset)
        self.best_features = [-1, -1]
    
    def print_best_features(self):
        print("Finished search!!! The best feature subset is {" + self.best_features[0] + "}, which has an accuracy of " + str(self.best_features[1]) + "%")

    def greedy_forward(self):
        if self.dataset.shape[1] == 1:
            return
        precision = []
        feature_name = []
        ### Retreiving the Columns for Feature Selection
        for column in self.dataset.columns:
            if column == 'label':
                continue
            feature = pd.concat([self.feature_subset, pd.DataFrame(self.dataset[column])], axis=1).to_numpy()
            # print(feature)
            correct = 0
            ### K-Fold CV
            for cfv in range(int(len(feature)/self.k)):
                # print(cfv)
                # print(len(feature)/self.k)
                train_data = np.delete(feature, cfv, axis=0)
                # print(train_data)
                test_data = feature[cfv]
                # print(test_data)

                knn = KNN_Classifier(train_data, test_data, 1)
                knn.train()
                # print(test_data[0])
                # print(knn.pred_class()[0])
                if knn.pred_class()[0] == test_data[0]:
                    # print('HELLO')
                    correct += 1
            precision.append(correct/int(len(feature)/self.k))
            feature_name.append(column)
            if self.feature_set:
                feat_str = ','.join(str(feature) for feature in self.feature_set)
                print("\tUsing feature(s) {" + feat_str + "," + str(column) + "} accuracy is " + str(correct/int(len(feature)/self.k)) + '%')
            else:
                print("\tUsing feature(s) {" + str(column) + "} accuracy is " + str(correct/int(len(feature)/self.k)) + '%')
        # print(precision)
        # print(feature_name)
        precision_index = np.argsort(precision)
        # print(precision_index)
        self.feature_set.append(feature_name[precision_index[-1]])
        # print(precision[precision_index[-1]])
        # print(self.feature_set)
        feat_str = ','.join(str(feature) for feature in self.feature_set)
        prev = self.best_features[1]
        self.best_features[1] = max(self.best_features[1], precision[precision_index[-1]])
        if (self.best_features[1] != prev):
            self.best_features[0] = feat_str
        if precision[precision_index[-1]] < self.best_features[1]:
            print("\n(Warning, Accuracy has decreased!!! Continuing search in case of local maxima)")
        print("\nFeature set {" + feat_str + "} was best, accuracy is " + str(precision[precision_index[-1]]) + "%\n")
        ### Referenced Pandas library to understand how to drop column https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop.html
        self.feature_subset = pd.concat([self.feature_subset, pd.DataFrame(self.dataset[feature_name[precision_index[-1]]])], axis=1)
        # print(self.feature_subset)
        self.dataset = self.dataset.drop(columns=[feature_name[precision_index[-1]]])
        # print(self.dataset)
        self.greedy_forward()
        pass
    
    def greedy_backward(self):
        if self.feature_subset_backwards.shape[1] == 1:
            return
        precision = []
        feature_name = []
        ### Retreiving the Columns for Feature Selection
        for column in self.dataset_backwards.columns:
            if column == 'label':
                continue
            # print(column)
            feature = self.feature_subset_backwards.drop(columns=[column]).to_numpy()
            # print(feature)
            correct = 0
            ### K-Fold CV
            for cfv in range(int(len(feature)/self.k)):
                # print(cfv)
                # print(len(feature)/self.k)
                train_data = np.delete(feature, cfv, axis=0)
                # print(train_data)
                test_data = feature[cfv]
                # print(test_data)

                knn = KNN_Classifier(train_data, test_data, 1)
                knn.train()
                # print(test_data[0])
                # print(knn.pred_class()[0])
                if knn.pred_class()[0] == test_data[0]:
                    # print('HELLO')
                    correct += 1
            precision.append(correct/int(len(feature)/self.k))
            feature_name.append(column)
            if self.feature_set_backwards:
                feat_str = ','.join(str(feature) for feature in self.feature_set_backwards)
                print("\tRemoving feature(s) {" + feat_str + "," + str(column) + "} accuracy is " + str(correct/int(len(feature)/self.k)) + '%')
            else:
                print("\tRemoving feature(s) {" + str(column) + "} accuracy is " + str(correct/int(len(feature)/self.k)) + '%')
        # print(precision)
        # print(feature_name)
        precision_index = np.argsort(precision)
        # print(precision_index)
        # print(precision[precision_index[-1]])
        self.feature_set_backwards.append(feature_name[precision_index[-1]])
        # print(self.feature_set_backwards)
        feat_str = ','.join(str(feature) for feature in self.feature_set_backwards)
        prev = self.best_features[1]
        self.best_features[1] = max(self.best_features[1], precision[precision_index[-1]])
        if (self.best_features[1] != prev):
            self.best_features[0] = feat_str
        if precision[precision_index[-1]] < self.best_features[1]:
            print("\n(Warning, Accuracy has decreased!!! Continuing search in case of local maxima)")
        print("\nFeature set {" + feat_str + "} was best, accuracy is " + str(precision[precision_index[-1]]) + "%\n")
        ### Referenced Pandas library to understand how to drop column https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop.html
        self.feature_subset_backwards = self.feature_subset_backwards.drop(columns=[feature_name[precision_index[-1]]])
        # print(self.feature_subset_backwards)
        self.dataset_backwards = self.dataset_backwards.drop(columns=[feature_name[precision_index[-1]]])
        # print(self.dataset_backwards)
        self.greedy_backward()
        pass
    

### Start by splitting my data into train and test set
data = {'label': [2, 1, 2, 1, 2],
        'feature_1': [1, 10, 2, 11, 1],
        'feature_2': [ 2, 11, 3, 12, 2],
        'feature_3': [ 15, 15, 15, 15, 15],}
df = pd.DataFrame(data)
# print(df)
# df = small_data_19.head(5)
# df = small_data_19
# df = large_data_6
train_data = df.sample(frac = 0.8, random_state = 4)
train_data.reset_index(drop=True, inplace=True)
# print(train_data)
test_data = df.drop(train_data.index)
test_data.reset_index(drop=True, inplace=True)
# print(test_data)

# Asks the user for puzzle_size
print("Welcome to KNN Feature Selection Algorithm!\n")
print("Please select the file you would like to test: ")
print("1. Sample Small 19\n" + 
        "2. Assigned Small 21\n" +
        "3. Sample Large 6\n" + 
        "4. Assigned Larg 13e\n")
file = input("Your selection: ")
file = int(file)
if file == 1:
        df = small_data_19
elif file == 2:
        df = small_data_21
elif file == 3:
        df = large_data_6
elif file == 4:
        df = large_data_13
    
# Asks the user the algorithm they would like to use
print("Please select the algorithm you would like to run: \n")
print("1. Forward Selection\n" + 
        "2. Backward Elimination\n" + 
        "3. Both\n")
algo = input("Your selection: ")
algo = int(algo)

print("This dataset has " + str(df.shape[1]-1) + " features (not including the class attribute), with " + str(df.shape[0]) + " instances.\n")
correct = 0
feature = df.to_numpy()
for cfv in range(int((df.shape[1]-1)/1)):
        train_data = np.delete(feature, cfv, axis=0)
        test_data = feature[cfv]

        knn = KNN_Classifier(train_data, test_data, 1)
        knn.train()
        if knn.pred_class()[0] == test_data[0]:
                correct += 1
print("Running KNN with all " + str(df.shape[1]-1) + " åfeatures, using \"leave-one-out\" evaluation, I get an accuracy of " + str(correct/int((df.shape[1]-1)/1)) + "%\n")

feat_select = Feature_Selection(df, 1)
print("Beginning search.\n")
if algo == 1:
        feat_select.greedy_forward()
        feat_select.print_best_features()
elif algo == 2:
        feat_select.greedy_backward()
        feat_select.print_best_features()
elif algo == 3:
        print("Starting with Forward Selection.\n")
        feat_select.greedy_forward()
        feat_select.print_best_features()
        print("Starting Backward Elimination.\n")
        feat_select.greedy_backward()
        feat_select.print_best_features()
