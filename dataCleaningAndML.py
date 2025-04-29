from sklearn.impute import KNNImputer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import numpy as np
import urllib.parse
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
import time


class DataCleaningAndML:
    def __init__(self):
        self.df_cleaned = None
        self.df_missed = None

    @staticmethod
    def first_look_at(df):
        firstLook = df.iloc[:, 3:8]
        # import matplotlib
        # matplotlib.use('Agg')
        sns.heatmap(firstLook.isnull(), cbar=False, cmap='viridis')
        plt.title('Heatmap of Missing Values')
        # plt.show()
        plt.savefig('heatmap.png')
        plt.close()
        img = Image.open('heatmap.png')
        img.show()
        time.sleep(2)
        img.close()
        # Index of rows with all 5 important features missing-------------
        missing_all_indices = firstLook[firstLook.isnull().all(axis=1)].index
        print("Indices of rows with all 5 features missing:", missing_all_indices.tolist())

    @staticmethod
    def fill_missing_by_mean(df, targetColumn):
        df[targetColumn].fillna(df[targetColumn].mean(), inplace=True)
        return df

    @staticmethod
    def fill_missing_by_median(df, targetColumn):
        df[targetColumn].fillna(df[targetColumn].median(), inplace=True)
        return df

    @staticmethod
    def fill_missing_by_mode(df, targetColumn):
        df[targetColumn].fillna(df[targetColumn].mode(), inplace=True)
        return df

    @staticmethod
    def fill_missing_by_interpolation(df, targetColumn, method='polynomial'):
        # method='linear'
        df[targetColumn].interpolate(method=method, order=2, inplace=True)
        return df

    @staticmethod
    def fill_missing_by_linear_regression(df, targetColumn):
        df_without_nan = df.dropna(subset=[targetColumn])
        X = df_without_nan.drop(columns=[targetColumn])
        y = df_without_nan[targetColumn]
        model = LinearRegression()
        model.fit(X, y)
        df_with_nan = df[df[targetColumn].isna()]
        X_nan = df_with_nan.drop(columns=[targetColumn])
        y_pred = model.predict(X_nan)
        df.loc[df[targetColumn].isna(), targetColumn] = y_pred
        return df

    @staticmethod
    def fill_missing_by_KNNImputation(df):
        imputer = KNNImputer(n_neighbors=5)
        df_imputed = imputer.fit_transform(df)
        df = pd.DataFrame(df_imputed, columns=df.columns)
        return df

    @staticmethod
    def plot_clustering_for(df, category):
        df = df.loc[df['category'] == category]
        sns.scatterplot(x='att1', y='att2', hue='cluster', data=df, palette='viridis', s=100)
        plt.title(f'Clustering of {category}')
        plt.xlabel('att1')
        plt.ylabel('att2')
        plt.savefig(f'clustering_{category}.png')
        plt.close()
        img = Image.open(f'clustering_{category}.png')
        img.show()
        time.sleep(1)

    def impute_clustering_for(self, df_subCat, category):
        min = self.df_cleaned[self.df_cleaned['category'] == category].index.min()
        max = self.df_cleaned[self.df_cleaned['category'] == category].index.max() + 1
        for i in range(min, max):
            self.df_cleaned.loc[(self.df_cleaned.index == i) & (self.df_cleaned['category'] == category), 'cluster'] = \
                df_subCat['cluster'].iloc[i - min]

    @staticmethod
    def show_similar_models(df):
        grouped = df.groupby('cluster')
        for cluster, group in grouped:
            print(f"Cluster: {cluster}")
            for index, row in group.iterrows():
                print(f"  Brand: {row['brand']}, Model: {row['model']}")
            print()

    def load_and_clean_data(self, fileName):
        result_df = pd.read_csv(fileName, encoding='utf-8')
        result_df = result_df.map(lambda x: np.nan if ((x is None) | (x == ' ')) else x)
        important_cols = result_df.loc[:, ['category', 'brand', 'model', 'att1', 'att2', 'att3', 'att4', 'att5']]
        # first look at missing data -----------------------------------
        self.first_look_at(important_cols)
        # Remove rows with more than 3 missing important features
        condition = important_cols[important_cols.columns[3:8]].isna().sum(axis=1) >= 3
        self.df_cleaned = important_cols[~condition].reset_index(drop=True)
        self.df_missed = important_cols[condition].reset_index(drop=True)
        self.df_cleaned['cluster'] = None
        # first look at truncated data -----------------------------------
        self.first_look_at(self.df_cleaned)

    def fill_and_normalize_and_clustering(self):
        # do clustering for each category----------------------------
        # https://scikit-learn.org/stable/modules/impute.html#estimators-that-handle-nan-values
        # https://scikit-learn.org/stable/modules/impute.html
        cat = set(self.df_cleaned['category'].tolist())
        for c in cat:
            print(f'For Category: {c}')
            df_subCat = self.df_cleaned.loc[self.df_cleaned['category'] == c]
            df_subCat.iloc[:, 3:8] = self.fill_missing_by_KNNImputation(df_subCat.iloc[:, 3:8]).round()
            df_input = df_subCat.iloc[:, 3:8]
            min_max_scaler = MinMaxScaler()
            normalized_data = min_max_scaler.fit_transform(df_input)
            df_normalized = pd.DataFrame(normalized_data, columns=df_input.columns)
            standard_scaler = StandardScaler()
            standardized_data = standard_scaler.fit_transform(df_normalized)
            df_normalized_standardized = pd.DataFrame(standardized_data, columns=df_input.columns)
            #kmeans = KMeans(n_clusters=3, random_state=42)
            #df_subCat['cluster'] = kmeans.fit_predict(df_normalized_standardized)
            dbscan = DBSCAN(eps=1.5, min_samples=2)
            df_subCat['cluster'] = dbscan.fit_predict(df_normalized_standardized)
            self.plot_clustering_for(df_subCat, c)
            self.impute_clustering_for(df_subCat, c)
            self.show_similar_models(df_subCat)

    def finish(self):
        self.df_cleaned = self.df_cleaned.sort_values(by=['category', 'cluster']).reset_index(drop=True)
        self.df_cleaned.to_csv('clustered_data.csv', encoding='utf-8', index=False)
        return 'clustered_data.csv'


if __name__ == '__main__':
    dataCleaningAndML = DataCleaningAndML()
    dataCleaningAndML.load_and_clean_data('links_and_features.csv')
    dataCleaningAndML.fill_and_normalize_and_clustering()
    fileName = dataCleaningAndML.finish()
