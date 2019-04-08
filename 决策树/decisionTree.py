%matplotlib inline
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

df_dataset = pd.read_csv('data/enroll.csv')
df_dataset


class DecisionTreeClassifier:
    
    def __init__(self):
        self.root = None
    
    def _cal_shannon_entropy(self, dataset):
        labels, length = set(dataset[:, -1]), dataset.shape[0]
        shannon_sum = 0
        for label in labels:
            p_label = dataset[dataset[:, -1] == label].shape[0] / length
            shannon_sum += -p_label * np.log(p_label)
        return shannon_sum
    
    def _split_dataset(self, dataset, feature, feature_value):
        split_data = dataset[dataset[:, feature] == feature_value]
        return np.delete(split_data, feature, axis=1)
    
    def _choose_best_feature(self, dataset):
        length = dataset.shape[0]
        features = dataset.shape[1] - 1
        base_shannon = self._cal_shannon_entropy(dataset)
        split_shannon = []
        for feature in range(features):
            feature_values = set(dataset[:, feature])
            shannon = 0
            for feature_value in feature_values:
                dataset_feature = self._split_dataset(dataset, feature, feature_value)
                shannon += (dataset_feature.shape[0] / length) * self._cal_shannon_entropy(dataset_feature)
            split_shannon.append(base_shannon - shannon)
        best_feature = np.argmax(split_shannon)
        return best_feature
    
    def _vote(dataset):
        labels = set(dataset[:, -1])
        label_max, label_max_count = 0, 0
        for label in labels:
            label_count = dataset[dataset[:, -1] == label].shape[0]
            if label_count > label_max_count:
                label_max, label_max_count = label, label_count
        return label_max
    
    def _create_decision_tree(self, dataset):
        labels, features = set(dataset[:, -1]), dataset.shape[1] - 1
        if features == 0:
            return TreeNode(vote(dataset), type='leaf')
        if len(labels) == 1:
            return TreeNode(dataset[0, -1], type='leaf')
        best_feature = self._choose_best_feature(dataset)
        best_feature_values = set(dataset[:, best_feature])
        node = TreeNode(best_feature, 'decision')
        for best_feature_value in best_feature_values:
            split_feature_data = self._split_dataset(dataset, best_feature, best_feature_value)
            if split_feature_data.shape[0] == 0:
                node.children[best_feature_value] = TreeNode(vote(dataset), type='leaf')
            else:
                node.children[best_feature_value] = self._create_decision_tree(split_feature_data)
        return node
    
    def _iter_predict(self, dt, data):
        feature, node_type = dt.value, dt.type
        if node_type == 'leaf':
            return feature
        feature_value = data[feature]
        for child in dt.children:
            if child == feature_value:
                return self._iter_predict(dt.children[child], data[:feature] + data[feature+1:])
    
    def fit(self, dataset):
        self.root = self._create_decision_tree(dataset)
        
    def predict(self, dataset):
        result = []
        for data in dataset:
            result.append(self._iter_predict(self.root, data))
        return result


model = DecisionTreeClassifier()
model.fit(dataset)
model.predict([['No', '本科', 'C++'], ['Yes', '博士', 'C++']])