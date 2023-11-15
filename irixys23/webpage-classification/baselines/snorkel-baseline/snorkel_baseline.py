#!/usr/bin/env python3
import argparse
import jsonlines
import pandas as pd
from snorkel.labeling import LabelingFunction, PandasLFApplier, LFAnalysis
from snorkel.labeling.model import LabelModel
from sklearn.metrics import classification_report
import os
import numpy as np

# Constants for the labels
ABSTAIN = -1
BENIGN = 0
MALICIOUS = 1
ADULT = 2

def lf_educational_government_domains(row):
    edu_gov_domains = ['.edu', '.gov']
    url = row['url']
    if any(url.endswith(domain) for domain in edu_gov_domains):
        return BENIGN
    return ABSTAIN

def lf_news_websites(row):
    news_domains = ['bbc.com', 'cnn.com', 'nytimes.com', 'theguardian.com']
    url = row['url']
    if any(domain in url for domain in news_domains):
        return BENIGN
    return ABSTAIN

def lf_health_related(row):
    health_keywords = ['health', 'medical', 'hospital', 'clinic', 'doctor']
    url = row['url']
    if any(keyword in url for keyword in health_keywords):
        return BENIGN
    return ABSTAIN

def lf_educational_content(row):
    edu_keywords = ['course', 'learn', 'education', 'school', 'university']
    url = row['url']
    if any(keyword in url for keyword in edu_keywords):
        return BENIGN
    return ABSTAIN

def lf_tech_companies(row):
    tech_domains = ['microsoft.com', 'apple.com', 'google.com', 'amazon.com']
    url = row['url']
    if any(domain in url for domain in tech_domains):
        return BENIGN
    return ABSTAIN

def lf_family_kids_related(row):
    family_keywords = ['family', 'kids', 'child', 'parenting', 'education']
    url = row['url']
    if any(keyword in url for keyword in family_keywords):
        return BENIGN
    return ABSTAIN

def lf_cultural_artistic_content(row):
    culture_art_keywords = ['museum', 'art', 'gallery', 'theatre', 'culture']
    url = row['url']
    if any(keyword in url for keyword in culture_art_keywords):
        return BENIGN
    return ABSTAIN

def lf_major_retailers(row):
    retailer_domains = ['ebay.com', 'amazon.com', 'walmart.com', 'target.com']
    url = row['url']
    if any(domain in url for domain in retailer_domains):
        return BENIGN
    return ABSTAIN

def lf_government_services(row):
    gov_keywords = ['gov', 'government', 'state', 'federal', 'official']
    url = row['url']
    if any(keyword in url for keyword in gov_keywords):
        return BENIGN
    return ABSTAIN

def lf_sports_recreation(row):
    sports_recreation_keywords = ['sport', 'fitness', 'gym', 'recreation', 'outdoor']
    url = row['url']
    if any(keyword in url for keyword in sports_recreation_keywords):
        return BENIGN
    return ABSTAIN

def lf_explicit_adult_keywords(row):
    explicit_keywords = ['nude', 'hot', 'erotic', 'escort', 'camgirl']
    url = row['url']
    if any(keyword in url for keyword in explicit_keywords):
        return ADULT
    return ABSTAIN

def lf_age_restriction(row):
    age_keywords = ['18+', 'adults-only', 'mature']
    url = row['url']
    if any(keyword in url for keyword in age_keywords):
        return ADULT
    return ABSTAIN

def lf_adult_industry_domains(row):
    adult_domains = ['.xxx', '.adult', '.sex']
    url = row['url']
    if any(url.endswith(domain) for domain in adult_domains):
        return ADULT
    return ABSTAIN

def lf_adult_url_structure(row):
    url = row['url']
    if '/adult/' in url or '/sex/' in url:
        return ADULT
    return ABSTAIN

def lf_euphemisms_for_adult(row):
    euphemisms = ['nsfw', 'afterdark', 'kinky']
    url = row['url']
    if any(euphemism in url for euphemism in euphemisms):
        return ADULT
    return ABSTAIN

def lf_common_adult_content_keywords(row):
    keywords = ['pornography', 'fetish', 'bdsm', 'swinger']
    url = row['url']
    if any(keyword in url for keyword in keywords):
        return ADULT
    return ABSTAIN

def lf_sexual_innuendos(row):
    innuendos = ['booty', 'babe', 'milf', 'daddy']
    url = row['url']
    if any(innuendo in url for innuendo in innuendos):
        return ADULT
    return ABSTAIN

def lf_adult_product_references(row):
    products = ['dildo', 'vibrator', 'lingerie', 'condom']
    url = row['url']
    if any(product in url for product in products):
        return ADULT
    return ABSTAIN

def lf_explicit_usernames(row):
    usernames = ['sexy', 'slutty', 'horny', 'naughty']
    url = row['url']
    if any(username in url for username in usernames):
        return ADULT
    return ABSTAIN

def lf_adult_forums_chatrooms(row):
    forums = ['chatroom', 'forum', 'webcam', 'livecam']
    url = row['url']
    if any(forum in url for forum in forums):
        return ADULT
    return ABSTAIN

def lf_common_benign_domains(row):
    common_domains = ['google.com', 'wikipedia.org', 'youtube.com']
    url = row['url']
    if any(domain in url for domain in common_domains):
        return BENIGN
    return ABSTAIN

def lf_malicious_keywords(row):
    malicious_keywords = ['hack', 'phish', 'malware', 'spyware']
    url = row['url']
    if any(keyword in url for keyword in malicious_keywords):
        return MALICIOUS
    return ABSTAIN

def lf_adult_keywords(row):
    adult_keywords = ['adult', 'sex', 'xxx', 'porn']
    url = row['url']
    if any(keyword in url for keyword in adult_keywords):
        return ADULT
    return ABSTAIN

def lf_shortened_url(row):
    shortened_services = ['bit.ly', 'goo.gl', 'tinyurl.com']
    url = row['url']
    if any(service in url for service in shortened_services):
        return MALICIOUS  # Often used for malicious purposes
    return ABSTAIN

def lf_long_url(row):
    url = row['url']
    if len(url) > 100:  # Arbitrary threshold
        return MALICIOUS
    return ABSTAIN

def lf_non_standard_port(row):
    url = row['url']
    if ':8080' in url or ':8000' in url:
        return MALICIOUS
    return ABSTAIN

def lf_https_protocol(row):
    url = row['url']
    if url.startswith('https://'):
        return BENIGN
    return ABSTAIN

def lf_numerical_url(row):
    url = row['url']
    if any(char.isdigit() for char in url):
        return MALICIOUS
    return ABSTAIN

def lf_suspicious_subdomain(row):
    suspicious_subdomains = ['secure-', 'account-', 'login-']
    url = row['url']
    if any(subdomain in url for subdomain in suspicious_subdomains):
        return MALICIOUS
    return ABSTAIN

def lf_uncommon_tld(row):
    uncommon_tlds = ['.biz', '.info', '.top']
    url = row['url']
    if any(url.endswith(tld) for tld in uncommon_tlds):
        return MALICIOUS
    return ABSTAIN




def load_data(file_path):
    with jsonlines.open(file_path) as reader:
        for obj in reader:
            obj_keys = obj.keys()
            break
    
    data = {k: [] for k in obj_keys}
    
    with jsonlines.open(file_path) as reader:
        for obj in reader:
            for k in obj_keys:
                data[k].append(obj[k])
    return pd.DataFrame(data)

def parse_args():
    parser = argparse.ArgumentParser(description='Webpage classification with sklearn pipeline')
    parser.add_argument("-d", "--data_dir", help="Path to the directory containing the data subfolders.", required=True)
    parser.add_argument("-o", "--output", help="Path to the directory to write the results to.", required=True)
    return parser.parse_args()

def preprocess(content):
    # Placeholder for the content preprocessing
    # You might want to add actual preprocessing logic here
    return content

def predict_with_tie_break(label_model, L, tie_break_label=BENIGN):
    # Get the probabilistic predictions
    probas = label_model.predict_proba(L)

    # Initialize an array to store the final predictions
    predictions = -1 * np.ones(L.shape[0])

    # Iterate over each item
    for i, prob in enumerate(probas):
        # Find the maximum probability
        max_prob = max(prob)

        # Check if there's a tie
        if (prob == max_prob).sum() > 1:
            # If there's a tie, predict BENIGN
            predictions[i] = tie_break_label
        else:
            # Otherwise, choose the label with the highest probability
            predictions[i] = np.argmax(prob)

    return predictions


def main(data_dir, output_dir):
    # Load datasets
    train_data = load_data(os.path.join(data_dir, 'train/D1_train.jsonl'))
    validation_data = load_data(os.path.join(data_dir, 'validation/D1_validation.jsonl'))
    test_data = load_data(os.path.join(data_dir, 'test/D1_test.jsonl'))

    # Define labeling functions
    lf_educational_government_domains_LF = LabelingFunction(
    name="lf_educational_government_domains",
    f=lf_educational_government_domains,
)
    original_lfs = [ lf_educational_government_domains, lf_news_websites, lf_health_related, 
            lf_educational_content, lf_tech_companies, lf_family_kids_related,
            lf_cultural_artistic_content, lf_major_retailers, lf_government_services,
            lf_sports_recreation, lf_explicit_adult_keywords, lf_age_restriction, lf_adult_industry_domains, 
            lf_adult_url_structure, lf_euphemisms_for_adult, lf_common_adult_content_keywords,
            lf_sexual_innuendos, lf_adult_product_references, lf_explicit_usernames, lf_adult_forums_chatrooms, 
            lf_common_benign_domains, lf_malicious_keywords, lf_adult_keywords,
            lf_shortened_url, lf_long_url, lf_non_standard_port, lf_https_protocol, 
            lf_numerical_url, lf_suspicious_subdomain, lf_uncommon_tld
          ] # Add all your labeling functions here

    # Create LabelingFunction instances dynamically
    lfs = [
        LabelingFunction(name=func.__name__, f=func)
        for func in original_lfs
    ]
    # Apply the labeling functions to the datasets
    applier = PandasLFApplier(lfs=lfs)
    L_train = applier.apply(df=train_data)
    L_validation = applier.apply(df=validation_data)
    L_test = applier.apply(df=test_data)

    # Train the label model
    label_model = LabelModel(cardinality=3, verbose=True)
    label_model.fit(L_train, n_epochs=1000, log_freq=100, seed=123)

    # Use the custom prediction function
    validation_predictions = predict_with_tie_break(label_model, L_validation)
    test_predictions = predict_with_tie_break(label_model, L_test)

    # # Predict on the validation and test set
    # validation_predictions = label_model.predict(L_validation, tie_break_policy='abstain')
    # test_predictions = label_model.predict(L_test, tie_break_policy='abstain')

    # Validate the model
    validation_labels = load_data(os.path.join(data_dir, 'validation/D1_validation-truth.jsonl'))['label']
    label_mapping = {'Benign': 0, 'Malicious': 1, 'Adult': 2}
    validation_labels_numeric = validation_labels.map(label_mapping)
    print(classification_report(validation_labels_numeric, validation_predictions))

    # print(classification_report(validation_labels, validation_predictions))

    # Save the predictions
    test_data['label'] = test_predictions
    output_path = os.path.join(output_dir, 'test_predictions.jsonl')
    test_data[['uid', 'label']].to_json(output_path, orient='records', lines=True)

if __name__ == "__main__":
    args = parse_args()
    main(args.data_dir, args.output)