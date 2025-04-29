from getLinks import GetLinks
from getFeatures import GetFeatures
from dataCleaningAndML import DataCleaningAndML


def main():
    # instantiate class objects
    getLink = GetLinks()
    getFeatures = GetFeatures()
    dataCleaningAndML = DataCleaningAndML()
    # first link scraping on search engines using selenium
    getLink.first_init_load_file('code.xlsx')
    getLink.init()
    domainList1 = ['digikala.com', 'sallambabaa.com', 'torob.com', 'atramart.com', 'entekhabcenter.com']
    getLink.start_link_engine(domainList1)
    getLink_fileName = getLink.finish()
    # first feature scraping using selenium
    getFeatures.load_file(getLink_fileName)
    getFeatures.init()
    getFeatures.start_feature_extraction()
    getFeatures_fileName = getFeatures.finish()
    # second link scraping on search engines using selenium
    getLink.load_file(getFeatures_fileName)
    getLink.init()
    domainList2 = ['entekhabcenter.com', 'atramart.com', 'torob.com', 'sallambabaa.com', 'digikala.com']
    getLink.start_link_engine(domainList2, repeat=True)
    getLink2_fileName = getLink.finish()
    # second feature scraping using selenium
    getFeatures.load_file(getLink2_fileName)
    getFeatures.init()
    getFeatures.start_feature_extraction(repeat=True)
    getFeatures2_fileName = getFeatures.finish()
    # clean and fill empty data, normalize and clustering using scikit-learn
    dataCleaningAndML.load_and_clean_data(getFeatures2_fileName)
    dataCleaningAndML.fill_and_normalize_and_clustering()
    dataCleaningAndML_fileName = dataCleaningAndML.finish()
    print('Clustered Data saved in: ', dataCleaningAndML_fileName)


if __name__ == "__main__":
    main()
