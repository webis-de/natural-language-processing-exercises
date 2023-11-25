#!/usr/bin/env python3
import argparse
import jsonlines
import pandas as pd
from snorkel.labeling import LabelingFunction, PandasLFApplier, LFAnalysis
from snorkel.labeling.model import LabelModel
import os
import joblib

# Constants for the labels
ABSTAIN = -1
BENIGN = 0
MALICIOUS = 1
ADULT = 2

# Label mapping from numeric to string
label_names = {BENIGN: 'Benign', MALICIOUS: 'Malicious', ADULT: 'Adult'}

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

def get_snorkel_pandas_lf_applier():
    lfs = [lf_educational_government_domains, lf_news_websites, lf_health_related, 
           lf_educational_content, lf_tech_companies, lf_family_kids_related,
           lf_cultural_artistic_content, lf_major_retailers, lf_government_services,
           lf_sports_recreation, lf_explicit_adult_keywords, lf_age_restriction, lf_adult_industry_domains, 
           lf_adult_url_structure, lf_euphemisms_for_adult, lf_common_adult_content_keywords,
           lf_sexual_innuendos, lf_adult_product_references, lf_explicit_usernames, lf_adult_forums_chatrooms, 
           lf_common_benign_domains, lf_malicious_keywords, lf_adult_keywords,
           lf_shortened_url, lf_long_url, lf_non_standard_port, lf_https_protocol, 
           lf_numerical_url, lf_suspicious_subdomain, lf_uncommon_tld
          ]

    return PandasLFApplier(lfs=[LabelingFunction(name=func.__name__, f=func) for func in lfs])

def parse_args():
    parser = argparse.ArgumentParser(description='Train a Snorkel labeling model')
    parser.add_argument("-d", "--data_dir", help="Path to the directory containing the data subfolders.", required=True)
    parser.add_argument("-m", "--model_output", help="Path to save the trained model.", required=True)
    return parser.parse_args()

def main(data_dir, model_output):
    # Load datasets
    train_data = load_data(os.path.join(data_dir, 'train/D1_train.jsonl'))

    # Apply the labeling functions to the datasets
    applier = get_snorkel_pandas_lf_applier()
    L_train = applier.apply(df=train_data)
    
    # Train the label model
    label_model = LabelModel(cardinality=3, verbose=True)
    label_model.fit(L_train, n_epochs=1000, log_freq=100, seed=123)

    # Save the trained label model
    joblib.dump(label_model, model_output)

if __name__ == "__main__":
    args = parse_args()
    main(args.data_dir, args.model_output)
